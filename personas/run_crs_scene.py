import asyncio
from pathlib import Path
from personas import get_modal_url
from investigate import run_investigation

async def main():
    url = get_modal_url()
    model = "Qwen/Qwen2.5-7B-Instruct"
    await run_investigation(
        url, model, ["crs_florida"],
        n_per_condition=10,
        output_path=Path(__file__).parent / "investigation_crs_scene.json",
        evidence_key="evidence",
    )

asyncio.run(main())
