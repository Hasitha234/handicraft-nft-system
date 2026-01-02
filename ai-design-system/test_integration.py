"""
Integration Test - Test All Components Together
"""

import sys
from pathlib import Path

def test_classification():
    """Test Component 1: Classification"""
    print("Testing Component 1: Classification...")
    try:
        from predict import predict, load_model
        model = load_model()
        
        # Test with a sample image
        test_image = Path("data/processed/test/traditional/traditional_1.jpg")
        if test_image.exists():
            pred_class, confidence, probs = predict(str(test_image), model)
            print(f"  ✅ Classification works: {pred_class} ({confidence*100:.2f}%)")
            return True
        else:
            print("  ⚠️  No test image found, skipping")
            return True
    except Exception as e:
        print(f"  ❌ Classification failed: {e}")
        return False

def test_design_generation():
    """Test Component 2: Design Generation"""
    print("Testing Component 2: Design Generation...")
    try:
        from design_generator import generate_design, load_model
        load_model()
        
        # Quick test generation
        image, prompt = generate_design("mask", "fusion", 60, "")
        if image:
            print(f"  ✅ Design generation works")
            print(f"  📝 Prompt: {prompt[:80]}...")
            return True
        else:
            print("  ❌ Generation returned None")
            return False
    except Exception as e:
        print(f"  ❌ Design generation failed: {e}")
        return False

def test_user_preferences():
    """Test Component 3: User Preferences"""
    print("Testing Component 3: User Preferences...")
    try:
        import sqlite3
        from user_preference_system import init_database, save_user, save_interaction
        
        # Test database
        init_database()
        user_id = save_user("Tourist", "25-34", "Male", "Germany")
        save_interaction(user_id, "1", "fusion", 60, "like", "Great design!")
        
        print(f"  ✅ Database operations work (User ID: {user_id})")
        return True
    except Exception as e:
        print(f"  ❌ User preferences failed: {e}")
        return False

def test_data_export():
    """Test Data Export"""
    print("Testing Data Export...")
    try:
        from export_data import export_all_data
        result = export_all_data()
        if result:
            print(f"  ✅ Data export works")
            return True
        else:
            print("  ⚠️  No data to export (this is OK if no users yet)")
            return True
    except Exception as e:
        print(f"  ❌ Data export failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("=" * 60)
    print("🧪 INTEGRATION TEST SUITE")
    print("=" * 60)
    print()
    
    results = {
        "Classification": test_classification(),
        "Design Generation": test_design_generation(),
        "User Preferences": test_user_preferences(),
        "Data Export": test_data_export()
    }
    
    print()
    print("=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    for component, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{component}: {status}")
    
    all_passed = all(results.values())
    
    print("=" * 60)
    if all_passed:
        print("🎉 All components working!")
    else:
        print("⚠️  Some components need attention")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)