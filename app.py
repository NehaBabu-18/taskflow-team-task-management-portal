"""
TaskFlow - Team Task Management Portal
Main Application Entry Point
"""

import os
from app import create_app, db
from app.models import User, Project, Task, Assignment
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask application
app = create_app(os.environ.get('FLASK_ENV', 'development'))

# Shell context for flask shell
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Project': Project,
        'Task': Task,
        'Assignment': Assignment
    }

# Application error handlers
@app.errorhandler(404)
def page_not_found(error):
    return '''
    <div style="text-align: center; padding: 50px;">
        <h1>404 - Page Not Found</h1>
        <p>The page you are looking for does not exist.</p>
        <a href="/">Go back to home</a>
    </div>
    ''', 404

@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return '''
    <div style="text-align: center; padding: 50px;">
        <h1>500 - Internal Server Error</h1>
        <p>An internal server error occurred.</p>
        <a href="/">Go back to home</a>
    </div>
    ''', 500

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=os.environ.get('FLASK_DEBUG', True)
    )
