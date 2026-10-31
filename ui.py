"""Small HTML building blocks. Everything user supplied is escaped."""
import html

import streamlit as st

LOW_ATTENDANCE = 75


def esc(value):
    return html.escape("" if value is None else str(value))


def render(markup):
    # Streamlit treats blank lines and indentation in markdown as structure, so flatten the markup.
    st.markdown("".join(line.strip() for line in markup.splitlines()), unsafe_allow_html=True)


def page_header(title, subtitle=None):
    sub = f'<div class="pg-sub">{esc(subtitle)}</div>' if subtitle else ""
    render(f'<div class="pg-head"><div class="pg-title">{esc(title)}</div>{sub}</div>')


def section(title):
    render(f'<div class="sec">{esc(title)}</div>')


def notice(kind, text):
    render(f'<div class="notice {kind}" role="status">{esc(text)}</div>')


def flash():
    message = st.session_state.pop("flash", None)
    if message:
        notice("good", message)


def empty(title, hint=""):
    render(f'<div class="empty"><div class="empty-t">{esc(title)}</div><div class="empty-h">{esc(hint)}</div></div>')


def stats(items):
    cells = "".join(
        f'<div class="stat"><div class="stat-n">{esc(value)}</div><div class="stat-l">{esc(label)}</div></div>'
        for value, label in items
    )
    render(f'<div class="stats">{cells}</div>')


def when(moment):
    return moment.strftime("%d %b %Y, %H:%M") if moment else "Never"


def table(columns, rows):
    """columns: list of (key, label, css class). rows: list of dicts."""
    head = "".join(f"<th>{esc(label)}</th>" for _, label, _ in columns)
    body = "".join(
        "<tr>" + "".join(f'<td class="{cls}">{esc(row.get(key))}</td>' for key, _, cls in columns) + "</tr>"
        for row in rows
    )
    render(f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')


def bars(rows, wide=False):
    """rows: list of (label, count)."""
    top = max((count for _, count in rows), default=0) or 1
    body = "".join(
        f'<div class="bar-row"><div class="bar-label">{esc(label)}</div>'
        f'<span class="track"><span class="fill brand" style="width:{count / top * 100:.0f}%"></span></span>'
        f'<div class="bar-count">{count}</div></div>'
        for label, count in rows
    )
    render(f'<div class="bars{" wide" if wide else ""}">{body}</div>')


def credentials(username, password, who=None):
    for_whom = f" for {esc(who)}" if who else ""
    render(
        f'<div class="slip"><div class="slip-row"><span class="slip-k">Username</span><span class="slip-v">{esc(username)}</span></div>'
        f'<div class="slip-row"><span class="slip-k">Temporary password</span><span class="slip-v">{esc(password)}</span></div>'
        f'<div class="slip-note">Copy these{for_whom} now. The password is shown once, and they choose their own at first sign in.</div></div>'
    )


def sidebar_user(name, role_label):
    initial = esc((name or "?").strip()[:1].upper())
    render(
        f'<div class="me"><div class="avatar">{initial}</div>'
        f'<div><div class="me-name">{esc(name)}</div><div class="me-role">{esc(role_label)}</div></div></div>'
    )


def band(score, good=70, warn=40):
    if score is None:
        return "none"
    return "good" if score >= good else "warn" if score >= warn else "bad"


# Marks to letter grade and grade points on a common Indian 10 point scale.
# This is an assumption, so change the table below if your department grades differently.
GRADE_SCALE = [(90, "O", 10), (80, "A+", 9), (70, "A", 8), (60, "B+", 7), (50, "B", 6), (45, "C", 5), (40, "P", 4)]


def grade(score):
    for cutoff, letter, _ in GRADE_SCALE:
        if score >= cutoff:
            return letter
    return "F"


def grade_points(score):
    for cutoff, _, points in GRADE_SCALE:
        if score >= cutoff:
            return points
    return 0


def gpa(rows):
    """Credit weighted grade point average over rows that have marks. Returns None if there are none."""
    graded = [r for r in rows if r["marks"] is not None]
    credits = sum(r["credits"] for r in graded)
    if not credits:
        return None
    return sum(grade_points(r["marks"]) * r["credits"] for r in graded) / credits
