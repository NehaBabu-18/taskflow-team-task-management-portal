# TaskFlow - Team Task Management Portal

A comprehensive web-based task management system built with Flask, MySQL, Bootstrap, and SQLAlchemy. TaskFlow enables teams to efficiently manage projects, assign tasks, and track progress in real-time.

## Features

### 🎯 Core Functionality
- **User Authentication**: Secure login/registration with password hashing
- **Dashboard**: Real-time overview of projects, tasks, and statistics
- **Project Management**: Create, read, update, and delete projects
- **Task Management**: Complete CRUD operations for tasks with priorities and statuses
- **Task Assignment**: Assign tasks to team members with tracking
- **Reports**: Comprehensive analytics and project statistics
- **Role-Based Access**: Admin, Manager, and User roles with different permissions

### 🎨 User Interface
- Responsive Bootstrap 5 design
- Modern gradient UI with smooth animations
- Mobile-friendly interface
- Interactive charts and progress bars
- Real-time status updates

### 📊 Key Modules
1. **Authentication Module**
   - User registration and login
   - Password hashing and security
   - Session management
   - Role-based authentication

2. **Dashboard Module**
   - Statistics overview
   - Task and project summaries
   - Quick access to recent items

3. **Project Module**
   - Create and manage projects
   - Project descriptions and timelines
   - Project-wise statistics
   - Task organization by project

4. **Task Module**
   - Task creation with priority levels (Low, Medium, High, Urgent)
   - Task status tracking (Pending, In Progress, Completed)
   - Task filtering and search
   - Deadline management

5. **Assignment Module**
   - Assign multiple users to tasks
   - Track assignment dates
   - Remove assignments

6. **Reports Module**
   - Priority distribution charts
   - Status overview analytics
   - Project-wise statistics
   - Completion rate tracking

## Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database operations
- **Flask-SQLAlchemy**: Flask integration for SQLAlchemy
- **PyMySQL**: MySQL database driver
- **Werkzeug**: Password hashing and utilities

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **HTML5**: Markup language
- **CSS3**: Custom styling with gradients and animations
- **JavaScript**: Interactive features and AJAX calls
- **Font Awesome**: Icon library

### Database
- **MySQL**: Relational database management system
- **InnoDB**: Storage engine with ACID compliance

### Development
- **Python 3.8+**: Programming language
- **Virtual Environment**: Dependency isolation

## Project Structure

```
TaskFlow/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── models.py            # Database models (User, Project, Task, Assignment)
│   ├── routes.py            # Application routes and blueprints
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── projects.html
│   │   ├── project_form.html
│   │   ├── project_detail.html
│   │   ├── tasks.html
│   │   ├── task_form.html
│   │   ├── task_detail.html
│   │   ├── reports.html
│   │   ├── profile.html
│   │   ├── 404.html
│   │   └── 500.html
│   └── static/
│       ├── css/
│       │   └── style.css     # Custom CSS styling
│       └── js/
│           └── main.js       # JavaScript functionality
├── app.py                   # Application entry point
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── database.sql             # Database initialization script
├── .env                     # Environment variables
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

### Step 1: Clone/Download the Project

Navigate to the TaskFlow directory and setup the environment.

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup MySQL Database

```bash
# Login to MySQL
mysql -u root -p

# Run the database script
source database.sql

# Or manually create database and tables
CREATE DATABASE taskflow_db;
USE taskflow_db;
-- Then import database.sql
```

Alternatively, use a GUI tool like MySQL Workbench or phpMyAdmin.

### Step 5: Configure Environment

Edit the `.env` file and update database credentials:

```
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/taskflow_db
```

Update `config.py` if needed:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/taskflow_db'
```

### Step 6: Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

### Admin Account
- **Username**: admin
- **Password**: password123

### Manager Account
- **Username**: manager  
- **Password**: password123

### User Account
- **Username**: user1
- **Password**: password123

> **Note**: These are sample accounts for testing. Change passwords in production!

### Creating Users

1. Go to `http://localhost:5000/auth/register`
2. Fill in username, email, and password
3. Submit the registration form
4. Login with your credentials

### Creating Projects

1. Click "Projects" in the navigation
2. Click "New Project" button
3. Fill in project details:
   - Project Name (required)
   - Description
   - Start Date
   - End Date
4. Click "Create Project"

### Creating Tasks

1. Click "Tasks" in the navigation
2. Click "New Task" button
3. Fill in task details:
   - Task Name (required)
   - Project (required)
   - Description
   - Priority (Low, Medium, High, Urgent)
   - Status (Pending, In Progress, Completed)
   - Due Date
4. Click "Create Task"

### Assigning Tasks

1. Go to task details by clicking "View"
2. Click "Assign User" button in Assignments section
3. Select user from dropdown
4. Click "Assign"
5. To remove assignment, click "Remove" next to user

### Viewing Reports

1. Click "Reports" in the navigation
2. Admin can see:
   - Overall system statistics
   - Priority distribution
   - Project-wise statistics
   - Status overview
3. Users can see their own statistics and project information

### Managing Status

Update task status from:
- Task detail page: Use status dropdown
- Task list: Click view and update status
- Status updates automatically reflect in reports

## Database Schema

### Users Table
- `id`: Primary key (INT)
- `username`: Unique username (VARCHAR 80)
- `email`: Unique email address (VARCHAR 120)
- `password_hash`: Hashed password (VARCHAR 255)
- `role`: User role - admin/manager/user (VARCHAR 20)
- `is_active`: Account active status (BOOLEAN)
- `created_at`: Account creation timestamp
- `last_login`: Last login timestamp

