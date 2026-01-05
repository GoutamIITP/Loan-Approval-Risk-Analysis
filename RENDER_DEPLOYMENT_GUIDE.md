# 🚀 Render Deployment Guide - FinCrime Loan Risk System

## ⚡ Quick Configuration for Render

Based on your Render deployment screen, here are the **exact settings** to use:

---

## 📋 Render Configuration Settings

### **Basic Settings**

| Field              | Value                                         |
| ------------------ | --------------------------------------------- |
| **Name**           | `fincrime-loan-risk-system`                   |
| **Language**       | `Python 3`                                    |
| **Branch**         | `main`                                        |
| **Region**         | `Oregon (US West)` (or your preferred region) |
| **Root Directory** | _(leave empty)_                               |

### **Build & Start Commands**

| Field             | Command                                                                    |
| ----------------- | -------------------------------------------------------------------------- |
| **Build Command** | `pip install -r requirements.txt && cd notebooks && python train_model.py` |
| **Start Command** | `cd backend && python app.py`                                              |

### **Instance Type**

For testing: **Free** ($0/month)
For production: **Starter** ($7/month) or higher

---

## 🔧 Environment Variables

Click **"Add Environment Variable"** and add these:

| Key              | Value        |
| ---------------- | ------------ |
| `PYTHON_VERSION` | `3.9.18`     |
| `FLASK_ENV`      | `production` |
| `PORT`           | `5000`       |

---

## 📁 Files Already Created for Deployment

I've created these files for you:

✅ **`render.yaml`** - Render configuration
✅ **`runtime.txt`** - Python version specification  
✅ **`Procfile`** - Process file for deployment
✅ **Updated `backend/app.py`** - Now works with Render's PORT
✅ **Updated `frontend/index.html`** - Auto-detects local vs deployed

---

## 🎯 Step-by-Step Deployment

### Step 1: Configure Render Settings

Use the exact settings from the table above:

```
Build Command: pip install -r requirements.txt && cd notebooks && python train_model.py
Start Command: cd backend && python app.py
```

### Step 2: Add Environment Variables

Add these 3 environment variables:

- `PYTHON_VERSION` = `3.9.18`
- `FLASK_ENV` = `production`
- `PORT` = `5000`

### Step 3: Deploy

Click **"Deploy web service"**

### Step 4: Wait for Build

The build process will:

1. ✅ Install Python dependencies
2. ✅ Train the ML model
3. ✅ Start the Flask server
4. ✅ Make your app live!

---

## 📊 What Happens During Build

```
[1/4] Installing dependencies...
      → pip install -r requirements.txt

[2/4] Training ML model...
      → cd notebooks && python train_model.py
      → Creates backend/models/*.pkl files

[3/4] Starting Flask server...
      → cd backend && python app.py
      → Server starts on Render's assigned port

[4/4] App is live!
      → Your app is accessible at your Render URL
```

---

## 🌐 Accessing Your Deployed App

After deployment, Render will give you a URL like:

```
https://fincrime-loan-risk-system.onrender.com
```

### Frontend Access

**Option 1: Serve Frontend from Flask (Recommended)**

I'll create a route to serve the frontend:

```python
# Add to backend/app.py
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)
```

**Option 2: Separate Frontend Deployment**

Deploy frontend separately as a static site on:

- Netlify
- Vercel
- GitHub Pages

---

## 🔧 Updated Code for Deployment

### **backend/app.py** (Already Updated)

```python
# Now uses environment PORT variable
port = int(os.environ.get('PORT', 5000))
debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
app.run(debug=debug_mode, host='0.0.0.0', port=port)
```

### **frontend/index.html** (Already Updated)

```javascript
// Auto-detects local vs deployed
const API_BASE_URL =
  window.location.hostname === "localhost"
    ? "http://localhost:5000/api"
    : "/api";
```

---

## 🐛 Troubleshooting

### Build Fails

**Common Issues:**

