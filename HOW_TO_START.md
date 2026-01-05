# 🚀 How to Start the Complete System

## ⚡ Quick Start (One Command)

### **Option 1: Double-Click Method (Easiest!)**

Simply **double-click** this file:

```
START_HERE.bat
```

That's it! The system will:

1. ✅ Start the backend server
2. ✅ Start the frontend server
3. ✅ Open your browser automatically
4. ✅ Show you the application

---

### **Option 2: Command Line**

Open Command Prompt or PowerShell in the project folder and run:

```bash
START_HERE.bat
```

Or directly run the PowerShell script:

```powershell
powershell -ExecutionPolicy Bypass -File start_system.ps1
```

---

## 📊 What Happens When You Start

### Step-by-Step Process

```
[1/5] Checking backend status...
      ↓
[2/5] Starting Backend Server (Flask API)
      → Opens in new window
      → Runs on http://localhost:5000
      ↓
[3/5] Waiting for backend to be ready...
      → Checks health endpoint
      → Waits up to 15 seconds
      ↓
[4/5] Starting Frontend Server (HTTP Server)
      → Opens in new window
      → Runs on http://localhost:8000
      ↓
[5/5] Opening browser automatically
      → Navigates to http://localhost:8000
      ↓
✅ System Ready!
```

---

## 🪟 Windows You'll See

After starting, you'll see **3 windows**:

### 1. **Startup Window** (This closes automatically)

- Shows startup progress
- Confirms everything started
- Can be closed after startup

### 2. **Backend Server Window** (Keep Open!)

```
🏦 FinCrime Loan Risk Assessment API
==================================================
Starting server on http://localhost:5000
==================================================
 * Running on http://127.0.0.1:5000
 * Debugger is active!
```

### 3. **Frontend Server Window** (Keep Open!)

```
🌐 Frontend Server Running on http://localhost:8000
Press Ctrl+C to stop
Serving HTTP on 0.0.0.0 port 8000...
```

### 4. **Browser Window** (Your Application!)

- Opens automatically
- Shows the loan assessment form
- Ready to use immediately

---

## 🌐 URLs After Startup

| Service          | URL                                  | Purpose             |
| ---------------- | ------------------------------------ | ------------------- |
| **Frontend**     | http://localhost:8000                | Main application UI |
| **Backend API**  | http://localhost:5000                | REST API endpoints  |
| **Health Check** | http://localhost:5000/health         | Backend status      |
| **Statistics**   | http://localhost:5000/api/statistics | System stats        |

---

## 🧪 Quick Test After Startup

Once the browser opens, try this:

### Test Case: Low Risk Application

Fill in the form:

```
Applicant Income: 8000
Co-applicant Income: 2000
Loan Amount: 150
Loan Term: 360 months
Credit History: Good (1)
Property Area: Urban
Self Employed: No
Dependents: 1
```

Click **"🔍 Assess Risk"**

**Expected Result:** ✅ APPROVED with LOW risk

---

## 🛑 How to Stop the System

### Method 1: Close Windows

- Close the **Backend Server** window
- Close the **Frontend Server** window
- Close the **Browser** tab

### Method 2: Press Ctrl+C

- In the **Backend Server** window: Press `Ctrl+C`
- In the **Frontend Server** window: Press `Ctrl+C`

### Method 3: Kill Processes (If stuck)

```bash
# Kill backend
taskkill /F /IM python.exe

# Or use PowerShell
Get-Process python | Stop-Process -Force
```

---

## 🔄 Restart the System

If you need to restart:

1. **Stop** both servers (Ctrl+C or close windows)
2. **Wait** 2-3 seconds
3. **Run** `START_HERE.bat` again

---

## 🐛 Troubleshooting

### Problem: "Port 5000 already in use"

**Solution:**

```bash
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual number)
taskkill /F /PID <PID>

# Or restart the system
```

### Problem: "Port 8000 already in use"

**Solution:**

```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /F /PID <PID>
```

### Problem: Backend won't start

**Solution:**

```bash
# Activate environment manually
venv\Scripts\activate

# Try starting backend manually
cd backend
python app.py
```

### Problem: Frontend won't open

**Solution:**

```bash
# Open manually in browser
start http://localhost:8000

# Or navigate to:
# frontend/index.html (double-click)
```

### Problem: Browser doesn't open automatically

**Solution:**

- Manually open browser
- Navigate to: http://localhost:8000

