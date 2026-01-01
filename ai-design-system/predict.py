"""
Inference Script - Classify New Handicraft Images
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import sys
from pathlib import Path

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Class names
class_names = ['Traditional', 'Fusion', 'Modern']

def load_model(model_path='models/best_model.pth'):
    """Load trained model"""
    model = models.resnet50(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 3)
    
    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()
    
    return model

def preprocess_image(image_path):
    """Preprocess image for inference"""
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                           std=[0.229, 0.224, 0.225])
    ])
    
    image = Image.open(image_path).convert('RGB')
    image_tensor = transform(image).unsqueeze(0)
    return image_tensor.to(device)

def predict(image_path, model):
    """Predict class for an image"""
    # Preprocess
    image_tensor = preprocess_image(image_path)
    
    # Predict
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        confidence, predicted = torch.max(probabilities, 0)
    
    return predicted.item(), confidence.item(), probabilities.cpu().numpy()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict.py <image_path>")
        print("Example: python predict.py test_image.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not Path(image_path).exists():
        print(f"❌ Error: Image not found at {image_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("🔍 Handicraft Classification")
    print("=" * 60)
    
    # Load model
    print("\nLoading model...")
    model = load_model()
    print("✅ Model loaded")
    
    # Predict
    print(f"\nAnalyzing: {image_path}")
    predicted_class, confidence, all_probs = predict(image_path, model)
    
    # Display results
    print("\n" + "=" * 60)
    print("📊 Results")
    print("=" * 60)
    print(f"Predicted Class: {class_names[predicted_class]}")
    print(f"Confidence: {confidence*100:.2f}%")
    print("\nAll Probabilities:")
    for i, class_name in enumerate(class_names):
        print(f"  {class_name}: {all_probs[i]*100:.2f}%")
    print("=" * 60)