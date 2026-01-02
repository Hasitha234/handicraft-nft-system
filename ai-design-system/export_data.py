"""
Data Export Tool - For Thesis Analysis
Exports user preference data to CSV/Excel for statistical analysis
"""

import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime
import json

DB_PATH = Path("user_preferences.db")
OUTPUT_DIR = Path("exports")

def export_all_data():
    """Export all data for thesis analysis"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    if not DB_PATH.exists():
        print("❌ No database found. Collect user data first.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    
    # Export users
    users_df = pd.read_sql_query('SELECT * FROM users', conn)
    users_path = OUTPUT_DIR / f"users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    users_df.to_csv(users_path, index=False)
    print(f"✅ Users exported: {users_path}")
    
    # Export interactions
    interactions_df = pd.read_sql_query('SELECT * FROM interactions', conn)
    interactions_path = OUTPUT_DIR / f"interactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    interactions_df.to_csv(interactions_path, index=False)
    print(f"✅ Interactions exported: {interactions_path}")
    
    # Export combined analysis
    combined_df = pd.read_sql_query('''
        SELECT 
            u.user_id,
            u.user_type,
            u.age_group,
            u.gender,
            u.country,
            i.design_id,
            i.design_style,
            i.fusion_level,
            i.action,
            i.comment_text,
            i.timestamp
        FROM interactions i
        JOIN users u ON i.user_id = u.user_id
    ''', conn)
    
    combined_path = OUTPUT_DIR / f"combined_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    combined_df.to_csv(combined_path, index=False)
    print(f"✅ Combined data exported: {combined_path}")
    
    # Export to Excel (better for thesis)
    excel_path = OUTPUT_DIR / f"thesis_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        users_df.to_excel(writer, sheet_name='Users', index=False)
        interactions_df.to_excel(writer, sheet_name='Interactions', index=False)
        combined_df.to_excel(writer, sheet_name='Combined', index=False)
    
    print(f"✅ Excel file exported: {excel_path}")
    
    # Generate summary statistics
    summary = {
        "export_date": datetime.now().isoformat(),
        "total_users": len(users_df),
        "total_interactions": len(interactions_df),
        "user_types": users_df['user_type'].value_counts().to_dict(),
        "actions": interactions_df['action'].value_counts().to_dict(),
        "styles": combined_df['design_style'].value_counts().to_dict() if len(combined_df) > 0 else {}
    }
    
    summary_path = OUTPUT_DIR / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Summary exported: {summary_path}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 DATA SUMMARY")
    print("=" * 60)
    print(f"Total Users: {summary['total_users']}")
    print(f"Total Interactions: {summary['total_interactions']}")
    print(f"\nUser Types: {summary['user_types']}")
    print(f"Actions: {summary['actions']}")
    if summary['styles']:
        print(f"Styles: {summary['styles']}")
    print("=" * 60)
    
    conn.close()
    return excel_path

if __name__ == "__main__":
    export_all_data()