"""
Gradio Web Interface for Handicraft Classification
"""

import gradio as gr
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from pathlib import Path

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Class names
class_names = ['Traditional', 'Fusion', 'Modern']

def load_model():
    """Load trained model"""
    model = models.resnet50(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 3)
    
    checkpoint = torch.load('models/best_model.pth', map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()
    return model

# Load model once at startup
model = load_model()

def preprocess_image(image):
    """Preprocess image"""
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])
    
    if isinstance(image, str):
        image = Image.open(image).convert('RGB')
    else:
        image = image.convert('RGB')
    
    image_tensor = transform(image).unsqueeze(0)
    return image_tensor.to(device)

def classify_image(image):
    """Classify uploaded image"""
    if image is None:
        return "Please upload an image", {}
    
    # Preprocess
    image_tensor = preprocess_image(image)
    
    # Predict
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        confidence, predicted = torch.max(probabilities, 0)
    
    # Format results
    result_text = f"**Predicted:** {class_names[predicted.item()]}\n"
    result_text += f"**Confidence:** {confidence.item()*100:.2f}%"
    
    # Create label dictionary for Gradio
    label_dict = {
        class_names[i]: float(probabilities[i].item()) 
        for i in range(3)
    }
    
    return result_text, label_dict

# Create Gradio interface
with gr.Blocks(title="Sri Lankan Handicraft Classifier", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎨 Sri Lankan Handicraft Classifier
    
    Upload an image of a Sri Lankan handicraft to classify it as **Traditional**, **Fusion**, or **Modern**.
    
    **Model Accuracy:** 79.25% on test set
    """)
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="Upload Handicraft Image")
            classify_btn = gr.Button("Classify", variant="primary", size="lg")
        
        with gr.Column():
            text_output = gr.Markdown(label="Prediction")
            label_output = gr.Label(label="Confidence Scores", num_top_classes=3)
    
    # Examples
    gr.Examples(
        examples=[
            ["data/processed/test/traditional/traditional_1.jpg"],
            ["data/processed/test/fusion/fusion_1.jpg"],
            ["data/processed/test/modern/modern_1.jpg"],
        ],
        inputs=image_input
    )
    
    # Connect button
    classify_btn.click(
        fn=classify_image,
        inputs=image_input,
        outputs=[text_output, label_output]
    )
    
    # Auto-classify on upload
    image_input.upload(
        fn=classify_image,
        inputs=image_input,
        outputs=[text_output, label_output]
    )

if __name__ == "__main__":
    print("🚀 Starting Gradio interface...")
    print("=" * 60)
    print("Open the URL shown below in your browser")
    print("=" * 60)
    demo.launch(share=True)  # share=True creates public URL