# 🛩️ AIRCRAFT ENGINE RUL DASHBOARD - FILE INDEX & NAVIGATION

## 📌 START HERE

### First Time? Read This First
👉 **[QUICK_START.md](QUICK_START.md)** - 30-second setup guide

### Need Full Details?
👉 **[00_PROJECT_SUMMARY.md](00_PROJECT_SUMMARY.md)** - Complete project overview

### Detailed Documentation?
👉 **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Comprehensive setup & troubleshooting

---

## 📦 DELIVERABLES (9 Files)

### 🎯 MAIN APPLICATION FILES

#### 1. **backend.py** (14 KB) ⭐ Core Backend
```python
python backend.py  # Start the API server
```
- Flask REST API server
- 3 ML models (LSTM, SVR, Linear Regression)
- Synthetic turbofan data (50 engines)
- 9 API endpoints
- Data preprocessing & prediction

**Runs on**: http://localhost:5000

---

#### 2. **dashboard.html** (25 KB) ⭐ Interactive UI
```
Double-click to open in browser
```
- Standalone React dashboard (no build needed!)
- 4 tabs: Overview, Engines, Prediction, Analysis
- Interactive charts and visualizations
- Beautiful dark theme
- Real-time data updates

**Opens as**: Local HTML file in your browser

---

### 🚀 LAUNCHER & SETUP SCRIPTS

#### 3. **launcher.py** (11 KB) ⭐ RECOMMENDED
```bash
python launcher.py  # Automated one-click setup
```
- Checks Python version
- Creates virtual environment
- Installs all dependencies
- Starts backend automatically
- Opens dashboard in browser

**Best For**: First-time users on any OS

---

#### 4. **run_windows.bat** (2 KB)
```
Double-click the file (Windows only)
```
- Automated setup for Windows
- Creates venv
- Installs dependencies
- Starts backend

**Best For**: Windows users wanting one-click launch

---

#### 5. **run_unix.sh** (2 KB)
```bash
chmod +x run_unix.sh
./run_unix.sh  # Mac/Linux one-click launch
```
- Automated setup for Mac/Linux
- Creates venv
- Installs dependencies
- Starts backend
- Opens browser

**Best For**: Mac and Linux users

---

### 📚 DOCUMENTATION

#### 6. **QUICK_START.md** (6 KB) ⚡ Fast Reference
```
Read this for quick answers!
```
- 30-second setup
- API quick reference
- Troubleshooting checklist
- Example workflows
- Command reference

**Read Time**: 5 minutes
**Best For**: Quick reference & getting started fast

---

#### 7. **SETUP_GUIDE.md** (14 KB) 📖 Full Guide
```
Read this for detailed help!
```
- Complete system architecture
- Step-by-step installation
- Detailed API documentation
- Configuration options
- Production deployment
- Comprehensive troubleshooting

**Read Time**: 20 minutes
**Best For**: Complete understanding & advanced config

---

#### 8. **00_PROJECT_SUMMARY.md** (15 KB) 📋 Overview
```
Read this for project context!
```
- All deliverables explained
- Feature overview
- Architecture diagram
- Getting started options
- Performance specifications
- Learning outcomes

**Read Time**: 15 minutes
**Best For**: Understanding what you have

---

### 🔧 CONFIGURATION

#### 9. **requirements.txt** (165 B)
```bash
pip install -r requirements.txt
```
- Python dependencies list
- Flask, TensorFlow, scikit-learn, pandas, numpy
- For virtual environment installation

---

## 🎯 QUICK NAVIGATION

### "I just want to start it now!"
```bash
python launcher.py
```
or double-click `dashboard.html` after starting backend

---

### "I want to understand what I have"
Read in this order:
1. QUICK_START.md (5 min)
2. 00_PROJECT_SUMMARY.md (15 min)

---

### "I need complete setup help"
Read in this order:
1. QUICK_START.md (5 min)
2. SETUP_GUIDE.md (20 min)

---

### "I want to customize everything"
1. Start with SETUP_GUIDE.md → "Configuration & Customization"
2. Edit backend.py for ML changes
3. Edit dashboard.html for UI changes

---

### "I need to deploy this to production"
1. Read SETUP_GUIDE.md → "Production Deployment"
2. Use gunicorn instead of Flask dev server
3. Add authentication
4. Configure HTTPS

---

## 📊 FILE DEPENDENCY TREE

```
00_PROJECT_SUMMARY.md (Start here for overview)
    ├── QUICK_START.md (Quick reference)
    ├── SETUP_GUIDE.md (Detailed help)
    └── Application Files:
        ├── backend.py (API Server)
        │   ├── requirements.txt (Dependencies)
        │   └── Trained ML Models
        │
        ├── dashboard.html (UI)
        │   └── Connects to backend API
        │
        └── frontend.jsx (React source code)
            └── Optional (for React development)
```

---

## ⚡ QUICK COMMAND REFERENCE

### Setup & Start (Pick One)

**Option 1: Auto-Launcher (Easiest)**
```bash
python launcher.py
```

**Option 2: Windows Batch**
```
Double-click run_windows.bat
```

**Option 3: Unix/Mac Shell**
```bash
bash run_unix.sh
```

**Option 4: Manual**
```bash
pip install -r requirements.txt
python backend.py
# Then open dashboard.html
```

---

### Test the System

```bash
# Check if backend is running
curl http://localhost:5000/api/health

# Get list of engines
curl http://localhost:5000/api/engines

# Get fleet statistics
curl http://localhost:5000/api/overview

# Run a prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"sensor_1": 300, "sensor_2": 250, ...}'
```

---

## 🗂️ FILE ORGANIZATION

