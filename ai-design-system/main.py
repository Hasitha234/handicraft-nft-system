"""
Main Application Launcher
Unified entry point for all components
"""

import sys
import subprocess
from pathlib import Path

def show_menu():
    """Show main menu"""
    print("=" * 60)
    print("🎨 HANDICRAFT AI SYSTEM")
    print("=" * 60)
    print()
    print("1. 🖼️  Image Classification (Component 1)")
    print("2. 🎨 Design Generator (Component 2)")
    print("3. 👥 User Preference System (Component 3)")
    print("4. 📊 Analytics Dashboard")
    print("5. 🔌 API Server (All Components)")
    print("6. 📤 Export Data for Thesis")
    print("7. 🧪 Run Integration Tests")
    print("8. ❌ Exit")
    print()

def launch_classification():
    """Launch classification interface"""
    print("🚀 Starting Classification Interface...")
    subprocess.run([sys.executable, "app.py"])

def launch_generator():
    """Launch design generator"""
    print("🚀 Starting Design Generator...")
    subprocess.run([sys.executable, "design_generator.py"])

def launch_preferences():
    """Launch user preference system"""
    print("🚀 Starting User Preference System...")
    subprocess.run([sys.executable, "user_preference_system.py"])

def launch_analytics():
    """Launch analytics dashboard"""
    print("🚀 Starting Analytics Dashboard...")
    subprocess.run([sys.executable, "analytics_dashboard.py"])

def launch_api():
    """Launch API server"""
    print("🚀 Starting API Server...")
    print("📖 API Docs: http://127.0.0.1:8000/docs")
    subprocess.run([sys.executable, "api_server.py"])

def export_data():
    """Export data"""
    print("📤 Exporting data...")
    subprocess.run([sys.executable, "export_data.py"])

def run_tests():
    """Run integration tests"""
    print("🧪 Running integration tests...")
    subprocess.run([sys.executable, "test_integration.py"])

def main():
    """Main loop"""
    while True:
        show_menu()
        choice = input("Select option (1-8): ").strip()
        
        if choice == "1":
            launch_classification()
        elif choice == "2":
            launch_generator()
        elif choice == "3":
            launch_preferences()
        elif choice == "4":
            launch_analytics()
        elif choice == "5":
            launch_api()
        elif choice == "6":
            export_data()
        elif choice == "7":
            run_tests()
        elif choice == "8":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please select 1-8.")
        
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)