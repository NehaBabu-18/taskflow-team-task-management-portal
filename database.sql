-- TaskFlow Database Script
-- Create Database

CREATE DATABASE IF NOT EXISTS taskflow_db;
USE taskflow_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Projects Table
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(150) NOT NULL,
    description LONGTEXT,
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP NULL,
    status VARCHAR(20) DEFAULT 'Active',
    creator_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_project_name (project_name),
    INDEX idx_creator_id (creator_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tasks Table
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_name VARCHAR(150) NOT NULL,
    description LONGTEXT,
    priority VARCHAR(20) DEFAULT 'Medium',
    status VARCHAR(20) DEFAULT 'Pending',
    due_date TIMESTAMP NULL,
    project_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    INDEX idx_task_name (task_name),
    INDEX idx_project_id (project_id),
    INDEX idx_status (status),
    INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Assignments Table
CREATE TABLE IF NOT EXISTS assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    task_id INT NOT NULL,
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_date TIMESTAMP NULL,
    notes LONGTEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_task (user_id, task_id),
    INDEX idx_user_id (user_id),
    INDEX idx_task_id (task_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert Sample Admin User (password: password123)
INSERT INTO users (username, email, password_hash, role, is_active) 
VALUES ('admin', 'admin@taskflow.com', 'pbkdf2:sha256:600000$hash_placeholder', 'admin', 1);

-- Insert Sample Manager User
INSERT INTO users (username, email, password_hash, role, is_active) 
VALUES ('manager', 'manager@taskflow.com', 'pbkdf2:sha256:600000$hash_placeholder', 'manager', 1);

-- Insert Sample User
INSERT INTO users (username, email, password_hash, role, is_active) 
VALUES ('user1', 'user1@taskflow.com', 'pbkdf2:sha256:600000$hash_placeholder', 'user', 1);

-- Insert Sample Project
INSERT INTO projects (project_name, description, creator_id) 
VALUES ('Website Redesign', 'Complete redesign of the company website', 1);

-- Insert Sample Tasks
INSERT INTO tasks (task_name, description, priority, status, project_id) 
VALUES ('Design Homepage', 'Create mockups for homepage', 'High', 'In Progress', 1);

INSERT INTO tasks (task_name, description, priority, status, project_id) 
VALUES ('Create Database Schema', 'Design database for new features', 'High', 'Pending', 1);

INSERT INTO tasks (task_name, description, priority, status, project_id) 
VALUES ('API Integration', 'Integrate third-party APIs', 'Medium', 'Pending', 1);

-- Create Views for Analytics
CREATE OR REPLACE VIEW task_statistics AS
SELECT 
    COUNT(*) as total_tasks,
    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed_tasks,
    SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) as pending_tasks,
    SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END) as in_progress_tasks
FROM tasks;

CREATE OR REPLACE VIEW project_statistics AS
SELECT 
    p.id,
    p.project_name,
    COUNT(t.id) as total_tasks,
    SUM(CASE WHEN t.status = 'Completed' THEN 1 ELSE 0 END) as completed_tasks,
    SUM(CASE WHEN t.status = 'Pending' THEN 1 ELSE 0 END) as pending_tasks,
    SUM(CASE WHEN t.status = 'In Progress' THEN 1 ELSE 0 END) as in_progress_tasks
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
GROUP BY p.id, p.project_name;

-- Performance Indexes
CREATE INDEX idx_task_project_status ON tasks(project_id, status);
CREATE INDEX idx_assignment_user_task ON assignments(user_id, task_id);
CREATE INDEX idx_task_created_date ON tasks(created_at);
CREATE INDEX idx_project_created_date ON projects(created_at);

-- Add privileges (update username/password as needed)
-- GRANT ALL PRIVILEGES ON taskflow_db.* TO 'taskflow_user'@'localhost' IDENTIFIED BY 'taskflow_password';
-- FLUSH PRIVILEGES;
