import streamlit as st

import db
import services
import ui

LEVELS = ["UG", "PG", "PhD", "Certificate"]


def _require_admin():
    user = st.session_state.get("user")
    if not user or user["role"] != "admin":
        ui.notice("bad", "This page is for admins.")
        st.stop()
    return user


def _programs():
    return db.query(
        "SELECT p.id, p.name, p.level, p.semesters, s.name AS school "
        "FROM programs p JOIN schools s ON s.id = p.school_id "
        "ORDER BY s.id, FIELD(p.level, 'UG', 'PG', 'PhD', 'Certificate'), p.name"
    )


def _program_select(label, programs, key, allow_all=False):
    names = {p["id"]: p["name"] for p in programs}
    options = [None, *names] if allow_all else list(names)
    return st.selectbox(
        label, options, key=key,
        format_func=lambda i: "All programmes" if i is None else names[i],
    )


@st.dialog("Please confirm")
def _confirm(kind, ident, message, success):
    st.markdown(message)
    yes, no = st.columns(2)
    if yes.button("Confirm", type="primary", key="confirm_yes"):
        try:
            if kind == "user":
                services.delete_user(ident, st.session_state["user"]["id"])
            elif kind == "subject":
                services.delete_subject(ident)
            elif kind == "promote":
                moved = services.promote(*ident)
                success = f"{moved} student{'s' if moved != 1 else ''} moved to semester {ident[1] + 1}."
        except ValueError as error:
            ui.notice("bad", str(error))
            return
        st.session_state["flash"] = success
        st.rerun()
    if no.button("Cancel", key="confirm_no"):
        st.rerun()


def dashboard_page():
    _require_admin()
    ui.page_header("Dashboard", "Who and what is in the portal right now.")
    ui.flash()

    counts = db.query(
        "SELECT (SELECT COUNT(*) FROM students) AS students, (SELECT COUNT(*) FROM teachers) AS teachers, "
        "(SELECT COUNT(*) FROM programs) AS programs, (SELECT COUNT(*) FROM subjects) AS subjects"
    )[0]
    ui.stats([
        (counts["students"], "Students"), (counts["teachers"], "Teachers"),
        (counts["programs"], "Programmes"), (counts["subjects"], "Subjects"),
    ])

    left, right = st.columns(2, gap="large")
    with left:
        ui.section("Students by school")
        rows = db.query(
            "SELECT s.name AS label, COUNT(st.id) AS n FROM schools s "
            "JOIN programs p ON p.school_id = s.id JOIN students st ON st.program_id = p.id "
            "GROUP BY s.id ORDER BY n DESC LIMIT 8"
        )
        if rows:
            ui.bars([(r["label"], r["n"]) for r in rows], wide=True)
        else:
            ui.empty("No students yet", "Add some on the Students page.")
    with right:
        ui.section("Students by semester")
        rows = db.query("SELECT semester, COUNT(*) AS n FROM students GROUP BY semester ORDER BY semester")
        if rows:
            ui.bars([(f"Semester {r['semester']}", r["n"]) for r in rows])
        else:
            ui.empty("No students yet", "")


