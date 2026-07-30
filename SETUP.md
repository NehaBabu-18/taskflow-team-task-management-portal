# TaskFlow - Complete Setup Instructions

## ✅ Pre-Installation Checklist

- [ ] Python 3.8+ installed
- [ ] MySQL Server 5.7+ installed
- [ ] Git (optional)
- [ ] Administrative access to install software

## 🔧 Installation Steps

### Option 1: Automated Setup (Recommended)

#### Windows Users
```batch
1. Navigate to TaskFlow folder
2. Right-click setup.bat
3. Select "Run as administrator"
4. Follow the on-screen instructions
```

#### Linux/macOS Users
```bash
1. Navigate to TaskFlow folder
2. chmod +x setup.sh
3. ./setup.sh
4. Follow the on-screen instructions
```

### Option 2: Manual Setup

#### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Output should show:
```
Successfully installed Flask, SQLAlchemy, PyMySQL, etc.
```

#### Step 3: Create Database

**A. Using Command Line:**
```bash
mysql -u root -p

# Inside MySQL:
CREATE DATABASE taskflow_db;
USE taskflow_db;
SOURCE database.sql;
EXIT;
```

**B. Using MySQL Workbench:**
1. Open MySQL Workbench
2. Create new connection
3. Go to Administration → Data Import/Restore
4. Select "Import from Self-Contained File"
5. Choose database.sql
6. Click Start Import

**C. Using phpMyAdmin:**
1. Open phpMyAdmin
2. Click Databases
3. Create "taskflow_db"
4. Select database
5. Go to Import tab
6. Select database.sql
7. Click Go

#### Step 4: Configure Database Connection

Edit .env file:
```
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:your_password@localhost:3306/taskflow_db'
```

Or edit config.py:
```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:your_password@localhost:3306/taskflow_db'
```

#### Step 5: Verify Installation

```bash
# Check Flask installation
python -c "import flask; print(flask.__version__)"

# Check SQLAlchemy
python -c "import sqlalchemy; print(sqlalchemy.__version__)"

# Check PyMySQL
python -c "import pymysql; print(pymysql.__version__)"
```

## ▶️ Running the Application

### Start the Server
```bash
# Make sure virtual environment is activated
python app.py
```

### Expected Output
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with reloader
 * Debugger is active!
 * Debugger PIN: 000-000-000
```

### Access the Application
1. Open web browser
2. Navigate to: **http://localhost:5000**
3. You should see the login page

## 🔐 Test Login

### First Login
```
URL: http://localhost:5000/auth/login
Username: admin
Password: password123
```

After login, you should see the Dashboard.

## 📝 Creating Additional Users

### Via Web Interface
1. Click "Register" on login page
2. Enter username, email, and password
3. Confirm password
4. Click "Create Account"
5. Login with new account

### Via Python Shell
```bash
python
```

Then in Python:
```python
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    user = User(username='newuser', email='newuser@example.com', role='user')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    print("User created successfully!")
```

## 🏗️ Project Setup Guide

### Creating Your First Project

1. **Login** with admin account
2. **Go to Projects** page from navigation
3. **Click "New Project"** button
4. **Fill in details:**
   - Project Name: "Website Redesign"
   - Description: "Complete redesign of company website"
   - Start Date: 2024-01-15
   - End Date: 2024-06-30
5. **Click "Create Project"**

You should now see your project in the list.

### Creating Tasks

1. **Click on your project** in the projects list
2. **Click "Add Task"** button
3. **Fill in task details:**
   - Task Name: "Design Homepage"
   - Description: "Create mockups and prototypes"
   - Priority: "High"
   - Status: "In Progress"
   - Due Date: 2024-02-15
   - Project: "Website Redesign"
4. **Click "Create Task"**

### Assigning Tasks

1. **Go to Tasks** page
2. **Click on a task** to view details
3. **In Assignments section, click "Assign User"**
4. **Select a user** from dropdown
5. **Click "Assign"**

The user will now see this task in their dashboard.

## 📊 Generating Reports

1. **Click "Reports"** in navigation
2. View:
   - Total tasks and completion rate
   - Task status distribution
   - Priority statistics
   - Project-wise breakdown
3. **Click "Print"** to generate PDF report

## 🐛 Troubleshooting

### Issue: "Connection refused" MySQL Error

**Solution:**
```bash
# Windows - Start MySQL
net start MySQL57

# Linux/macOS - Start MySQL
sudo service mysql start

# Or check if MySQL is running
mysql -u root -p -e "SELECT 1;"
```

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
# Reactivate virtual environment
# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"

**Solution - Windows:**
```bash
# Find process using port 5000
netstat -ano | findstr ":5000"

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F

# Or use different port in app.py:
app.run(port=5001)
```

**Solution - Linux/macOS:**
```bash
# Find process
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
app.run(port=5001)
```

### Issue: Database Password Issues

**Solution:**
```bash
# Reset MySQL root password (if forgotten)
mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'newpassword';"

# Update .env file with new password
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:newpassword@localhost:3306/taskflow_db'
```

### Issue: 404 Page Not Found

**Solution:**
1. Check URL is correct
2. Ensure virtual environment is activated
3. Restart Flask application
4. Clear browser cache (Ctrl+F5 / Cmd+Shift+R)

## 🔄 Common Operations

### Reset Database
```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.drop_all()
...     db.create_all()
...     print("Database reset complete")
```

### Backup Database
```bash
mysqldump -u root -p taskflow_db > taskflow_backup.sql
```

### Restore Database
```bash
mysql -u root -p taskflow_db < taskflow_backup.sql
```

### Update User Password
```bash
python
>>> from app import create_app, db
>>> from app.models import User
>>> app = create_app()
>>> with app.app_context():
...     user = User.query.filter_by(username='admin').first()
...     user.set_password('newpassword123')
...     db.session.commit()
...     print("Password updated!")
```

## 🚀 Production Deployment

### Before Deployment

1. **Security**
   ```python
   # config.py
   SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secure-random-key'
   FLASK_ENV = 'production'
   DEBUG = False
   ```

2. **Database**
   ```
   Use strong password
   Remote backup servers
   Regular maintenance
   ```

3. **Server**
   - Use Gunicorn or uWSGI
   - Setup Nginx reverse proxy
   - Enable HTTPS/SSL
   - Configure firewall

### Deploy with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Deploy with PythonAnywhere

1. Upload files to PythonAnywhere
2. Setup virtual environment
3. Configure MySQL database
4. Setup web app configuration
5. Add start/end times for auto-reload

## 📞 Support Resources

### Online Documentation
- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Bootstrap: https://getbootstrap.com/
- MySQL: https://dev.mysql.com/doc/

### Getting Help
1. Check README.md for detailed docs
2. Review QUICKSTART.md for quick reference
3. Check console error messages
4. Search internet for specific error
5. Review Flask debug toolbar

## ✨ Next Steps

1. ✅ Setup complete!
2. Create projects and tasks
3. Assign tasks to team members
4. Track progress with reports
5. Customize for your needs
6. Deploy to production

## 📋 Quick Checklist

- [ ] Python installed
- [ ] MySQL running
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database created
- [ ] Configuration updated
- [ ] Application started
- [ ] Login successful
- [ ] Created first project
- [ ] Created first task
- [ ] Assigned task to user

---

## 🎉 Congratulations!

Your TaskFlow system is now ready to use. 

**Start managing tasks like a pro!**

For more information, see README.md

Last Updated: 2024
Version: 1.0.0
