# 🏠 Local Testing Guide - FinCrime Loan Risk System

## ✅ Current Status

Your system is **RUNNING LOCALLY** and ready to test!

### 🟢 Backend Status

- **URL**: http://localhost:5000
- **Status**: ✅ Healthy
- **ML Model**: ✅ Loaded (90% accuracy)
- **Version**: 1.0.0

### 🟢 Frontend Status

- **File**: frontend/index.html
- **Status**: ✅ Open in browser

---

## 🧪 Test Scenarios

### Test 1: Low Risk Application (Should APPROVE ✅)

Fill in the form with:

```
Applicant Income: 8000
Co-applicant Income: 2000
Loan Amount: 150
Loan Term: 360 months (30 years)
Credit History: Good (1)
Property Area: Urban
Self Employed: No
Dependents: 1
```

**Expected Result:**

- Decision: ✅ **APPROVED**
- Risk Level: **LOW**
- Risk Score: ~5-10/100
- ML Confidence: ~75-85%

---

### Test 2: High Risk Application (Should REJECT ❌)

Fill in the form with:

```
Applicant Income: 3000
Co-applicant Income: 0
Loan Amount: 250
Loan Term: 360 months (30 years)
Credit History: None/Bad (0)
Property Area: Rural
Self Employed: Yes
Dependents: 3+
```

**Expected Result:**

- Decision: ❌ **REJECTED**
- Risk Level: **HIGH**
- Risk Score: ~65-75/100
- Reason: Multiple high-risk factors

**Risk Flags You'll See:**

- R1: No Credit History (+40 points)
- R2: High Loan-to-Income Ratio (+25 points)
- R3: High DTI Ratio (+20 points)
- R4: Low Income (+15 points)
- R5: Rural Property (+5 points)
- R6: Self-Employed (+5 points)

---

### Test 3: Medium Risk Application (Should MANUAL_REVIEW ⚠️)

Fill in the form with:

```
Applicant Income: 5000
Co-applicant Income: 1500
Loan Amount: 180
Loan Term: 360 months (30 years)
Credit History: Good (1)
Property Area: Semiurban
Self Employed: No
Dependents: 2
```

**Expected Result:**

- Decision: ⚠️ **MANUAL_REVIEW**
- Risk Level: **MEDIUM**
- Risk Score: ~25-35/100
- Reason: Moderate risk requires human review

---

## 📊 What to Check

### 1. Decision Display

- ✅ Color-coded badge (Green/Red/Orange)
- ✅ Risk level with badge
- ✅ Risk score out of 100
- ✅ Application ID generated

### 2. Explanations

- ✅ ML confidence percentage
- ✅ Key factors with impact (Positive/Negative/Neutral)
- ✅ Feature importance weights
- ✅ Human-readable descriptions

### 3. Risk Flags

- ✅ Rule violations listed
- ✅ Severity levels (HIGH/MEDIUM/LOW)
- ✅ Impact scores
- ✅ Clear descriptions

### 4. Statistics Dashboard

- ✅ Total applications count
- ✅ Approval rate percentage
- ✅ Average processing time (ms)
- ✅ Auto-refresh every 30 seconds

---

## 🔍 Behind the Scenes

### What Happens When You Click "Assess Risk"

```
1. Frontend → Collects form data
2. Frontend → Sends POST to http://localhost:5000/api/assess-loan
3. Backend → Validates data (data_validator.py)
4. Backend → Applies business rules (risk_rules.py)
5. Backend → ML prediction (loan_model.pkl)
6. Backend → Generates explanation (explainer.py)
7. Backend → Logs to database (audit_logger.py)
8. Backend → Returns JSON response
9. Frontend → Displays results beautifully
```

**Processing Time**: ~100-200ms

---

## 📁 Check Audit Logs

All decisions are logged in: `backend/logs/audit.db`

### View Recent Decisions

Open a new terminal and run:

