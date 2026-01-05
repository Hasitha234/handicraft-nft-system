"""Quick test - generate 5 designs"""
from design_generator import generate_design, load_model
from pathlib import Path
import json

load_model()

output_dir = Path("generated_designs")
output_dir.mkdir(exist_ok=True)

metadata = []
for i in range(5):
    image, prompt = generate_design("mask", "fusion", 60, "")
    if image:
        filename = f"test_design_{i+1}.png"
        image.save(output_dir / filename)
        metadata.append({"id": i+1, "filename": filename, "craft_type": "mask", "style": "fusion", "fusion_level": 60})

with open(output_dir / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print(f"✅ Generated 5 test designs in {output_dir}")