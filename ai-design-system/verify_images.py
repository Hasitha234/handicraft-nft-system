"""
Image Quality Verification Script
Checks all collected images for quality, dimensions, and issues
"""

import os
from pathlib import Path
from PIL import Image
import pandas as pd

# Path to your images
BASE_PATH = Path(r"C:\Users\bdils\OneDrive\Desktop\research\handicraft-nft-system\ai-design-system\data\raw-images")

def verify_images():
    """Check all images and generate quality report"""
    
    results = []
    categories = ['traditional', 'fusion', 'modern']
    
    print("🔍 Verifying image quality...")
    print("=" * 60)
    
    for category in categories:
        folder_path = BASE_PATH / category
        
        if not folder_path.exists():
            print(f"⚠️  Folder not found: {category}")
            continue
        
        print(f"\n📁 Checking {category.upper()} folder...")
        
        image_files = list(folder_path.glob("*.*"))
        image_files = [f for f in image_files if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.jfif']]
        
        for img_file in image_files:
            try:
                with Image.open(img_file) as img:
                    width, height = img.size
                    format_type = img.format
                    file_size = img_file.stat().st_size / (1024 * 1024)  # MB
                    
                    # Quality checks
                    is_hd = width >= 1920 or height >= 1080
                    is_square = abs(width - height) < 50  # Close to square
                    is_large = file_size > 0.5  # > 500KB
                    
                    results.append({
                        'category': category,
                        'filename': img_file.name,
                        'width': width,
                        'height': height,
                        'format': format_type,
                        'size_mb': round(file_size, 2),
                        'is_hd': is_hd,
                        'is_square': is_square,
                        'is_large': is_large,
                        'status': '✅ Good' if (is_hd and is_large) else '⚠️ Check'
                    })
                    
            except Exception as e:
                results.append({
                    'category': category,
                    'filename': img_file.name,
                    'width': 0,
                    'height': 0,
                    'format': 'ERROR',
                    'size_mb': 0,
                    'is_hd': False,
                    'is_square': False,
                    'is_large': False,
                    'status': f'❌ ERROR: {str(e)}'
                })
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Save report
    report_path = BASE_PATH.parent / 'metadata' / 'image_quality_report.csv'
    report_path.parent.mkdir(exist_ok=True)
    df.to_csv(report_path, index=False)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 QUALITY SUMMARY")
    print("=" * 60)
    
    for category in categories:
        cat_df = df[df['category'] == category]
        total = len(cat_df)
        hd_count = cat_df['is_hd'].sum()
        good_count = len(cat_df[cat_df['status'] == '✅ Good'])
        errors = len(cat_df[cat_df['status'].str.contains('ERROR', na=False)])
        
        print(f"\n{category.upper()}:")
        print(f"  Total images: {total}")
        print(f"  HD quality: {hd_count}/{total} ({hd_count/total*100:.1f}%)")
        print(f"  Good quality: {good_count}/{total} ({good_count/total*100:.1f}%)")
        if errors > 0:
            print(f"  ⚠️  Errors: {errors}")
    
    print("\n" + "=" * 60)
    print(f"✅ Report saved to: {report_path}")
    print("=" * 60)
    
    return df

if __name__ == "__main__":
    try:
        df = verify_images()
        
        # Show sample of issues
        issues = df[df['status'] != '✅ Good']
        if len(issues) > 0:
            print("\n⚠️  Images that need attention:")
            print(issues[['category', 'filename', 'status']].head(10))
        
    except ImportError:
        print("❌ Missing required packages!")
        print("Install with: pip install pillow pandas")
    except Exception as e:
        print(f"❌ Error: {e}")










