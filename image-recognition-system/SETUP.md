# 🚀 Setup Guide - First Step Implementation

This guide will help you get the MVP image recognition system running on your computer.

## Step 1: Install Python

Make sure you have Python 3.8 or higher installed.

Check your version:
```bash
python --version
# or
python3 --version
```

If you don't have Python, download it from: https://www.python.org/downloads/

## Step 2: Navigate to Project Directory

```bash
cd image-recognition-system
```

## Step 3: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your command prompt.

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** This will:
- Download CLIP model (~350MB) - be patient!
- Install PyTorch, FAISS, FastAPI, and other dependencies
- May take 5-10 minutes depending on your internet speed

## Step 5: Run the Server

```bash
python run.py
```

Or:
```bash
python -m app.main
```

You should see output like:
```
🚀 Initializing Image Recognition System...
📦 Loading CLIP model: ViT-B/32 on cpu
✅ CLIP model loaded (embedding_dim=512)
🆕 Creating new FAISS index
📝 Creating sample products for testing...
💾 Saved index with 5 products
✅ System ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 6: Test the API

### Option 1: Use the Interactive Docs

Open your browser and go to:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Click on `/api/v1/search` → "Try it out" → Upload an image → Execute

### Option 2: Use curl (Command Line)

```bash
curl -X POST "http://localhost:8000/api/v1/search" \
  -F "file=@path/to/your/image.jpg"
```

### Option 3: Use Python Requests

Create a test script `test_api.py`:
```python
import requests

url = "http://localhost:8000/api/v1/search"
files = {"file": open("path/to/your/image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## What Happens on First Run?

1. ✅ CLIP model downloads and loads (one-time, ~350MB)
2. ✅ FAISS index is created
3. ✅ 5 sample products are added with random embeddings
4. ✅ Server starts on port 8000

## Troubleshooting

### "ModuleNotFoundError: No module named 'clip'"

Make sure you activated the virtual environment and installed requirements:
```bash
pip install -r requirements.txt
```

### "CUDA out of memory"

The system automatically uses CPU if CUDA is not available. This is fine for testing. For faster inference, you can use GPU if you have one with CUDA installed.

### Port 8000 already in use

Change the port in `run.py`:
```python
uvicorn.run(..., port=8001)  # Use different port
```

### Slow first request

The first request takes longer because models need to be loaded. Subsequent requests are faster.

## Next Steps

Once you have this working:

1. **Add Real Product Images:**
   - Use the `/api/v1/upload-product` endpoint to add real product images
   - Or create a script to batch-load images from a directory

2. **Test with Different Images:**
   - Try uploading various handicraft images
   - See how similarity scores change

3. **Check the Data:**
   - Look in the `data/` folder
   - You'll see `faiss_index.idx` and `metadata.pkl` files

## Understanding the Response

When you search, you'll get:
```json
{
  "query_id": "image.jpg",
  "total_matches": 5,
  "results": [
    {
      "product_id": "MASK_001",
      "title": "Traditional Sanni Mask",
      "description": "Hand-carved wooden mask...",
      "similarity_score": 0.75,  // 0.0 to 1.0 (1.0 = most similar)
      "rank": 1
    },
    ...
  ]
}
```

**Note:** Since we're using random embeddings for sample data, the similarity scores will be random. Once you add real product images with actual CLIP embeddings, the scores will be meaningful!

## Questions?

- Check the main README.md for more details
- Review the code comments for explanations
- Test with the interactive API docs at http://localhost:8000/docs

Happy coding! 🎉



