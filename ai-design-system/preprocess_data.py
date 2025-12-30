from pathlib import Path
from PIL import Image
import numpy as np
from tqdm import tqdm

# Paths
RAW_PATH = Path("data/raw-images")
PROCESSED_PATH = Path("data/processed")
TRAIN_PATH = PROCESSED_PATH / "train"
TEST_PATH = PROCESSED_PATH / "test"

# Create folders
for split in ['train', 'test']:
    for category in ['traditional', 'fusion', 'modern']:
        (PROCESSED_PATH / split / category).mkdir(parents=True, exist_ok=True)

def preprocess_image(img_path, output_path, size=(224, 224)):
    """Resize and normalize image"""
    try:
        with Image.open(img_path) as img:
            # Convert to RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize
            img = img.resize(size, Image.Resampling.LANCZOS)
            
            # Save as JPG
            img.save(output_path, 'JPEG', quality=95)
            return True
    except Exception as e:
        print(f"Error processing {img_path}: {e}")
        return False

def split_data(category, train_ratio=0.8):
    """Split images into train/test sets"""
    category_path = RAW_PATH / category
    images = sorted([f for f in category_path.iterdir() 
                     if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.jfif']])
    
    # Shuffle for randomness
    np.random.seed(42)
    np.random.shuffle(images)
    
    # Split
    split_idx = int(len(images) * train_ratio)
    train_images = images[:split_idx]
    test_images = images[split_idx:]
    
    print(f"\n{category.upper()}:")
    print(f"  Total: {len(images)}")
    print(f"  Train: {len(train_images)} ({len(train_images)/len(images)*100:.1f}%)")
    print(f"  Test: {len(test_images)} ({len(test_images)/len(images)*100:.1f}%)")
    
    # Process train set
    for img_file in tqdm(train_images, desc=f"Processing {category} train"):
        output_name = f"{category}_{img_file.stem}.jpg"
        output_path = TRAIN_PATH / category / output_name
        preprocess_image(img_file, output_path)
    
    # Process test set
    for img_file in tqdm(test_images, desc=f"Processing {category} test"):
        output_name = f"{category}_{img_file.stem}.jpg"
        output_path = TEST_PATH / category / output_name
        preprocess_image(img_file, output_path)
    
    return len(train_images), len(test_images)

if __name__ == "__main__":
    print("🚀 Starting data preprocessing...")
    print("=" * 60)
    
    total_train = 0
    total_test = 0
    
    for category in ['traditional', 'fusion', 'modern']:
        train_count, test_count = split_data(category)
        total_train += train_count
        total_test += test_count
    
    print("\n" + "=" * 60)
    print("✅ PREPROCESSING COMPLETE!")
    print(f"Total train images: {total_train}")
    print(f"Total test images: {total_test}")
    print(f"Total: {total_train + total_test}")
    print("=" * 60)