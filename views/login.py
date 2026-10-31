import streamlit as st

import auth
import ui


def _login_form(key, roles):
    with st.form(key):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", type="primary")
    if not submitted:
        return
    if not username or not password:
        ui.notice("bad", "Enter your username and password.")
        return
    user, error = auth.authenticate(username, password, roles)
    if error:
        ui.notice("bad", error)
        return
    st.session_state["user"] = auth.build_session(user)
    st.rerun()


def login_page():
    left, right = st.columns([1.15, 1], gap="large")
    with left:
        ui.render(
            '<div class="hero"><div class="hero-title">Campus Portal</div>'
            '<div class="hero-sub">Marks, attendance and SGPA for every MIT-WPU programme.</div>'
            '<div class="hero-roles">'
            '<div class="hero-role"><b>Students</b>See your marks, attendance and SGPA for each semester.</div>'
            '<div class="hero-role"><b>Teachers</b>Keep marks and attendance current for the subjects you teach.</div>'
            '<div class="hero-role"><b>Admins</b>Manage students, teachers, programmes and subjects.</div>'
            "</div></div>"
        )
    with right:
        ui.render('<div class="signin-title">Sign in</div>')
        student_tab, staff_tab = st.tabs(["Student", "Teacher or admin"])
        with student_tab:
            st.caption("Your username is your PRN.")
            _login_form("student_login", ("student",))
        with staff_tab:
            st.caption("Teachers and admins sign in here.")
            _login_form("staff_login", ("teacher", "admin"))
