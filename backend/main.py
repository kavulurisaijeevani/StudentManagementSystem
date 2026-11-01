
import re

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

import mysql.connector
from database import get_connection


app = FastAPI(title="Student Management API")


# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Common validation model
class StudentFields(BaseModel):

    name: str
    email: str
    department: str

    @field_validator("name", "email", "department")
    @classmethod
    def remove_extra_spaces(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty.")

        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):

        email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

        if not re.fullmatch(email_pattern, value):
            raise ValueError("Please enter a valid email address.")

        return value


# Model for normal student registration
class StudentCreate(StudentFields):
    pass


# Model for manually assigning original MySQL ID
class StudentWithID(StudentFields):
    id: int = Field(gt=0)


# FUNCTION: Generate customized department-based student ID
def generate_student_code(cursor, department):

    department_code = re.sub(
        r"\s+",
        "",
        department
    ).upper()

    # Create department sequence if it does not exist
    cursor.execute(
        """
        INSERT INTO department_sequences
            (department_code, last_number)
        VALUES (%s, 0)
        ON DUPLICATE KEY UPDATE
            department_code = department_code
        """,
        (department_code,)
    )

    # Increase sequence number safely
    cursor.execute(
        """
        UPDATE department_sequences
        SET last_number = LAST_INSERT_ID(last_number + 1)
        WHERE department_code = %s
        """,
        (department_code,)
    )

    # Retrieve the newly generated sequence number
    cursor.execute("SELECT LAST_INSERT_ID()")
    serial_number = cursor.fetchone()[0]

    return f"{department_code}{serial_number:03d}"


# HOME
@app.get("/")
def home():

    return {
        "message": "Welcome to Student Management System"
    }


# 1. GET - Retrieve all students
@app.get("/students")
def get_students():

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT id, student_code, name, email, department
        FROM students
        ORDER BY id
        """

        cursor.execute(query)
        students = cursor.fetchall()

        result = []

        for student in students:

            result.append({
                "id": student[0],
                "student_code": student[1],
                "name": student[2],
                "email": student[3],
                "department": student[4]
            })

        return result

    except mysql.connector.Error as error:

        print("Database error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve students."
        ) from error

    finally:

        if cursor:
            cursor.close()

        connection.close()


# 2. GET - Retrieve one student by original MySQL ID
@app.get("/students/{student_id}")
def get_student_by_id(student_id: int):

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT id, student_code, name, email, department
        FROM students
        WHERE id = %s
        """

        cursor.execute(query, (student_id,))
        student = cursor.fetchone()

        if student is None:

            raise HTTPException(
                status_code=404,
                detail="Student not found."
            )

        return {
            "id": student[0],
            "student_code": student[1],
            "name": student[2],
            "email": student[3],
            "department": student[4]
        }

    except HTTPException:
        raise

    except mysql.connector.Error as error:

        print("Database error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve student."
        ) from error

    finally:

        if cursor:
            cursor.close()

        connection.close()


# 3. POST - Add one student
# MySQL ID and customized student code are generated automatically
@app.post("/students", status_code=201)
def add_student(student: StudentCreate):

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        student_code = generate_student_code(
            cursor,
            student.department
        )

        query = """
        INSERT INTO students
            (student_code, name, email, department)
        VALUES (%s, %s, %s, %s)
        """

        values = (
            student_code,
            student.name,
            student.email,
            student.department
        )

        cursor.execute(query, values)

        new_student_id = cursor.lastrowid

        connection.commit()

        return {
            "message": "Student added successfully!",
            "student": {
                "id": new_student_id,
                "student_code": student_code,
                "name": student.name,
                "email": student.email,
                "department": student.department
            }
        }

    except mysql.connector.IntegrityError as error:

        connection.rollback()
        print("Database integrity error:", error)

        raise HTTPException(
            status_code=409,
            detail="This email address or student code already exists."
        ) from error

    except mysql.connector.Error as error:

        connection.rollback()
        print("Database error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to add student."
        ) from error

    finally:

        if cursor:
            cursor.close()

        connection.close()


