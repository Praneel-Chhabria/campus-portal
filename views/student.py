import streamlit as st

import db
import ui


def _subject_row(row):
    marks, attendance = row["marks"], row["attendance"]
    marks_band = ui.band(marks)
    if marks is None:
        marks_html = '<span class="none">Not entered</span><span class="track"></span>'
    else:
        marks_html = (
            f'<span class="num">{marks}</span>'
            f'<span class="track"><span class="fill {marks_band}" style="width:{marks}%"></span></span>'
        )
    if attendance is None:
        att_html = '<span class="track"></span><span class="pct">-</span>'
    else:
        att_band = ui.band(attendance, good=ui.LOW_ATTENDANCE, warn=60)
        att_html = (
            f'<span class="track"><span class="fill {att_band}" style="width:{attendance}%"></span></span>'
            f'<span class="pct">{attendance}%</span>'
        )
    letter = ui.grade(marks) if marks is not None else "-"
    code = f"{ui.esc(row['code'])}, " if row["code"] else ""
    return (
        f'<div class="rc-row"><div class="rc-subject">{ui.esc(row["name"])}'
        f'<div class="rc-sub-meta">{code}{row["credits"]} credits</div></div>'
        f'<div class="rc-marks">{marks_html}</div>'
        f'<div class="rc-grade {marks_band}">{letter}</div>'
        f'<div class="rc-att">{att_html}</div></div>'
    )


def results_page():
    user = st.session_state["user"]
    if user["role"] != "student" or "student_id" not in user:
        ui.notice("bad", "This page is for students.")
        st.stop()

    current = db.query("SELECT semester FROM students WHERE id = %s", (user["student_id"],))[0]["semester"]
    rows = db.query(
        "SELECT sub.semester, sub.code, sub.name, sub.credits, r.marks, r.attendance "
        "FROM subject_records r JOIN subjects sub ON sub.id = r.subject_id "
        "WHERE r.student_id = %s ORDER BY sub.semester, sub.name",
        (user["student_id"],),
    )
    semesters = sorted({r["semester"] for r in rows} | {current})
    selected = current
    if len(semesters) > 1:
        selected = st.selectbox(
            "Semester", semesters, index=semesters.index(current), key="stu_sem",
            format_func=lambda s: f"Semester {s}" + (" (current)" if s == current else ""),
        )

    shown = [r for r in rows if r["semester"] == selected]
    scored = [r for r in shown if r["marks"] is not None]
    attended = [r["attendance"] for r in shown if r["attendance"] is not None]
    average = sum(r["marks"] for r in scored) / len(scored) if scored else None
    attendance = sum(attended) / len(attended) if attended else None
    sgpa, cgpa = ui.gpa(shown), ui.gpa(rows)

    if sgpa is None:
        right = '<div class="rc-gpa"><div class="rc-gpa-n">-</div><div class="rc-avg-l">No marks yet</div></div>'
    else:
        stamp = f'<div class="stamp {ui.band(average)}">{ui.grade(average)}</div>'
        extra = f" | CGPA {cgpa:.2f}" if cgpa is not None and len(semesters) > 1 else ""
        right = (
            f'<div class="rc-gpa"><div class="rc-gpa-n">{sgpa:.2f}</div>'
            f'<div class="rc-avg-l">SGPA{extra}</div></div>{stamp}'
        )
    ui.render(
        f'<div class="rc-top"><div><div class="rc-name">{ui.esc(user["name"])}</div>'
        f'<div class="chips"><span class="chip">{ui.esc(user["program"])}</span>'
        f'<span class="chip">Semester {selected}</span><span class="chip">PRN {ui.esc(user["prn"])}</span></div></div>'
        f'<div class="rc-avg">{right}</div></div>'
    )

    if len(scored) >= 2:
        best = max(scored, key=lambda r: r["marks"])
        lowest = min(scored, key=lambda r: r["marks"])
        ui.render(
            f'<div class="rc-note">Best in {ui.esc(best["name"])} with {best["marks"]}. '
            f'Lowest in {ui.esc(lowest["name"])} with {lowest["marks"]}.</div>'
        )
    if attendance is not None and attendance < ui.LOW_ATTENDANCE:
        ui.notice("warn", f"Your average attendance is {attendance:.0f}%, below {ui.LOW_ATTENDANCE}%.")

    if not shown:
        ui.empty("No subjects yet", "Subjects for this semester appear here once an admin adds them.")
        return
    ui.render(
        '<div class="rc-table"><div class="rc-head"><div>Subject</div><div>Marks</div><div>Grade</div><div>Attendance</div></div>'
        + "".join(_subject_row(r) for r in shown)
        + "</div>"
    )
