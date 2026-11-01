
from database import get_connection

connection = get_connection()
cursor = None

try:
    cursor = connection.cursor()

    # Number of students to add
    number_of_students = int(input("How many students do you want to add? "))

    students = []

    for i in range(number_of_students):
        print(f"\nEnter details for Student {i + 1}")

        name = input("Enter name: ")
        email = input("Enter email: ")
        department = input("Enter department: ")

        students.append((name, email, department))

    # Insert multiple rows and columns
    query = """
    INSERT INTO students (name, email, department)
    VALUES (%s, %s, %s)
    """

    cursor.executemany(query, students)
    connection.commit()

    print(f"\n{cursor.rowcount} students added successfully!")

except Exception as error:
    connection.rollback()
    print("Error:", error)

finally:
    if cursor:
        cursor.close()

    connection.close()
