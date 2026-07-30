# TaskFlow - Quick Start Guide

## 🚀 Quick Setup (Windows)

```batch
# 1. Double-click setup.bat
setup.bat

# 2. Create database (open MySQL)
mysql -u root -p < database.sql

# 3. Update .env file with MySQL credentials

# 4. Run application
python app.py
```

## 🚀 Quick Setup (Linux/macOS)

```bash
# 1. Make setup script executable
chmod +x setup.sh

# 2. Run setup script
./setup.sh

# 3. Create database
mysql -u root -p < database.sql

# 4. Update .env file with MySQL credentials

# 5. Run application
python app.py
```

## 📋 Manual Setup Steps

### Step 1: Create Virtual Environment
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/macOS)
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup Database
```bash
# Login to MySQL
mysql -u root -p

# Inside MySQL
CREATE DATABASE taskflow_db;
USE taskflow_db;
source database.sql;
exit;
```

### Step 4: Configure Environment
```
Edit .env file:
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/taskflow_db
```

### Step 5: Run Application
```bash
python app.py
```

Access at: http://localhost:5000

## 🔐 Default Login Credentials

| User | Username | Password | Role |
|------|----------|----------|------|
| Admin | admin | password123 | admin |
| Manager | manager | password123 | manager |
| User | user1 | password123 | user |

## 📝 Common Commands

### Create New User
```bash
python
>>> from app import db
>>> from app.models import User
>>> user = User(username='newuser', email='newuser@example.com', role='user')
>>> user.set_password('password123')
>>> db.session.add(user)
>>> db.session.commit()
```

### Reset Database
```bash
python
>>> from app import db
>>> db.drop_all()
>>> db.create_all()
```

### View Database URL
Update config.py to check:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/taskflow_db'
```

## 🔧 Troubleshooting

### Python Not Found
- Install Python 3.8+ from https://www.python.org/
- Add Python to PATH
- Restart terminal/command prompt

### MySQL Connection Error
- Verify MySQL is running
- Check username and password
- Ensure database exists: `SHOW DATABASES;`
- Update DATABASE_URL in .env

### Port 5000 Already in Use
- Change port in app.py
- Or find and kill process on port 5000

### Module Not Found
- Activate virtual environment
- Run `pip install -r requirements.txt`
- Check `pip list` for all packages

### Database Tables Not Created
- Run database.sql manually
- Or delete database and run setup again
- Check SQLAlchemy configuration

## 📚 Project Structure Quick Reference

```
TaskFlow/
├── app/                  # Flask application
│   ├── __init__.py      # App factory
│   ├── models.py        # Database models
│   ├── routes.py        # Route handlers
│   ├── templates/       # HTML templates
│   └── static/          # CSS, JS, uploads
├── config.py            # Configuration
├── app.py               # Entry point
├── requirements.txt     # Dependencies
├── database.sql         # Database setup
└── README.md            # Full documentation
```

## 🌐 Key URLs

| Page | URL | Access |
|------|-----|--------|
| Home | http://localhost:5000/ | All |
| Login | http://localhost:5000/auth/login | Anonymous |
| Register | http://localhost:5000/auth/register | Anonymous |
| Dashboard | http://localhost:5000/dashboard | Logged In |
| Projects | http://localhost:5000/projects/ | Logged In |
| Tasks | http://localhost:5000/tasks/ | Logged In |
| Reports | http://localhost:5000/reports/ | Logged In |
| Profile | http://localhost:5000/profile | Logged In |

## 💾 Backup & Restore

### Backup Database
```bash
mysqldump -u root -p taskflow_db > backup.sql
```

### Restore Database
```bash
mysql -u root -p taskflow_db < backup.sql
```

## 🚀 Deployment Checklist

- [ ] Change SECRET_KEY in config.py
- [ ] Set FLASK_ENV=production
- [ ] Use strong database password
- [ ] Enable HTTPS
- [ ] Configure server (Gunicorn/Nginx)
- [ ] Setup email notifications
- [ ] Configure logging
- [ ] Setup database backups
- [ ] Security audit

## 📞 Quick Help

### Check Python Version
```bash
python --version
```

### Check Installed Packages
```bash
pip list
```

### Upgrade pip
```bash
python -m pip install --upgrade pip
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Run with Logging
```bash
FLASK_ENV=development FLASK_DEBUG=1 python app.py
```

## 🐛 Debug Mode

Enable detailed error messages:

In app.py:
```python
app.run(debug=True)
```

Or set environment variable:
```bash
export FLASK_DEBUG=1
python app.py
```

## 📊 Database Backup Schedule

Recommended backup schedule:
- Daily incremental backups
- Weekly full backups
- Monthly archive backups
- Test restore monthly

## 🔒 Security Tips

1. Change default passwords immediately
2. Use strong database passwords
3. Regular security updates
4. Enable HTTPS in production
5. Validate user inputs
6. Regular backups
7. Monitor access logs
8. Update dependencies regularly

---

For detailed documentation, see README.md

Last Updated: 2024
