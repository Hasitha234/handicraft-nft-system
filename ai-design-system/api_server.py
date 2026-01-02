"""
Unified API Server - All Components
FastAPI server exposing classification, generation, and preference collection
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io
from pathlib import Path
import sqlite3
import json
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI(title="Handicraft AI System API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load classification model
CLASSIFICATION_MODEL = None
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_classification_model():
    """Load classification model"""
    global CLASSIFICATION_MODEL
    if CLASSIFICATION_MODEL is None:
        model = models.resnet50(weights=None)
        model.fc = nn.Linear(model.fc.in_features, 3)
        checkpoint = torch.load('models/best_model.pth', map_location=DEVICE)
        model.load_state_dict(checkpoint['model_state_dict'])
        model = model.to(DEVICE)
        model.eval()
        CLASSIFICATION_MODEL = model
    return CLASSIFICATION_MODEL

# Request/Response models
class ClassificationResponse(BaseModel):
    predicted_class: str
    confidence: float
    probabilities: dict

class UserRegistration(BaseModel):
    user_type: str
    age_group: str
    gender: str
    country: str

class Interaction(BaseModel):
    user_id: int
    design_id: str
    action: str
    comment: Optional[str] = ""

# API Endpoints

@app.get("/")
def root():
    """API health check"""
    return {
        "status": "online",
        "components": {
            "classification": "ready",
            "generation": "ready",
            "preferences": "ready"
        },
        "version": "1.0.0"
    }

@app.post("/classify", response_model=ClassificationResponse)
async def classify_image(file: UploadFile = File(...)):
    """Classify uploaded handicraft image"""
    try:
        # Load model
        model = load_classification_model()
        
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Preprocess
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])
        image_tensor = transform(image).unsqueeze(0).to(DEVICE)
        
        # Predict
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            confidence, predicted = torch.max(probabilities, 0)
        
        class_names = ['Traditional', 'Fusion', 'Modern']
        
        return ClassificationResponse(
            predicted_class=class_names[predicted.item()],
            confidence=float(confidence.item()),
            probabilities={
                class_names[i]: float(probabilities[i].item())
                for i in range(3)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/register")
async def register_user(user: UserRegistration):
    """Register new user"""
    conn = sqlite3.connect('user_preferences.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_type, age_group, gender, country)
        VALUES (?, ?, ?, ?)
    ''', (user.user_type, user.age_group, user.gender, user.country))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"user_id": user_id, "status": "registered"}

@app.post("/interact")
async def record_interaction(interaction: Interaction):
    """Record user interaction"""
    # Load design metadata
    designs_dir = Path("generated_designs")
    if (designs_dir / "metadata.json").exists():
        with open(designs_dir / "metadata.json") as f:
            designs = json.load(f)
        
        design = next((d for d in designs if str(d['id']) == interaction.design_id), None)
        if design:
            conn = sqlite3.connect('user_preferences.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO interactions (user_id, design_id, design_style, fusion_level, action, comment_text)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (interaction.user_id, interaction.design_id, design['style'],
                  design['fusion_level'], interaction.action, interaction.comment))
            conn.commit()
            conn.close()
            return {"status": "recorded"}
    
    raise HTTPException(status_code=404, detail="Design not found")

@app.get("/analytics")
async def get_analytics():
    """Get analytics data"""
    import pandas as pd
    
    if not Path('user_preferences.db').exists():
        return {"error": "No data available"}
    
    conn = sqlite3.connect('user_preferences.db')
    
    try:
        df = pd.read_sql_query('''
            SELECT i.*, u.user_type, u.age_group
            FROM interactions i
            JOIN users u ON i.user_id = u.user_id
        ''', conn)
        
        if len(df) == 0:
            return {"message": "No interactions yet"}
        
        likes = df[df['action'] == 'like']
        
        analytics = {
            "total_interactions": len(df),
            "total_users": df['user_id'].nunique(),
            "total_likes": len(likes),
            "likes_by_style": likes['design_style'].value_counts().to_dict() if len(likes) > 0 else {},
            "user_types": df['user_type'].value_counts().to_dict(),
            "popular_fusion_levels": likes.groupby('fusion_level').size().to_dict() if len(likes) > 0 else {}
        }
        
        conn.close()
        return analytics
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/designs")
async def list_designs():
    """List all available designs"""
    designs_dir = Path("generated_designs")
    if (designs_dir / "metadata.json").exists():
        with open(designs_dir / "metadata.json") as f:
            designs = json.load(f)
        return {"designs": designs, "count": len(designs)}
    return {"designs": [], "count": 0}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting API Server...")
    print("=" * 60)
    print("API Documentation: http://127.0.0.1:8000/docs")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)