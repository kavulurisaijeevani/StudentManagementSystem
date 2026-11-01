
from database import get_connection

connection = get_connection()
cursor = None

try:
    cursor = connection.cursor()

    # Select which student to update
    student_id = int(input("Enter student ID: "))

    print("\nWhich column do you want to update?")
    print("1. Name")
    print("2. Email")
    print("3. Department")
    print("4. Multiple columns")

    choice = input("Enter your choice: ")

    if choice == "1":
        new_name = input("Enter new name: ")

        query = """
        UPDATE students
        SET name = %s
        WHERE id = %s
        """
        values = (new_name, student_id)

    elif choice == "2":
        new_email = input("Enter new email: ")

        query = """
        UPDATE students
        SET email = %s
        WHERE id = %s
        """
        values = (new_email, student_id)

    elif choice == "3":
        new_department = input("Enter new department: ")

        query = """
        UPDATE students
        SET department = %s
        WHERE id = %s
        """
        values = (new_department, student_id)

    elif choice == "4":
        new_name = input("Enter new name: ")
        new_email = input("Enter new email: ")
        new_department = input("Enter new department: ")

        query = """
        UPDATE students
        SET name = %s,
            email = %s,
            department = %s
        WHERE id = %s
        """
        values = (new_name, new_email, new_department, student_id)

    else:
        print("Invalid choice!")
        raise SystemExit

    cursor.execute(query, values)
    connection.commit()

    if cursor.rowcount > 0:
        print("Student details updated successfully!")
    else:
        print("Student not found or no changes made.")

except Exception as error:
    connection.rollback()
    print("Error:", error)

finally:
    if cursor:
        cursor.close()
    connection.close()
