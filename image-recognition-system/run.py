"""
Simple script to run the FastAPI server
Usage: python run.py
"""

import uvicorn
import sys
import os

if __name__ == "__main__":
    # On Windows, disable reload to avoid subprocess issues with venv
    # Use reload=False for production, or set reload=True only if needed
    use_reload = os.getenv("RELOAD", "false").lower() == "true"
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=use_reload,  # Disabled by default on Windows
        log_level="info"
    )



