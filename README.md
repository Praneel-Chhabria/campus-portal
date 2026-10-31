# Campus Portal (MIT-WPU)

Streamlit + MySQL 8 portal for marks, attendance and SGPA across MIT-WPU programmes and semesters.

## Setup (Python 3.11 or 3.12)

1. `python3.12 -m venv .venv` then `source .venv/bin/activate`
2. `python -m pip install -r requirements.txt`
3. `cp .env.example .env`, then put your MySQL password in it. Keep `DB_NAME=mitwpu_portal`. Do not reuse the old school database name, because the tables are different.
4. `python setup_db.py` creates the tables, loads all 167 MIT-WPU programmes and creates the first admin. Add `--sample` to also load a few sample teachers, subjects and students.
5. `streamlit run app.py`

## How it works

- Students sign in with their PRN. Teachers and admins use the Teacher or admin tab.
- Admin: add and remove students and teachers, add subjects to a programme and semester, assign teachers to subjects, move a whole batch up a semester, and edit the programme list.
- Teachers see only the subjects assigned to them and edit marks and attendance for those.
- Students see each semester they have records for, with SGPA and CGPA.
- Everyone created by an admin gets a temporary password and chooses their own at first sign in.

## Things to check

- Programme names and durations come from mitwpu.edu.in. The grouping into schools is a best effort mapping, edit it in `catalog.py`.
- Grades use a common 10 point scale (O is 90 and above, then A+, A, B+, B, C, P, F). If MIT-WPU grades differently, change `GRADE_SCALE` in `ui.py`.
