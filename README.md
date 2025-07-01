# ASSIGNMENT EZ-Labs(Backend) #
 <div align="center"> <br />   <img src= "https://github.com/Akpan123/project_reachify/blob/main/frontend/public/SITE%20IMAGE.png" alt="Project Banner"> <br /> <div align="center"> <br /> <h1>Secure File Management System</h1> <div> <img src="https://img.shields.io/badge/-Flask-black?style=for-the-badge&logoColor=white&logo=flask&color=000000" alt="Flask" /> <img src="https://img.shields.io/badge/-Bootstrap-black?style=for-the-badge&logoColor=white&logo=bootstrap&color=7952B3" alt="Bootstrap" /> <img src="https://img.shields.io/badge/-WTForms-black?style=for-the-badge&logoColor=white&logo=python&color=3776AB" alt="WTForms" /> <img src="https://img.shields.io/badge/-Jinja2-black?style=for-the-badge&logoColor=white&logo=jinja&color=B41717" alt="Jinja2" /> </div> <h3 align="center">Secure Document Management for Operations and Client Users</h3> </div>
  
# 📋 Introduction #
The File Management System is a secure web application designed for operations teams and clients to manage office documents. It features role-based access control, encrypted email verification, and secure file handling with strict format validation (pptx, docx, xlsx). The application demonstrates modern web development practices with Flask and Bootstrap.

# ⚙️ Tech Stack #

Frontend: Bootstrap 5, Font Awesome
Backend: Flask, Flask-WTF, WTForms
Security: ItsDangerous (token generation), Session-based authentication
Templating: Jinja2 with custom filters
File Handling: Secure filename validation, type restrictions


# 🌟 Features #

Role-Based Access Control:
    Operations users: Upload office documents (pptx/docx/xlsx)
    Client users: List and download available files
    
Secure Authentication:
    Encrypted email verification links
    Session management with secret key

File Management:
    Strict file type validation
    Human-readable file size display
    Visual file type indicators
    
Responsive Design:
    Mobile-friendly interface
    Intuitive navigation

Error Handling:
    Custom 404 and 500 error pages
    Form validation with user feedback


# 🤸 Quick Start #

Prerequisites

Ensure you have installed:

    Python 3.8+
    pip package manager
  


```bash
# Clone the repository
git clone https://github.com/your-username/file-management-system.git
cd file-management-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```
Running the Application
<br>
```bash
# Start the Flask development server
python main.py
```
<br>
Accessing the Application
Open your browser: http://localhost:5000

Operations Credentials: ops@example.com / opspassword

Client users can sign up with any email


<div align="center"> <h3>Built with ❤️ by Akshat Pandey</h3> <a href="https://github.com/Akpan123">GitHub</a> | <a href="https://linkedin.com/in/akshat-pandey-7397b7258/">LinkedIn</a> </div>
