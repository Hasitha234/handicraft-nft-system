# Frontend - Handicraft Image Recognition System

React-based web interface for the image recognition system.

## Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start development server:**
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## Features

- ✅ Image upload (drag & drop or file picker)
- ✅ Real-time search results
- ✅ Per-feature similarity breakdown
- ✅ Material & object type predictions
- ✅ Related products
- ✅ Outlet recommendations
- ✅ Modern, responsive UI

## API Configuration

The frontend connects to the backend API at `http://localhost:8000` by default.

To change this, create a `.env` file:
```
VITE_API_URL=http://your-api-url:8000
```

## Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.


