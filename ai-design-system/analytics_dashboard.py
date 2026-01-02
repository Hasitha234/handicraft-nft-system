"""
Analytics Dashboard - Component 3
Shows user preference statistics
"""

import sqlite3
import pandas as pd
import gradio as gr
from pathlib import Path

DB_PATH = Path("user_preferences.db")

def get_analytics():
    """Generate analytics report"""
    if not DB_PATH.exists():
        return "No data yet. Users need to interact with designs first."
    
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Load data
        df = pd.read_sql_query('''
            SELECT i.*, u.user_type, u.age_group
            FROM interactions i
            JOIN users u ON i.user_id = u.user_id
        ''', conn)
        
        if len(df) == 0:
            return "No interactions recorded yet."
        
        # Calculate stats
        stats = []
        stats.append("=" * 60)
        stats.append("📊 ANALYTICS DASHBOARD")
        stats.append("=" * 60)
        stats.append(f"\nTotal Interactions: {len(df)}")
        stats.append(f"Total Users: {df['user_id'].nunique()}")
        
        # Likes by style
        likes = df[df['action'] == 'like']
        if len(likes) > 0:
            stats.append(f"\n❤️ Likes: {len(likes)}")
            style_likes = likes['design_style'].value_counts()
            stats.append("\nLikes by Style:")
            for style, count in style_likes.items():
                stats.append(f"  {style.title()}: {count}")
        
        # User type breakdown
        user_types = df['user_type'].value_counts()
        stats.append("\n👥 User Types:")
        for utype, count in user_types.items():
            stats.append(f"  {utype}: {count}")
        
        # Fusion level preferences
        if len(likes) > 0:
            fusion_prefs = likes.groupby('fusion_level').size().sort_values(ascending=False)
            stats.append("\n🎨 Most Popular Fusion Levels:")
            for level, count in fusion_prefs.head(5).items():
                stats.append(f"  {level}%: {count} likes")
        
        conn.close()
        return "\n".join(stats)
    
    except Exception as e:
        conn.close()
        return f"Error: {str(e)}"

with gr.Blocks(title="Analytics Dashboard") as demo:
    gr.Markdown("# 📊 Handicraft Design Analytics")
    
    stats = gr.Textbox(label="Statistics", lines=20)
    refresh_btn = gr.Button("Refresh", variant="primary")
    
    refresh_btn.click(fn=get_analytics, outputs=[stats])
    demo.load(fn=get_analytics, outputs=[stats])

if __name__ == "__main__":
    demo.launch(share=True)