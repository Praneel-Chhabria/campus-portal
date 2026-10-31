import streamlit as st

import db
import ui

WIDTHS = [1.5, 3, 1.4, 1.4]


def class_records_page():
    user = st.session_state["user"]
    if user["role"] != "teacher" or "teacher_id" not in user:
        ui.notice("bad", "This page is for teachers.")
        st.stop()

    subjects = db.query(
        "SELECT sub.id, sub.name, sub.semester, p.name AS program "
        "FROM teaching t JOIN subjects sub ON sub.id = t.subject_id JOIN programs p ON p.id = sub.program_id "
        "WHERE t.teacher_id = %s ORDER BY p.name, sub.semester, sub.name",
        (user["teacher_id"],),
    )
    if not subjects:
        ui.page_header("Class records", f"{user['name']}")
        ui.empty("No subjects assigned yet", "An admin can assign subjects to you from the Courses page.")
        return

    by_id = {s["id"]: s for s in subjects}
    subject_id = st.selectbox(
        "Subject", list(by_id), key="teach_subject",
        format_func=lambda i: f"{by_id[i]['name']} (semester {by_id[i]['semester']}, {by_id[i]['program']})",
    )
    subject = by_id[subject_id]
    ui.page_header(subject["name"], f"{subject['program']}, semester {subject['semester']}")
    ui.flash()

    rows = db.query(
        "SELECT st.id, st.prn, st.full_name, r.marks, r.attendance "
        "FROM subject_records r JOIN students st ON st.id = r.student_id "
        "WHERE r.subject_id = %s ORDER BY st.prn",
        (subject_id,),
    )
    if not rows:
        ui.empty("No students yet", "Students appear here when an admin adds them to this programme and semester.")
        return

    marks = [r["marks"] for r in rows if r["marks"] is not None]
    low = sum(1 for r in rows if r["attendance"] is not None and r["attendance"] < ui.LOW_ATTENDANCE)
    ui.stats([
        (len(rows), "Students"),
        (f"{sum(marks) / len(marks):.1f}" if marks else "-", "Class average"),
        (low, f"Below {ui.LOW_ATTENDANCE}% attendance"),
    ])

    with st.form(f"records_{subject_id}"):
        head = st.columns(WIDTHS)
        for cell, text in zip(head, ["PRN", "Student", "Marks", "Attendance %"]):
            cell.markdown(f'<div class="col-head">{text}</div>', unsafe_allow_html=True)

        entered = {}
        for r in rows:
            cells = st.columns(WIDTHS, vertical_alignment="center")
            cells[0].markdown(f'<span class="cell-muted">{ui.esc(r["prn"])}</span>', unsafe_allow_html=True)
            cells[1].markdown(f'<span class="cell-name">{ui.esc(r["full_name"])}</span>', unsafe_allow_html=True)
            new_marks = cells[2].number_input(
                f"Marks for {r['full_name']}", 0, 100, value=r["marks"], step=1,
                key=f"m_{subject_id}_{r['id']}", label_visibility="collapsed",
            )
            new_att = cells[3].number_input(
                f"Attendance for {r['full_name']}", 0, 100, value=r["attendance"], step=1,
                key=f"a_{subject_id}_{r['id']}", label_visibility="collapsed",
            )
            entered[r["id"]] = (new_marks, new_att)
        saved = st.form_submit_button("Save changes", type="primary", icon=":material/save:")

    if not saved:
        return
    changes = [
        (entered[r["id"]][0], entered[r["id"]][1], r["id"], subject_id)
        for r in rows
        if entered[r["id"]] != (r["marks"], r["attendance"])
    ]
    if not changes:
        ui.notice("info", "Nothing to save.")
        return
    with db.transaction() as cur:
        cur.executemany(
            "UPDATE subject_records SET marks = %s, attendance = %s WHERE student_id = %s AND subject_id = %s",
            changes,
        )
    plural = "s" if len(changes) != 1 else ""
    st.session_state["flash"] = f"Saved {subject['name']} records for {len(changes)} student{plural}."
    st.rerun()
