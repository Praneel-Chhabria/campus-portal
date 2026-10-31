"""MIT-WPU schools and programmes, from mitwpu.edu.in/programmes (checked October 2026).

Each programme is (school, level, name, years). Semesters are years x 2, and a half year
(certificates) counts as one semester. The grouping into schools is a best effort mapping,
so adjust it here if your department lists a programme elsewhere.
"""

ENG = "WPU School of Engineering and Technology"
CSE = "WPU School of Computer Science & Engineering"
ARCH = "Hafeez Contractor School of Architecture"
CON = "Hastak School of Construction Engineering and Management"
LEAD = "Ram Charan School of Leadership"
BUS = "WPU School of Business"
EC = "WPU School of Economics and Commerce"
GOV = "MIT School of Government"
HEALTH = "WPU School of Health Sciences & Technology"
SCI = "WPU School of Science & Environmental Studies"
DES = "WPU School of Design"
LA = "WPU School of Liberal Arts"
LAW = "WPU School of Law"
CONS = "WPU School of Consciousness"
PHOTO = "WPU School of Photography"

SCHOOLS = [ENG, CSE, ARCH, CON, LEAD, BUS, EC, GOV, HEALTH, SCI, DES, LA, LAW, CONS, PHOTO]

UG, PG, PHD, CERT = "UG", "PG", "PhD", "Certificate"


def _many(school, level, years, names):
    return [(school, level, name, years) for name in names]