def students_page():
    _require_admin()
    ui.page_header("Students", "Add students, move a batch up a semester, remove them, or reset a password.")
    ui.flash()

    programs = _programs()
    names = {p["id"]: p["name"] for p in programs}
    by_id = {p["id"]: p for p in programs}
    all_tab, add_tab, promote_tab, manage_tab = st.tabs(
        ["All students", "Add student", "Move up a semester", "Remove or reset password"]
    )

    with all_tab:
        c1, c2 = st.columns([3, 1])
        with c1:
            program_filter = _program_select("Programme", programs, "stu_filter_program", allow_all=True)
        with c2:
            semester_filter = st.selectbox(
                "Semester", [None, *range(1, 13)], key="stu_filter_sem",
                format_func=lambda s: "All" if s is None else f"Semester {s}",
            )
        sql = (
            "SELECT st.prn, st.full_name, p.name AS program, st.semester, u.last_login "
            "FROM students st JOIN programs p ON p.id = st.program_id JOIN users u ON u.id = st.user_id"
        )
        clauses, params = [], []
        if program_filter:
            clauses.append("st.program_id = %s")
            params.append(program_filter)
        if semester_filter:
            clauses.append("st.semester = %s")
            params.append(semester_filter)
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        rows = db.query(sql + " ORDER BY p.name, st.semester, st.prn LIMIT 500", tuple(params))
        if rows:
            for r in rows:
                r["last_login"] = ui.when(r["last_login"])
            ui.table(
                [("prn", "PRN", "mono"), ("full_name", "Name", "strong"), ("program", "Programme", ""),
                 ("semester", "Semester", "num"), ("last_login", "Last sign in", "")],
                rows,
            )
        else:
            ui.empty("No students here yet", "Add one on the next tab.")

    with add_tab:
        with st.form("add_student"):
            program_id = _program_select("Programme", programs, "add_stu_program")
            semester = st.number_input("Semester", min_value=1, max_value=12, step=1, value=1)
            prn = st.text_input("PRN", help="Their university PRN. It becomes their username.")
            full_name = st.text_input("Full name")
            submitted = st.form_submit_button("Add student", type="primary", icon=":material/person_add:")
        if submitted:
            try:
                result = services.create_student(prn, full_name, program_id, int(semester))
            except ValueError as error:
                ui.notice("bad", str(error))
            else:
                ui.notice("good", f"{full_name.strip()} was added to {names[program_id]}, semester {int(semester)}.")
                ui.credentials(result["username"], result["password"], full_name.strip())

    with promote_tab:
        st.caption("Moves every student of a programme from one semester to the next. Marks they already have stay on record.")
        program_id = _program_select("Programme", programs, "promote_program")
        last = by_id[program_id]["semesters"]
        if last < 2:
            ui.empty("One semester only", "This programme has nothing to move up to.")
        else:
            semester = st.selectbox("From semester", list(range(1, last)), key="promote_sem", format_func=lambda s: f"Semester {s}")
            count = db.query(
                "SELECT COUNT(*) AS n FROM students WHERE program_id = %s AND semester = %s", (program_id, semester)
            )[0]["n"]
            st.caption(f"{count} student{'s' if count != 1 else ''} in semester {semester}.")
            if st.button("Move up", type="primary", key="promote_go", disabled=count == 0, icon=":material/arrow_upward:"):
                _confirm(
                    "promote", (program_id, semester),
                    f"Move **{count}** student{'s' if count != 1 else ''} of **{names[program_id]}** from semester {semester} to semester {semester + 1}?",
                    "",
                )

    with manage_tab:
        program_id = _program_select("Programme", programs, "manage_stu_program")
        students = db.query(
            "SELECT st.user_id, st.prn, st.full_name, st.semester, u.username "
            "FROM students st JOIN users u ON u.id = st.user_id WHERE st.program_id = %s ORDER BY st.semester, st.prn",
            (program_id,),
        )
        if not students:
            ui.empty("No students in this programme", "")
        else:
            by_user = {s["user_id"]: s for s in students}
            user_id = st.selectbox(
                "Student", list(by_user), key="manage_stu_pick",
                format_func=lambda i: f"{by_user[i]['prn']}, {by_user[i]['full_name']} (semester {by_user[i]['semester']})",
            )
            reset, remove, _ = st.columns([1.2, 1.2, 3])
            if reset.button("Reset password", key="reset_stu", icon=":material/key:"):
                ui.credentials(by_user[user_id]["username"], services.reset_password(user_id), by_user[user_id]["full_name"])
            if remove.button("Remove student", type="primary", key="remove_stu", icon=":material/person_remove:"):
                name = by_user[user_id]["full_name"]
                _confirm("user", user_id, f"Remove **{name}**? Their marks and attendance are deleted too. This cannot be undone.", f"{name} was removed.")


