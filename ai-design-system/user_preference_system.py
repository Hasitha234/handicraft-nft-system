"""
User Preference System - Component 3
Instagram-style interface for collecting design preferences
"""

import gradio as gr
import sqlite3
from pathlib import Path
import json
from datetime import datetime
import pandas as pd

DB_PATH = Path("user_preferences.db")

def init_database():
    """Initialize database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_type TEXT,
            age_group TEXT,
            gender TEXT,
            country TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            design_id TEXT,
            design_style TEXT,
            fusion_level INTEGER,
            action TEXT,
            comment_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_user(user_type, age_group, gender, country):
    """Save user info"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_type, age_group, gender, country)
        VALUES (?, ?, ?, ?)
    ''', (user_type, age_group, gender, country))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id

def save_interaction(user_id, design_id, design_style, fusion_level, action, comment=""):
    """Save interaction"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO interactions (user_id, design_id, design_style, fusion_level, action, comment_text)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, design_id, design_style, fusion_level, action, comment))
    conn.commit()
    conn.close()

# Load designs metadata
DESIGNS_DIR = Path("generated_designs")
if (DESIGNS_DIR / "metadata.json").exists():
    with open(DESIGNS_DIR / "metadata.json") as f:
        DESIGNS_METADATA = json.load(f)
else:
    DESIGNS_METADATA = []
    print("⚠️  No designs found! Run batch_generate.py first to create designs.")

init_database()

def load_design(idx):
    """Load design by index"""
    if len(DESIGNS_METADATA) == 0:
        return None, "No designs available. Generate designs first."
    
    idx = idx % len(DESIGNS_METADATA)
    design = DESIGNS_METADATA[idx]
    
    img_path = DESIGNS_DIR / design['filename']
    if img_path.exists():
        from PIL import Image
        image = Image.open(img_path)
    else:
        image = None
    
    info = f"**Design #{design['id']}**\n- Craft: {design['craft_type'].title()}\n- Style: {design['style'].title()}\n- Fusion: {design['fusion_level']}%"
    
    return image, info, idx

def register_and_start(utype, age, gen, country):
    """Register user and load first design"""
    user_id = save_user(utype, age, gen, country)
    return gr.update(visible=True), user_id, 0, *load_design(0)

def interact(user_id, design_idx, action, comment=""):
    """Handle user interaction"""
    if user_id and design_idx < len(DESIGNS_METADATA):
        design = DESIGNS_METADATA[design_idx]
        save_interaction(user_id, design['id'], design['style'], 
                        design['fusion_level'], action, comment)
        return f"✅ {action.title()}d!" if action != 'skip' else "⏭️ Skipped"
    return ""

def next_design(design_idx):
    """Load next design"""
    new_idx = (design_idx + 1) % len(DESIGNS_METADATA)
    return *load_design(new_idx), new_idx

# Create interface
with gr.Blocks(title="Handicraft Gallery", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎨 Handicraft Design Gallery\n\nBrowse and rate AI-generated designs!")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Your Info:")
            user_type = gr.Radio(["Tourist", "Local", "Expat"], value="Tourist", label="I am")
            age_group = gr.Dropdown(["18-24", "25-34", "35-44", "45-54", "55+"], value="25-34", label="Age")
            gender = gr.Radio(["Male", "Female", "Other"], label="Gender")
            country = gr.Textbox(label="Country", placeholder="e.g., Germany")
            start_btn = gr.Button("Start Browsing", variant="primary")
        
        with gr.Column(visible=False) as gallery_col:
            current_user_id = gr.State()
            current_design_idx = gr.State(0)
            
            design_image = gr.Image(label="Design", type="pil")
            design_info = gr.Markdown()
            feedback_msg = gr.Textbox(label="", interactive=False)
            
            with gr.Row():
                like_btn = gr.Button("❤️ Like")
                save_btn = gr.Button("🔖 Save")
                skip_btn = gr.Button("⏭️ Skip")
            
            comment_box = gr.Textbox(label="💬 Comment (optional)", lines=2)
            comment_btn = gr.Button("Post Comment")
            
            next_btn = gr.Button("Next Design →", variant="primary")
    
    # Events
    start_btn.click(
        fn=register_and_start,
        inputs=[user_type, age_group, gender, country],
        outputs=[gallery_col, current_user_id, current_design_idx, design_image, design_info]
    )
    
    like_btn.click(
        fn=lambda uid, idx: interact(uid, idx, "like"),
        inputs=[current_user_id, current_design_idx],
        outputs=[feedback_msg]
    )
    
    save_btn.click(
        fn=lambda uid, idx: interact(uid, idx, "save"),
        inputs=[current_user_id, current_design_idx],
        outputs=[feedback_msg]
    )
    
    next_btn.click(
        fn=next_design,
        inputs=[current_design_idx],
        outputs=[design_image, design_info, current_design_idx]
    )
    
    comment_btn.click(
        fn=lambda uid, idx, cmt: interact(uid, idx, "comment", cmt),
        inputs=[current_user_id, current_design_idx, comment_box],
        outputs=[feedback_msg]
    )

if __name__ == "__main__":
    print("🚀 Starting User Preference System...")
    demo.launch(share=True)