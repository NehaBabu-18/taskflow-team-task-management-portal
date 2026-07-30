from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum

class Role(Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    USER = 'user'

class TaskStatus(Enum):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'

class TaskPriority(Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    URGENT = 'Urgent'

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    assignments = db.relationship('Assignment', backref='user', lazy=True, cascade='all, delete-orphan')
    created_projects = db.relationship('Project', backref='creator', lazy=True, foreign_keys='Project.creator_id', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def get_assigned_tasks(self):
        """Get all tasks assigned to this user"""
        return db.session.query(Task).join(Assignment).filter(Assignment.user_id == self.id).all()
    
    def get_task_statistics(self):
        """Get task statistics for user"""
        tasks = self.get_assigned_tasks()
        total = len(tasks)
        completed = len([t for t in tasks if t.status == 'Completed'])
        pending = len([t for t in tasks if t.status == 'Pending'])
        in_progress = len([t for t in tasks if t.status == 'In Progress'])
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'in_progress': in_progress
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Active')
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def get_project_statistics(self):
        """Get statistics for this project"""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t.status == 'Completed'])
        pending_tasks = len([t for t in self.tasks if t.status == 'Pending'])
        in_progress_tasks = len([t for t in self.tasks if t.status == 'In Progress'])
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'in_progress_tasks': in_progress_tasks,
            'completion_rate': round(completion_rate, 2)
        }
    
    def __repr__(self):
        return f'<Project {self.project_name}>'


class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='Medium')
    status = db.Column(db.String(20), default='Pending')
    due_date = db.Column(db.DateTime)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    attachment = db.Column(db.String(255), nullable=True)
    
    # Relationships
    assignments = db.relationship('Assignment', backref='task', lazy=True, cascade='all, delete-orphan')
    
    def get_assigned_users(self):
        """Get all users assigned to this task"""
        return [assignment.user for assignment in self.assignments]
    
    def __repr__(self):
        return f'<Task {self.task_name}>'


class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    completed_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    # Unique constraint on user_id and task_id
    __table_args__ = (db.UniqueConstraint('user_id', 'task_id', name='unique_user_task_assignment'),)
    
    def __repr__(self):
        return f'<Assignment User:{self.user_id} Task:{self.task_id}>'
