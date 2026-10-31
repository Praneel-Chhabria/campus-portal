import streamlit as st

import auth
import ui


def account_page():
    user = st.session_state["user"]
    forced = user["must_change"]

    ui.page_header(
        "Choose a new password" if forced else "Account",
        f"Signed in as {user['username']}",
    )
    if forced:
        ui.notice("info", "An administrator set your current password. Choose your own to continue.")

    _, centre, _ = st.columns([0.2, 1, 0.2]) if forced else (None, st.container(), None)
    with centre:
        with st.form("change_password", clear_on_submit=True):
            current = None if forced else st.text_input("Current password", type="password")
            new = st.text_input("New password", type="password", help="8 or more characters, with letters and numbers.")
            again = st.text_input("Repeat new password", type="password")
            submitted = st.form_submit_button("Save password", type="primary")

        if not submitted:
            return
        if not forced and not auth.check_current_password(user["id"], current):
            ui.notice("bad", "Current password is incorrect.")
            return
        problem = auth.password_problem(new)
        if problem:
            ui.notice("bad", problem)
            return
        if new != again:
            ui.notice("bad", "The two new passwords do not match.")
            return

        auth.change_password(user["id"], new)
        st.session_state["user"]["must_change"] = False
        if forced:
            st.rerun()
        ui.notice("good", "Password updated.")