# 4. POST - Add multiple students
@app.post("/students/bulk", status_code=201)
def add_multiple_students(students: list[StudentCreate]):

    if not students:

        raise HTTPException(
            status_code=400,
            detail="Student list cannot be empty."
        )

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        added_students = []

        for student in students:

            student_code = generate_student_code(
                cursor,
                student.department
            )

            query = """
            INSERT INTO students
                (student_code, name, email, department)
            VALUES (%s, %s, %s, %s)
            """

            values = (
                student_code,
                student.name,
                student.email,
                student.department
            )

            cursor.execute(query, values)

            added_students.append({
                "id": cursor.lastrowid,
                "student_code": student_code,
                "name": student.name,
                "email": student.email,
                "department": student.department
            })

        connection.commit()

        return {
            "message": "Students added successfully!",
            "total_added": len(added_students),
            "students": added_students
        }

    except mysql.connector.IntegrityError as error:

        connection.rollback()
        print("Database integrity error:", error)

        raise HTTPException(
            status_code=409,
            detail="One or more email addresses or student codes already exist."
        ) from error

    except mysql.connector.Error as error:

        connection.rollback()
        print("Database error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to add students."
        ) from error

    finally:

        if cursor:
            cursor.close()

        connection.close()


# 5. POST - Add student with manually assigned original MySQL ID
@app.post("/students/manual", status_code=201)
def add_student_with_id(student: StudentWithID):

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        student_code = generate_student_code(
            cursor,
            student.department
        )

        query = """
        INSERT INTO students
            (id, student_code, name, email, department)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            student.id,
            student_code,
            student.name,
            student.email,
            student.department
        )

        cursor.execute(query, values)

        connection.commit()

        return {
            "message": "Student added successfully with manual MySQL ID!",
            "student": {
                "id": student.id,
                "student_code": student_code,
                "name": student.name,
                "email": student.email,
                "department": student.department
            }
        }

    except mysql.connector.IntegrityError as error:

        connection.rollback()
        print("Database integrity error:", error)

        raise HTTPException(
            status_code=409,
            detail="This MySQL ID, email, or student code already exists."
        ) from error

    except mysql.connector.Error as error:

        connection.rollback()
        print("Database error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to add student."
        ) from error

    finally:

        if cursor:
            cursor.close()

        connection.close()


# 6. PUT - Update student details
# Customized student code remains unchanged
@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate):

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        # Check whether student exists
        check_query = """
        SELECT id
        FROM students
        WHERE id = %s
        """

        cursor.execute(check_query, (student_id,))
        existing_student = cursor.fetchone()

        if existing_student is None:

            raise HTTPException(
                status_code=404,
                detail="Student not found."
            )

        # Update student details without changing student_code
        query = """
        UPDATE students
        SET name = %s,
            email = %s,
            department = %s
        WHERE id = %s
        """

        values = (
            student.name,
            student.email,
            student.department,
            student_id
        )

        cursor.execute(query, values)

        connection.commit()

        return {
            "message": "Student updated successfully!",
            "student_id": student_id
        }

    except HTTPException:

        connection.rollback()
        raise

    except mysql.connector.IntegrityError as error:

        connection.rollback()
        print("Database integrity error:", error)

        raise HTTPException(
            status_code=409,
            detail="This email address may already belong to another student."
        ) from error

    except mysql.connector.Error as error:

        connection.rollback()
        print("Database error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to update student."
        ) from error

    finally:

        if cursor:
            cursor.close()

        connection.close()


# 7. DELETE - Delete student by original MySQL ID
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        DELETE FROM students
        WHERE id = %s
        """

        cursor.execute(query, (student_id,))

        if cursor.rowcount == 0:

            raise HTTPException(
                status_code=404,
                detail="Student not found."
            )

        connection.commit()

        return {
            "message": "Student deleted successfully!",
            "student_id": student_id
        }

    except HTTPException:

        connection.rollback()
        raise

    except mysql.connector.Error as error:

        connection.rollback()
        print("Database error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to delete student."
        ) from error

    finally:

        if cursor:
            cursor.close()

        connection.close()
