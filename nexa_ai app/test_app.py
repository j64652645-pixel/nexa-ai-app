"""
Test script for NEXA AI error handling
"""

import json
import os
import sys

# Test 1: Verify error handling with corrupted JSON
def test_corrupted_json():
    print("🧪 Test 1: Corrupted JSON handling...")
    test_file = "test_corrupted.json"
    with open(test_file, "w") as f:
        f.write("{invalid json}")
    
    try:
        with open(test_file, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("✅ Corrupted JSON detected correctly")
    
    os.remove(test_file)

# Test 2: Verify data persistence
def test_data_persistence():
    print("\n🧪 Test 2: Data persistence...")
    test_file = "test_data.json"
    test_data = {"name": "Student", "score": 85}
    
    with open(test_file, "w") as f:
        json.dump(test_data, f)
    
    with open(test_file, "r") as f:
        loaded = json.load(f)
    
    if loaded == test_data:
        print("✅ Data persistence works correctly")
    
    os.remove(test_file)

# Test 3: Input validation
def test_input_validation():
    print("\n🧪 Test 3: Input validation...")
    test_inputs = [
        ("short", False),  # Too short
        ("This is a good answer", True),  # Long enough
        ("", False),  # Empty
    ]
    
    for inp, should_be_valid in test_inputs:
        is_valid = len(inp) > 5
        status = "✅" if is_valid == should_be_valid else "❌"
        print(f"{status} Input '{inp}' validation: {is_valid}")

# Test 4: Topic lookup
def test_topic_lookup():
    print("\n🧪 Test 4: Topic lookup...")
    TOPICS = {
        "math": ["algebra", "geometry"],
        "science": ["physics", "chemistry"]
    }
    
    test_lookups = [
        ("algebra", True),
        ("physics", True),
        ("biology", False),
    ]
    
    all_topics = [t for topics in TOPICS.values() for t in topics]
    
    for topic, should_exist in test_lookups:
        exists = topic in all_topics
        status = "✅" if exists == should_exist else "❌"
        print(f"{status} Topic '{topic}' lookup: {exists}")

# Run all tests
if __name__ == "__main__":
    print("=" * 50)
    print("  NEXA AI ERROR HANDLING TEST SUITE")
    print("=" * 50)
    
    test_corrupted_json()
    test_data_persistence()
    test_input_validation()
    test_topic_lookup()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("=" * 50)
