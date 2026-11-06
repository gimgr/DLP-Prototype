import sqlite3
import bcrypt


# -----------------
# Database creation
# -----------------
DB_NAME = "users.db"

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# -------------
# User creation
# -------------
def create_user(username, password, role):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    try:
        cursor.execute(
            """
            INSERT INTO users(username, password, role)
            VALUES (?, ?, ?)
            """,
            (username, hashed_password, role)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# -------------------
# Verifies user creds
# -------------------
def verify_user(username, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT password, role
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    if result is None:
        return None

    stored_password, role = result

    if bcrypt.checkpw(
        password.encode(),
        stored_password.encode()
    ):
        return role

    return None


#---------------------------------------------
# Creates default admin
# userame = admin       password = password123
#---------------------------------------------
def create_default_admin():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if the admin account already exists
    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        ("admin",)
    )

    if cursor.fetchone() is None:
        hashed_password = bcrypt.hashpw(
            "password123".encode(),
            bcrypt.gensalt()
        ).decode()

        cursor.execute(
            """
            INSERT INTO users(username, password, role)
            VALUES (?, ?, ?)
            """,
            ("admin", hashed_password, "Administrator")
        )

        conn.commit()

    conn.close()


# ----------------------------------
# Displays all users and their roles
# ----------------------------------
def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, role
        FROM users
        ORDER BY username
    """)

    users = cursor.fetchall()
    conn.close()

    return users


# -----------------
# Updates user role
# -----------------
def update_user_role(user_id, new_role):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET role = ?
        WHERE id = ?
    """, (new_role, user_id))

    conn.commit()
    conn.close()


#---------------------
# deletes user account
#---------------------
def delete_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


create_database()
create_default_admin()