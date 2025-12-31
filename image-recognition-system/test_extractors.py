"""
Test script for all feature extractors
Tests each extractor individually on sample images
"""

import sys
from pathlib import Path
import numpy as np
from PIL import Image

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.image_processor import ImageProcessor
from app.services.feature_extractors.geometric_extractor import GeometricExtractor
from app.services.feature_extractors.color_extractor import ColorExtractor
from app.services.feature_extractors.texture_extractor import TextureExtractor
from app.services.feature_extractors.pattern_extractor import PatternExtractor
from app.services.feature_extractors.material_classifier import MaterialClassifier
from app.services.feature_extractors.object_type_classifier import ObjectTypeClassifier
from app.services.feature_extractors.master_extractor import MasterFeatureExtractor


def load_image(image_path: str) -> np.ndarray:
    """Load and preprocess image"""
    processor = ImageProcessor()
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    return processor.preprocess(image_bytes)


def test_geometric_extractor(image: np.ndarray):
    """Test geometric feature extractor"""
    print("\n" + "=" * 60)
    print("Testing Geometric Feature Extractor")
    print("=" * 60)
    
    extractor = GeometricExtractor()
    features = extractor.extract(image)
    
    print(f"Edge Count: {features['edge_count']}")
    print(f"Edge Density: {features['edge_density']:.4f}")
    print(f"Vertex Count: {features['vertex_count']}")
    print(f"Contour Count: {features['contour_count']}")
    print(f"Aspect Ratio: {features['aspect_ratio']:.4f}")
    print(f"Compactness: {features['compactness']:.4f}")
    print(f"Symmetry: {features['symmetry']:.4f}")
    print(f"Curvature: {features['curvature']:.4f}")
    print(f"Complexity: {features['complexity']:.4f}")
    print(f"Feature Vector Shape: {features['feature_vector'].shape}")
    print(f"Feature Vector (first 5): {features['feature_vector'][:5]}")


def test_color_extractor(image: np.ndarray):
    """Test color feature extractor"""
    print("\n" + "=" * 60)
    print("Testing Color Feature Extractor")
    print("=" * 60)
    
    extractor = ColorExtractor()
    features = extractor.extract(image)
    
    print(f"Brightness: {features['brightness']:.4f}")
    print(f"Saturation: {features['saturation']:.4f}")
    print(f"Contrast: {features['contrast']:.4f}")
    print(f"Color Uniformity: {features['color_uniformity']:.4f}")
    print(f"Color Transitions: {features['color_transitions']:.4f}")
    print(f"Dominant Colors (RGB): {features['dominant_colors']}")
    print(f"HSV Histogram H bins: {len(features['hsv_histogram']['h'])}")
    print(f"HSV Histogram S bins: {len(features['hsv_histogram']['s'])}")
    print(f"HSV Histogram V bins: {len(features['hsv_histogram']['v'])}")
    print(f"Feature Vector Shape: {features['feature_vector'].shape}")
    print(f"Feature Vector (first 10): {features['feature_vector'][:10]}")


def test_texture_extractor(image: np.ndarray):
    """Test texture feature extractor"""
    print("\n" + "=" * 60)
    print("Testing Texture Feature Extractor")
    print("=" * 60)
    
    extractor = TextureExtractor()
    features = extractor.extract(image)
    
    print(f"Roughness: {features['roughness']:.4f}")
    print(f"Grain Direction: {features['grain_direction']:.4f}")
    print(f"Texture Uniformity: {features['texture_uniformity']:.4f}")
    print(f"Pattern Strength: {features['pattern_strength']:.4f}")
    print(f"Irregularities: {features['irregularities']:.4f}")
    print(f"LBP Histogram bins: {len(features['lbp_histogram'])}")
    print(f"Feature Vector Shape: {features['feature_vector'].shape}")
    print(f"Feature Vector (first 10): {features['feature_vector'][:10]}")


def test_pattern_extractor(image: np.ndarray):
    """Test pattern feature extractor"""
    print("\n" + "=" * 60)
    print("Testing Pattern Feature Extractor")
    print("=" * 60)
    
    extractor = PatternExtractor()
    features = extractor.extract(image)
    
    print(f"Keypoint Count: {features['keypoint_count']}")
    print(f"Pattern Density: {features['pattern_density']:.4f}")
    print(f"Pattern Distribution: {features['pattern_distribution']:.4f}")
    print(f"Detail Strength: {features['detail_strength']:.4f}")
    print(f"Descriptor Vector Shape: {len(features['descriptor_vector'])}")
    print(f"Feature Vector Shape: {features['feature_vector'].shape}")
    print(f"Feature Vector (first 10): {features['feature_vector'][:10]}")


