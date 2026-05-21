

A production-ready **Role-Based Task Management System** built using Django and Django REST Framework with JWT authentication and PostgreSQL support.

---

Features
Role-Based Access Control (Admin / Employee)
JWT Authentication (Login / Register)
Project Management (Create / Update / Delete)
Task Management System
Task Assignment (Admin only) Task Status Tracking (Pending / In Progress / Completed)
 Secure API with permissions

---

 Tech Stack

* Python 3.x
* Django 5.x
* Django REST Framework
* Simple JWT
* PostgreSQL (Production)
* SQLite (Development)
* Gunicorn (Deployment)

---
 Installation (Local Setup)

`
cd project_TaskManagerApp
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

---

 Run Project Locally

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

Create Superuser

```bash
python manage.py createsuperuser
```

---

Environment Variables (.env)

Create a `.env` file in project root:

```env
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/dbname
```

---

API Endpoints
Authentication

* POST `/api/register/` → Register User
* POST `/api/token/` → Login (JWT)

Projects

* GET/POST `/api/projects/`
* PUT/DELETE `/api/projects/{id}/`
Tasks

* GET/POST `/api/tasks/`
* PATCH `/api/tasks/{id}/`
* POST `/api/tasks/{id}/assign/`

---

 User Roles

 Admin

* Create projects
* Create tasks
* Assign tasks to employees
* Manage everything

 Employee

* View assigned tasks
* Update task status only

---
 Deployment

Deployed using:

* Railway
* Gunicorn
* PostgreSQL
* Environment Variables

-

