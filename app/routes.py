from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app import db
from app.models import User, Project, Task, Assignment
from datetime import datetime, timedelta
from functools import wraps
import os
from sqlalchemy import or_

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
projects_bp = Blueprint('projects', __name__, url_prefix='/projects')
tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')
assignments_bp = Blueprint('assignments', __name__, url_prefix='/assignments')
reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

# ==================== DECORATORS ====================

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('auth.login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role not in ['admin', 'manager']:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current logged-in user"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

# ==================== MAIN ROUTES ====================

@main_bp.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard showing statistics"""
    user = get_current_user()
    
    if user.role == 'admin':
        # Admin dashboard
        total_users = User.query.count()
        total_projects = Project.query.count()
        total_tasks = Task.query.count()
        completed_tasks = Task.query.filter_by(status='Completed').count()
        pending_tasks = Task.query.filter_by(status='Pending').count()
        in_progress_tasks = Task.query.filter_by(status='In Progress').count()
        
        recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
        recent_tasks = Task.query.order_by(Task.created_at.desc()).limit(5).all()
        
        context = {
            'total_users': total_users,
            'total_projects': total_projects,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'in_progress_tasks': in_progress_tasks,
            'recent_projects': recent_projects,
            'recent_tasks': recent_tasks,
            'user_role': 'admin'
        }
    else:
        # User/Manager dashboard
        stats = user.get_task_statistics()
        user_projects = Project.query.filter_by(creator_id=user.id).all()
        user_tasks = user.get_assigned_tasks()
        
        context = {
            'total_tasks': stats['total'],
            'completed_tasks': stats['completed'],
            'pending_tasks': stats['pending'],
            'in_progress_tasks': stats['in_progress'],
            'total_projects': len(user_projects),
            'user_projects': user_projects,
            'user_tasks': user_tasks[:5],
            'user_role': user.role
        }
    
    return render_template('dashboard.html', **context)

@main_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    user = get_current_user()
    stats = user.get_task_statistics()
    
    return render_template('profile.html', user=user, stats=stats)

# ==================== AUTHENTICATION ROUTES ====================

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(username=username, email=email, role='user')
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('Your account has been deactivated.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Set session
        session['user_id'] = user.id
        session['username'] = user.username
        session.permanent = True
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        flash(f'Welcome, {user.username}!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

# ==================== PROJECTS ROUTES ====================

@projects_bp.route('/')
@login_required
def list_projects():
    """List all projects"""
    user = get_current_user()
    
    if user.role == 'admin':
        projects = Project.query.all()
    else:
        projects = Project.query.filter_by(creator_id=user.id).all()
    
    return render_template('projects.html', projects=projects)

@projects_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    """Create a new project"""
    user = get_current_user()
    
    if request.method == 'POST':
        project_name = request.form.get('project_name', '').strip()
        description = request.form.get('description', '').strip()
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        
        if not project_name:
            flash('Project name is required.', 'danger')
            return redirect(url_for('projects.create_project'))
        
        project = Project(
            project_name=project_name,
            description=description,
            creator_id=user.id
        )
        
        if start_date:
            project.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        
        if end_date:
            project.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        db.session.add(project)
        db.session.commit()
        
        flash('Project created successfully!', 'success')
        return redirect(url_for('projects.list_projects'))
    
    return render_template('project_form.html', action='Create')

@projects_bp.route('/<int:project_id>')
@login_required
def view_project(project_id):
    """View project details"""
    project = Project.query.get_or_404(project_id)
    user = get_current_user()
    
    if user.role not in ['admin'] and project.creator_id != user.id:
        flash('You do not have permission to view this project.', 'danger')
        return redirect(url_for('projects.list_projects'))
    
    stats = project.get_project_statistics()
    
    return render_template('project_detail.html', project=project, stats=stats)

@projects_bp.route('/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """Edit project"""
    project = Project.query.get_or_404(project_id)
    user = get_current_user()
    
    if user.role not in ['admin'] and project.creator_id != user.id:
        flash('You do not have permission to edit this project.', 'danger')
        return redirect(url_for('projects.list_projects'))
    
    if request.method == 'POST':
        project.project_name = request.form.get('project_name', '').strip()
        project.description = request.form.get('description', '').strip()
        
        start_date = request.form.get('start_date')
        if start_date:
            project.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        
        end_date = request.form.get('end_date')
        if end_date:
            project.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        project.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Project updated successfully!', 'success')
        return redirect(url_for('projects.view_project', project_id=project.id))
    
    return render_template('project_form.html', project=project, action='Edit')

@projects_bp.route('/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    """Delete project"""
    project = Project.query.get_or_404(project_id)
    user = get_current_user()
    
    if user.role not in ['admin'] and project.creator_id != user.id:
        flash('You do not have permission to delete this project.', 'danger')
        return redirect(url_for('projects.list_projects'))
    
    db.session.delete(project)
    db.session.commit()
    
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('projects.list_projects'))

# ==================== TASKS ROUTES ====================

@tasks_bp.route('/')
@login_required
def list_tasks():
    """List all tasks"""
    user = get_current_user()
    filter_status = request.args.get('status', '')
    filter_priority = request.args.get('priority', '')
    
    query = Task.query
    
    if user.role != 'admin':
        # Show tasks from user's projects or assigned tasks
        user_project_ids = [p.id for p in Project.query.filter_by(creator_id=user.id).all()]
        user_task_ids = [a.task_id for a in Assignment.query.filter_by(user_id=user.id).all()]
        query = query.filter(db.or_(Task.project_id.in_(user_project_ids), Task.id.in_(user_task_ids)))
    
    if filter_status:
        query = query.filter_by(status=filter_status)
    
    if filter_priority:
        query = query.filter_by(priority=filter_priority)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    
    return render_template('tasks.html', tasks=tasks, filter_status=filter_status, filter_priority=filter_priority)

@tasks_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    """Create a new task"""
    user = get_current_user()
    
    if user.role == 'admin':
        projects = Project.query.all()
    else:
        projects = Project.query.filter_by(creator_id=user.id).all()
    
    if request.method == 'POST':
        task_name = request.form.get('task_name', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'Medium')
        status = request.form.get('status', 'Pending')
        due_date = request.form.get('due_date')
        project_id = request.form.get('project_id')# Capture the Assigned User
        assigned_to_input = request.form.get('assigned_to')
        if assigned_to_input and assigned_to_input != "None":
            assigned_to_id = int(assigned_to_input)
        else:
            assigned_to_id = None
        
        if not task_name or not project_id:
            flash('Task name and project are required.', 'danger')
            return redirect(url_for('tasks.create_task'))
        
        # Verify project permission
        project = Project.query.get(project_id)
        if not project:
            flash('Invalid project selected.', 'danger')
            return redirect(url_for('tasks.create_task'))
        
        if user.role not in ['admin'] and project.creator_id != user.id:
            flash('You do not have permission to create tasks for this project.', 'danger')
            return redirect(url_for('tasks.create_task'))
        
        task = Task(
            task_name=task_name,
            description=description,
            priority=priority,
            status=status,
            project_id=project_id
        )
        
        if due_date:
            task.due_date = datetime.strptime(due_date, '%Y-%m-%d')
        
        db.session.add(task)
        db.session.commit()

        if assigned_to_id:
            db.session.add(Assignment(user_id=assigned_to_id, task_id=task.id))
            db.session.commit()
        
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks.list_tasks'))
    users = User.query.all()
    return render_template('task_form.html', projects=projects, users=users, action='Create', selected_user_id=None)

@tasks_bp.route('/<int:task_id>')
@login_required
def view_task(task_id):
    """View task details"""
    task = Task.query.get_or_404(task_id)
    user = get_current_user()
    
    # Check permissions
    is_creator = task.project.creator_id == user.id
    is_assigned = Assignment.query.filter_by(user_id=user.id, task_id=task_id).first()
    has_permission = user.role == 'admin' or is_creator or is_assigned
    
    if not has_permission:
        flash('You do not have permission to view this task.', 'danger')
        return redirect(url_for('tasks.list_tasks'))
    
    assigned_users = task.get_assigned_users()
    all_users = User.query.all()
    
    return render_template('task_detail.html', task=task, assigned_users=assigned_users, all_users=all_users)

@tasks_bp.route('/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    user = get_current_user()

    is_creator = task.project.creator_id == user.id
    is_assigned = Assignment.query.filter_by(user_id=user.id, task_id=task_id).first()
    if not (user.role == 'admin' or is_creator or is_assigned):
        flash('You do not have permission to edit this task.', 'danger')
        return redirect(url_for('tasks.list_tasks'))

    if user.role == 'admin':
        projects = Project.query.all()
    else:
        projects = Project.query.filter_by(creator_id=user.id).all()

    users = User.query.all()

    if request.method == 'POST':
        task_name = request.form.get('task_name')
        if task_name is not None:
            task.task_name = task_name.strip() or task.task_name

        description = request.form.get('description')
        if description is not None:
            task.description = description.strip()

        priority = request.form.get('priority')
        if priority:
            task.priority = priority

        status = request.form.get('status')
        if status:
            task.status = status

        due_date = request.form.get('due_date')
        if due_date:
            task.due_date = datetime.strptime(due_date, '%Y-%m-%d')
        elif due_date == '':
            task.due_date = None

        project_id = request.form.get('project_id')
        if project_id:
            project = Project.query.get(project_id)
            if project and (user.role == 'admin' or project.creator_id == user.id):
                task.project_id = project.id

        assigned_user_id = request.form.get('assigned_to')
        if assigned_user_id in [None, '', 'None']:
            Assignment.query.filter_by(task_id=task_id).delete()
        else:
            assigned_user_id = int(assigned_user_id)
            if not Assignment.query.filter_by(task_id=task_id, user_id=assigned_user_id).first():
                Assignment.query.filter_by(task_id=task_id).delete()
                db.session.add(Assignment(user_id=assigned_user_id, task_id=task.id))

        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks.list_tasks'))

    selected_user_id = task.assignments[0].user_id if task.assignments else None
    return render_template(
        'task_form.html',
        task=task,
        users=users,
        projects=projects,
        selected_user_id=selected_user_id,
        action='Edit'
    )

@tasks_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    user = get_current_user()

    is_creator = task.project.creator_id == user.id
    is_assigned = Assignment.query.filter_by(user_id=user.id, task_id=task_id).first()
    if not (user.role == 'admin' or is_creator or is_assigned):
        flash('You do not have permission to delete this task.', 'danger')
        return redirect(url_for('tasks.list_tasks'))

    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks.list_tasks'))
    # ==================== ASSIGNMENT ROUTES ====================

@assignments_bp.route('/assign/<int:task_id>', methods=['POST'])
@login_required
def assign_task(task_id):
    task = Task.query.get_or_404(task_id)

    user_id = request.form.get('user_id')

    if not user_id:
        flash('Please select a user.', 'danger')
        return redirect(url_for('tasks.view_task', task_id=task_id))

    existing = Assignment.query.filter_by(
        task_id=task_id,
        user_id=user_id
    ).first()

    if existing:
        flash('User already assigned.', 'warning')
        return redirect(url_for('tasks.view_task', task_id=task_id))

    assignment = Assignment(
        user_id=user_id,
        task_id=task_id
    )

    db.session.add(assignment)
    db.session.commit()

    flash('Task assigned successfully.', 'success')
    return redirect(url_for('tasks.view_task', task_id=task_id))


@assignments_bp.route('/remove/<int:assignment_id>', methods=['POST'])
@login_required
def remove_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)

    db.session.delete(assignment)
    db.session.commit()

    flash('Assignment removed.', 'success')

    return redirect(
        url_for(
            'tasks.view_task',
            task_id=assignment.task_id
        )
    )
# ==================== REPORT ROUTES ====================

@reports_bp.route('/')
@login_required
def reports_dashboard():
    user = get_current_user()

    if user.role in ['admin', 'manager']:
        total_projects = Project.query.count()
        total_tasks = Task.query.count()

        completed_tasks = Task.query.filter_by(status='Completed').count()
        pending_tasks = Task.query.filter_by(status='Pending').count()
        in_progress_tasks = Task.query.filter_by(status='In Progress').count()

        priority_distribution = {
            'low': Task.query.filter_by(priority='Low').count(),
            'medium': Task.query.filter_by(priority='Medium').count(),
            'high': Task.query.filter_by(priority='High').count(),
            'urgent': Task.query.filter_by(priority='Urgent').count()
        }

        project_stats = [
            {
                'project': project,
                'stats': project.get_project_statistics()
            }
            for project in Project.query.order_by(Project.created_at.desc()).all()
        ]

        completion_rate = round((completed_tasks / total_tasks) * 100, 2) if total_tasks else 0

        return render_template(
            'reports.html',
            user_role=user.role,
            total_projects=total_projects,
            total_tasks=total_tasks,
            total_completed=completed_tasks,
            total_pending=pending_tasks,
            total_in_progress=in_progress_tasks,
            completion_rate=completion_rate,
            priority_distribution=priority_distribution,
            project_stats=project_stats
        )

    user_stats = user.get_task_statistics()
    user_projects = Project.query.filter_by(creator_id=user.id).all()
    project_stats = [
        {
            'project': project,
            'stats': project.get_project_statistics()
        }
        for project in user_projects
    ]

    return render_template(
        'reports.html',
        user_role=user.role,
        user_stats=user_stats,
        project_stats=project_stats
    )


@reports_bp.route('/project/<int:project_id>')
@login_required
def project_report(project_id):
    user = get_current_user()
    project = Project.query.get_or_404(project_id)

    if user.role not in ['admin', 'manager'] and project.creator_id != user.id:
        flash('You do not have permission to view this project report.', 'danger')
        return redirect(url_for('reports.reports_dashboard'))

    stats = project.get_project_statistics()

    return render_template(
        'project_report.html',
        project=project,
        stats=stats
    )


@reports_bp.route('/api/task-stats')
@login_required
def task_stats_api():

    data = {
        "completed": Task.query.filter_by(
            status='Completed'
        ).count(),

        "pending": Task.query.filter_by(
            status='Pending'
        ).count(),

        "in_progress": Task.query.filter_by(
            status='In Progress'
        ).count()
    }

    return jsonify(data)