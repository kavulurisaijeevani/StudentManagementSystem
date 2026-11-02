# Student Management System

A full-stack web application developed to manage student records using React, FastAPI, and MySQL. It provides a user-friendly interface for adding, viewing, updating, deleting, and searching student information.

## Features

- Add new student records
- View all student records
- Update existing student details
- Delete student records
- Search student records
- Input validation
- Success and error messages
- Department-based student IDs (CSE, ECE, EEE, IT)
- REST API integration between frontend and backend
- MySQL database connectivity

## Technology Stack

### Frontend
- React
- Vite
- JavaScript
- CSS

### Backend
- Python
- FastAPI
- Pydantic
- Uvicorn

### Database
- MySQL
- MySQL Connector for Python

### Development Tools
- Visual Studio Code
- Git
- GitHub
- Postman / FastAPI Swagger UI

## Project Structure

```text
StudentManagementSystem/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── add_student.py
│   ├── read_students.py
│   ├── update_student.py
│   ├── delete_student.py
│   ├── test_connection.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## Application Setup

Follow these steps to run the project on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/kavulurisaijeevani/StudentManagementSystem.git
cd StudentManagementSystem
```

### 2. Set Up the MySQL Database

Make sure MySQL Server is installed and running.

Open MySQL and create the database:

```sql
CREATE DATABASE student_management;
```

The application requires the following database tables:

- `students` – stores student records.
- `department_sequences` – maintains department-wise student ID sequences.

Create the tables using the schema configured for this project.

### 3. Set Up the Backend

Open a terminal and navigate to the backend folder:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\Activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a file named `.env` inside the `backend` folder.

Use `.env.example` as a reference and provide your own MySQL credentials:

```env
DB_HOST=localhost
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_NAME=student_management
```

**Important:** Never upload your actual `.env` file or database password to GitHub.

### 5. Run the Backend Server

From the backend folder, execute:

```bash
uvicorn main:app --reload
```

The FastAPI backend will run at:

http://127.0.0.1:8000

To access the interactive API documentation:

http://127.0.0.1:8000/docs

### 6. Set Up the Frontend

Open a second terminal and navigate to the frontend folder:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

Open the local URL displayed in your terminal. It is normally:

http://localhost:5173

## How the Application Works

1. The user interacts with the React frontend.
2. React sends HTTP requests to the FastAPI backend.
3. FastAPI processes the requests and communicates with MySQL.
4. MySQL stores and retrieves student records.
5. The backend returns responses to the frontend.
6. React displays the updated information to the user.

## Security

- Database credentials are stored in environment variables.
- The actual `.env` file is excluded using `.gitignore`.
- Database access uses a separate application user.
- Private credentials should never be committed to GitHub.

## Project Status

**Current status:** Developed and tested locally.

The application currently supports student record management through the React frontend, FastAPI backend, and MySQL database.

Cloud deployment and online database integration are planned as future improvements.

## Future Enhancements

- Deploy the frontend and backend online.
- Integrate a cloud-hosted MySQL database.
- Implement user authentication and authorization.
- Add student profile management.
- Improve application security and performance.

## Author

**Sai Jeevani**

GitHub: https://github.com/kavulurisaijeevani

LinkedIn: https://www.linkedin.com/in/sai-jeevani-kavuluri/