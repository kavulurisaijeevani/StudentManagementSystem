
from database import get_connection

# Step 1: Connect to MySQL
connection = get_connection()

try:
    # Step 2: Create a cursor
    cursor = connection.cursor()

    # Step 3: Write SQL query
    query = "SELECT * FROM students"

    # Step 4: Execute the query
    cursor.execute(query)

    # Step 5: Retrieve all records
    students = cursor.fetchall()

    # Step 6: Display the records
    for student in students:
        print("Student ID:", student[0])
        print("Name:", student[1])
        print("Email:", student[2])
        print("Department:", student[3])
        print("----------------------")

finally:
    cursor.close()
    connection.close()
