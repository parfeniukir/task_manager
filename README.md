# Task Manager

Task Manager is a web application for personal task management with user authentication and data access control.
The project is built on Django using Class-Based Views

---

## Features

- User authentication (login, logout, signup)
- Custom user model
- Personal task management
- Create, view, update and delete tasks
- Mark tasks as completed
- Task ownership and access control
- Form validation
- Clean separation of concerns (apps, views, templates)

---

## Tech Stack

- Python 3.10+
- Django 5.x
- SQLite (default, easily replaceable)
- Django Templates
- HTML5

---

## Project Structure

```
task_manager/
├── config/              # Project configuration
├── accounts/            # User management and authentication
├── tasks/               # Task domain logic
├── templates/           # Global templates
│   └── registration/    # Django auth templates
├── static/              # Static assets
├── manage.py
└── requirements.txt
```

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone <repository_url>
cd task_manager
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

`pip install -r requirements.txt`

### 4. Install Pre-commit tool

`pre-commit install`

### 5. Apply database migrations

`python manage.py migrate`

### 6. Create superuser (optional)

`python manage.py createsuperuser`

### 7. Run development server

`python manage.py runserver`

Application will be available at:

`http://127.0.0.1:8000/`

---

## Authentication Flow

- Users can sign up using a custom registration page
- Login and logout are handled by Django’s built-in authentication views
- After login, users are redirected to their task list
- Logout is performed via POST request for security reasons

---

## Task Management Logic

- Each task is linked to a specific user
- Users can only view and manage their own tasks
- Task completion is toggled via a dedicated POST action
- All data-modifying actions are protected by authentication and ownership checks

---

## Security Considerations

- All task-related views require authentication
- Ownership checks are enforced at the view level
- State-changing actions use POST requests
- No sensitive data is exposed in templates
