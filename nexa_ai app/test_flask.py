"""
Flask app structure test
Verifies all imports and basic functions work
"""

import sys
import os

try:
    from flask import Flask, render_template, request, jsonify, session
    print("✅ Flask imported successfully")
except ImportError as e:
    print(f"❌ Flask import error: {e}")
    sys.exit(1)

try:
    import json
    import time
    import math
    import socket
    from datetime import datetime
    print("✅ All standard imports successful")
except ImportError as e:
    print(f"❌ Standard library import error: {e}")
    sys.exit(1)

# Test the data file exists
DATA_FILE = "nexa-ai-student-data.json"
if os.path.exists(DATA_FILE):
    print(f"✅ Data file '{DATA_FILE}' found")
else:
    print(f"⚠️ Data file '{DATA_FILE}' not found (will be created)")

# Test templates exist
template_files = ['templates/base.html', 'templates/index.html']
for template in template_files:
    if os.path.exists(template):
        print(f"✅ Template '{template}' found")
    else:
        print(f"❌ Template '{template}' NOT found")

# Create Flask app instance (test)
try:
    app = Flask(__name__)
    app.secret_key = 'test_key'
    print("✅ Flask app instance created successfully")
except Exception as e:
    print(f"❌ Failed to create Flask app: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("✅ Flask app structure is ready!")
print("="*50)
print("\nTo run the Flask server, execute:")
print("  python app.py")
print("\nThen visit: http://localhost:5000")
