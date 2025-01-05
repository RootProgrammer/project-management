# Project Management Tool API  

TechForing Limited is developing a robust project management tool to enable team collaboration on projects. This tool provides a RESTful API for managing users, projects, tasks, and comments, intended to be consumed by a front-end web application and a mobile application.  

---

## **Features**  

### **Users**  
- Register, login, retrieve, update, and delete user accounts.  

### **Projects**  
- Create, retrieve, update, and delete projects.  
- Assign users with roles (`Admin` or `Member`) to projects.  

### **Tasks**  
- Manage tasks within projects, including assignment and status updates.  

### **Comments**  
- Add and manage comments on tasks to improve collaboration.  

---

## **Database Schema**  

### **Users**  
- **ID**: Primary Key  
- **Username**: Unique String  
- **Email**: Unique String  
- **Password**: String  
- **First Name**: String  
- **Last Name**: String  
- **Date Joined**: DateTime  

### **Projects**  
- **ID**: Primary Key  
- **Name**: String  
- **Description**: Text  
- **Owner**: Foreign Key to Users  
- **Created At**: DateTime  

### **Project Members**  
- **ID**: Primary Key  
- **Project**: Foreign Key to Projects  
- **User**: Foreign Key to Users  
- **Role**: String (Admin or Member)  

### **Tasks**  
- **ID**: Primary Key  
- **Title**: String  
- **Description**: Text  
- **Status**: String (To Do, In Progress, Done)  
- **Priority**: String (Low, Medium, High)  
- **Assigned To**: Foreign Key to Users (nullable)  
- **Project**: Foreign Key to Projects  
- **Created At**: DateTime  
- **Due Date**: DateTime  

### **Comments**  
- **ID**: Primary Key  
- **Content**: Text  
- **User**: Foreign Key to Users  
- **Task**: Foreign Key to Tasks  
- **Created At**: DateTime  

---

## **REST API Endpoints**  

### **Users**  
- **Register**: `POST /api/users/register/`  
- **Login**: `POST /api/users/login/`  
- **Retrieve**: `GET /api/users/{id}/`  
- **Update**: `PUT/PATCH /api/users/{id}/`  
- **Delete**: `DELETE /api/users/{id}/`  

### **Projects**  
- **List**: `GET /api/projects/`  
- **Create**: `POST /api/projects/`  
- **Retrieve**: `GET /api/projects/{id}/`  
- **Update**: `PUT/PATCH /api/projects/{id}/`  
- **Delete**: `DELETE /api/projects/{id}/`  

### **Tasks**  
- **List**: `GET /api/projects/{project_id}/tasks/`  
- **Create**: `POST /api/projects/{project_id}/tasks/`  
- **Retrieve**: `GET /api/tasks/{id}/`  
- **Update**: `PUT/PATCH /api/tasks/{id}/`  
- **Delete**: `DELETE /api/tasks/{id}/`  

### **Comments**  
- **List**: `GET /api/tasks/{task_id}/comments/`  
- **Create**: `POST /api/tasks/{task_id}/comments/`  
- **Retrieve**: `GET /api/comments/{id}/`  
- **Update**: `PUT/PATCH /api/comments/{id}/`  
- **Delete**: `DELETE /api/comments/{id}/`  

---

## **Setup Instructions**  

### **Prerequisites**  
- Python 3.13.1 installed.  
- Ensure `pip` and `virtualenv` are installed.  

---

### **Steps to Run Locally**  

1. **Clone the Repository**:  
   ```bash  
   git clone <repository-url>  
   cd <project-directory>  
   ```  

2. **Create and Activate a Virtual Environment**:  
   ```bash  
   python -m venv venv  
   source venv/bin/activate  # For Linux/Mac  
   venv\Scripts\activate     # For Windows  
   ```  

3. **Install Dependencies**:  
   ```bash  
   pip install -r requirements.txt  
   ```  

4. **Run Migrations**:  
   ```bash  
   python manage.py migrate  
   ```  

5. **Start the Server**:  
   ```bash  
   python manage.py runserver  
   ```  

6. **Access the API**:  
   API will be available at `http://127.0.0.1:8000/`.  

---

## **API Documentation**  

Detailed API documentation can be accessed via:  
[Postman Documentation](https://documenter.getpostman.com/view/19687041/2sAYJ9AJPF)  

---
