"""
NEXA AI Flask Web Application
Grade 9 Hybrid AI Revision Platform
"""

from flask import Flask, render_template, request, jsonify, session
import json
import os
import time
import math
import socket
from datetime import datetime
try:
    from dotenv import load_dotenv  # type: ignore
except Exception:
    # dotenv not available in minimal environments; provide a no-op fallback
    def load_dotenv():
        return None

# Load environment variables (if python-dotenv is installed)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

DATA_FILE = "nexa-ai-student-data.json"

# ==================
# SUBJECT & CONTENT
# ==================
SUBJECT_TOPICS = {
    "math": ["linear equations", "algebra", "ratio"],
    "biology": ["cells", "photosynthesis", "respiration"],
    "chemistry": ["states of matter", "separation of mixtures"],
    "physics": ["force", "energy", "motion"],
    "geography": ["weather", "climate"]
}

SIMPLE_EXPLANATIONS = {
    "linear equations": "A linear equation has power of x as 1. Example: 2x + 3 = 7.",
    "algebra": "Algebra uses letters to represent numbers.",
    "ratio": "Ratio compares two quantities.",
    "cells": "Cells are the basic units of life.",
    "photosynthesis": "Plants use sunlight to make food.",
    "respiration": "Respiration releases energy from food.",
    "states of matter": "Matter exists as solid, liquid, or gas.",
    "separation of mixtures": "Mixtures can be separated by filtration or evaporation.",
    "force": "A force is a push or pull.",
    "energy": "Energy is the ability to do work.",
    "motion": "Motion is a change in position.",
    "weather": "Weather is daily atmospheric condition.",
    "climate": "Climate is average weather over long time."
}

# ==================
# UTILITIES
# ==================
def is_online():
    """Check if internet connection is available."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

def load_student():
    """Load student data with error handling."""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                return data
    except json.JSONDecodeError:
        print("⚠️ Corrupted data file. Starting fresh.")
    except IOError as e:
        print(f"⚠️ Error loading file: {e}")
    
    return {
        "username": "Student",
        "baseline_done": False,
        "topic_strength": {},
        "mistakes": {},
        "study_log": {},
        "reflections": []
    }

def save_student(data):
    """Save student data with error handling."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except IOError as e:
        print(f"❌ Error saving data: {e}")
        return False

def get_student():
    """Get current student session data."""
    if 'student' not in session:
        session['student'] = load_student()
    return session['student']

def save_session_student(data):
    """Save student to session and file."""
    session['student'] = data
    save_student(data)

def forgetting_retention(topic, student_data):
    """Calculate retention based on forgetting curve."""
    try:
        last_time = student_data["study_log"].get(topic, time.time())
        hours = (time.time() - last_time) / 3600
        retention = math.exp(-0.15 * hours)
        return round(retention, 2)
    except:
        return 1.0

def readiness_score(student_data):
    """Calculate overall readiness score."""
    try:
        if not student_data["topic_strength"]:
            return 0
        avg = sum(student_data["topic_strength"].values()) / len(student_data["topic_strength"])
        return int(avg * 100)
    except:
        return 0

def register_mistake(topic, student_data):
    """Register a mistake and lower topic strength."""
    try:
        student_data["mistakes"].setdefault(topic, 0)
        student_data["mistakes"][topic] += 1
        student_data["topic_strength"][topic] = max(
            0.1, student_data["topic_strength"].get(topic, 0.5) - 0.1
        )
    except Exception as e:
        print(f"Error registering mistake: {e}")

# ==================
# ROUTES
# ==================

@app.route('/')
def index():
    """Home page."""
    student = get_student()
    return render_template('index.html', 
                         app_version="1.0",
                         online_status="🌐 ONLINE" if is_online() else "📴 OFFLINE")

