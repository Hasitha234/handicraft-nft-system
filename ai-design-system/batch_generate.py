"""
Batch Design Generation
Generate multiple designs for user preference testing
"""

from design_generator import generate_design, load_model
from pathlib import Path
import json
from tqdm import tqdm

def batch_generate():
    """Generate designs for testing"""
    
    # Load model once
    load_model()
    
    output_dir = Path("generated_designs")
    output_dir.mkdir(exist_ok=True)
    
    # Test configurations
    configs = [
        {"craft": "mask", "style": "traditional", "fusion": 20, "count": 10},
        {"craft": "mask", "style": "fusion", "fusion": 50, "count": 15},
        {"craft": "mask", "style": "fusion", "fusion": 70, "count": 15},
        {"craft": "mask", "style": "modern", "fusion": 90, "count": 10},
        {"craft": "batik", "style": "traditional", "fusion": 20, "count": 10},
        {"craft": "batik", "style": "fusion", "fusion": 60, "count": 15},
        {"craft": "batik", "style": "modern", "fusion": 85, "count": 10},
    ]
    
    metadata = []
    design_id = 1
    
    print("=" * 60)
    print("🚀 Batch Design Generation")
    print("=" * 60)
    
    for config in configs:
        craft = config["craft"]
        style = config["style"]
        fusion = config["fusion"]
        count = config["count"]
        
        print(f"\n{craft.upper()} - {style} ({fusion}%): {count} designs")
        
        for i in tqdm(range(count), desc=f"Generating {craft}"):
            image, prompt = generate_design(craft, style, fusion, "")
            
            if image:
                filename = f"design_{design_id:03d}_{craft}_{style}_{fusion}.png"
                filepath = output_dir / filename
                image.save(filepath)
                
                metadata.append({
                    "id": design_id,
                    "filename": filename,
                    "craft_type": craft,
                    "style": style,
                    "fusion_level": fusion,
                    "prompt": prompt
                })
                
                design_id += 1
    
    # Save metadata
    with open(output_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✅ Generated {design_id-1} designs")
    print(f"📁 Saved to: {output_dir}")
    print(f"📄 Metadata: {output_dir / 'metadata.json'}")

if __name__ == "__main__":
    batch_generate()