### Problem: "Python not found"

**Solution:**

```bash
# Check Python installation
python --version

# If not installed, download from:
# https://www.python.org/downloads/
```

---

## 📁 Startup Scripts Explained

### `START_HERE.bat` (Main Entry Point)

- **What it does**: Launches the PowerShell script
- **Fallback**: Uses batch script if PowerShell fails
- **Best for**: Double-clicking

### `start_system.ps1` (PowerShell Script)

- **What it does**: Smart startup with health checks
- **Features**:
  - Checks if ports are available
  - Waits for backend to be ready
  - Opens browser automatically
  - Shows detailed progress
- **Best for**: Advanced users

### `start_complete.bat` (Batch Script)

- **What it does**: Simple startup without checks
- **Features**:
  - Starts both servers
  - Opens browser
  - No health checks
- **Best for**: Fallback option

---

## ⚙️ Advanced Options

### Start Backend Only

```bash
cd backend
..\venv\Scripts\activate
python app.py
```

### Start Frontend Only

```bash
cd frontend
python -m http.server 8000
```

### Custom Ports

**Backend (edit `backend/app.py`):**

```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port
```

**Frontend:**

```bash
python -m http.server 8001  # Change port
```

---

## 🎯 Startup Checklist

Before starting, ensure:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created (`venv` folder exists)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] ML model trained (files in `backend/models/`)
- [ ] Ports 5000 and 8000 are free

---

## 📊 What Runs Where

```
┌─────────────────────────────────────────┐
│         Your Computer (localhost)       │
├─────────────────────────────────────────┤
│                                         │
│  Port 5000: Backend (Flask)             │
│  ├── API Endpoints                      │
│  ├── ML Model                           │
│  ├── Risk Engine                        │
│  └── Audit Logger                       │
│                                         │
│  Port 8000: Frontend (HTTP Server)      │
│  ├── HTML/CSS/JavaScript                │
│  ├── User Interface                     │
│  └── Connects to Backend                │
│                                         │
│  Browser: http://localhost:8000         │
│  └── Displays the application           │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🎓 Understanding the Startup

### Why Two Servers?

1. **Backend (Port 5000)**

   - Handles business logic
   - Runs ML model
   - Processes loan applications
   - Stores audit logs

2. **Frontend (Port 8000)**
   - Serves HTML/CSS/JavaScript
   - Provides user interface
   - Sends requests to backend
   - Displays results

### Why Not Just Open HTML File?

Opening `index.html` directly causes CORS issues when calling the backend API. Running a local HTTP server solves this.

---

## 🚀 Quick Commands Reference

```bash
# Start everything
START_HERE.bat

# Check backend health
curl http://localhost:5000/health

# Check frontend
curl http://localhost:8000

# View backend logs
# (Check the Backend Server window)

# Stop everything
# Press Ctrl+C in both server windows
```

---

## 🎉 Success Indicators

You'll know the system started successfully when you see:

✅ **Backend Server Window** shows:

```
✅ ML model loaded successfully!
✅ Application initialized successfully!
Starting server on http://localhost:5000
```

✅ **Frontend Server Window** shows:

```
Serving HTTP on 0.0.0.0 port 8000...
```

✅ **Browser** opens automatically to http://localhost:8000

✅ **Application** displays the loan assessment form

---

## 📝 Tips

1. **Keep server windows open** - Don't close them while using the app
2. **Check backend logs** - Useful for debugging
3. **Refresh browser** - If UI doesn't update
4. **Restart if needed** - Close and run `START_HERE.bat` again
5. **Check ports** - Make sure 5000 and 8000 are free

---

## 🎯 Next Steps After Starting

1. ✅ System starts automatically
2. ✅ Browser opens to the application
3. ✅ Fill out the loan application form
4. ✅ Click "🔍 Assess Risk"
5. ✅ See instant results!
6. ✅ Check statistics dashboard
7. ✅ Try different test cases

---

## 📚 Additional Resources

- **Testing Guide**: `LOCAL_TESTING_GUIDE.md`
- **Model Details**: `MODEL_TRAINING_EXPLAINED.md`
- **Full Documentation**: `README.md`
- **Project Summary**: `PROJECT_SUMMARY.md`

---

**Ready to start? Just double-click `START_HERE.bat`!** 🚀

---

**Built with ❤️ for FinCrime Risk Assessment**

_One command to rule them all!_
