// TaskFlow - Team Task Management Portal
// Main JavaScript File

document.addEventListener('DOMContentLoaded', function () {
    initializeEventListeners();
    initializeTooltips();
});

// Initialize tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize event listeners
function initializeEventListeners() {
    // Logout confirmation
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function (e) {
            if (!confirm('Are you sure you want to logout?')) {
                e.preventDefault();
            }
        });
    }

    // Delete confirmation
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });

    // Assign task to user
    const assignButtons = document.querySelectorAll('.assign-task-btn');
    assignButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            assignTaskToUser(this);
        });
    });

    // Remove assignment
    const removeAssignmentButtons = document.querySelectorAll('.remove-assignment-btn');
    removeAssignmentButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            if (confirm('Are you sure you want to remove this assignment?')) {
                this.closest('form').submit();
            }
        });
    });

    // Status update
    const statusSelects = document.querySelectorAll('.task-status-select');
    statusSelects.forEach(select => {
        select.addEventListener('change', function () {
            updateTaskStatus(this);
        });
    });

    // Search and filter
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('keyup', function () {
            filterTable(this);
        });
    }

    // Priority filter
    const priorityFilter = document.getElementById('priority-filter');
    if (priorityFilter) {
        priorityFilter.addEventListener('change', function () {
            location.href = updateUrlParameter(window.location.href, 'priority', this.value);
        });
    }

    // Status filter
    const statusFilter = document.getElementById('status-filter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function () {
            location.href = updateUrlParameter(window.location.href, 'status', this.value);
        });
    }
}

// Assign task to user
function assignTaskToUser(button) {
    const modal = new bootstrap.Modal(document.getElementById('assignModal'));
    const taskId = button.closest('.task-card').getAttribute('data-task-id');
    document.getElementById('assignModal').setAttribute('data-task-id', taskId);
    modal.show();
}

// Submit task assignment
function submitTaskAssignment() {
    const taskId = document.getElementById('assignModal').getAttribute('data-task-id');
    const userId = document.getElementById('user-select').value;

    if (!userId) {
        showAlert('Please select a user', 'warning');
        return;
    }

    const formData = new FormData();
    formData.append('task_id', taskId);
    formData.append('user_id', userId);

    fetch('/assignments/assign', {
        method: 'POST',
        body: JSON.stringify({ task_id: taskId, user_id: userId }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showAlert('Task assigned successfully!', 'success');
                bootstrap.Modal.getInstance(document.getElementById('assignModal')).hide();
                setTimeout(() => location.reload(), 500);
            } else {
                showAlert(data.message, 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('An error occurred while assigning the task', 'danger');
        });
}

// Update task status
function updateTaskStatus(select) {
    const taskId = select.getAttribute('data-task-id');
    const newStatus = select.value;
    const form = select.closest('form');

    if (form) {
        form.submit();
    }
}

// Filter table by search input
function filterTable(input) {
    const searchText = input.value.toLowerCase();
    const rows = document.querySelectorAll('table tbody tr');

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchText) ? '' : 'none';
    });
}

// Update URL parameter
function updateUrlParameter(url, param, value) {
    const urlParams = new URLSearchParams(new URL(url).search);
    urlParams.set(param, value);
    return url.split('?')[0] + '?' + urlParams.toString();
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) {
        const container = document.createElement('div');
        container.id = 'alert-container';
        container.style.position = 'fixed';
        container.style.top = '80px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        container.style.maxWidth = '400px';
        document.body.appendChild(container);
    }

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    document.getElementById('alert-container').appendChild(alertDiv);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = new bootstrap.Alert(alertDiv);
        alert.close();
    }, 5000);
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Get status badge class
function getStatusBadgeClass(status) {
    const statusMap = {
        'Pending': 'badge-pending',
        'In Progress': 'badge-in-progress',
        'Completed': 'badge-completed'
    };
    return statusMap[status] || 'badge-secondary';
}

// Get priority badge class
function getPriorityBadgeClass(priority) {
    const priorityMap = {
        'Low': 'badge-low',
        'Medium': 'badge-medium',
        'High': 'badge-high',
        'Urgent': 'badge-urgent'
    };
    return priorityMap[priority] || 'badge-secondary';
}

// Export table to CSV
function exportTableToCSV(filename) {
    const csv = [];
    const rows = document.querySelectorAll('table tr');

    for (let i = 0; i < rows.length; i++) {
        const row = [];
        const cols = rows[i].querySelectorAll('td, th');

        for (let j = 0; j < cols.length; j++) {
            row.push(cols[j].innerText);
        }

        csv.push(row.join(','));
    }

    downloadCSV(csv.join('\n'), filename);
}

// Download CSV file
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// Print page
function printPage() {
    window.print();
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Validate email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate password
function validatePassword(password) {
    return password && password.length >= 6;
}

// Show loading spinner
function showSpinner(element) {
    element.innerHTML = '<span class="spinner"></span>';
}

// Hide loading spinner
function hideSpinner(element, content) {
    element.innerHTML = content;
}

// Make AJAX request
async function makeRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Toggle sidebar
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    }
}

// Close sidebar on link click
document.addEventListener('click', function (e) {
    const sidebar = document.querySelector('.sidebar');
    const toggleBtn = document.querySelector('.sidebar-toggle');

    if (sidebar && toggleBtn && !sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
        sidebar.classList.remove('active');
    }
});

// Scroll to top button
const scrollToTopBtn = document.getElementById('scroll-to-top');
if (scrollToTopBtn) {
    window.addEventListener('scroll', function () {
        if (window.pageYOffset > 300) {
            scrollToTopBtn.style.display = 'block';
        } else {
            scrollToTopBtn.style.display = 'none';
        }
    });

    scrollToTopBtn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}