def teachers_page():
    _require_admin()
    ui.page_header("Teachers", "Add teachers, remove them, or reset a password. Assign subjects on the Courses page.")
    ui.flash()

    all_tab, add_tab, manage_tab = st.tabs(["All teachers", "Add teacher", "Remove or reset password"])

    with all_tab:
        rows = db.query(
            "SELECT t.full_name, u.username, COUNT(tc.subject_id) AS subjects, u.last_login "
            "FROM teachers t JOIN users u ON u.id = t.user_id LEFT JOIN teaching tc ON tc.teacher_id = t.id "
            "GROUP BY t.id ORDER BY t.full_name"
        )
        if rows:
            for r in rows:
                r["last_login"] = ui.when(r["last_login"])
            ui.table(
                [("full_name", "Name", "strong"), ("username", "Username", "mono"),
                 ("subjects", "Subjects taught", "num"), ("last_login", "Last sign in", "")],
                rows,
            )
        else:
            ui.empty("No teachers yet", "Add one on the next tab.")

    with add_tab:
        with st.form("add_teacher"):
            full_name = st.text_input("Full name")
            username = st.text_input("Username", help="Lowercase letters, numbers, dots or underscores. Example: anita.rao")
            submitted = st.form_submit_button("Add teacher", type="primary", icon=":material/person_add:")
        if submitted:
            try:
                result = services.create_teacher(username, full_name)
            except ValueError as error:
                ui.notice("bad", str(error))
            else:
                ui.notice("good", f"{full_name.strip()} was added. Assign their subjects on the Courses page.")
                ui.credentials(result["username"], result["password"], full_name.strip())

    with manage_tab:
        teachers = db.query(
            "SELECT t.user_id, t.full_name, u.username FROM teachers t JOIN users u ON u.id = t.user_id ORDER BY t.full_name"
        )
        if not teachers:
            ui.empty("No teachers to manage", "")
        else:
            by_user = {t["user_id"]: t for t in teachers}
            user_id = st.selectbox(
                "Teacher", list(by_user), key="manage_teacher_pick",
                format_func=lambda i: f"{by_user[i]['full_name']} ({by_user[i]['username']})",
            )
            reset, remove, _ = st.columns([1.2, 1.2, 3])
            if reset.button("Reset password", key="reset_teacher", icon=":material/key:"):
                ui.credentials(by_user[user_id]["username"], services.reset_password(user_id), by_user[user_id]["full_name"])
            if remove.button("Remove teacher", type="primary", key="remove_teacher", icon=":material/person_remove:"):
                name = by_user[user_id]["full_name"]
                _confirm("user", user_id, f"Remove **{name}**? Their subject assignments are removed too. This cannot be undone.", f"{name} was removed.")


