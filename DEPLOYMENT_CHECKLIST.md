# 🚀 Deployment Checklist - FinCrime Loan Risk System

## ✅ Pre-Deployment Verification

### 1. Local Testing Complete

- [ ] Backend starts without errors
- [ ] Frontend loads correctly
- [ ] All 3 test cases pass (low/medium/high risk)
- [ ] Statistics display correctly
- [ ] Audit database is created
- [ ] ML model files exist in `backend/models/`

### 2. Code Quality

- [ ] No syntax errors
- [ ] All imports working
- [ ] Error handling in place
- [ ] Logging configured
- [ ] Comments and documentation updated

### 3. Security Review

- [ ] Input validation enabled
- [ ] SQL injection prevention (parameterized queries)
- [ ] CORS configured appropriately
- [ ] No hardcoded secrets
- [ ] Error messages don't leak sensitive info

## 🔧 Configuration Changes for Production

### 1. Flask Configuration

**In `backend/app.py`, change:**

```python
# Development
app.run(debug=True, host='0.0.0.0', port=5000)

# Production
app.run(debug=False, host='0.0.0.0', port=5000)
```

### 2. CORS Configuration

**In `backend/app.py`, update:**

```python
# Development (allows all origins)
CORS(app)

# Production (restrict to your domain)
CORS(app, origins=['https://yourdomain.com'])
```

### 3. Database Configuration

**For production, consider:**

```python
# Development - SQLite
db_path = 'logs/audit.db'

# Production - PostgreSQL
# Update audit_logger.py to use PostgreSQL
# Install: pip install psycopg2-binary
```

### 4. Environment Variables

Create `.env` file:

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:5432/dbname
ALLOWED_ORIGINS=https://yourdomain.com
```

## 🐳 Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy application files
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/backend/logs /app/backend/models

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["python", "backend/app.py"]
```

### 2. Create docker-compose.yml

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./backend/logs:/app/backend/logs
      - ./backend/models:/app/backend/models
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

### 3. Build and Run

```bash
# Build image
docker build -t loan-risk-system .

# Run container
docker run -d -p 5000:5000 --name loan-risk loan-risk-system

# Or use docker-compose
docker-compose up -d
```

## ☁️ Cloud Platform Deployment

### Option 1: Heroku

```bash
# 1. Create Procfile
echo "web: python backend/app.py" > Procfile

# 2. Create runtime.txt
echo "python-3.9.18" > runtime.txt

# 3. Deploy
heroku create your-app-name
git push heroku main
```

### Option 2: AWS EC2

```bash
# 1. Launch EC2 instance (Ubuntu)
# 2. SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# 3. Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# 4. Clone repository
git clone your-repo-url
cd fincrime-loan-risk-system

# 5. Setup application
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Train model
cd notebooks && python train_model.py && cd ..

# 7. Configure Nginx (reverse proxy)
sudo nano /etc/nginx/sites-available/loan-risk

# 8. Start application with gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

### Option 3: Google Cloud Run

```bash
# 1. Build container
gcloud builds submit --tag gcr.io/PROJECT-ID/loan-risk

# 2. Deploy
gcloud run deploy loan-risk \
  --image gcr.io/PROJECT-ID/loan-risk \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🔒 Security Hardening

### 1. Add Authentication

```python
# Install Flask-Login
pip install flask-login

# Add to app.py
from flask_login import LoginManager, login_required

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/api/assess-loan', methods=['POST'])
@login_required
def assess_loan():
    # ... existing code
```

### 2. Add Rate Limiting

```python
# Install Flask-Limiter
pip install flask-limiter

# Add to app.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/assess-loan', methods=['POST'])
@limiter.limit("10 per minute")
def assess_loan():
    # ... existing code
```

### 3. Enable HTTPS

```bash
# Using Let's Encrypt with Nginx
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 4. Add Input Sanitization

```python
# Install bleach
pip install bleach

# Add to data_validator.py
import bleach

def sanitize_input(data):
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = bleach.clean(value)
    return data
