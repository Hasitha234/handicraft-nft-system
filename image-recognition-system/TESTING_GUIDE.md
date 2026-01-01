# Testing Guide - Image Recognition System

## Quick Start Testing

### Option 1: Interactive API Documentation (Easiest)

1. **Start the server** (if not already running):
   ```bash
   python run.py
   ```

2. **Open your browser** and go to:
   ```
   http://localhost:8000/docs
   ```

3. **Test the search endpoint**:
   - Click on `POST /api/v1/search`
   - Click "Try it out"
   - Click "Choose File" and select an image from your `images/` folder
   - Click "Execute"
   - See the results!

### Option 2: Command Line Test Script

1. **Make sure server is running**:
   ```bash
   python run.py
   ```

2. **In a new terminal**, run the test script:
   ```bash
   python test_api.py images/1.png
   ```

### Option 3: Using curl (Command Line)

```bash
curl -X POST "http://localhost:8000/api/v1/search" \
  -F "file=@images/1.png"
```

### Option 4: Using Python Requests

```python
import requests

url = "http://localhost:8000/api/v1/search"
files = {"file": open("images/1.png", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## Available Endpoints

### 1. Health Check
```bash
GET http://localhost:8000/health
```

### 2. Search Similar Products
```bash
POST http://localhost:8000/api/v1/search
Content-Type: multipart/form-data
Body: file (image file)
```

### 3. Add Product to Index
```bash
POST http://localhost:8000/api/v1/upload-product
Content-Type: multipart/form-data
Body: 
  - file (image file)
  - product_id (optional)
  - title (optional)
  - description (optional)
```

## Expected Response Format

When you search, you'll get:
```json
{
  "query_id": "1.png",
  "total_matches": 5,
  "results": [
    {
      "product_id": "1",
      "title": "1",
      "description": "Handicraft product from 1.png",
      "similarity_score": 0.85,
      "rank": 1
    },
    ...
  ]
}
```

## Testing Tips

1. **Try different images**: Test with various images from your `images/` folder
2. **Check similarity scores**: Higher scores (closer to 1.0) mean better matches
3. **Compare results**: Upload the same image twice and see if it finds itself
4. **Test with similar items**: Upload images of similar handicrafts to see if they match

## Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Make sure all dependencies are installed
- Check for error messages in the terminal

### No results returned
- Make sure images were loaded: Check that `data/faiss_index.idx` exists
- Verify images were indexed: Should have 190 products

### Low similarity scores
- This is normal for CLIP-only search
- Scores will improve when we add more feature extractors in Step 2

## Next Steps After Testing

Once you've verified the system works:
- ✅ Basic search is functional
- ✅ Images are indexed
- ✅ API responds correctly

You're ready for **Step 2: Physical Feature Extraction**!


