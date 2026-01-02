"""
AI Design Generator - Component 2
Generates fusion handicraft designs using Stable Diffusion
"""

from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import gradio as gr
from pathlib import Path

# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

print(f"Using device: {device}")

# Load Stable Diffusion model (lazy loading - only when needed)
pipe = None

def load_model():
    """Load Stable Diffusion model on first use"""
    global pipe
    if pipe is None:
        print("Loading Stable Diffusion model (first time - this takes 2-3 minutes)...")
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=dtype
        )
        pipe = pipe.to(device)
        if device == "cpu":
            pipe.enable_attention_slicing()  # Reduce memory on CPU
        print("✅ Model loaded")
    return pipe

# Prompt templates
PROMPT_TEMPLATES = {
    "mask": {
        "traditional": "Traditional Sri Lankan demon mask, Raksha mask, red and black colors, intricate hand-carved details, authentic Kandyan style, ceremonial mask, high quality, detailed",
        "fusion": "Fusion design: Sri Lankan traditional mask pattern blended with modern minimalist aesthetic, contemporary colors, simplified traditional elements, artistic interpretation",
        "modern": "Modern minimalist mask design, abstract interpretation of Sri Lankan mask, contemporary art style, bold colors, simple lines, geometric patterns"
    },
    "batik": {
        "traditional": "Traditional Sri Lankan batik fabric, hand-painted wax resist technique, peacock and lotus patterns, natural dyes, authentic Kandyan batik, detailed patterns",
        "fusion": "Fusion batik design: Traditional Sri Lankan batik patterns with modern color palette, contemporary layout, simplified traditional motifs, artistic blend",
        "modern": "Modern textile design inspired by Sri Lankan batik, abstract geometric patterns, contemporary colors, minimalist aesthetic, fabric design"
    },
    "wood_carving": {
        "traditional": "Traditional Sri Lankan wood carving, hand-carved elephant statue, mahogany wood, temple art style, intricate details, authentic craftsmanship",
        "fusion": "Fusion wood carving: Traditional Sri Lankan carving patterns with modern design elements, contemporary finish, simplified traditional motifs",
        "modern": "Modern wooden sculpture inspired by Sri Lankan crafts, minimalist design, contemporary art, geometric shapes, modern aesthetic"
    },
    "pottery": {
        "traditional": "Traditional Sri Lankan pottery, clay pot with traditional patterns, hand-crafted, authentic design, cultural heritage",
        "fusion": "Fusion pottery design: Traditional Sri Lankan pottery shape with modern patterns, contemporary colors, artistic blend",
        "modern": "Modern ceramic design inspired by Sri Lankan pottery, minimalist aesthetic, contemporary style"
    }
}

def generate_design(craft_type, style_preference, fusion_level, additional_prompt=""):
    """Generate single design"""
    pipe = load_model()
    
    # Get base prompt
    base_prompt = PROMPT_TEMPLATES[craft_type][style_preference]
    
    # Adjust based on fusion level
    if fusion_level < 30:
        prompt = f"{base_prompt}, heavily traditional, minimal modern influence"
    elif fusion_level < 70:
        if style_preference == "traditional":
            modern_part = PROMPT_TEMPLATES[craft_type]["modern"]
            prompt = f"Fusion design: {base_prompt} combined with {modern_part}, balanced blend"
        else:
            prompt = f"{base_prompt}, moderate fusion, some traditional elements"
    else:
        prompt = f"{base_prompt}, modern aesthetic, subtle traditional inspiration"
    
    # Add user input
    if additional_prompt.strip():
        prompt = f"{prompt}, {additional_prompt}"
    
    prompt = f"{prompt}, high quality, detailed, professional design, Sri Lankan handicraft"
    
    try:
        image = pipe(
            prompt=prompt,
            num_inference_steps=50,
            guidance_scale=7.5,
            height=512,
            width=512
        ).images[0]
        
        return image, prompt
    except Exception as e:
        return None, f"Error: {str(e)}"

def generate_multiple(craft_type, style_preference, fusion_level, additional_prompt, num_designs=5):
    """Generate multiple designs"""
    designs = []
    prompts = []
    
    for i in range(num_designs):
        print(f"Generating design {i+1}/{num_designs}...")
        image, prompt = generate_design(craft_type, style_preference, fusion_level, additional_prompt)
        if image:
            designs.append(image)
            prompts.append(prompt)
    
    return designs, "\n\n".join([f"Design {i+1}:\n{p}" for i, p in enumerate(prompts)])

# Gradio Interface
with gr.Blocks(title="AI Handicraft Design Generator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎨 AI Handicraft Design Generator
    
    Generate fusion designs by blending traditional Sri Lankan patterns with modern styles.
    """)
    
    with gr.Row():
        with gr.Column():
            craft_type = gr.Dropdown(
                choices=["mask", "batik", "wood_carving", "pottery"],
                value="mask",
                label="Craft Type"
            )
            
            style_preference = gr.Radio(
                choices=["traditional", "fusion", "modern"],
                value="fusion",
                label="Style Preference"
            )
            
            fusion_level = gr.Slider(
                minimum=0,
                maximum=100,
                value=50,
                step=10,
                label="Fusion Level (%)",
                info="0% = Traditional, 100% = Modern"
            )
            
            additional_prompt = gr.Textbox(
                label="Additional Details (Optional)",
                placeholder="e.g., bright colors, gold accents",
                lines=2
            )
            
            generate_btn = gr.Button("Generate 5 Designs", variant="primary", size="lg")
        
        with gr.Column():
            output_gallery = gr.Gallery(
                label="Generated Designs",
                columns=2,
                rows=2,
                height="auto"
            )
            
            prompt_display = gr.Textbox(
                label="Generated Prompts",
                lines=5,
                interactive=False
            )
    
    generate_btn.click(
        fn=generate_multiple,
        inputs=[craft_type, style_preference, fusion_level, additional_prompt],
        outputs=[output_gallery, prompt_display]
    )

if __name__ == "__main__":
    print("🚀 Starting Design Generator...")
    demo.launch(share=True)