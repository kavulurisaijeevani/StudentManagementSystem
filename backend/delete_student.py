
from database import get_connection

student_id = int(input("Enter student ID to delete: "))

connection = get_connection()
cursor = None

try:
    cursor = connection.cursor()

    query = "DELETE FROM students WHERE id = %s"

    cursor.execute(query, (student_id,))
    connection.commit()

    if cursor.rowcount > 0:
        print("Student deleted successfully!")
    else:
        print("No student found with that ID.")

except Exception as error:
    connection.rollback()
    print("Error:", error)

finally:
    if cursor:
        cursor.close()
    connection.close()
