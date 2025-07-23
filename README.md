# 🧠 Internship Assignments - Backend (Python, Django, DRF)

This repository contains backend development assignments completed during an internship. Each assignment is organized into its own folder and built using:

- 🐍 Python
- 🌐 Django
- ⚙️ Django REST Framework (DRF)
- 🔐 JWT Authentication

---

## 📂 Folder Structure

Each folder represents a self-contained Django project:

Internship_Assignments_Backend/
├── Assignment_1/
│ ├── manage.py
│ └── ...
├── Assignment_2/
│ ├── manage.py
│ └── ...
├── Assignment_3/
│ └── ...
└── README.md

yaml
Copy
Edit

---

## 🚀 How to Run an Assignment

> 📝 Every assignment is a complete Django project and can be run independently.

### Steps:

1. Open terminal or command prompt.
2. Navigate into the specific assignment folder:
   ```bash
   cd Assignment_1  # Replace with your assignment folder
(Optional) Create and activate a virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install dependencies (if requirements.txt exists):

bash
Copy
Edit
pip install -r requirements.txt
Run the Django server:

bash
Copy
Edit
python manage.py runserver
🔐 JWT Authentication Flow
Most assignments use token-based authentication using Simple JWT.

🧾 Authentication Process:
Register or Login to get JWT tokens:

bash
Copy
Edit
POST /api/token/
Response:

json
Copy
Edit
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
Use the access token for authenticated requests:

makefile
Copy
Edit
Authorization: Bearer <your_access_token>
To refresh your token:

swift
Copy
Edit
POST /api/token/refresh/
⚙️ Technologies Used
Python 3.8+

Django 4.x

Django REST Framework

Simple JWT

SQLite3 or PostgreSQL (depends on assignment)

🧪 Sample API Usage
http
Copy
Edit
# Example: Get all blog posts (public)
GET /api/blogs/

# Create blog post (writer role only)
POST /api/blogs/
Headers:
  Authorization: Bearer <access_token>
Body:
  {
    "title": "My Post",
    "content": "This is a blog post."
  }
📦 Virtual Environment & Dependencies
It’s recommended to use a virtual environment for each project:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
If there’s no requirements.txt, you can generate one by:

bash
Copy
Edit
pip freeze > requirements.txt
✅ Assignment Topics Covered
User Registration/Login with JWT

Role-based access (Writer vs Viewer)

Blog APIs (CRUD)

Custom permissions

ViewSets & Routers

Django settings management

Modular app structure

Token refresh and protection

🤝 Contributions
This repository is intended for personal learning and internship tasks. Feel free to fork it, learn from it, or refer to it in your own Django backend projects.
