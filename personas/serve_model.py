import modal

# Define the container image with vLLM installed
vllm_image = modal.Image.debian_slim().pip_install("vllm==0.6.0")

app = modal.App("epistemic-vllm-server")

# Define the model. Qwen 2.5 requires no API keys or HuggingFace tokens.
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"


@app.function(
    image=vllm_image,
    gpu="A10G",
    min_containers=0,
)
@modal.concurrent(max_inputs=10)
@modal.asgi_app()
def serve():
    import vllm
    from vllm.entrypoints.openai.api_server import build_app
    from vllm.entrypoints.openai.cli_args import make_arg_parser

    # Initialize the vLLM engine
    parser = make_arg_parser()
    args = parser.parse_args([
        "--model", MODEL_NAME,
        "--gpu-memory-utilization", "0.90",
        "--max-model-len", "4096",
    ])

    engine = vllm.AsyncLLMEngine.from_engine_args(
        vllm.AsyncEngineArgs.from_cli_args(args)
    )

    # Return the FastAPI app that mimics OpenAI's endpoint
    return build_app(args)