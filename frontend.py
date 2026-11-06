import streamlit as st
from userdatabase import create_user
from userdatabase import verify_user
from userdatabase import (
    get_all_users,
    update_user_role,
    delete_user)
import re


# ---------------------
# Password requirements
# ---------------------
def validate_password(password):
    errors = []

    if len(password) < 12:
        errors.append("Password must be at least 8 characters long.")

    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")

    if not re.search(r"\d", password):
        errors.append("Password must contain at least one number.")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password must contain at least one special character.")

    return errors


# -------------
# Session State
# -------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "password" not in st.session_state:
    st.session_state.password = ""


# --------------
# Authentication
# --------------
def login():
    role = verify_user(
        st.session_state.username,
        st.session_state.password
    )

    if role:
        st.session_state.logged_in = True
        st.session_state.role = role

        st.rerun()

    else:
        st.error("Invalid username or password.")


def logout():
    st.session_state.logged_in = False
    st.rerun()


# --------------
# Page Functions
# --------------
def home():
    st.title("Home")
    st.header("Welcome to the rough draft frontend. Things are a little rough but this serves as a stepping point")
    st.image(
        "logo.webp",
        width=500
    )

def labels():
    st.title("Sensitivity Labels")

def roles():
    st.title("User Roles")

    # Only administrators may manage users
    if st.session_state.role != "Administrator":
        st.error("Access Denied")
        return

    users = get_all_users()

    for user in users:
        user_id, username, role = user
        col1, col2, col3, col4 = st.columns([3,2,2,1])

        with col1:
            st.write(username)

        with col2:
            new_role = st.selectbox(
                "Role",
                ["User", "Manager", "Administrator"],
                index=["User","Manager","Administrator"].index(role),
                key=f"role_{user_id}"
            )

        with col3:
            if st.button(
                "Update",
                key=f"update_{user_id}"
            ):
                update_user_role(user_id, new_role)
                st.rerun()

        with col4:
            # Prevent deleting yourself
            if username not in ("admin", st.session_state.username):
                if st.button(
                    "Delete",
                    key=f"delete_{user_id}"
                ):
                    delete_user(user_id)
                    st.rerun()

def assignments():
    st.title("Assignments")

def log():
    st.title("Activity Log")

def settings():
    st.title("Settings")




if not st.session_state.logged_in:
# -----
# Login
# -----
    option = st.radio(
        "",
        ["Login", "Create Account"]
    )

    if option == "Login":

        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")

        st.button("Login", on_click=login)

    else:
# -----------------
# New user creation
#------------------
        new_username = st.text_input("Username")

        new_password = st.text_input(
            "Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        role = "User"

        if st.button("Create Account"):

            if new_password != confirm:
                st.error("Passwords do not match.")

            else:
                password_errors = validate_password(new_password)

                if password_errors:
                    for error in password_errors:
                        st.error(error)

                elif create_user(new_username, new_password, role):
                    st.success("Account created!")

                else:
                    st.error("Username already exists.")

else:
# -------------
# Sidebar pages
# -------------
    st.sidebar.title("Navigation")

    page = st.sidebar.radio(
        "Go to",
        [
            "Home",
            "Sensitivity Labels",
            "User Roles",
            "Assignment",
            "Activity Logs",
            "Settings",
        ],
    )

    st.sidebar.button("Log Out", on_click=logout)


# ----------------
# Function calling
# ----------------
    if page == "Home":
        home()

    elif page == "Sensitivity Labels":
        labels()

    elif page == "User Roles":
        roles()

    elif page == "Assignment":
        assignments()

    elif page == "Activity Logs":
        log()

    elif page == "Settings":
        settings()