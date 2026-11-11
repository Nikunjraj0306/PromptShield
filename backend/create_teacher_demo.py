
import getpass

from app.database import get_connection
from app.security import hash_password


EMAIL = "teacher.demo@promptshield.local"
ROLE = "Analyst"


def main():
    print("PromptShield Teacher Demo Account Setup")
    print("---------------------------------------")

    password = getpass.getpass("Enter a strong demo password: ")
    confirm = getpass.getpass("Confirm demo password: ")

    if password != confirm:
        print("Passwords do not match.")
        return

    if len(password) < 14:
        print("Use a password with at least 14 characters.")
        return

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT user_id FROM dbo.Users WHERE email = ?",
            (EMAIL,),
        )

        if cursor.fetchone():
            print("Teacher demo account already exists.")
            print("No account changes were made.")
            return

        password_hash = hash_password(password)

        cursor.execute(
            """
            INSERT INTO dbo.Users
                (email, password_hash, role, is_active)
            VALUES (?, ?, ?, 1)
            """,
            (EMAIL, password_hash, ROLE),
        )

        connection.commit()

        print("\nTeacher demo account created successfully.")
        print(f"Email: {EMAIL}")
        print(f"Role: {ROLE}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