1. **Dependencies not installing**

   ```
   Solution: Check requirements.txt is in root directory
   ```

2. **Model training fails**

   ```
   Solution: Ensure notebooks/train_model.py exists
   Build Command: pip install -r requirements.txt && cd notebooks && python train_model.py
   ```

3. **Python version issues**
   ```
   Solution: Add PYTHON_VERSION=3.9.18 environment variable
   ```

### App Starts But Doesn't Work

**Check:**

1. **Port configuration**

   ```
   Environment Variable: PORT=5000
   Start Command: cd backend && python app.py
   ```

2. **CORS issues**

   ```
   Solution: Flask-CORS is already configured in app.py
   ```

3. **Frontend can't reach backend**
   ```
   Solution: Frontend auto-detects deployment (already fixed)
   ```

### Free Tier Limitations

**Render Free Tier:**

- ✅ Spins down after 15 minutes of inactivity
- ✅ Cold start takes 30-60 seconds
- ✅ 512MB RAM, 0.1 CPU
- ❌ No persistent storage
- ❌ No custom domains

**For Production:** Use Starter ($7/month) or higher

---

## 📈 Monitoring Your Deployment

### Render Dashboard

Monitor:

- ✅ Build logs
- ✅ Runtime logs
- ✅ Metrics (CPU, memory)
- ✅ Deploy history

### Health Check

Your app includes a health endpoint:

```
GET https://your-app.onrender.com/health
```

Response:

```json
{
  "status": "healthy",
  "ml_available": true,
  "timestamp": "2026-01-05T10:30:00.000Z",
  "version": "1.0.0"
}
```

---

## 🔄 Updates and Redeployment

### Automatic Deployment

Render automatically redeploys when you:

- Push to the `main` branch
- Make changes to your GitHub repository

### Manual Deployment

From Render dashboard:

- Click **"Manual Deploy"**
- Select **"Deploy latest commit"**

---

## 💰 Cost Optimization

### Free Tier (Good for Demo)

```
Cost: $0/month
RAM: 512MB
CPU: 0.1
Limitations: Spins down, cold starts
```

### Starter Tier (Recommended)

```
Cost: $7/month
RAM: 512MB
CPU: 0.5
Benefits: Always on, faster, SSH access
```

---

## 🎯 Production Checklist

Before going live:

- [ ] Use Starter tier or higher
- [ ] Set up custom domain
- [ ] Configure environment variables
- [ ] Set up monitoring/alerts
- [ ] Test all functionality
- [ ] Set up backup strategy
- [ ] Configure logging

---

## 📚 Additional Resources

- **Render Docs**: https://render.com/docs
- **Python on Render**: https://render.com/docs/deploy-flask
- **Environment Variables**: https://render.com/docs/environment-variables

---

## 🎉 Success Indicators

Your deployment is successful when:

✅ **Build completes** without errors
✅ **Health endpoint** returns 200 OK
✅ **Frontend loads** at your Render URL
✅ **API calls work** (test loan assessment)
✅ **ML model** makes predictions
✅ **Audit logging** works

---

## 🔗 Example URLs

After deployment:

```
Main App:     https://your-app.onrender.com
Health Check: https://your-app.onrender.com/health
API:          https://your-app.onrender.com/api/assess-loan
Statistics:   https://your-app.onrender.com/api/statistics
```

---

## 📝 Quick Reference

**Build Command:**

```bash
pip install -r requirements.txt && cd notebooks && python train_model.py
```

**Start Command:**

```bash
cd backend && python app.py
```

**Environment Variables:**

```
PYTHON_VERSION=3.9.18
FLASK_ENV=production
PORT=5000
```

---

**Ready to deploy? Use the settings above and click "Deploy web service"!** 🚀

Your FinCrime Loan Risk Assessment System will be live on the internet in minutes! 🌐

---

**Built with ❤️ for FinCrime Risk Assessment**

_From local development to global deployment!_
