"""Light and dark themes. Colours live in CSS variables, so every page follows the toggle."""
from string import Template

import streamlit as st

LIGHT = dict(
    scheme="light", bg="#F4F6FB", surface="#FFFFFF", surface2="#EBEFF7", ink="#0F1B36",
    muted="#5A6785", line="#D9E0EE", primary="#14284B", on_primary="#FFFFFF",
    accent="#F5D547", accent_ink="#3A2F00", ring="#3B62D9",
    good="#1B8A5A", warn="#A35C00", bad="#C93C37",
    good_bg="#E3F4EB", warn_bg="#FFF1D6", bad_bg="#FCE6E5", info_bg="#E6ECFA",
    panel="#14284B", panel_ink="#F2F5FC", panel_line="rgba(255,255,255,.08)",
    shadow="0 1px 2px rgba(15,27,54,.05), 0 10px 28px rgba(15,27,54,.06)",
)

DARK = dict(
    scheme="dark", bg="#0E1715", surface="#16231F", surface2="#1F302B", ink="#ECF0E8",
    muted="#9BB0A8", line="#2C423C", primary="#F2D45C", on_primary="#241D00",
    accent="#F2D45C", accent_ink="#241D00", ring="#F2D45C",
    good="#63D6A0", warn="#F0B450", bad="#FF8078",
    good_bg="#173A2C", warn_bg="#3A2E14", bad_bg="#40201F", info_bg="#1B2D3F",
    panel="#16231F", panel_ink="#ECF0E8", panel_line="rgba(236,240,232,.07)",
    shadow="0 1px 2px rgba(0,0,0,.25), 0 10px 28px rgba(0,0,0,.28)",
)