```

## 📊 Monitoring Setup

### 1. Application Monitoring

```python
# Install Flask-Monitoring-Dashboard
pip install flask-monitoringdashboard

# Add to app.py
import flask_monitoringdashboard as dashboard
dashboard.bind(app)
```

### 2. Error Tracking

```python
# Install Sentry
pip install sentry-sdk[flask]

# Add to app.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()]
)
```

### 3. Logging Configuration

```python
# Add to app.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10240000,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

## 🗄️ Database Migration

### Upgrade to PostgreSQL

```python
# 1. Install psycopg2
pip install psycopg2-binary

# 2. Update audit_logger.py
import psycopg2
from psycopg2.extras import RealDictCursor

class AuditLogger:
    def __init__(self, db_url):
        self.db_url = db_url
        self._initialize_database()

    def _get_connection(self):
        return psycopg2.connect(self.db_url)

    # Update all methods to use PostgreSQL
```

## 🧪 Production Testing

### 1. Load Testing

```bash
# Install Apache Bench
sudo apt install apache2-utils

# Test endpoint
ab -n 1000 -c 10 -p test_data.json -T application/json \
   http://your-domain.com/api/assess-loan
```

### 2. Security Scanning

```bash
# Install OWASP ZAP
# Run security scan
zap-cli quick-scan http://your-domain.com
```

### 3. Performance Monitoring

```bash
# Install New Relic or DataDog
pip install newrelic

# Configure in app.py
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')
```

## 📋 Post-Deployment Checklist

### Immediate (Day 1)

- [ ] Application is accessible
- [ ] Health check endpoint responds
- [ ] Test all 3 scenarios work
- [ ] Statistics are updating
- [ ] Audit logs are being created
- [ ] SSL certificate is valid
- [ ] Monitoring is active

### Short-term (Week 1)

- [ ] Review error logs daily
- [ ] Monitor response times
- [ ] Check database growth
- [ ] Verify backup system
- [ ] Test disaster recovery
- [ ] Review security logs

### Long-term (Month 1)

- [ ] Analyze usage patterns
- [ ] Optimize slow queries
- [ ] Review and update rules
- [ ] Retrain ML model if needed
- [ ] Update documentation
- [ ] Plan scaling strategy

## 🔄 Maintenance Schedule

### Daily

- Check error logs
- Monitor response times
- Verify backups

### Weekly

- Review audit statistics
- Check disk space
- Update dependencies (if needed)

### Monthly

- Analyze model performance
- Review and update rules
- Security audit
- Performance optimization

### Quarterly

- Retrain ML model
- Major version updates
- Disaster recovery test
- Compliance review

## 📞 Support & Rollback

### Rollback Plan

```bash
# 1. Keep previous version tagged
git tag -a v1.0 -m "Production release"

# 2. If issues occur, rollback
git checkout v1.0
docker build -t loan-risk-system:v1.0 .
docker run -d -p 5000:5000 loan-risk-system:v1.0
```

### Emergency Contacts

- **Technical Lead**: [Contact info]
- **DevOps**: [Contact info]
- **Security Team**: [Contact info]

## 🎯 Success Criteria

### Performance

- [ ] Response time < 200ms (95th percentile)
- [ ] Uptime > 99.9%
- [ ] Error rate < 0.1%

### Business

- [ ] Automated decision rate > 70%
- [ ] Manual review rate < 30%
- [ ] Zero data loss
- [ ] 100% audit coverage

### Security

- [ ] No security vulnerabilities
- [ ] All data encrypted
- [ ] Access logs maintained
- [ ] Compliance requirements met

---

## 🚀 Ready to Deploy?

Once all items are checked:

1. **Tag the release**: `git tag -a v1.0 -m "Production release"`
2. **Deploy to staging first**: Test thoroughly
3. **Deploy to production**: Use blue-green deployment
4. **Monitor closely**: Watch for 24 hours
5. **Celebrate**: You've deployed a production system! 🎉

---

**Remember**: Always test in staging before production!

**Pro Tip**: Keep this checklist updated as your system evolves.
