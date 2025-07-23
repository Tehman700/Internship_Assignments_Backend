<?xml version="1.0" encoding="UTF-8"?>
<readme>
  <title>Internship Assignments - Backend (Python, Django, DRF)</title>
  <description>
    This repository contains backend development assignments completed during an internship. Each assignment is organized into its own folder and built using:
    - Python
    - Django
    - Django REST Framework (DRF)
    - JWT Authentication
  </description>

  <folderStructure>
    <![CDATA[
    Internship_Assignments_Backend/
    ├── Assignment_1/
    │   ├── manage.py
    │   └── ...
    ├── Assignment_2/
    │   ├── manage.py
    │   └── ...
    ├── Assignment_3/
    │   └── ...
    └── README.md
    ]]>
  </folderStructure>

  <runInstructions>
    <![CDATA[
    1. Open terminal or command prompt.
    2. Navigate into the specific assignment folder:
       cd Assignment_1
    3. (Optional) Create and activate a virtual environment:
       python -m venv venv
       source venv/bin/activate   # Or venv\Scripts\activate on Windows
    4. Install dependencies:
       pip install -r requirements.txt
    5. Run the server:
       python manage.py runserver
    ]]>
  </runInstructions>

  <jwtAuthentication>
    <flow>
      <step>1. Register or login to get tokens: POST /api/token/</step>
      <step>2. Use access token in headers: Authorization: Bearer &lt;access_token&gt;</step>
      <step>3. Refresh token: POST /api/token/refresh/</step>
    </flow>
  </jwtAuthentication>

  <technologies>
    <item>Python 3.8+</item>
    <item>Django 4.x</item>
    <item>Django REST Framework</item>
    <item>Simple JWT</item>
    <item>SQLite3 / PostgreSQL</item>
  </technologies>

  <apiUsage>
    <![CDATA[
    # Get public blog posts
    GET /api/blogs/

    # Create blog post (writer role)
    POST /api/blogs/
    Headers:
      Authorization: Bearer <access_token>
    Body:
      {
        "title": "My Post",
        "content": "This is a blog post."
      }
    ]]>
  </apiUsage>

  <venv>
    <![CDATA[
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ]]>
  </venv>

  <assignmentsCovered>
    <topic>User Registration/Login with JWT</topic>
    <topic>Role-based access (Writer vs Viewer)</topic>
    <topic>Blog APIs (CRUD)</topic>
    <topic>Custom permissions</topic>
    <topic>ViewSets & Routers</topic>
    <topic>Django settings management</topic>
    <topic>Modular app structure</topic>
    <topic>Token refresh and protection</topic>
  </assignmentsCovered>

  <contribution>This repository is intended for personal learning and internship tasks. Feel free to fork it, learn from it, or refer to it in your own Django backend projects.</contribution>

  <license>
    MIT License - Free to use for personal and educational purposes.
  </license>

  <author>
    <name>Tehman Hassan</name>
    <github>https://github.com/Tehman700</github>
  </author>
</readme>
