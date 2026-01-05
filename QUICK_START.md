# 🚀 Quick Start Guide - FinCrime Loan Risk System

Get up and running in **5 minutes**!

## ✅ Prerequisites Check

```bash
# Check Python version (need 3.8+)
python --version

# Check pip
python -m pip --version
```

## 📦 Installation (2 minutes)

### Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install flask flask-cors pandas numpy scikit-learn joblib
```

### Step 2: Train ML Model

```bash
cd notebooks
python train_model.py
cd ..
```

**Expected output:**

```
✅ Model training complete!
Saved files:
  - backend/models/loan_model.pkl
  - backend/models/label_encoder.pkl
  - backend/models/feature_importance.csv
  - backend/models/model_metadata.json
```

## 🎯 Running the System (1 minute)

### Option 1: Using the Batch Script (Windows)

```bash
start.bat
```

### Option 2: Manual Start

```bash
# Activate environment
venv\Scripts\activate

# Start backend
cd backend
python app.py
```

**You should see:**

```
🏦 FinCrime Loan Risk Assessment API
==================================================
Starting server on http://localhost:5000
==================================================
```

## 🌐 Open the Frontend

1. Open a new terminal/command prompt
2. Navigate to the `frontend` folder
3. Double-click `index.html` OR run:

```bash
python -m http.server 8000
```

Then visit: http://localhost:8000

## 🧪 Test It! (2 minutes)

### Test Case 1: Low Risk (Should APPROVE)

Fill in the form:

- Applicant Income: **8000**
- Co-applicant Income: **2000**
- Loan Amount: **150**
- Loan Term: **360 months**
- Credit History: **Good (1)**
- Property Area: **Urban**
- Self Employed: **No**
- Dependents: **1**

Click "🔍 Assess Risk"

**Expected Result:** ✅ APPROVED with LOW risk

### Test Case 2: High Risk (Should REJECT)

Fill in the form:

- Applicant Income: **3000**
- Co-applicant Income: **0**
- Loan Amount: **250**
- Loan Term: **360 months**
- Credit History: **None/Bad (0)**
- Property Area: **Rural**
- Self Employed: **Yes**
- Dependents: **3+**

Click "🔍 Assess Risk"

**Expected Result:** ❌ REJECTED with HIGH risk

## 🎉 You're Done!

Your production-grade loan risk assessment system is now running!

## 📊 What You Can Do Now

1. **Test different scenarios** - Try various combinations
2. **View statistics** - Check the dashboard at the bottom
3. **Review decisions** - All decisions are logged in `backend/logs/audit.db`
4. **Customize rules** - Edit `backend/risk_rules.py`
5. **Adjust thresholds** - Modify risk scoring in the rules engine

## 🔧 Quick Commands

```bash
# Test the API directly
curl http://localhost:5000/health

# Run automated tests
python test_system.py

# View audit database
sqlite3 backend/logs/audit.db "SELECT * FROM audit_log LIMIT 5"
```

## 🐛 Troubleshooting

### Backend won't start?

```bash
# Reinstall dependencies
pip install --upgrade flask flask-cors pandas numpy scikit-learn joblib
```

### Model not found?

```bash
# Retrain the model
cd notebooks
python train_model.py
cd ..
```

### Frontend can't connect?

- Make sure backend is running on port 5000
- Check browser console (F12) for errors
- Verify `http://localhost:5000/health` returns OK

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [API endpoints](README.md#-api-endpoints)
- Learn about [customization options](README.md#-customization-guide)
- Understand the [risk engine](README.md#-understanding-the-risk-engine)

## 💡 Pro Tips

1. **Keep the backend running** - Don't close the terminal
2. **Use the test script** - `python test_system.py` for quick testing
3. **Check the logs** - All decisions are audited in SQLite
4. **Experiment safely** - The system uses synthetic data for training

---

**Need help?** Check the main README.md or review the troubleshooting section.

**Ready to deploy?** See the deployment options in README.md.

🎯 **You now have a production-grade loan risk assessment system!**
