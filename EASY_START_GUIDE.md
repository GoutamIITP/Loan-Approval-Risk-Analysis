# 🎯 EASY START GUIDE - One Command to Start Everything!

## ⚡ **THE EASIEST WAY TO START**

### Just Double-Click This File:

```
📄 START_HERE.bat
```

**That's it!** Everything will start automatically:

- ✅ Backend server
- ✅ Frontend server
- ✅ Browser opens automatically
- ✅ Ready to use!

---

## 🎬 What You'll See

### 1. **Startup Window** (Shows progress)

```
==========================================
🏦 Starting FinCrime Loan Risk System
==========================================

[1/5] Checking backend status...
[2/5] Starting Backend Server...
[3/5] Waiting for backend to initialize...
[4/5] Starting Frontend Server...
[5/5] Opening browser...

✅ System Started Successfully!
```

### 2. **Backend Window** (Keep this open!)

```
🏦 FinCrime Loan Risk Assessment API
==================================================
Starting server on http://localhost:5000
==================================================
✅ ML model loaded successfully!
```

### 3. **Frontend Window** (Keep this open!)

```
🌐 Frontend Server Running on http://localhost:8000
Press Ctrl+C to stop
```

### 4. **Browser** (Opens automatically!)

- Shows the loan assessment form
- Ready to test immediately!

---

## 🧪 Quick Test

Once the browser opens:

**Fill in the form:**

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

**Click:** "🔍 Assess Risk"

**Result:** ✅ APPROVED with LOW risk!

---

## 🛑 How to Stop

**Easy way:**

- Close the Backend window
- Close the Frontend window

**Or press:** `Ctrl+C` in each window

---

## 🔄 Restart

1. Stop the system (close windows)
2. Double-click `START_HERE.bat` again
3. Done!

---

## 🐛 If Something Goes Wrong

### Backend won't start?

```bash
# Open Command Prompt in project folder
cd backend
..\venv\Scripts\activate
python app.py
```

### Frontend won't start?

```bash
# Open Command Prompt in project folder
cd frontend
python -m http.server 8000
```

### Browser didn't open?

- Manually open: http://localhost:8000

---

## 📊 URLs to Remember

| What             | URL                          |
| ---------------- | ---------------------------- |
| **Main App**     | http://localhost:8000        |
| **Backend API**  | http://localhost:5000        |
| **Health Check** | http://localhost:5000/health |

---

## ✅ Success Checklist

After starting, you should see:

- [ ] Backend window showing "ML model loaded successfully"
- [ ] Frontend window showing "Serving HTTP on port 8000"
- [ ] Browser opened to http://localhost:8000
- [ ] Loan assessment form visible
- [ ] No error messages

---

## 🎯 That's It!

**To start:** Double-click `START_HERE.bat`

**To test:** Fill form → Click "Assess Risk"

**To stop:** Close the windows

**Simple!** 🚀

---

## 📚 More Information

- **Detailed Guide**: `HOW_TO_START.md`
- **Testing Guide**: `LOCAL_TESTING_GUIDE.md`
- **Full Docs**: `README.md`

---

**Built with ❤️ for FinCrime Risk Assessment**

_One click to start everything!_
