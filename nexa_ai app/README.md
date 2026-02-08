# 📚 NEXA AI - Grade 9 AI Revision Platform

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎓 About NEXA AI

NEXA AI is an intelligent, adaptive learning platform for Grade 9 students covering:
- **Math** - Linear equations, Algebra, Ratios
- **Biology** - Cells, Photosynthesis, Respiration
- **Chemistry** - States of Matter, Separation of Mixtures
- **Physics** - Force, Energy, Motion
- **Geography** - Weather, Climate

### ✨ Key Features

✅ **Offline-First Design** - Works without internet  
✅ **Online AI Assistance** - Enhanced explanations when online  
✅ **Adaptive Learning** - Questions adjust to your level  
✅ **Forgetting Curve** - Predicts retention rates  
✅ **Personalized Study Plans** - Focus on weak areas  
✅ **Progress Tracking** - Dashboard with real-time metrics  
✅ **Reflection Journal** - Document your learning journey  
✅ **Error Handling** - Robust & user-friendly  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git (optional, for GitHub deployment)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/nexa-ai-app.git
cd nexa-ai-app
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the app**
```bash
python app.py
```

5. **Open in browser**
```
http://localhost:5000
```

---

## 📁 Project Structure

```
nexa-ai-app/
├── app.py                          # Flask application
├── main.py                         # CLI version
├── requirements.txt                # Python dependencies
├── Procfile                        # Render deployment config
├── runtime.txt                     # Python version
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── nexa-ai-student-data.json       # User data storage
├── templates/
│   ├── base.html                   # Base template
│   └── index.html                  # Main dashboard
├── static/                         # Static files (CSS, JS, images)
└── DEPLOYMENT_GUIDE.md             # Deployment instructions
```

---

## 🎯 How It Works

### 1. **Baseline Assessment**
Start by completing a baseline assessment across all subjects to establish your initial knowledge level.

### 2. **Personalized Study Plan**
Get a customized study plan based on your weak areas, ranked by priority.

### 3. **Adaptive Quiz**
Take quizzes on your weakest topics. The system learns from your mistakes.

### 4. **Smart Explanations**
- **Offline Mode:** Get simple, clear explanations
- **Online Mode:** Access advanced AI-powered explanations with deeper insights

### 5. **Progress Tracking**
Monitor your progress with:
- Readiness Score (%)
- Topic Strength (0-100%)
- Retention Rates (forgetting curve)
- Mistake Tracking

### 6. **Reflection Journal**
Document what you found difficult and track your learning journey over time.

---

## 🌐 Deployment

### Deploy to Render (Recommended - Free)

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions.

**Quick Steps:**
1. Push code to GitHub
2. Connect GitHub to Render
3. Deploy in 3 clicks
4. Get live URL in 5 minutes

### Other Platforms
- **Heroku** - `heroku create` + `git push heroku main`
- **PythonAnywhere** - Upload files + configure WSGI
- **Replit** - Import GitHub repo + run

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
PORT=5000
```

---

## 📊 Data Storage

Student data is stored in `nexa-ai-student-data.json`:

```json
{
  "username": "Student",
  "baseline_done": true,
  "topic_strength": {
    "algebra": 0.75,
    "photosynthesis": 0.6
  },
  "mistakes": {
    "algebra": 2
  },
  "study_log": { ... },
  "reflections": [...]
}
```

---

## 🧪 Testing

### Run Tests

```bash
# Test error handling
python test_app.py

# Test Flask setup
python test_flask.py
```

### Manual Testing

1. Start the app: `python app.py`
2. Visit: `http://localhost:5000`
3. Complete baseline assessment
4. Test all features in the menu

---

## 🐛 Troubleshooting

### App won't start?
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port already in use?
```bash
# Change PORT in .env
PORT=8000
```

### Data not saving?
```bash
# Check file permissions
# Make sure nexa-ai-student-data.json exists and is writable
```

---

## 📝 License

This project is open source under the MIT License.

---

## 🙏 Acknowledgments

- Built with Python, Flask, and modern web technologies
- Inspired by spaced repetition learning techniques
- Designed for Grade 9 students worldwide

---

## 📞 Support & Contributing

**Issues?** Open an issue on GitHub  
**Want to contribute?** Fork the repo and submit a pull request  
**Questions?** Check the documentation or open a discussion

---

## 🎉 Let's Make Learning Smarter! 

**NEXA AI: Offline-First • Online-Boosted • AI-Powered** 💪📚

### Deploy Now! 
👉 [See Deployment Guide](DEPLOYMENT_GUIDE.md)
