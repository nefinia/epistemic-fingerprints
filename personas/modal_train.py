import modal
import json
import os

app = modal.App("epistemic-fine-tuning")

# A clean, standardized image without fragile wrapper dependencies
train_image = (
    modal.Image.debian_slim(python_version="3.10")
    .run_commands("echo 'Direct SFT Cache Bust v2'") # Bumped cache
    .pip_install(
        "torch==2.4.0",
        "transformers==4.43.2",
        "datasets",
        "trl==0.9.6",      # <-- Pinned to match our transformers version!
        "accelerate",
        "bitsandbytes",
        "peft",
        "rich"
    )
)

personas = ["causal", "analogical", "teleological", "dialectical"]

@app.function(image=train_image, gpu="A100", timeout=7200, volumes={"/root/data": modal.Volume.from_name("epistemic-data", create_if_missing=True)})
def train_single_persona(persona_name: str, raw_data: list):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
    from peft import LoraConfig, get_peft_model
    from trl import SFTTrainer
    from datasets import Dataset

    print(f"[{persona_name.upper()}] Loading Qwen-2.5-7B-Instruct for PEFT training...")
    
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct", trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen2.5-7B-Instruct",
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True
    )
    
    # Configure LoRA adapters
    peft_config = LoraConfig(
        r=16,
        lora_alpha=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.0,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    model = get_peft_model(model, peft_config)
    
    # Format dataset into plain text strings for SFTTrainer
    formatted_texts = []
    for item in raw_data:
        messages = item["messages"]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        formatted_texts.append(text)
        
    dataset = Dataset.from_dict({"text": formatted_texts})
    
    training_args = TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=10,
        num_train_epochs=3,
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=5,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir=f"/tmp/{persona_name}_checkpoints",
    )
    
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=4096,
        args=training_args,
    )
    
    print(f"[{persona_name.upper()}] Starting SFT training...")
    trainer.train()
    
    output_dir = f"/root/data/{persona_name}_adapter"
    trainer.model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Explicitly save the training state (which includes the loss logs) to the persistent volume
    trainer.state.save_to_json(f"{output_dir}/trainer_state.json")
    
    print(f"✅ Successfully saved LoRA adapter and training logs for {persona_name} to volume!")
    return f"{persona_name}: SUCCESS"

@app.local_entrypoint()
def main():
    training_data_by_persona = {}
    for p in personas:
        file_path = f"data/{p}_train.jsonl"
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Could not find {file_path}. Make sure data generation finished successfully!")
        
        with open(file_path, "r", encoding="utf-8") as f:
            training_data_by_persona[p] = [json.loads(line) for line in f]

    print("🚀 Spawning 4 parallel GPU workers on Modal for direct PEFT training...")
    results = list(train_single_persona.starmap([
        (p, training_data_by_persona[p]) for p in personas
    ]))
    
    for res in results:
        print(res)
    print("🎉 All persona models successfully fine-tuned!")