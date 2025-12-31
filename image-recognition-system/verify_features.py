"""Quick script to verify enhanced features are loaded"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.clip_encoder import CLIPEncoder
from app.services.enhanced_vector_store import EnhancedVectorStore

clip_encoder = CLIPEncoder()
vector_store = EnhancedVectorStore()
vector_store.load_or_create_index(clip_encoder, create_sample_data=False)

print(f"Products: {len(vector_store.products)}")
print(f"Features: {len(vector_store.features)}")
if len(vector_store.features) > 0:
    print("\nSample product features:")
    sample_id = list(vector_store.features.keys())[0]
    features = vector_store.features[sample_id]
    print(f"Product ID: {sample_id}")
    print(f"  Has geometric: {'geometric' in features}")
    print(f"  Has color: {'color' in features}")
    print(f"  Has texture: {'texture' in features}")
    print(f"  Has pattern: {'pattern' in features}")
    print(f"  Has material: {'material' in features}")
    print(f"  Has object_type: {'object_type' in features}")
    if 'material' in features:
        print(f"  Material: {features['material'].get('predicted_material', 'N/A')}")
    if 'object_type' in features:
        print(f"  Object Type: {features['object_type'].get('predicted_type', 'N/A')}")


