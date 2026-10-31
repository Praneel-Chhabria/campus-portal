from pathlib import Path

import streamlit as st

import theme
import ui
from views import account, admin, login, student, teacher

st.set_page_config(page_title="Campus Portal", page_icon=":material/school:", layout="wide")
theme.apply()
st.logo(str(Path(__file__).parent / "assets" / "logo.svg"))

user = st.session_state.get("user")

if not user:
    theme.topbar_toggle()
    pg = st.navigation([st.Page(login.login_page, title="Sign in", url_path="login")])
elif user["must_change"]:
    theme.topbar_toggle()
    pg = st.navigation([st.Page(account.account_page, title="Choose a new password", url_path="new-password")])
else:
    account_pg = st.Page(account.account_page, title="Account", icon=":material/lock:", url_path="account")
    if user["role"] == "student":
        pages = [
            st.Page(student.results_page, title="My results", icon=":material/grade:", url_path="results", default=True),
            account_pg,
        ]
        role_label = f"Semester {user.get('semester', '')}"
    elif user["role"] == "teacher":
        pages = [
            st.Page(teacher.class_records_page, title="Class records", icon=":material/edit_note:", url_path="records", default=True),
            account_pg,
        ]
        role_label = "Teacher"
    else:
        pages = [
            st.Page(admin.dashboard_page, title="Dashboard", icon=":material/dashboard:", url_path="dashboard", default=True),
            st.Page(admin.students_page, title="Students", icon=":material/school:", url_path="students"),
            st.Page(admin.teachers_page, title="Teachers", icon=":material/badge:", url_path="teachers"),
            st.Page(admin.courses_page, title="Courses", icon=":material/menu_book:", url_path="courses"),
            account_pg,
        ]
        role_label = "Admin"
    pg = st.navigation(pages)

    with st.sidebar:
        ui.sidebar_user(user["name"], role_label)
        theme.toggle()
        if st.button("Sign out", icon=":material/logout:"):
            theme.sign_out()

pg.run()