def test_material_classifier(image: np.ndarray):
    """Test material classifier"""
    print("\n" + "=" * 60)
    print("Testing Material Classifier")
    print("=" * 60)
    
    classifier = MaterialClassifier()
    result = classifier.classify(image)
    
    print(f"Predicted Material: {result['predicted_material']}")
    print(f"Confidence: {result['confidence']:.4f}")
    print("\nMaterial Probabilities:")
    for material, prob in result['probabilities'].items():
        bar = "=" * int(prob * 50)
        print(f"  {material:10s}: {prob:.4f} {bar}")
    print(f"Feature Vector Shape: {result['feature_vector'].shape}")


def test_object_type_classifier(image: np.ndarray):
    """Test object type classifier"""
    print("\n" + "=" * 60)
    print("Testing Object Type Classifier")
    print("=" * 60)
    
    classifier = ObjectTypeClassifier()
    result = classifier.classify(image)
    
    print(f"Predicted Type: {result['predicted_type']}")
    print(f"Confidence: {result['confidence']:.4f}")
    print("\nObject Type Probabilities:")
    for obj_type, prob in result['probabilities'].items():
        bar = "=" * int(prob * 50)
        print(f"  {obj_type:10s}: {prob:.4f} {bar}")
    print(f"Feature Vector Shape: {result['feature_vector'].shape}")


def test_master_extractor(image: np.ndarray):
    """Test master feature extractor"""
    print("\n" + "=" * 60)
    print("Testing Master Feature Extractor")
    print("=" * 60)
    
    extractor = MasterFeatureExtractor()
    all_features = extractor.extract_all(image)
    
    print("Extracted Features:")
    print(f"  - Geometric: {all_features['geometric']['feature_vector'].shape}")
    print(f"  - Color: {all_features['color']['feature_vector'].shape}")
    print(f"  - Texture: {all_features['texture']['feature_vector'].shape}")
    print(f"  - Pattern: {all_features['pattern']['feature_vector'].shape}")
    print(f"  - Material: {all_features['material']['feature_vector'].shape}")
    print(f"  - Object Type: {all_features['object_type']['feature_vector'].shape}")
    print(f"\nFused Vector Shape: {all_features['fused_vector'].shape}")
    print(f"Fused Vector (first 20): {all_features['fused_vector'][:20]}")
    
    print("\nSummary:")
    print(f"  Material: {all_features['material']['predicted_material']} "
          f"({all_features['material']['confidence']:.2%})")
    print(f"  Object Type: {all_features['object_type']['predicted_type']} "
          f"({all_features['object_type']['confidence']:.2%})")
    print(f"  Edges: {all_features['geometric']['edge_count']}")
    print(f"  Dominant Colors: {len(all_features['color']['dominant_colors'])}")
    print(f"  Keypoints: {all_features['pattern']['keypoint_count']}")


def main():
    """Main test function"""
    print("=" * 60)
    print("Feature Extractor Test Suite")
    print("=" * 60)
    
    # Get image path from command line or use default
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Use first image in images folder
        images_dir = Path("images")
        if images_dir.exists():
            image_files = list(images_dir.glob("*.png")) + list(images_dir.glob("*.jpg"))
            if image_files:
                image_path = str(image_files[0])
            else:
                print("[ERROR] No images found in images/ folder")
                print("Usage: python test_extractors.py <image_path>")
                sys.exit(1)
        else:
            print("[ERROR] Images folder not found")
            print("Usage: python test_extractors.py <image_path>")
            sys.exit(1)
    
    print(f"\n[INFO] Testing with image: {image_path}")
    
    try:
        # Load image
        print("\n[INFO] Loading image...")
        image = load_image(image_path)
        print(f"[OK] Image loaded: shape {image.shape}")
        
        # Test each extractor
        test_geometric_extractor(image)
        test_color_extractor(image)
        test_texture_extractor(image)
        test_pattern_extractor(image)
        test_material_classifier(image)
        test_object_type_classifier(image)
        test_master_extractor(image)
        
        print("\n" + "=" * 60)
        print("[SUCCESS] All extractors tested successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