```
project-folder/
│
├── 00_PROJECT_SUMMARY.md    ← Start here!
├── QUICK_START.md           ← Fast reference
├── SETUP_GUIDE.md           ← Full guide
│
├── backend.py               ← Backend server
├── dashboard.html           ← Frontend UI
├── frontend.jsx             ← React source (optional)
│
├── launcher.py              ← Auto-launcher
├── run_windows.bat          ← Windows launcher
├── run_unix.sh              ← Mac/Linux launcher
│
└── requirements.txt         ← Dependencies
```

---

## 🎓 LEARNING PATH

### Beginner (30 minutes)
1. Read QUICK_START.md
2. Run `python launcher.py`
3. Click around dashboard
4. Run a prediction
5. Done! ✅

### Intermediate (2 hours)
1. Read 00_PROJECT_SUMMARY.md
2. Read SETUP_GUIDE.md
3. Test all API endpoints with curl
4. Try different models
5. Explore different sensors

### Advanced (4+ hours)
1. Study backend.py code
2. Learn TensorFlow/LSTM
3. Customize ML models
4. Modify dashboard
5. Deploy to production

---

## ✅ SETUP VERIFICATION

After running setup, verify these work:

- [ ] `curl http://localhost:5000/api/health` returns OK
- [ ] dashboard.html opens and loads data
- [ ] Overview tab shows KPI cards
- [ ] Can select engine and see details
- [ ] Prediction tab runs without errors
- [ ] Models show in performance table
- [ ] Maintenance recommendations appear

If all pass, you're ready to go! ✅

---

## 🆘 HELP MATRIX

| You Need Help With | Read This | Section |
|-------------------|-----------|---------|
| Getting started | QUICK_START.md | Quick Start |
| Setup errors | SETUP_GUIDE.md | Troubleshooting |
| Understanding architecture | 00_PROJECT_SUMMARY.md | System Architecture |
| API usage | SETUP_GUIDE.md | API Endpoints |
| Customizing ML | backend.py comments | Code |
| Customizing UI | dashboard.html comments | Code |
| Production deployment | SETUP_GUIDE.md | Production Deployment |
| Configuration | SETUP_GUIDE.md | Configuration |

---

## 🔐 FILE DESCRIPTIONS AT A GLANCE

| File | Type | Size | Purpose | Run How |
|------|------|------|---------|---------|
| backend.py | Python | 14 KB | API & ML | `python backend.py` |
| dashboard.html | HTML/React | 25 KB | UI | Open in browser |
| launcher.py | Python | 11 KB | Setup automation | `python launcher.py` |
| run_windows.bat | Batch | 2 KB | Windows launcher | Double-click |
| run_unix.sh | Bash | 2 KB | Unix launcher | `bash run_unix.sh` |
| requirements.txt | Text | 165 B | Dependencies | `pip install -r` |
| QUICK_START.md | Markdown | 6 KB | Fast reference | Read |
| SETUP_GUIDE.md | Markdown | 14 KB | Full documentation | Read |
| 00_PROJECT_SUMMARY.md | Markdown | 15 KB | Project overview | Read |

---

## 🎯 COMMON WORKFLOWS

### Workflow 1: "Just get it running"
```
1. python launcher.py
2. Wait for browser to open
3. Explore dashboard
Done! 2 minutes ⏱️
```

### Workflow 2: "Test the API"
```
1. python launcher.py (or run backend separately)
2. In new terminal:
   curl http://localhost:5000/api/engines
3. Explore endpoints
Done! 5 minutes ⏱️
```

### Workflow 3: "Run a prediction"
```
1. Open dashboard.html
2. Go to "Prediction" tab
3. Select LSTM model
4. Click "Run Prediction"
5. See RUL and maintenance plan
Done! 3 minutes ⏱️
```

### Workflow 4: "Understand the system"
```
1. Read QUICK_START.md (5 min)
2. Read 00_PROJECT_SUMMARY.md (15 min)
3. Run launcher.py
4. Explore code in backend.py
5. Test all API endpoints
Done! 1-2 hours ⏱️
```

---

## 📞 SUPPORT QUICK LINKS

**Problem**: Connection refused  
**Solution**: Make sure `python backend.py` is running  
**Reference**: SETUP_GUIDE.md → Troubleshooting

**Problem**: Dependencies not installing  
**Solution**: Ensure Python 3.8+ installed, try `pip install --upgrade pip`  
**Reference**: SETUP_GUIDE.md → Installation

**Problem**: Port 5000 in use  
**Solution**: Kill existing process or use different port  
**Reference**: SETUP_GUIDE.md → Troubleshooting

**Problem**: Models not loading  
**Solution**: Wait 30+ seconds for training, check console logs  
**Reference**: SETUP_GUIDE.md → Troubleshooting

---

## 🚀 YOU'RE READY!

Everything you need is in this folder:

✅ Fully functional backend with ML models
✅ Beautiful interactive dashboard
✅ Automated setup scripts
✅ Complete documentation
✅ Test endpoints and data

**Next Step**: Run `python launcher.py` and explore!

---

**Version**: 1.0.0  
**Status**: Production Ready ✅  
**Last Updated**: April 2024

---

## 📋 CHECKLIST FOR FIRST RUN

- [ ] Read QUICK_START.md (5 min)
- [ ] Run `python launcher.py`
- [ ] Wait for browser to open
- [ ] See 4 KPI cards in Overview
- [ ] Select an engine in Engines tab
- [ ] Go to Prediction tab
- [ ] Run a prediction with LSTM
- [ ] See maintenance recommendations
- [ ] Congratulations! 🎉

---

**Happy flying! Your RUL prediction system is ready! 🛩️✨**
