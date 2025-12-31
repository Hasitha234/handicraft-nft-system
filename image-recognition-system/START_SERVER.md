# How to Start the Backend Server

## Problem: Port 8000 Already in Use

If you see this error:
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
```

It means another process is using port 8000.

## Solution 1: Use the PowerShell Script (Easiest)

```powershell
cd image-recognition-system
.\start_backend.ps1
```

This script will:
- Automatically kill any process on port 8000
- Start the backend server

## Solution 2: Manual Fix

### Step 1: Find Process Using Port 8000
```powershell
netstat -ano | findstr :8000
```

### Step 2: Kill the Process
```powershell
taskkill /F /PID <process_id>
```

Replace `<process_id>` with the PID from Step 1.

### Step 3: Start Backend
```powershell
cd image-recognition-system
venv\Scripts\activate
python run.py
```

## Solution 3: Change Port (Alternative)

If you can't kill the process, change the port:

1. Edit `run.py`:
```python
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8001,  # Changed from 8000
    reload=False,
    log_level="info"
)
```

2. Update frontend `vite.config.js`:
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8001',  // Changed from 8000
    changeOrigin: true
  }
}
```

## Quick Check: Is Backend Running?

```powershell
curl http://localhost:8000/health
```

Should return: `{"status":"healthy",...}`

## Both Servers Running?

- **Backend**: `http://localhost:8000` (Python/FastAPI)
- **Frontend**: `http://localhost:3000` (React/Vite)

Open `http://localhost:3000` in your browser to use the system!