### Projects Table
- `id`: Primary key (INT)
- `project_name`: Project name (VARCHAR 150)
- `description`: Project description (LONGTEXT)
- `start_date`: Project start date (TIMESTAMP)
- `end_date`: Project end date (TIMESTAMP)
- `status`: Active/Inactive status (VARCHAR 20)
- `creator_id`: Foreign key to users (INT)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Tasks Table
- `id`: Primary key (INT)
- `task_name`: Task name (VARCHAR 150)
- `description`: Task description (LONGTEXT)
- `priority`: Priority level (VARCHAR 20)
- `status`: Task status (VARCHAR 20)
- `due_date`: Due date (TIMESTAMP)
- `project_id`: Foreign key to projects (INT)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Assignments Table
- `id`: Primary key (INT)
- `user_id`: Foreign key to users (INT)
- `task_id`: Foreign key to tasks (INT)
- `assigned_date`: Assignment date (TIMESTAMP)
- `completed_date`: Completion date (TIMESTAMP)
- `notes`: Assignment notes (LONGTEXT)

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Dashboard
- `GET /` - Home/Dashboard redirect
- `GET /dashboard` - Main dashboard
- `GET /profile` - User profile

### Projects
- `GET /projects/` - List all projects
- `GET /projects/create` - Create project form
- `POST /projects/create` - Create project
- `GET /projects/<id>` - View project details
- `GET /projects/<id>/edit` - Edit project form
- `POST /projects/<id>/edit` - Update project
- `POST /projects/<id>/delete` - Delete project

### Tasks
- `GET /tasks/` - List all tasks
- `GET /tasks/create` - Create task form
- `POST /tasks/create` - Create task
- `GET /tasks/<id>` - View task details
- `GET /tasks/<id>/edit` - Edit task form
- `POST /tasks/<id>/edit` - Update task
- `POST /tasks/<id>/delete` - Delete task

### Assignments
- `POST /assignments/assign` - Assign task to user (JSON)
- `POST /assignments/<id>/remove` - Remove assignment

### Reports
- `GET /reports/` - View reports dashboard

## Features in Detail

### User Authentication
- Passwords are hashed using PBKDF2 with SHA256
- Secure session management with timeout
- Role-based access control
- Account activation/deactivation

### Task Management
- Priority levels: Low, Medium, High, Urgent
- Status tracking: Pending, In Progress, Completed
- Due date assignment
- Task filtering by status and priority
- Search functionality

### Project Management
- Create projects with descriptions and timelines
- Track project progress
- View all project tasks
- Calculate completion rates
- Project-wise statistics

### Reporting
- Real-time statistics
- Priority distribution analysis
- Status overview charts
- Project performance metrics
- User task completion tracking

### Security
- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- SQL injection prevention with SQLAlchemy ORM
- Secure session cookies
- Role-based authorization

## Troubleshooting

### Database Connection Error
```
Error: Can't connect to MySQL server
```

**Solution**:
1. Ensure MySQL server is running
2. Check username and password in `.env` file
3. Verify database exists: `SHOW DATABASES;`
4. Check DATABASE_URL in config.py

### Module Not Found Error
```
ModuleNotFoundError: No module named 'flask'
```

**Solution**:
1. Activate virtual environment
2. Run: `pip install -r requirements.txt`
3. Verify with: `pip list`

### Port Already in Use
```
OSError: [Errno 48] Address already in use
```

**Solution**:
1. Change port in app.py: `app.run(host='0.0.0.0', port=5001)`
2. Or kill process on port 5000

### Permission Denied
```
PermissionError: [Errno 13] Permission denied: 'app/static/uploads'
```

**Solution**:
1. Create uploads directory: `mkdir app/static/uploads`
2. Set permissions: `chmod 755 app/static/uploads`

## Performance Optimization

1. **Database Indexes**: Optimized queries with proper indexing
2. **Caching**: Browser caching for static files
3. **Sessions**: Efficient session management
4. **Lazy Loading**: Count queries only when needed
5. **Pagination**: Implement for large datasets

## Security Best Practices

1. Change `SECRET_KEY` in production
2. Use strong database passwords
3. Enable HTTPS in production
4. Set `SESSION_COOKIE_SECURE = True`
5. Regular security updates
6. Backup database regularly
7. Validate all user inputs

## Deployment

### Production Deployment Checklist
- [ ] Change SECRET_KEY
- [ ] Set FLASK_ENV=production
- [ ] Use strong database password
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Configure gunicorn/wsgi server
- [ ] Set up proper error handling
- [ ] Regular backups

### Deploy with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Deploy with Python Anywhere
1. Upload project files
2. Configure MySQL database
3. Set variables in web app settings
4. Reload web app

## Future Enhancements

- [ ] Email notifications for task assignments
- [ ] File attachments for tasks
- [ ] Task comments and discussion
- [ ] Time tracking and logging
- [ ] Gantt charts for projects
- [ ] Calendar view for tasks
- [ ] Export reports to PDF/Excel
- [ ] Mobile app
- [ ] Real-time notifications with WebSockets
- [ ] Integration with external APIs
- [ ] Dark mode theme

## Contributing

To contribute to TaskFlow:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

TaskFlow is open source software licensed under the MIT license.

## Support

For issues, questions, or suggestions:
- Check the troubleshooting section
- Review database schema
- Check console logs
- Monitor SQL queries

## Version History

- **v1.0.0** (2024)
  - Initial release
  - Core features implemented
  - Full CRUD operations
  - Reporting system
  - Role-based access control

## Credits

Built with:
- Flask Framework
- MySQL Database
- Bootstrap 5
- SQLAlchemy ORM
- Font Awesome Icons

## Contact

For more information or support, please contact the development team.

---

**Happy Task Management! 🎉**

Last Updated: 2024
Application: TaskFlow v1.0.0