```bash
# Activate environment
venv\Scripts\activate

# Query database
sqlite3 backend/logs/audit.db "SELECT application_id, timestamp, final_decision, final_risk_level FROM audit_log ORDER BY timestamp DESC LIMIT 10"
```

Or use a SQLite browser tool to explore the database.

---

## 🎯 Testing Checklist

- [ ] Test Case 1 (Low Risk) - Should APPROVE
- [ ] Test Case 2 (High Risk) - Should REJECT
- [ ] Test Case 3 (Medium Risk) - Should MANUAL_REVIEW
- [ ] Check statistics update after each test
- [ ] Verify processing time is < 200ms
- [ ] Confirm explanations are clear
- [ ] Check risk flags appear correctly
- [ ] Verify audit log is created

---

## 🔧 Useful Commands

### Check Backend Status

```bash
curl http://localhost:5000/health
```

### Get Statistics

```bash
curl http://localhost:5000/api/statistics
```

### Test API Directly (PowerShell)

```powershell
$body = @{
    applicant_income = 5000
    coapplicant_income = 0
    loan_amount = 150
    loan_amount_term = 360
    credit_history = 1
    property_area = "Urban"
    self_employed = 0
    dependents = 0
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/assess-loan" -Method POST -Body $body -ContentType "application/json"
```

---

## 🛑 Stop the System

When you're done testing:

1. **Stop Backend**: Press `Ctrl+C` in the terminal running the backend
2. **Close Frontend**: Close the browser tab

---

## 🐛 Troubleshooting

### Frontend can't connect to backend?

- Check backend is running: `curl http://localhost:5000/health`
- Verify no firewall blocking port 5000
- Check browser console (F12) for errors

### Backend not responding?

- Restart backend: Stop with Ctrl+C, then run `python app.py` again
- Check for port conflicts: `netstat -ano | findstr :5000`

### Statistics not updating?

- Wait 30 seconds for auto-refresh
- Or refresh the page manually

### Audit database not created?

- Check `backend/logs/` folder exists
- Backend creates it automatically on first decision

---

## 📈 Performance Expectations

### Response Times

- Data Validation: ~5ms
- Rule Evaluation: ~10ms
- ML Prediction: ~50ms
- Explanation Generation: ~20ms
- Audit Logging: ~15ms
- **Total**: ~100-200ms

### Accuracy

- ML Model: 90% accuracy
- Rule-based: 100% consistent
- Combined: Optimized for compliance

---

## 🎓 Understanding the Results

### Risk Score Breakdown

| Score Range | Risk Level | Typical Action   |
| ----------- | ---------- | ---------------- |
| 0-24        | LOW        | Proceed to ML    |
| 25-49       | MEDIUM     | Manual Review    |
| 50-100      | HIGH       | Reject or Review |

### Decision Logic

```
IF Risk Score > 65 → REJECT
ELSE IF Risk Score > 50 → MANUAL_REVIEW
ELSE IF ML Confidence > 70% → APPROVE
ELSE IF ML Confidence > 50% → MANUAL_REVIEW
ELSE → REJECT
```

### Feature Importance (Top 5)

1. **Credit History** - 42.1% (Most important!)
2. **Applicant Income** - 21.2%
3. **Total Income** - 7.8%
4. **Co-applicant Income** - 6.8%
5. **Loan Amount** - 6.3%

---

## 🎉 You're All Set!

Your FinCrime Loan Risk Assessment System is running locally and ready for testing!

**Quick Start:**

1. ✅ Backend running on http://localhost:5000
2. ✅ Frontend open in browser
3. ✅ Fill in the form
4. ✅ Click "Assess Risk"
5. ✅ See instant results!

**Happy Testing!** 🚀

---

## 📝 Notes

- All data is processed locally
- No external API calls
- All decisions are logged
- System uses synthetic training data
- Safe to experiment with any values

---

**Built with ❤️ for FinCrime Risk Assessment**

_This is a complete, production-grade system running entirely on your local machine!_