@app.route('/api/student-info')
def api_student_info():
    """Get student info."""
    try:
        student = get_student()
        return jsonify({
            "status": "success",
            "data": {
                "username": student.get("username", "Student"),
                "baseline_done": student["baseline_done"],
                "readiness_score": readiness_score(student),
                "online": is_online()
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/baseline', methods=['POST'])
def api_baseline():
    """Complete baseline assessment."""
    try:
        student = get_student()
        
        if student["baseline_done"]:
            return jsonify({"status": "error", "message": "Baseline already completed"}), 400
        
        data = request.get_json()
        answers = data.get('answers', {})
        
        if not answers:
            return jsonify({"status": "error", "message": "No answers provided"}), 400
        
        score = 0
        for topic, answer in answers.items():
            if len(answer.strip()) > 5:
                student["topic_strength"][topic] = 0.7
                score += 1
            else:
                student["topic_strength"][topic] = 0.3
        
        student["baseline_done"] = True
        save_session_student(student)
        
        readiness = int((score / len(answers)) * 100) if answers else 0
        
        return jsonify({
            "status": "success",
            "readiness_score": readiness,
            "message": f"Baseline completed! Initial Readiness: {readiness}%"
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/dashboard')
def api_dashboard():
    """Get dashboard data."""
    try:
        student = get_student()
        
        topics_data = []
        for topic, strength in student["topic_strength"].items():
            retention = forgetting_retention(topic, student)
            topics_data.append({
                "topic": topic,
                "strength": round(strength, 2),
                "retention": retention,
                "mistakes": student["mistakes"].get(topic, 0)
            })
        
        return jsonify({
            "status": "success",
            "data": {
                "online": is_online(),
                "readiness_score": readiness_score(student),
                "topics": topics_data
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/quiz', methods=['POST'])
def api_quiz():
    """Process quiz answer."""
    try:
        student = get_student()
        
        if not student["topic_strength"]:
            return jsonify({"status": "error", "message": "No topics to quiz"}), 400
        
        data = request.get_json()
        topic = data.get('topic')
        answer = data.get('answer', '').strip().lower()
        
        if not topic or topic not in student["topic_strength"]:
            return jsonify({"status": "error", "message": "Invalid topic"}), 400
        
        if not answer:
            register_mistake(topic, student)
            save_session_student(student)
            return jsonify({
                "status": "success",
                "correct": False,
                "explanation": "Empty answer. Try again!",
                "online": is_online()
            })
        
        if topic in answer:
            student["topic_strength"][topic] += 0.05
            save_session_student(student)
            return jsonify({
                "status": "success",
                "correct": True,
                "explanation": "✅ Great understanding!"
            })
        else:
            register_mistake(topic, student)
            student["study_log"][topic] = time.time()
            save_session_student(student)
            
            explanation = "❌ Not quite right. "
            if is_online():
                explanation += f"Advanced tip for {topic}: This is a deeper concept related to fundamental science principles."
            else:
                explanation += f"Simple explanation: {SIMPLE_EXPLANATIONS.get(topic, 'Topic not found')}"
            
            return jsonify({
                "status": "success",
                "correct": False,
                "explanation": explanation,
                "online": is_online()
            })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/study-plan')
def api_study_plan():
    """Get personalized study plan."""
    try:
        student = get_student()
        
        if not student["topic_strength"]:
            return jsonify({"status": "error", "message": "Complete baseline first"}), 400
        
        ranked = sorted(student["topic_strength"], key=lambda t: student["topic_strength"][t])
        
        plan = []
        for topic in ranked[:5]:
            retention = forgetting_retention(topic, student)
            strength = round(student["topic_strength"][topic], 2)
            plan.append({
                "topic": topic,
                "strength": strength,
                "retention": retention,
                "priority": "High" if strength < 0.4 else "Medium" if strength < 0.7 else "Low"
            })
        
        return jsonify({
            "status": "success",
            "data": plan
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/exam-predictor')
def api_exam_predictor():
    """Predict likely exam topics."""
    try:
        student = get_student()
        
        if not student["topic_strength"]:
            return jsonify({"status": "error", "message": "No data available"}), 400
        
        predicted = sorted(student["topic_strength"], key=lambda t: student["topic_strength"][t])[:3]
        
        return jsonify({
            "status": "success",
            "data": predicted
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/explain', methods=['POST'])
def api_explain():
    """Explain a topic."""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        
        if not topic:
            return jsonify({"status": "error", "message": "Topic cannot be empty"}), 400
        
        if is_online():
            explanation = f"🌐 Advanced explanation for {topic}: This topic involves complex principles in science and has real-world applications."
        else:
            explanation = f"📴 {SIMPLE_EXPLANATIONS.get(topic, 'Topic not found in database.')}"
        
        return jsonify({
            "status": "success",
            "explanation": explanation,
            "online": is_online()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/reflection', methods=['POST'])
def api_reflection():
    """Save reflection."""
    try:
        student = get_student()
        data = request.get_json()
        entry = data.get('entry', '').strip()
        
        if not entry:
            return jsonify({"status": "error", "message": "Reflection cannot be empty"}), 400
        
        student["reflections"].append({
            "entry": entry,
            "timestamp": datetime.now().isoformat()
        })
        
        save_session_student(student)
        
        return jsonify({
            "status": "success",
            "message": "✅ Reflection saved!"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/topics')
def api_topics():
    """Get all available topics by subject."""
    return jsonify({
        "status": "success",
        "topics": SUBJECT_TOPICS
    })

@app.route('/api/reset', methods=['POST'])
def api_reset():
    """Reset student data (for testing)."""
    try:
        student = {
            "username": "Student",
            "baseline_done": False,
            "topic_strength": {},
            "mistakes": {},
            "study_log": {},
            "reflections": []
        }
        save_session_student(student)
        return jsonify({"status": "success", "message": "Data reset successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==================
# ERROR HANDLERS
# ==================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({"status": "error", "message": "Page not found"}), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return jsonify({"status": "error", "message": "Server error"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    print("=" * 50)
    print("  NEXA AI WEB SERVER STARTING")
    print(f"  http://localhost:{port}")
    print("=" * 50)
    app.run(debug=debug, port=port, host='0.0.0.0')
