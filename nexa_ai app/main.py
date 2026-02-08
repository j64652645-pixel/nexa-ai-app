import json
import os
import time
import math
import random
import socket

DATA_FILE = "nexa-ai-student-data.json"

# =========================
# INTERNET / OFFLINE CHECK
# =========================
def is_online():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

# =========================
# CORE SUBJECT & CONTENT DB
# =========================
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

# =========================
# STUDENT MODEL (ML-STYLE)
# =========================
def load_student():
    """Load student data from JSON file with error handling."""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                return data
    except json.JSONDecodeError:
        print("⚠️  WARNING: Corrupted student data file. Starting fresh.")
    except IOError as e:
        print(f"⚠️  ERROR reading file: {e}. Starting fresh.")
    
    return {
        "baseline_done": False,
        "topic_strength": {},
        "mistakes": {},
        "study_log": {},
        "reflections": []
    }

def save_student(data):
    """Save student data to JSON file with error handling."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"❌ ERROR saving data: {e}")

student = load_student()

# =========================
# BASELINE ASSESSMENT
# =========================
def baseline_assessment():
    """Baseline assessment with input validation."""
    print("\n📋 NEXA AI Baseline Assessment")
    total = 0
    score = 0

    try:
        for subject, topics in SUBJECT_TOPICS.items():
            for topic in topics:
                print(f"\nWhat do you know about {topic}?")
                ans = input("Your answer: ").strip()
                total += 1

                if len(ans) > 5:
                    student["topic_strength"][topic] = 0.7
                    score += 1
                else:
                    student["topic_strength"][topic] = 0.3

        student["baseline_done"] = True
        save_student(student)

        readiness = int((score / total) * 100) if total > 0 else 0
        print(f"\n✅ Baseline completed. Initial Readiness Score: {readiness}%")
    except KeyboardInterrupt:
        print("\n⚠️  Baseline assessment cancelled.")
    except Exception as e:
        print(f"❌ ERROR during baseline: {e}")

# =========================
# FORGETTING CURVE
# =========================
def forgetting_retention(topic):
    last_time = student["study_log"].get(topic, time.time())
    hours = (time.time() - last_time) / 3600
    retention = math.exp(-0.15 * hours)
    return round(retention, 2)

# =========================
# READINESS SCORE
# =========================
def readiness_score():
    if not student["topic_strength"]:
        return 0
    avg = sum(student["topic_strength"].values()) / len(student["topic_strength"])
    return int(avg * 100)

# =========================
# SIMPLE LANGUAGE EXPLAINER
# =========================
def simple_explain(topic):
    return SIMPLE_EXPLANATIONS.get(topic, "Topic not found in database.")

# =========================
# ONLINE AI PLACEHOLDER
# =========================
def online_ai_explain(topic):
    # In real app, this would call cloud AI
    return f"(Online AI) Advanced explanation for {topic}. More examples and deeper help."

# =========================
# MISTAKE PATTERN ANALYSIS
# =========================
def register_mistake(topic):
    student["mistakes"].setdefault(topic, 0)
    student["mistakes"][topic] += 1

    student["topic_strength"][topic] = max(
        0.1, student["topic_strength"].get(topic, 0.5) - 0.1
    )

# =========================
# ADAPTIVE QUIZ ENGINE
# =========================
def adaptive_quiz():
    """Adaptive quiz with error handling."""
    try:
        if not student["topic_strength"]:
            print("⚠️  No topics to quiz on. Complete baseline assessment first.")
            return
        
        topic = min(student["topic_strength"], key=lambda t: student["topic_strength"][t])

        print(f"\n🎯 Adaptive Question on: {topic}")
        print(f"Explain: {topic}")
        ans = input("Your answer: ").strip().lower()

        if not ans:
            print("⚠️  Empty answer. Marking as incorrect.")
            register_mistake(topic)
        elif topic in ans:
            print("✅ Correct understanding!")
            student["topic_strength"][topic] += 0.05
        else:
            print("❌ Not correct.")

            if is_online():
                print("🌐 Using Online AI for better help...")
                print("Correct:", online_ai_explain(topic))
            else:
                print("📴 Offline mode.")
                print("Correct (simple):", simple_explain(topic))

            register_mistake(topic)

        student["study_log"][topic] = time.time()
        save_student(student)
    except Exception as e:
        print(f"❌ ERROR in quiz: {e}")

# =========================
# PERSONALIZED STUDY PLANNER
# =========================
def study_planner():
    print("\n🗓 Personalized Study Plan (NEXA AI)")
    ranked = sorted(student["topic_strength"], key=lambda t: student["topic_strength"][t])

    for topic in ranked[:5]:
        retention = forgetting_retention(topic)
        strength = round(student["topic_strength"][topic], 2)
        print(f"- {topic:20} | Strength: {strength} | Retention: {retention}")

# =========================
# EXAM QUESTION PREDICTOR
# =========================
def exam_predictor():
    print("\n📈 Likely Exam Focus Topics")
    predicted = sorted(student["topic_strength"], key=lambda t: student["topic_strength"][t])
    for t in predicted[:3]:
        print("-", t)

# =========================
# MULTI-SUBJECT DASHBOARD
# =========================
def dashboard():
    print("\n📊 NEXA AI MULTI-SUBJECT DASHBOARD")

    status = "🌐 ONLINE" if is_online() else "📴 OFFLINE"
    print("System Status:", status)

    for topic, strength in student["topic_strength"].items():
        retention = forgetting_retention(topic)
        print(f"{topic:22} | Strength: {round(strength,2)} | Retention: {retention}")

    print("\nOverall Readiness Score:", readiness_score(), "%")

# =========================
# REFLECTION JOURNAL
# =========================
def reflection_journal():
    """Reflection journal with error handling."""
    try:
        print("\n📝 Reflection Journal")
        entry = input("What was hard today? ").strip()
        
        if not entry:
            print("⚠️  Empty entry. Reflection not saved.")
            return
        
        student["reflections"].append(entry)
        save_student(student)
        print("✅ Reflection saved.")
    except Exception as e:
        print(f"❌ ERROR saving reflection: {e}")

# =========================
# MAIN NEXA AI SYSTEM
# =========================
def main():
    print("========================================")
    print("              NEXA AI")
    print(" Grade 9 Hybrid AI Revision Platform")
    print(" Offline-First • Online-Boosted AI")
    print("========================================")
    
    print("\n📚 APP OVERVIEW:")
    print("NEXA AI is an intelligent revision platform for Grade 9 students")
    print("covering Math, Biology, Chemistry, Physics, and Geography.")
    print("\n🎯 KEY FEATURES:")
    print("  • Baseline Assessment - Initial knowledge evaluation")
    print("  • Dashboard - Track progress across all topics")
    print("  • Personalized Study Plan - Focuses on your weak areas")
    print("  • Adaptive Quiz - Questions adapt to your level")
    print("  • Exam Predictor - Identifies likely exam topics")
    print("  • Smart Explainer - Offline mode + Online AI assistance")
    print("  • Reflection Journal - Track what you find difficult")
    print("\n🔄 SMART FEATURES:")
    print("  • Forgetting Curve Algorithm - Predicts retention rates")
    print("  • Mistake Tracking - Learns from your errors")
    print("  • Auto-saves Progress - Your data is preserved")
    print("\n🌐 CONNECTIVITY:")
    print("  • Works OFFLINE with simplified explanations")
    print("  • Activates ONLINE mode for advanced AI help (if internet available)")
    print("========================================\n")

    if not student["baseline_done"]:
        baseline_assessment()

    while True:
        try:
            print("\nMenu:")
            print("1. Dashboard")
            print("2. Personalized study plan")
            print("3. Adaptive quiz")
            print("4. Exam question predictor")
            print("5. Topic explainer (Offline/Online)")
            print("6. Reflection journal")
            print("7. Exit")

            choice = input("Choose option: ").strip()

            if choice == "1":
                dashboard()

            elif choice == "2":
                study_planner()

            elif choice == "3":
                adaptive_quiz()

            elif choice == "4":
                exam_predictor()

            elif choice == "5":
                topic = input("Enter topic: ").strip()
                
                if not topic:
                    print("⚠️  Topic cannot be empty.")
                    continue

                if is_online():
                    print("🌐 Online mode:")
                    print(online_ai_explain(topic))
                else:
                    print("📴 Offline mode:")
                    print(simple_explain(topic))

            elif choice == "6":
                reflection_journal()

            elif choice == "7":
                print("Goodbye! Keep improving with NEXA AI 💪📚")
                break

            else:
                print("❌ Invalid option. Please choose 1-7.")
        
        except KeyboardInterrupt:
            print("\n⚠️  App interrupted. Exiting...")
            break
        except Exception as e:
            print(f"❌ ERROR: {e}. Please try again.")

if __name__ == "__main__":
    main()
    