def courses_page():
    _require_admin()
    ui.page_header("Courses", "Subjects for each programme and semester, who teaches them, and the programme list.")
    ui.flash()

    programs = _programs()
    by_id = {p["id"]: p for p in programs}
    subjects_tab, programmes_tab = st.tabs(["Subjects", "Programmes"])

    with subjects_tab:
        c1, c2 = st.columns([3, 1])
        with c1:
            program_id = _program_select("Programme", programs, "sub_program")
        with c2:
            semester = st.selectbox(
                "Semester", list(range(1, by_id[program_id]["semesters"] + 1)), key="sub_sem",
                format_func=lambda s: f"Semester {s}",
            )
        subjects = db.query(
            "SELECT sub.id, sub.code, sub.name, sub.credits, "
            "COALESCE(GROUP_CONCAT(t.full_name ORDER BY t.full_name SEPARATOR ', '), '') AS teachers "
            "FROM subjects sub LEFT JOIN teaching tc ON tc.subject_id = sub.id LEFT JOIN teachers t ON t.id = tc.teacher_id "
            "WHERE sub.program_id = %s AND sub.semester = %s GROUP BY sub.id ORDER BY sub.name",
            (program_id, semester),
        )
        if subjects:
            for s in subjects:
                s["code"] = s["code"] or "-"
                s["teachers"] = s["teachers"] or "Not assigned"
            ui.table(
                [("code", "Code", "mono"), ("name", "Subject", "strong"), ("credits", "Credits", "num"), ("teachers", "Teachers", "")],
                subjects,
            )
        else:
            ui.empty("No subjects yet", "Add the first one below.")

        add_tab, assign_tab, remove_tab = st.tabs(["Add subject", "Assign teacher", "Unassign or remove"])
        with add_tab:
            with st.form("add_subject"):
                name = st.text_input("Subject name")
                code = st.text_input("Code (optional)")
                credits = st.number_input("Credits", min_value=1, max_value=10, step=1, value=3)
                submitted = st.form_submit_button("Add subject", type="primary", icon=":material/add:")
            if submitted:
                try:
                    services.add_subject(program_id, semester, name, int(credits), code)
                except ValueError as error:
                    ui.notice("bad", str(error))
                else:
                    st.session_state["flash"] = f"{name.strip()} was added to semester {semester}."
                    st.rerun()
        with assign_tab:
            teachers = db.query("SELECT id, full_name FROM teachers ORDER BY full_name")
            if not subjects or not teachers:
                ui.empty("Nothing to assign yet", "You need at least one subject here and one teacher.")
            else:
                sub_names = {s["id"]: s["name"] for s in subjects}
                teacher_names = {t["id"]: t["full_name"] for t in teachers}
                with st.form("assign_teacher"):
                    sub_id = st.selectbox("Subject", list(sub_names), format_func=sub_names.get, key="assign_sub")
                    teacher_id = st.selectbox("Teacher", list(teacher_names), format_func=teacher_names.get, key="assign_teacher")
                    submitted = st.form_submit_button("Assign", type="primary", icon=":material/link:")
                if submitted:
                    services.assign_teacher(teacher_id, sub_id)
                    st.session_state["flash"] = f"{teacher_names[teacher_id]} now teaches {sub_names[sub_id]}."
                    st.rerun()
        with remove_tab:
            if not subjects:
                ui.empty("Nothing to remove", "")
            else:
                sub_names = {s["id"]: s["name"] for s in subjects}
                sub_id = st.selectbox("Subject", list(sub_names), format_func=sub_names.get, key="remove_sub")
                assigned = db.query(
                    "SELECT t.id, t.full_name FROM teaching tc JOIN teachers t ON t.id = tc.teacher_id "
                    "WHERE tc.subject_id = %s ORDER BY t.full_name",
                    (sub_id,),
                )
                unassign, remove, _ = st.columns([1.4, 1.4, 3])
                if assigned:
                    teacher_id = st.selectbox(
                        "Assigned teacher", [a["id"] for a in assigned], key="unassign_teacher",
                        format_func={a["id"]: a["full_name"] for a in assigned}.get,
                    )
                    if unassign.button("Unassign teacher", key="unassign_go", icon=":material/link_off:"):
                        services.unassign_teacher(teacher_id, sub_id)
                        st.session_state["flash"] = "Teacher unassigned."
                        st.rerun()
                if remove.button("Remove subject", type="primary", key="remove_subject_go", icon=":material/delete:"):
                    _confirm(
                        "subject", sub_id,
                        f"Remove **{sub_names[sub_id]}**? All marks and attendance recorded for it are deleted too. This cannot be undone.",
                        f"{sub_names[sub_id]} was removed.",
                    )

    with programmes_tab:
        schools = db.query("SELECT id, name FROM schools ORDER BY id")
        school_names = {s["id"]: s["name"] for s in schools}
        school_filter = st.selectbox(
            "School", [None, *school_names], key="prog_school",
            format_func=lambda i: "All schools" if i is None else school_names[i],
        )
        shown = [p for p in programs if school_filter is None or p["school"] == school_names[school_filter]]
        ui.table(
            [("name", "Programme", "strong"), ("level", "Level", ""), ("semesters", "Semesters", "num"), ("school", "School", "")],
            shown,
        )

        add_tab, edit_tab = st.tabs(["Add programme", "Change number of semesters"])
        with add_tab:
            with st.form("add_programme"):
                school_id = st.selectbox("School", list(school_names), format_func=school_names.get, key="add_prog_school")
                level = st.selectbox("Level", LEVELS, key="add_prog_level")
                name = st.text_input("Programme name")
                semesters = st.number_input("Semesters", min_value=1, max_value=12, step=1, value=8)
                submitted = st.form_submit_button("Add programme", type="primary", icon=":material/add:")
            if submitted:
                try:
                    services.add_program(school_id, level, name, int(semesters))
                except ValueError as error:
                    ui.notice("bad", str(error))
                else:
                    st.session_state["flash"] = f"{name.strip()} was added."
                    st.rerun()
        with edit_tab:
            with st.form("edit_semesters"):
                program_id = _program_select("Programme", programs, "edit_prog")
                semesters = st.number_input("Semesters", min_value=1, max_value=12, step=1, value=8, key="edit_prog_sem")
                submitted = st.form_submit_button("Save", type="primary", icon=":material/save:")
            if submitted:
                try:
                    services.set_semesters(program_id, int(semesters))
                except ValueError as error:
                    ui.notice("bad", str(error))
                else:
                    st.session_state["flash"] = f"{by_id[program_id]['name']} now has {int(semesters)} semesters."
                    st.rerun()