PROGRAMMES = (
    # Engineering and Technology
    _many(ENG, UG, 4, [
        "B.Tech Bioengineering", "B.Tech Chemical Engineering", "B.Tech Civil Engineering",
        "B.Tech Electrical and Computer Engineering", "B.Tech Electronics and Communication Engineering",
        "B.Tech Electronics and Communication Engineering (Artificial Intelligence and Machine Learning)",
        "B.Tech Electronics (Semiconductor & VLSI Design)", "B.Tech Materials Science and Engineering",
        "B.Tech Mechanical Engineering", "B.Tech Mechanical Engineering (Robotics and Automation)",
        "B.Tech Petroleum Engineering", "B.Tech Renewable Energy Engineering", "B.Tech in Defense Technology",
    ])
    + _many(ENG, UG, 3, ["B.Tech (2nd Year Lateral Entry) After 3 Years of Diploma in Engineering"])
    + _many(ENG, UG, 6, [
        "B.Tech. After 10th (3 years Diploma + 3 years Degree) in Electronics and Communication Engineering - Artificial Intelligence and Machine Learning",
        "B.Tech. After 10th (3 years Diploma + 3 years Degree) in Mechanical Engineering",
        "B.Tech. After 10th (3 years Diploma + 3 years Degree) in Mechanical Engineering - Robotics and Automation",
    ])
    + _many(ENG, PG, 2, [
        "M.Tech Chemical Engineering", "M.Tech Civil Engineering (Structural Engineering)",
        "M.Tech Civil Engineering (Tunnel Engineering and Underground Construction)",
        "M.Tech Electronics and Communication Engineering (VLSI and Embedded Systems)", "M.Tech e-Mobility",
        "M.Tech Environmental Engineering", "M.Tech Mechanical Engineering (Design Engineering)",
        "M.Tech Mechanical Engineering (Robotics and Automation)", "M.Tech Petroleum Engineering",
    ])
    + _many(ENG, PHD, 3, [
        "Ph.D. in Bioengineering", "Ph.D. in Chemical Engineering", "Ph.D. in Civil Engineering",
        "Ph.D. in Electronics and Communication Engineering", "Ph.D. in Mechanical Engineering",
        "Ph.D. in Petroleum Engineering", "Ph.D Programmes with ARAI",
    ])
    # Computer Science and Engineering
    + _many(CSE, UG, 4, [
        "B.Tech Computer Science and Engineering",
        "B.Tech Computer Science and Engineering (Artificial Intelligence and Data Science)",
        "B.Tech Computer Science and Engineering (Cloud Computing)",
        "B.Tech Computer Science and Engineering (Cyber Security and Forensics)",
        "B.Tech. Computer Science and Engineering (Quantum Computing)",
        "B.Sc. Computer Science (Hons)", "B.Sc. Data Science and Big Data Analytics (Hons)", "BCA (Hons)",
    ])
    + _many(CSE, UG, 6, [
        "B.Tech. After 10th (3 years Diploma + 3 years Degree) in Computer Science and Engineering - Artificial Intelligence & Data Science",
        "B.Tech. After 10th (3 years Diploma + 3 years Degree) in Computer Science and Engineering",
    ])
    + _many(CSE, PG, 2, [
        "M.Tech Computer Science and Engineering (Artificial Intelligence and Optimization Methods)",
        "M.Tech Computer Science and Engineering (Cyber Security)",
        "M.Tech Computer Science and Engineering (Data Science And Analytics)",
        "M.Tech Computer Science and Engineering (Data Centre Systems Engineering)",
        "M.Tech. Artificial Intelligence and Machine Learning", "M.Sc. Computer Science",
        "M.Sc. Data Science and Big Data Analytics", "MCA", "M.Sc. Cyber Security and Digital Forensics",
    ])
    + _many(CSE, PHD, 3, ["Ph.D. in Computer Engineering", "Ph.D. in Computer Science"])
    # Architecture and Construction
    + _many(ARCH, UG, 5, ["Bachelor of Architecture (B.Arch.)"])
    + _many(CON, UG, 4, ["B.Tech Civil Engineering (Smart Infrastructure and Construction)"])
    + _many(CON, UG, 6, ["B.Tech. After 10th (3 years Diploma + 3 years Degree) in Civil Engineering - Smart Infrastructure & Construction"])
    + _many(CON, PG, 2, ["M.Tech Civil Engineering (Construction Engineering and Management)", "MBA Construction Management"])
    # Leadership (MBA) and Business
    + _many(LEAD, PG, 2, [
        "MBA Dual", "MBA Banking and Financial Services", "MBA Business Analytics", "MBA Digital Marketing",
        "MBA Entrepreneurship and Family Business Management", "MBA Finance", "MBA Healthcare Management",
        "MBA Human Resource Management", "MBA International Business", "MBA Marketing",
        "MBA Operations and Supply Chain Management",
    ])
    + _many(LEAD, PG, 1, ["Post Graduate Diploma in Management"])
    + _many(LEAD, UG, 5, ["Integrated Business Management (BBA+MBA)"])
    + _many(LEAD, CERT, 0.5, ["Executive Certificate in AI for Leadership"])
    + _many(LEAD, PHD, 3, ["Ph.D. in Management"])
    + _many(BUS, UG, 4, [
        "BBA (Hons)", "BBA Banking Finance and Insurance (Hons)", "BBA Business Analytics (Hons)",
        "BBA Digital Marketing (Hons)", "BBA Entrepreneurship and Family Business Management (Hons)",
        "BBA Global Business Management (Hons)", "BBA Events, Entertainment and Media Management (Hons)",
        "BBA Hospitality and Hotel Administration (Hons)", "BBA International Business (Hons)",
        "BBA Sales and Marketing (Hons)", "BBA Financial Technology and Digital Banking (Hons)",
        "BBA Artificial Intelligence & Business Intelligence (Hons)",
    ])
    + _many(BUS, PHD, 3, ["Ph.D. in Business Administration"])
    # Economics, Commerce and Government
    + _many(EC, UG, 4, [
        "B.Com (Hons.)", "B.Com Advanced Accounting and Auditing (Hons.)", "B.Com Financial Analysis (Hons.)",
        "B.Com Fintech (Hons.)", "B.Com International Accounting and Finance (Hons.)", "B.Sc. Economics (Hons.)",
    ])
    + _many(EC, PG, 2, ["M.Com.", "M.Sc. Economics"])
    + _many(EC, PHD, 3, ["Ph.D. in Commerce", "Ph.D. in Economics"])
    + _many(GOV, PG, 2, ["MA in Political Leadership and Government"])
    + _many(GOV, PHD, 3, ["Ph.D. in Governance and Public Policy"])
    # Health Sciences and Technology
    + _many(HEALTH, UG, 4, ["B.Pharm"])
    + _many(HEALTH, UG, 3, ["B.Pharm (2nd Year Lateral Entry) After 2 Years Pharmacy Diploma"])
    + _many(HEALTH, UG, 6, ["Pharm.D (Doctor of Pharmacy)"])
    + _many(HEALTH, PG, 3, ["Pharm.D (Post Baccalaureate)"])
    + _many(HEALTH, PG, 2, [
        "M.Pharm Pharmaceutical Chemistry", "M.Pharm Pharmaceutics", "M.Pharm Pharmaceutical Quality Assurance",
        "M.Pharm Pharmacology", "M.Pharm Pharmaceutical Analysis", "M.Tech Medical Devices",
        "M.Sc. Yoga and Meditation", "Master of Public Health", "M.Sc. Clinical Psychology",
    ])
    + _many(HEALTH, PHD, 3, ["Ph.D. in Pharmaceutical Sciences"])
    # Science and Environmental Studies
    + _many(SCI, UG, 4, [
        "B.Sc. (Hons.) Applied Statistics and Data Analytics", "B.Sc. Chemistry (Hons)", "B.Sc. Physics (Hons)",
    ])
    + _many(SCI, UG, 5, ["B.Sc. Integrated M.Sc. Biotechnology"])
    + _many(SCI, PG, 2, [
        "M.Sc. Biotechnology", "M.Sc. Chemistry (Industrial Polymer Chemistry)", "M.Sc. Chemistry (Organic Chemistry)",
        "M.Sc. Environment Science", "M.Sc. Mathematics and Data Science", "M.Sc. Applied Statistics",
        "M.Sc. Microbiology", "M.Sc. Physics", "M.Sc. Genomics and Precision Medicine",
    ])
    + _many(SCI, PHD, 3, [
        "Ph.D. in Biochemistry", "Ph.D. in Biotechnology", "Ph.D. in Chemistry", "Ph.D. in Environmental Science",
        "Ph.D. in Mathematics", "Ph.D. in Microbiology", "Ph.D. in Physics", "Ph.D. in Statistics",
    ])
    # Design and Visual Arts
    + _many(DES, UG, 4, [
        "B.Des. Product Design", "B.Des. User Experience Design", "B.Des. Visual Communication Design",
        "B.Des. Fashion and Apparel Design", "B.Des. Animation and VFX Design", "B.Des. Interior and Space Design",
        "Bachelor of Visual Arts",
    ])
    + _many(DES, PG, 2, ["M.Des. User Experience Design", "M.Des. Strategic Product Design", "Master of Visual Arts"])
    + _many(DES, PHD, 3, ["Ph.D. in Visual Arts"])
    # Liberal Arts, Film, Media, Education, Peace
    + _many(LA, UG, 4, [
        "BA / B.Sc. Liberal Arts (Honours / Honours with Research)", "BA Filmmaking (Hons)",
        "BA Media and Communication (Hons)",
    ])
    + _many(LA, UG, 2, ["Bachelor of Education (B.Ed.)"])
    + _many(LA, PG, 2, [
        "MA Psychology", "MA Media and Communication", "MA in Peace and Conflict Management", "Master of Education (M.Ed.)",
    ])
    + _many(LA, PHD, 3, [
        "Ph.D. in Education", "Ph.D. in English", "Ph.D. in Peace Studies", "Ph.D. in Psychology", "Ph.D. in Sociology",
    ])
    # Law, Consciousness, Photography
    + _many(LAW, UG, 5, ["BA LL.B. (Hons)", "BBA LL.B. (Hons)"])
    + _many(LAW, UG, 3, ["LL.B."])
    + _many(LAW, PG, 1, ["LL.M."])
    + _many(LAW, PHD, 3, ["Ph.D. in Law"])
    + _many(CONS, PHD, 3, ["Ph.D. in Consciousness Studies"])
    + _many(PHOTO, UG, 4, ["BA Photography and Visual communication (Hons)"])
    + _many(PHOTO, PG, 2, ["MA Photography"])
    + _many(PHOTO, CERT, 0.5, ["Advance Certification in Photography"])
)


def semesters(years):
    return max(1, round(years * 2))
