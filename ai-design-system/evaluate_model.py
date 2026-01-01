"""
Model Evaluation Script
Generates confusion matrix, per-class metrics, and detailed analysis
"""

import torch
import torch.nn as nn
from torchvision import models
from torch.utils.data import DataLoader
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from dataset import test_loader, test_dataset

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_model(model_path='models/best_model.pth'):
    """Load trained model"""
    model = models.resnet50(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 3)
    
    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()
    
    return model

def evaluate_model(model, test_loader, device):
    """Evaluate model and return predictions"""
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    return np.array(all_preds), np.array(all_labels)

def plot_confusion_matrix(y_true, y_pred, class_names):
    """Create confusion matrix visualization"""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix - Handicraft Classification', fontsize=16, fontweight='bold')
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    plt.savefig('models/confusion_matrix.png', dpi=150, bbox_inches='tight')
    print("📊 Confusion matrix saved to: models/confusion_matrix.png")

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 Model Evaluation")
    print("=" * 60)
    
    # Load model
    print("\nLoading trained model...")
    model = load_model()
    print("✅ Model loaded")
    
    # Evaluate
    print("\nEvaluating on test set...")
    predictions, true_labels = evaluate_model(model, test_loader, device)
    
    # Calculate metrics
    accuracy = (predictions == true_labels).mean() * 100
    print(f"\n✅ Overall Test Accuracy: {accuracy:.2f}%")
    
    # Per-class metrics
    class_names = ['Traditional', 'Fusion', 'Modern']
    print("\n" + "=" * 60)
    print("📊 Classification Report")
    print("=" * 60)
    print(classification_report(true_labels, predictions, target_names=class_names))
    
    # Confusion matrix
    plot_confusion_matrix(true_labels, predictions, class_names)
    
    # Per-class accuracy
    print("\n" + "=" * 60)
    print("📈 Per-Class Performance")
    print("=" * 60)
    for i, class_name in enumerate(class_names):
        class_mask = true_labels == i
        if class_mask.sum() > 0:
            class_acc = (predictions[class_mask] == true_labels[class_mask]).mean() * 100
            print(f"{class_name}: {class_acc:.2f}% ({class_mask.sum()} samples)")
    
    print("\n" + "=" * 60)
    print("✅ Evaluation Complete!")
    print("=" * 60)