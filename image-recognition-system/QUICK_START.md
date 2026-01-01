# Quick Start Guide 🚀

## Complete System Setup

### Prerequisites
- Python 3.8+ (with venv)
- Node.js 16+ and npm

### Step 1: Backend Setup

```bash
cd image-recognition-system

# Activate virtual environment
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

# Install Python dependencies (if not done)
pip install -r requirements.txt

# Start backend server
python run.py
```

Backend runs on: `http://localhost:8000`

### Step 2: Frontend Setup

Open a **new terminal**:

```bash
cd image-recognition-system/frontend

# Install dependencies (first time only)
npm install

# Start frontend development server
npm run dev
```

Frontend runs on: `http://localhost:3000`

### Step 3: Test the System

1. Open browser: `http://localhost:3000`
2. Upload an image from `images/` folder
3. See search results with all features!

## System Architecture

```
┌─────────────┐
│   Frontend  │  React + Vite (Port 3000)
│  (Browser)  │
└──────┬──────┘
       │ HTTP API
       ▼
┌─────────────┐
│   Backend   │  FastAPI (Port 8000)
│   (Python)  │
└──────┬──────┘
       │
       ├──► CLIP Encoder (Semantic Search)
       ├──► Feature Extractors (Physical Attributes)
       ├──► FAISS Vector DB (Similarity Search)
       └──► NetworkX Graph (Product Relationships)
```

## Features Available

✅ **Image Search**
- Upload image → Get similar products
- Multi-feature similarity scoring
- Per-feature breakdown visualization

✅ **Product Details**
- Material classification
- Object type classification
- Related products
- Outlet recommendations

✅ **Graph Database**
- 4,213 product relationships
- Material-based connections
- Type-based connections

## Troubleshooting

**Backend won't start:**
- Check port 8000 is free: `netstat -ano | findstr :8000`
- Kill process if needed: `taskkill /F /PID <pid>`

**Frontend can't connect:**
- Verify backend is running
- Check API status indicator (top right of frontend)
- Verify CORS is enabled (already configured)

**npm install fails:**
- Try: `npm install --legacy-peer-deps`
- Or: `npm cache clean --force` then retry

**Port conflicts:**
- Change frontend port in `frontend/vite.config.js`
- Change backend port in `run.py`

## Next Steps

1. ✅ Backend API - Complete
2. ✅ Multi-feature search - Complete
3. ✅ Graph database - Complete
4. ✅ Frontend UI - Complete
5. 🎯 **Ready for demo!**

## For Your Project Report

You now have:
- Complete image recognition system
- Multi-feature extraction (6 feature types)
- Graph-based product relationships
- Professional web interface
- Full API documentation

Perfect for 4th-year IT project demonstration! 🎓


