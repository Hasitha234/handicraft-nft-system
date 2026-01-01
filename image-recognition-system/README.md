# 🖼️ Image Recognition System

**Component:** Handicraft image recognition and similarity search  
**Team Member:** Rajapaksha D N  
**Status:** 🟡 In Progress (MVP)

## Overview

This system allows users to upload a photo of a handicraft item and find similar products from the LAKARCADE catalog. The MVP uses CLIP (Contrastive Language-Image Pre-Training) embeddings for semantic similarity search.

## 🎯 Current Status: MVP Phase 1

**What's Working:**
- ✅ Image upload and preprocessing
- ✅ CLIP embedding extraction
- ✅ FAISS vector database for fast similarity search
- ✅ REST API with FastAPI
- ✅ Basic similarity scoring

**Next Steps:**
- 🔲 Add real product data indexing
- 🔲 Implement per-feature scoring (shape, color, texture, pattern)
- 🔲 Add PostgreSQL for product metadata
- 🔲 Background removal/preprocessing
- 🔲 Graph database (Neo4j) for related items

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Navigate to the image-recognition-system directory:**
   ```bash
   cd image-recognition-system
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   **Note:** This will download the CLIP model (~350MB) on first run. The first startup may take a few minutes.

### Running the Server

```bash
python -m app.main
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at: `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Interactive API Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

## 📡 API Endpoints

### 1. Health Check
```http
GET /health
```

### 2. Search Similar Products
```http
POST /api/v1/search
Content-Type: multipart/form-data

Body: file (image file)
```

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/search" \
  -F "file=@path/to/your/image.jpg"
```

**Response:**
```json
{
  "query_id": "image.jpg",
  "total_matches": 5,
  "results": [
    {
      "product_id": "MASK_001",
      "title": "Traditional Sanni Mask",
      "description": "Hand-carved wooden mask...",
      "similarity_score": 0.85,
      "rank": 1
    },
    ...
  ]
}
```

### 3. Add Product to Index
```http
POST /api/v1/upload-product
Content-Type: multipart/form-data

Body:
  - file (image file)
  - product_id (optional)
  - title (optional)
  - description (optional)
```

## 📁 Project Structure

```
image-recognition-system/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   └── search.py           # Pydantic models
│   └── services/
│       ├── __init__.py
│       ├── image_processor.py  # Image preprocessing
│       ├── clip_encoder.py     # CLIP embedding extraction
│       └── vector_store.py     # FAISS vector database
├── data/                       # Generated data (gitignored)
│   ├── faiss_index.idx         # FAISS index file
│   └── metadata.pkl            # Product metadata
├── requirements.txt
├── README.md
└── .gitignore
```

## 🧪 Testing with Sample Data

The system automatically creates 5 sample products on first run (with random embeddings). To test:

1. Start the server
2. Use the `/api/v1/search` endpoint to upload any image
3. You'll get back 5 sample results (with random similarity scores)

**To use real product data:**
1. Prepare your product images
2. Use the `/api/v1/upload-product` endpoint to add each product
3. Or modify `vector_store.py` to load products from a directory

## 🔧 Configuration

### CLIP Model
Default model: `ViT-B/32` (faster, smaller)  
To use a larger model, edit `app/services/clip_encoder.py`:
```python
clip_encoder = CLIPEncoder(model_name="ViT-L/14")  # Better accuracy, slower
```

### Image Preprocessing
Default target size: 384px (shorter edge)  
Edit `app/services/image_processor.py` to change:
```python
image_processor = ImageProcessor(target_size=512)
```

## 🐛 Troubleshooting

### "CUDA out of memory" or slow performance
- The system automatically uses CPU if CUDA is not available
- To force CPU, edit `app/services/clip_encoder.py` and set `device="cpu"`

### "No module named 'clip'"
- Make sure you installed requirements: `pip install -r requirements.txt`
- The `clip-by-openai` package should install automatically

### Index not found
- This is normal on first run - a new index will be created
- Sample products will be automatically added

## 📚 Next Development Steps

1. **Add Real Product Data**
   - Create script to batch-load product images
   - Store product metadata in PostgreSQL

2. **Enhance Feature Extraction**
   - Add shape CNN (EfficientNet/ResNet)
   - Add color histogram extraction
   - Add texture analysis (LBP)
   - Add pattern descriptors (SIFT/ORB)

3. **Improve Similarity Scoring**
   - Implement per-feature scoring
   - Weighted fusion of multiple features
   - Re-ranking based on business rules

4. **Add Graph Database**
   - Store product relationships in Neo4j
   - Traverse graph for related items

5. **Production Features**
   - Background removal
   - Object detection
   - Material classification
   - User feedback loop
   - Monitoring and analytics

## 📝 Notes

- **For Academic Use:** This is a research project for SLIIT final year
- **Performance:** MVP focuses on functionality over optimization
- **Scalability:** FAISS can handle millions of vectors efficiently
- **GPU:** Optional but recommended for faster inference

## 📞 Support

For questions or issues, contact the team or refer to the main project README.