CSS = Template("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Figtree:wght@400;500;600;700&display=swap');

:root {
  --bg:$bg; --surface:$surface; --surface-2:$surface2; --ink:$ink; --muted:$muted; --line:$line;
  --primary:$primary; --on-primary:$on_primary; --accent:$accent; --accent-ink:$accent_ink; --ring:$ring;
  --good:$good; --warn:$warn; --bad:$bad;
  --good-bg:$good_bg; --warn-bg:$warn_bg; --bad-bg:$bad_bg; --info-bg:$info_bg;
  --panel:$panel; --panel-ink:$panel_ink; --panel-line:$panel_line; --shadow:$shadow;
  --display:'Fraunces', Georgia, 'Times New Roman', serif;
  --body:'Figtree', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --mono:ui-monospace, 'SF Mono', Menlo, Consolas, monospace;
  color-scheme:$scheme;
}

/* Page */
html, body, .stApp, [data-testid="stApp"], [data-testid="stAppViewContainer"], [data-testid="stMain"] {
  background:var(--bg) !important; color:var(--ink) !important; font-family:var(--body) !important;
}
[data-testid="stHeader"] { background:transparent !important; }
[data-testid="stHeader"] *, [data-testid="stSidebarCollapseButton"] * { color:var(--muted) !important; }
[data-testid="stDecoration"], #MainMenu, footer { display:none !important; }
.block-container { max-width:1120px; padding:4.2rem 2rem 4rem !important; }
.stApp p, .stApp li, .stApp label, .stApp input, .stApp textarea, .stApp button, .stApp td, .stApp th {
  font-family:var(--body) !important;
}
.stApp h1, .stApp h2, .stApp h3 {
  font-family:var(--display) !important; color:var(--ink) !important; font-weight:600 !important; letter-spacing:-.01em;
}
[data-testid="stMarkdownContainer"] { color:var(--ink) !important; }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li,
[data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label { color:var(--ink) !important; }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p { color:var(--muted) !important; }
::selection { background:var(--accent); color:var(--accent-ink); }
[data-testid="stElementContainer"]:has(> [data-testid="stMarkdown"] style),
.element-container:has(> [data-testid="stMarkdown"] style) { display:none !important; }

/* Sidebar */
[data-testid="stSidebar"] { background:var(--surface) !important; border-right:1px solid var(--line); }
[data-testid="stSidebarNavLink"], [data-testid="stSidebarNav"] a {
  border-radius:10px !important; color:var(--ink) !important; font-weight:600;
}
[data-testid="stSidebarNavLink"] span, [data-testid="stSidebarNavLink"] p { color:var(--ink) !important; }
[data-testid="stSidebarNavLink"]:hover { background:var(--surface-2) !important; }
[data-testid="stSidebarNavLink"] [data-testid="stIconMaterial"] { color:var(--muted) !important; }
[data-testid="stSidebarNavLink"][aria-current="page"] {
  background:var(--surface-2) !important; box-shadow:inset 3px 0 0 var(--primary);
}

/* Inputs */
[data-testid="stTextInputRootElement"], [data-testid="stNumberInputContainer"], [data-testid="stSelectbox"] [role="group"] {
  background:var(--surface-2) !important; border:1px solid var(--line) !important; border-radius:10px !important; color:var(--ink) !important;
}
[data-testid="stTextInputRootElement"]:focus-within, [data-testid="stNumberInputContainer"]:focus-within, [data-testid="stSelectbox"] [role="group"]:focus-within {
  border-color:var(--ring) !important; box-shadow:0 0 0 2px var(--ring) !important;
}
input, textarea {
  color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important; caret-color:var(--ink) !important; background:transparent !important;
}
input::placeholder, textarea::placeholder { color:var(--muted) !important; -webkit-text-fill-color:var(--muted) !important; opacity:.8; }
[data-testid="stTextInputRootElement"] button, [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"],
[data-testid="stSelectbox"] button[aria-label="Open"] { background:transparent !important; color:var(--muted) !important; }
[data-testid="stNumberInputStepUp"]:hover, [data-testid="stNumberInputStepDown"]:hover { color:var(--ink) !important; }
[data-testid="stSelectboxVirtualDropdown"] {
  background:var(--surface) !important; color:var(--ink) !important; border:1px solid var(--line); border-radius:12px !important; box-shadow:var(--shadow) !important;
}
[data-testid="stSelectboxVirtualDropdown"] [role="listbox"] { background:transparent !important; }
[role="option"], [role="option"] * { background:transparent !important; color:var(--ink) !important; }
[role="option"]:hover, [role="option"][data-focused="true"], [role="option"][data-selected="true"] { background:var(--surface-2) !important; }
[data-testid="stTooltipContent"] { background:var(--surface) !important; color:var(--ink) !important; border:1px solid var(--line); }
[data-testid="stTooltipContent"] * { color:var(--ink) !important; }
[data-testid="stCaptionContainer"] { opacity:1 !important; }
[data-testid="stSelectbox"] svg { fill:var(--muted) !important; color:var(--muted) !important; }

/* Toggle */
label:has(input[role="switch"]) > span + div { background:color-mix(in srgb, var(--muted) 45%, var(--surface)) !important; }
label:has(input[role="switch"]:checked) > span + div { background:var(--primary) !important; }
label:has(input[role="switch"]) > span + div > div { background:var(--surface) !important; }

/* Buttons */
[data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-secondaryFormSubmit"],
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primaryFormSubmit"] {
  border-radius:10px !important; font-weight:600 !important; padding:.5rem 1.15rem !important;
  border:1px solid var(--line) !important; background:var(--surface) !important; color:var(--ink) !important;
  transition:filter .15s, border-color .15s;
}
[data-testid="stBaseButton-secondary"] [data-testid="stMarkdownContainer"] p, [data-testid="stBaseButton-secondaryFormSubmit"] [data-testid="stMarkdownContainer"] p,
[data-testid="stBaseButton-secondary"] [data-testid="stIconMaterial"], [data-testid="stBaseButton-secondaryFormSubmit"] [data-testid="stIconMaterial"] { color:var(--ink) !important; }
[data-testid="stBaseButton-secondary"]:hover, [data-testid="stBaseButton-secondaryFormSubmit"]:hover { border-color:var(--ring) !important; }
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primaryFormSubmit"] {
  background:var(--primary) !important; border-color:var(--primary) !important; color:var(--on-primary) !important;
}
[data-testid="stBaseButton-primary"] [data-testid="stMarkdownContainer"] p, [data-testid="stBaseButton-primaryFormSubmit"] [data-testid="stMarkdownContainer"] p,
[data-testid="stBaseButton-primary"] [data-testid="stIconMaterial"], [data-testid="stBaseButton-primaryFormSubmit"] [data-testid="stIconMaterial"] { color:var(--on-primary) !important; }
[data-testid="stBaseButton-primary"]:hover, [data-testid="stBaseButton-primaryFormSubmit"]:hover { filter:brightness(1.12); }
button:focus-visible { outline:2px solid var(--ring) !important; outline-offset:2px; }

/* Tabs */
[role="tablist"] { gap:1.2rem; background:transparent !important; border-bottom:1px solid var(--line) !important; }
[data-testid="stTab"] { background:transparent !important; margin-right:1.4rem !important; padding-left:0 !important; padding-right:0 !important; }
[data-testid="stTab"] [data-testid="stMarkdownContainer"] p { color:var(--muted) !important; font-weight:600 !important; }
[data-testid="stTab"]:hover [data-testid="stMarkdownContainer"] p, [data-testid="stTab"][aria-selected="true"] [data-testid="stMarkdownContainer"] p { color:var(--ink) !important; }
.react-aria-SelectionIndicator { background:var(--primary) !important; height:3px !important; }

/* Forms and dialogs */
[data-testid="stForm"] {
  background:var(--surface) !important; border:1px solid var(--line) !important; border-radius:16px !important;
  padding:1.3rem 1.3rem 1.1rem !important; box-shadow:var(--shadow);
}
[data-testid="stDialog"] { background:rgba(8,14,12,.5) !important; }
[data-testid="stDialog"] > div { background:var(--surface) !important; color:var(--ink) !important; border:1px solid var(--line); border-radius:16px !important; box-shadow:var(--shadow); }
[data-testid="stDialog"] section[role="dialog"] { background:transparent !important; color:var(--ink) !important; }
[data-testid="stDialog"] h2, [data-testid="stDialog"] p, [data-testid="stDialog"] span, [data-testid="stDialog"] strong { color:var(--ink) !important; }
[data-testid="stDialog"] h2 { font-family:var(--display) !important; }
[data-testid="stDialog"] button[aria-label="Close"] svg, [data-testid="stDialog"] > div > div > button svg { color:var(--muted) !important; fill:var(--muted) !important; }
[data-testid="stCheckbox"] p, [data-testid="stToggle"] p { color:var(--ink) !important; }

/* Page furniture */
.pg-head { margin:0 0 1.5rem; }
.pg-title { font-family:var(--display); font-weight:600; font-size:2.5rem; line-height:1.08; letter-spacing:-.02em; color:var(--ink); }
.pg-sub { color:var(--muted); margin-top:.45rem; font-size:1.02rem; }
.sec { font-family:var(--display); font-size:1.4rem; font-weight:600; margin:1.8rem 0 .8rem; color:var(--ink); }
.notice { border-radius:12px; padding:.8rem 1.05rem; margin:.6rem 0 1rem; border:1px solid var(--line); border-left-width:5px; color:var(--ink); }
.notice.good { background:var(--good-bg); border-color:var(--good); }
.notice.warn { background:var(--warn-bg); border-color:var(--warn); }
.notice.bad { background:var(--bad-bg); border-color:var(--bad); }
.notice.info { background:var(--info-bg); border-color:var(--ring); }
.empty { border:1.5px dashed var(--line); border-radius:16px; padding:2rem 1.5rem; text-align:center; background:var(--surface); }
.empty-t { font-family:var(--display); font-size:1.25rem; font-weight:600; color:var(--ink); }
.empty-h { color:var(--muted); margin-top:.3rem; }

.stats { display:flex; flex-wrap:wrap; background:var(--surface); border:1px solid var(--line); border-radius:16px; box-shadow:var(--shadow); overflow:hidden; margin:0 0 1.4rem; }
.stat { flex:1 1 170px; padding:1.1rem 1.5rem; border-right:1px solid var(--line); }
.stat:last-child { border-right:0; }
.stat-n { font-family:var(--display); font-size:2.3rem; font-weight:600; line-height:1; font-variant-numeric:tabular-nums; color:var(--ink); }
.stat-l { color:var(--muted); margin-top:.4rem; font-size:.93rem; }

.tbl-wrap { background:var(--surface); border:1px solid var(--line); border-radius:16px; overflow:auto; box-shadow:var(--shadow); }
.tbl-wrap .tbl { width:100%; border-collapse:collapse; font-size:.97rem; margin:0; }
.tbl-wrap .tbl th { text-align:left; padding:.8rem 1.15rem; color:var(--muted) !important; font-weight:600; font-size:.88rem; background:var(--surface-2) !important; border:0 !important; border-bottom:1px solid var(--line) !important; white-space:nowrap; }
.tbl-wrap .tbl td { padding:.8rem 1.15rem; color:var(--ink) !important; background:transparent !important; border:0 !important; border-bottom:1px solid var(--line) !important; }
.tbl-wrap .tbl tbody tr:last-child td { border-bottom:0 !important; }
.tbl-wrap .tbl tbody tr:hover td { background:var(--surface-2) !important; }
.tbl-wrap .tbl .num { font-variant-numeric:tabular-nums; }
.tbl-wrap .tbl .mono { font-family:var(--mono); }
.tbl-wrap .tbl .strong { font-weight:600; }

.bars { background:var(--surface); border:1px solid var(--line); border-radius:16px; box-shadow:var(--shadow); padding:1rem 1.5rem; }
.bars.wide .bar-row { grid-template-columns:minmax(7rem, 11rem) 1fr 2.5rem; }
.bar-row { display:grid; grid-template-columns:9rem 1fr 3rem; gap:1rem; align-items:center; padding:.55rem 0; }
.bar-label { font-weight:600; color:var(--ink); }
.bar-count { text-align:right; font-weight:700; font-variant-numeric:tabular-nums; color:var(--ink); }
.track { display:block; height:10px; border-radius:999px; background:var(--surface-2); overflow:hidden; }
.fill { display:block; height:100%; border-radius:999px; }
.fill.good { background:var(--good); } .fill.warn { background:var(--warn); } .fill.bad { background:var(--bad); } .fill.brand { background:var(--primary); }

.slip { margin:1rem 0; background:var(--surface); border:1.5px dashed var(--line); border-left:6px solid var(--accent); border-radius:12px; padding:1rem 1.4rem; }
.slip-row { display:flex; flex-wrap:wrap; gap:.3rem 1.2rem; align-items:baseline; padding:.3rem 0; }
.slip-k { color:var(--muted); min-width:11rem; font-size:.93rem; }
.slip-v { font-family:var(--mono); font-size:1.2rem; font-weight:600; letter-spacing:.03em; color:var(--ink); user-select:all; }
.slip-note { color:var(--muted); font-size:.9rem; margin-top:.5rem; }

.me { display:flex; gap:.75rem; align-items:center; padding:.9rem 0 .4rem; }
.avatar { width:40px; height:40px; border-radius:50%; background:var(--accent); color:var(--accent-ink); display:flex; align-items:center; justify-content:center; font-family:var(--display); font-weight:700; font-size:1.15rem; flex:none; }
.me-name { font-weight:700; line-height:1.2; color:var(--ink); }
.me-role { color:var(--muted); font-size:.9rem; }

.cell-name { font-family:var(--display); font-size:1.05rem; font-weight:600; color:var(--ink); }
.cell-muted { color:var(--muted); font-variant-numeric:tabular-nums; }
.col-head { color:var(--muted); font-size:.88rem; font-weight:600; padding-bottom:.2rem; }

/* Report card */
.rc-top { display:flex; justify-content:space-between; align-items:center; gap:1.5rem; flex-wrap:wrap; background:var(--surface); border:1px solid var(--line); border-radius:18px; padding:1.6rem 1.8rem; box-shadow:var(--shadow); margin-bottom:1rem; }
.rc-name { font-family:var(--display); font-size:2.4rem; font-weight:600; line-height:1.1; letter-spacing:-.02em; color:var(--ink); }
.chips { display:flex; gap:.5rem; margin-top:.8rem; flex-wrap:wrap; }
.chip { padding:.2rem .75rem; border-radius:999px; background:var(--surface-2); border:1px solid var(--line); color:var(--ink); font-size:.88rem; font-weight:600; }
.rc-avg { display:flex; align-items:center; gap:1.3rem; flex:none; }
.rc-top > div:first-child { flex:1 1 22rem; min-width:0; }
.chip { max-width:100%; }
.rc-avg-n { font-family:var(--display); font-size:2.7rem; font-weight:600; line-height:1; text-align:right; font-variant-numeric:tabular-nums; color:var(--ink); }
.rc-avg-l { color:var(--muted); font-size:.9rem; text-align:right; margin-top:.25rem; }
.stamp { width:88px; height:88px; border-radius:50%; border:3px solid currentColor; box-shadow:inset 0 0 0 4px var(--surface), inset 0 0 0 5px currentColor; display:flex; align-items:center; justify-content:center; font-family:var(--display); font-weight:700; font-size:2rem; transform:rotate(-8deg); flex:none; }
.stamp.good { color:var(--good); } .stamp.warn { color:var(--warn); } .stamp.bad { color:var(--bad); }
.rc-note { color:var(--muted); margin:.2rem 0 1rem .2rem; }
.rc-table { background:var(--surface); border:1px solid var(--line); border-radius:18px; box-shadow:var(--shadow); overflow:hidden; }
.rc-head, .rc-row { display:grid; grid-template-columns:1.5fr 2.4fr .6fr 1.7fr; gap:1.3rem; align-items:center; padding:1rem 1.7rem; }
.rc-head { color:var(--muted); font-size:.88rem; font-weight:600; background:var(--surface-2); border-bottom:1px solid var(--line); padding-top:.75rem; padding-bottom:.75rem; }
.rc-row { grid-template-areas:"s m g a"; border-bottom:1px solid var(--line); }
.rc-row:last-child { border-bottom:0; }
.rc-subject { grid-area:s; font-family:var(--display); font-size:1.2rem; font-weight:600; color:var(--ink); line-height:1.25; }
.rc-sub-meta { font-family:var(--body); font-size:.85rem; font-weight:500; color:var(--muted); margin-top:.15rem; }
.rc-gpa { text-align:right; }
.rc-gpa-n { font-family:var(--display); font-size:2.7rem; font-weight:600; line-height:1; font-variant-numeric:tabular-nums; color:var(--ink); }
.rc-marks { grid-area:m; display:flex; align-items:center; gap:.9rem; }
.rc-marks .num { min-width:2.6ch; text-align:right; font-family:var(--display); font-size:1.55rem; font-weight:600; font-variant-numeric:tabular-nums; color:var(--ink); }
.rc-marks .none { color:var(--muted); font-size:.95rem; }
.rc-marks .track, .rc-att .track { flex:1; }
.rc-grade { grid-area:g; font-weight:700; font-size:1.1rem; }
.rc-grade.good { color:var(--good); } .rc-grade.warn { color:var(--warn); } .rc-grade.bad { color:var(--bad); } .rc-grade.none { color:var(--muted); }
.rc-att { grid-area:a; display:flex; align-items:center; gap:.8rem; }
.rc-att .pct { min-width:3.6ch; text-align:right; font-weight:700; font-variant-numeric:tabular-nums; color:var(--ink); }
.rc-att .track { height:7px; }
@media (max-width:760px) {
  .block-container { padding:1.2rem 1rem 3rem !important; }
  .rc-head { display:none; }
  .rc-row { grid-template-areas:"s g" "m m" "a a"; grid-template-columns:1fr auto; gap:.7rem 1rem; padding:1rem 1.2rem; }
  .rc-grade { text-align:right; }
  .rc-name { font-size:1.9rem; }
  .pg-title { font-size:2rem; }
}

/* Sign in */
.hero { position:relative; min-height:470px; border-radius:20px; overflow:hidden; background-color:var(--panel); color:var(--panel-ink);
  background-image:repeating-linear-gradient(to bottom, transparent 0, transparent 35px, var(--panel-line) 35px, var(--panel-line) 36px);
  padding:3.2rem 2.4rem 2.4rem 5.6rem; border:1px solid var(--line); box-shadow:var(--shadow); }
.hero::before { content:""; position:absolute; top:0; bottom:0; left:3.4rem; width:2px; background:#E5584F; opacity:.75; }
.hero-title { font-family:var(--display); font-size:3.4rem; font-weight:600; line-height:1.02; letter-spacing:-.03em; color:var(--panel-ink); }
.hero-sub { margin-top:1rem; font-size:1.1rem; max-width:22rem; color:var(--panel-ink); opacity:.85; }
.hero-roles { margin-top:2.4rem; display:grid; gap:1.1rem; }
.hero-role { color:var(--panel-ink); opacity:.92; line-height:1.4; }
.hero-role b { font-family:var(--display); font-size:1.15rem; font-weight:600; display:block; }
.signin-title { font-family:var(--display); font-size:2rem; font-weight:600; letter-spacing:-.02em; margin:.3rem 0 .6rem; color:var(--ink); }
@media (max-width:760px) { .hero { min-height:0; padding:2rem 1.4rem 1.6rem 3.4rem; } .hero::before { left:2rem; } .hero-title { font-size:2.5rem; } }
</style>
""")


def _system_dark():
    try:
        return st.context.theme.type == "dark"
    except Exception:
        return False


def is_dark():
    return st.session_state.get("_dark", _system_dark())


def apply():
    tokens = DARK if is_dark() else LIGHT
    st.markdown(CSS.substitute(tokens), unsafe_allow_html=True)


def _remember():
    st.session_state["_dark"] = st.session_state["dark_toggle"]


def toggle():
    st.toggle("Dark mode", value=is_dark(), key="dark_toggle", on_change=_remember)


def topbar_toggle():
    """Right aligned switch for pages that have no sidebar (sign in)."""
    _, right = st.columns([5, 1.4])
    with right:
        toggle()


def sign_out():
    dark = st.session_state.get("_dark")
    st.session_state.clear()
    if dark is not None:
        st.session_state["_dark"] = dark
    st.rerun()
