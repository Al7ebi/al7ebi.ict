"""
app_1.py — رادار المحرك الذكي  |  Smart Engine Radar
Modern Arabic Dashboard  —  No Sidebar  —  Light Mode First
Run: streamlit run app_1.py   |   Requires: engine.py
"""

import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import engine as E

# ══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="رادار المحرك الذكي",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════
#  GLOBAL CSS — Modern Arabic Dashboard
# ══════════════════════════════════════════════════════════════
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&family=IBM+Plex+Sans+Arabic:wght@300;400;500;600&display=swap');

/* ── Reset & root ── */
:root {
    --bg-page:    #F0F2F6;
    --bg-card:    #FFFFFF;
    --bg-header:  linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
    --bg-sidebar: #FAFAFA;

    --blue-500:   #4F46E5;
    --blue-400:   #6366F1;
    --blue-100:   #EEF2FF;
    --purple-500: #7C3AED;
    --purple-100: #F5F3FF;
    --green-500:  #10B981;
    --green-100:  #ECFDF5;
    --red-500:    #EF4444;
    --red-100:    #FEF2F2;
    --amber-500:  #F59E0B;
    --amber-100:  #FFFBEB;
    --gray-50:    #F9FAFB;
    --gray-100:   #F3F4F6;
    --gray-200:   #E5E7EB;
    --gray-300:   #D1D5DB;
    --gray-400:   #9CA3AF;
    --gray-500:   #6B7280;
    --gray-700:   #374151;
    --gray-900:   #111827;

    --shadow-sm:  0 1px 2px rgba(0,0,0,.06), 0 1px 3px rgba(0,0,0,.10);
    --shadow-md:  0 4px 6px rgba(0,0,0,.07), 0 2px 4px rgba(0,0,0,.06);
    --shadow-lg:  0 10px 15px rgba(0,0,0,.08), 0 4px 6px rgba(0,0,0,.05);
    --radius-sm:  8px;
    --radius-md:  12px;
    --radius-lg:  16px;
    --radius-xl:  24px;

    --font-ar:    'Tajawal', 'IBM Plex Sans Arabic', sans-serif;
}

/* ── Global ── */
html, body, [class*="css"] {
    background-color: var(--bg-page) !important;
    font-family: var(--font-ar) !important;
    direction: rtl !important;
    color: var(--gray-900) !important;
}
* { box-sizing: border-box; margin: 0; }

/* Hide sidebar toggle */
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* Streamlit main padding */
.main .block-container {
    padding: 0 1.5rem 2rem !important;
    max-width: 1400px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--gray-100); border-radius: 10px; }
::-webkit-scrollbar-thumb { background: var(--gray-300); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--blue-400); }

/* ══════════════════════════════════════
   TOP HEADER
══════════════════════════════════════ */
.app-header {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 60%, #9333EA 100%);
    padding: 28px 36px;
    margin: -1rem -1.5rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.app-header-left { display: flex; align-items: center; gap: 14px; }
.app-header-icon {
    width: 50px; height: 50px;
    background: rgba(255,255,255,.18);
    border-radius: var(--radius-md);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem;
}
.app-header-title {
    font-family: var(--font-ar);
    font-size: 1.7rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.1;
    letter-spacing: -0.3px;
}
.app-header-sub {
    font-size: 0.8rem;
    font-weight: 400;
    color: rgba(255,255,255,.7);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 2px;
}
.app-header-right {
    display: flex; align-items: center; gap: 12px;
}
.header-badge {
    background: rgba(255,255,255,.15);
    border: 1px solid rgba(255,255,255,.25);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.75rem;
    color: rgba(255,255,255,.9);
    font-family: var(--font-ar);
    backdrop-filter: blur(4px);
}

/* ══════════════════════════════════════
   CONTROL BAR
══════════════════════════════════════ */
.control-bar {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    padding: 18px 24px;
    margin: 20px 0 8px;
    border: 1px solid var(--gray-200);
}
.control-bar-title {
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--gray-400);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

/* Streamlit widget overrides inside control bar */
.stSelectbox label, .stTextInput label,
.stMultiSelect label, .stSlider label {
    font-family: var(--font-ar) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: var(--gray-500) !important;
    margin-bottom: 4px !important;
}
div[data-baseweb="select"] > div {
    background: var(--gray-50) !important;
    border: 1px solid var(--gray-200) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-ar) !important;
    font-size: 0.88rem !important;
    transition: border-color .2s !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: var(--blue-400) !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--blue-500) !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,.12) !important;
}
div[data-baseweb="input"] > div {
    background: var(--gray-50) !important;
    border: 1px solid var(--gray-200) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-ar) !important;
    transition: border-color .2s !important;
}
div[data-baseweb="input"] > div:focus-within {
    border-color: var(--blue-500) !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,.12) !important;
}

/* ══════════════════════════════════════
   BUTTONS
══════════════════════════════════════ */
.stButton > button {
    font-family: var(--font-ar) !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    border-radius: var(--radius-sm) !important;
    padding: 10px 22px !important;
    transition: all .2s ease !important;
    border: none !important;
    cursor: pointer !important;
}
/* Default button */
.stButton > button:not([kind="primary"]) {
    background: var(--gray-100) !important;
    color: var(--gray-700) !important;
    border: 1px solid var(--gray-200) !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: var(--gray-200) !important;
    border-color: var(--gray-300) !important;
}
/* Primary */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
    color: #fff !important;
    box-shadow: 0 4px 12px rgba(79,70,229,.35) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(79,70,229,.45) !important;
}
.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
}

/* ══════════════════════════════════════
   KPI METRIC CARDS
══════════════════════════════════════ */
.kpi-row {
    display: grid;
    gap: 16px;
    margin: 20px 0;
}
.kpi-card {
    background: var(--bg-card);
    border-radius: var(--radius-md);
    padding: 20px 22px;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--gray-100);
    display: flex;
    align-items: center;
    gap: 16px;
    transition: box-shadow .2s, transform .2s;
    position: relative;
    overflow: hidden;
}
.kpi-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 4px; height: 100%;
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
}
.kpi-card.blue::before  { background: #4F46E5; }
.kpi-card.green::before { background: #10B981; }
.kpi-card.red::before   { background: #EF4444; }
.kpi-card.amber::before { background: #F59E0B; }
.kpi-card.purple::before{ background: #7C3AED; }
.kpi-card.teal::before  { background: #14B8A6; }

.kpi-icon-wrap {
    width: 52px; height: 52px;
    border-radius: var(--radius-sm);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    flex-shrink: 0;
}
.kpi-icon-wrap.blue   { background: var(--blue-100);   }
.kpi-icon-wrap.green  { background: var(--green-100);  }
.kpi-icon-wrap.red    { background: var(--red-100);    }
.kpi-icon-wrap.amber  { background: var(--amber-100);  }
.kpi-icon-wrap.purple { background: var(--purple-100); }
.kpi-icon-wrap.teal   { background: #F0FDFA; }

.kpi-body { flex: 1; direction: rtl; text-align: right; }
.kpi-value {
    font-family: var(--font-ar);
    font-size: 1.85rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-value.blue   { color: #4F46E5; }
.kpi-value.green  { color: #10B981; }
.kpi-value.red    { color: #EF4444; }
.kpi-value.amber  { color: #F59E0B; }
.kpi-value.purple { color: #7C3AED; }
.kpi-value.teal   { color: #14B8A6; }

.kpi-label-ar {
    font-family: var(--font-ar);
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--gray-700);
    line-height: 1.3;
}
.kpi-label-en {
    font-size: 0.68rem;
    font-weight: 400;
    color: var(--gray-400);
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ══════════════════════════════════════
   SECTION HEADER
══════════════════════════════════════ */
.sec-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 24px 0 14px;
}
.sec-head-left { display: flex; align-items: center; gap: 10px; }
.sec-head-icon {
    width: 36px; height: 36px;
    background: var(--blue-100);
    border-radius: var(--radius-sm);
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}
.sec-head-ar {
    font-family: var(--font-ar);
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--gray-900);
}
.sec-head-en {
    font-size: 0.7rem;
    font-weight: 400;
    color: var(--gray-400);
    letter-spacing: 1px;
    text-transform: uppercase;
}
.sec-head-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--gray-200), transparent);
    margin: 0 16px;
}

/* ══════════════════════════════════════
   GRADE PILLS
══════════════════════════════════════ */
.grade-pill {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-family: var(--font-ar);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 4px 10px;
    border-radius: 20px;
}
.gp-ap { background: #DCFCE7; color: #15803D; }
.gp-a  { background: #DBEAFE; color: #1D4ED8; }
.gp-b  { background: #FEF9C3; color: #854D0E; }
.gp-c  { background: #FEE2E2; color: #991B1B; }
.gp-sk { background: var(--gray-100); color: var(--gray-500); }

/* ══════════════════════════════════════
   RADAR TABLE — custom card-style wrapper
══════════════════════════════════════ */
.table-card {
    background: var(--bg-card);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--gray-100);
    overflow: hidden;
    margin-bottom: 16px;
}
.table-card-header {
    background: var(--gray-50);
    border-bottom: 1px solid var(--gray-200);
    padding: 14px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.table-card-title {
    font-family: var(--font-ar);
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--gray-700);
}
.stDataFrame iframe { border: none !important; }
.stDataFrame > div  {
    border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
    border: none !important;
}

/* ══════════════════════════════════════
   DECISION LOG CARD
══════════════════════════════════════ */
.dlog-card {
    background: var(--bg-card);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--gray-100);
    overflow: hidden;
}
.dlog-card-head {
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    padding: 16px 20px;
    display: flex; align-items: center; justify-content: space-between;
}
.dlog-bias-label {
    font-family: var(--font-ar);
    font-size: 1.1rem;
    font-weight: 700;
    color: #fff;
}
.dlog-body { padding: 0; }
.dlog-entry {
    padding: 14px 20px;
    border-bottom: 1px solid var(--gray-100);
    transition: background .15s;
}
.dlog-entry:last-child { border-bottom: none; }
.dlog-entry:hover { background: var(--gray-50); }
.dlog-stage {
    font-size: 0.62rem;
    font-weight: 600;
    color: var(--blue-400);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 3px;
}
.dlog-finding {
    font-family: var(--font-ar);
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--gray-800);
    margin-bottom: 3px;
}
.dlog-reason  { font-size: 0.75rem; color: var(--gray-500); line-height: 1.5; }
.dlog-risk    { font-size: 0.72rem; color: #D97706; margin-top: 3px; }
.dlog-delta   { font-size: 0.72rem; font-weight: 700; margin-top: 4px; }
.dlog-pnl {
    background: var(--gray-50);
    padding: 14px 20px;
    border-top: 2px solid var(--gray-200);
}
.dlog-pnl-lbl {
    font-size: 0.65rem;
    color: var(--gray-400);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.dlog-pnl-val {
    font-family: var(--font-ar);
    font-size: 1.35rem;
    font-weight: 800;
}

/* ══════════════════════════════════════
   TRADE LEVELS TABLE
══════════════════════════════════════ */
.tl-wrap {
    background: var(--bg-card);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--gray-100);
    overflow: hidden;
}
.tl-table { width: 100%; border-collapse: collapse; font-family: var(--font-ar); }
.tl-table thead th {
    background: var(--gray-50);
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--gray-500);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 10px 16px;
    text-align: right;
    border-bottom: 1px solid var(--gray-200);
}
.tl-table tbody td { padding: 11px 16px; font-size: 0.88rem; border-bottom: 1px solid var(--gray-100); }
.tl-table tbody tr:last-child td { border-bottom: none; }
.tl-table tbody tr:hover td { background: var(--gray-50); }
.tl-entry td:first-child { color: #4F46E5; font-weight: 700; }
.tl-sl    td:first-child { color: #EF4444; font-weight: 700; }
.tl-tp    td:first-child { color: #10B981; font-weight: 700; }
.tl-price { font-family: 'JetBrains Mono', monospace; font-size: 0.88rem; }

/* ══════════════════════════════════════
   DRILL DOWN BADGE
══════════════════════════════════════ */
.drill-badge {
    background: linear-gradient(135deg, #EEF2FF, #F5F3FF);
    border: 1px solid #C7D2FE;
    border-radius: var(--radius-md);
    padding: 14px 20px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 16px;
}
.drill-sym {
    font-family: var(--font-ar);
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--blue-500);
    letter-spacing: 1px;
}
.drill-meta { font-size: 0.75rem; color: var(--gray-500); letter-spacing: 0.5px; }

/* ══════════════════════════════════════
   STAT BAR
══════════════════════════════════════ */
.stat-bar { display: flex; gap: 2px; height: 6px; border-radius: 3px; overflow: hidden; margin: 8px 0 20px; }
.stat-seg { flex: 1; }
.stat-seg.ap { background: #10B981; }
.stat-seg.aa { background: #4F46E5; }
.stat-seg.bb { background: #F59E0B; }
.stat-seg.sk { background: var(--gray-200); }

/* ══════════════════════════════════════
   ALERTS
══════════════════════════════════════ */
div[data-testid="stInfo"]    { background: #EEF2FF !important; border: 1px solid #C7D2FE !important; border-radius: var(--radius-sm) !important; color: var(--gray-700) !important; font-family: var(--font-ar) !important; }
div[data-testid="stSuccess"] { background: #ECFDF5 !important; border: 1px solid #A7F3D0 !important; border-radius: var(--radius-sm) !important; color: var(--gray-700) !important; font-family: var(--font-ar) !important; }
div[data-testid="stError"]   { background: #FEF2F2 !important; border: 1px solid #FECACA !important; border-radius: var(--radius-sm) !important; color: var(--gray-700) !important; font-family: var(--font-ar) !important; }

/* Progress bar */
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #4F46E5, #7C3AED) !important;
    border-radius: 4px !important;
}
div[data-testid="stProgressBar"] > div {
    background: var(--gray-200) !important;
    border-radius: 4px !important;
}

/* ══════════════════════════════════════
   RADIO & MULTISELECT
══════════════════════════════════════ */
div[data-testid="stRadio"] label {
    font-family: var(--font-ar) !important;
    font-size: 0.85rem !important;
    color: var(--gray-700) !important;
}
div[data-testid="stMultiSelect"] span {
    font-family: var(--font-ar) !important;
}

/* ══════════════════════════════════════
   FOOTER
══════════════════════════════════════ */
.app-footer {
    margin-top: 48px;
    padding: 20px 0 8px;
    border-top: 1px solid var(--gray-200);
    text-align: center;
}
.app-footer-ar {
    font-family: var(--font-ar);
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--blue-500);
    margin-bottom: 4px;
}
.app-footer-en {
    font-size: 0.65rem;
    color: var(--gray-400);
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

/* ══════════════════════════════════════
   PLACEHOLDER
══════════════════════════════════════ */
.placeholder-card {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    border: 2px dashed var(--gray-200);
    padding: 48px 24px;
    text-align: center;
}
.placeholder-icon { font-size: 3rem; display: block; margin-bottom: 14px; }
.placeholder-title {
    font-family: var(--font-ar);
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--gray-700);
    margin-bottom: 8px;
}
.placeholder-body {
    font-family: var(--font-ar);
    font-size: 0.85rem;
    color: var(--gray-400);
    line-height: 1.7;
}

/* Divider */
hr { border: none !important; border-top: 1px solid var(--gray-200) !important; margin: 8px 0 !important; }
</style>
"""

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  CACHED ENGINE CALLS  (logic unchanged)
# ══════════════════════════════════════════════════════════════
@st.cache_data(ttl=300, show_spinner=False)
def cached_run_engine(ticker, smt_ticker, htf_interval, exec_interval,
                      entry_interval, htf_period, exec_period):
    return E.run_engine(ticker, smt_ticker,
                        htf_interval=htf_interval,
                        exec_interval=exec_interval,
                        entry_interval=entry_interval,
                        htf_period=htf_period,
                        exec_period=exec_period)


@st.cache_data(ttl=300, show_spinner=False)
def cached_scan_pair(ticker, smt_ticker, htf_interval, exec_interval,
                     entry_interval, htf_period, exec_period):
    try:
        result = E.run_engine(ticker, smt_ticker,
                              htf_interval=htf_interval,
                              exec_interval=exec_interval,
                              entry_interval=entry_interval,
                              htf_period=htf_period,
                              exec_period=exec_period)
        return E.extract_row(result[0], ticker, smt_ticker)
    except Exception:
        return {"Ticker": ticker, "SMT": smt_ticker, "Grade": "ERR",
                "Score": "—", "Bias": "ERROR", "Entry": "—", "SL": "—",
                "TP1": "—", "TP2": "—", "Potential R:R": "—",
                "DOL": "—", "SMT Signal": "—", "Fractal": "—",
                "Killzone": "—", "PD Array": "—",
                "_score_num": -1, "_grade_rank": 100}


# ══════════════════════════════════════════════════════════════
#  DESIGN HELPERS
# ══════════════════════════════════════════════════════════════
def grade_color_hex(g):
    return {"A+": "#10B981", "A": "#4F46E5", "B": "#F59E0B", "C": "#EF4444"}.get(g, "#9CA3AF")

def grade_pill(g):
    cls = {"A+": "gp-ap", "A": "gp-a", "B": "gp-b", "C": "gp-c"}.get(g, "gp-sk")
    return f'<span class="grade-pill {cls}">{g}</span>'

def kpi_card_html(icon, value, label_ar, label_en, color_cls):
    return f"""
    <div class="kpi-card {color_cls}">
      <div class="kpi-icon-wrap {color_cls}">{icon}</div>
      <div class="kpi-body">
        <div class="kpi-value {color_cls}">{value}</div>
        <div class="kpi-label-ar">{label_ar}</div>
        <div class="kpi-label-en">{label_en}</div>
      </div>
    </div>"""

def sec_header(icon, ar, en=""):
    st.markdown(f"""
    <div class="sec-head">
      <div class="sec-head-left">
        <div class="sec-head-icon">{icon}</div>
        <div>
          <div class="sec-head-ar">{ar}</div>
          {"<div class='sec-head-en'>" + en + "</div>" if en else ""}
        </div>
      </div>
      <div class="sec-head-line"></div>
    </div>""", unsafe_allow_html=True)

def app_footer():
    st.markdown("""
    <div class="app-footer">
      <div class="app-footer-ar">© جميع الحقوق محفوظة للحبي</div>
      <div class="app-footer-en">ICT Smart Engine Radar · Educational Use Only · Not Financial Advice</div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  TOP HEADER
# ══════════════════════════════════════════════════════════════
def render_header(mode, ticker="", smt="", preset="", n_symbols=0):
    badge_mode = "تحليل منفرد" if mode == "single" else "مسح الرادار"
    badge_sym  = f"<span class='header-badge'>{ticker} / {smt}</span>" if mode == "single" else \
                 f"<span class='header-badge'>{preset} · {n_symbols} سهم</span>"
    st.markdown(f"""
    <div class="app-header">
      <div class="app-header-left">
        <div class="app-header-icon">📡</div>
        <div>
          <div class="app-header-title">رادار المحرك الذكي</div>
          <div class="app-header-sub">Smart Engine Radar · ICT Protocol</div>
        </div>
      </div>
      <div class="app-header-right">
        <span class="header-badge">{badge_mode}</span>
        {badge_sym}
      </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  CONTROL BAR  (horizontal, no sidebar)
# ══════════════════════════════════════════════════════════════
def render_controls():
    """Returns (mode, ticker, smt_ticker, watchlist, preset, cfg, run_btn, scan_btn)"""

    st.markdown('<div class="control-bar">'
                '<div class="control-bar-title">⚙ إعدادات التحليل — Analysis Settings</div>',
                unsafe_allow_html=True)

    # Row 1 — Mode + main controls
    c_mode, c_sym, c_smt, c_wl, c_htf, c_exec, c_per = st.columns([1.2, 1.2, 1, 1.8, 1, 1, 1])

    with c_mode:
        mode_choice = st.radio(
            "النوع / Mode",
            ["📈 سهم واحد", "📡 رادار"],
            horizontal=False,
            label_visibility="visible"
        )
        mode = "single" if "سهم" in mode_choice else "radar"

    with c_sym:
        ticker = st.text_input(
            "الرمز / Symbol",
            value="TSLA",
            placeholder="TSLA"
        ).strip().upper()

    with c_smt:
        smt_ticker = st.text_input(
            "SMT Pair",
            value="QQQ",
            placeholder="QQQ"
        ).strip().upper()

    with c_wl:
        preset = st.selectbox(
            "قائمة المراقبة / Watchlist",
            list(E.WATCHLIST_PRESETS.keys()),
            disabled=(mode == "single")
        )
        watchlist = E.WATCHLIST_PRESETS[preset]

    with c_htf:
        htf_interval = st.selectbox("الإطار / HTF", ["1d", "1wk", "4h", "1h"])

    with c_exec:
        exec_interval = st.selectbox("تنفيذ / Exec", ["15m", "30m", "1h", "5m"])

    with c_per:
        htf_period = st.selectbox("الفترة / Period", ["6mo", "3mo", "1y", "2y"])

    # Row 2 — Engine params + action buttons
    p1, p2, p3, p4, p5, p6 = st.columns([1.2, 1.2, 1.2, 1.2, 1.2, 1.8])
    with p1:
        exec_period = st.selectbox("Exec Period", ["5d", "10d", "1mo"],
                                   label_visibility="visible")
    with p2:
        score_min = st.slider("الحد الأدنى للنقاط", 1, 13, E.SCORE_MIN,
                              label_visibility="visible")
    with p3:
        wick_min = st.slider("Wick % Min", 5, 40, int(E.SWEEP_WICK_MIN),
                             label_visibility="visible")
    with p4:
        n_candles = st.slider("عدد الشموع", 40, 150, 80,
                              label_visibility="visible")
    with p5:
        grade_filter = st.multiselect("فلتر Grade",
                                      ["A+", "A", "B", "C"],
                                      default=["A+", "A"],
                                      label_visibility="visible")
    with p6:
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            run_btn = st.button("▶ تحليل", type="primary",
                                use_container_width=True,
                                disabled=(mode == "radar"))
        with btn_c2:
            scan_btn = st.button("📡 مسح الرادار",
                                 use_container_width=True,
                                 disabled=(mode == "single"))

    st.markdown("</div>", unsafe_allow_html=True)

    cfg = dict(htf_interval=htf_interval, exec_interval=exec_interval,
               entry_interval="5m", htf_period=htf_period,
               exec_period=exec_period, score_min=score_min,
               wick_min=wick_min, n_candles=n_candles,
               grade_filter=grade_filter)

    return mode, ticker, smt_ticker, watchlist, preset, cfg, run_btn, scan_btn


# ══════════════════════════════════════════════════════════════
#  KPI ROW — Single Stock
# ══════════════════════════════════════════════════════════════
def render_kpi_single(setup, df_htf, dol):
    current    = float(df_htf["Close"].iloc[-1])
    price_prev = float(df_htf["Close"].iloc[-2]) if len(df_htf) > 1 else current
    chg_pct    = (current - price_prev) / price_prev * 100
    sign       = "+" if chg_pct >= 0 else ""
    chg_cls    = "green" if chg_pct >= 0 else "red"
    bias_val   = "صعودي ▲" if (setup and setup.bias=="long") else \
                 "هبوطي ▼" if (setup and setup.bias=="short") else "—"
    bias_cls   = "green" if (setup and setup.bias=="long") else \
                 "red"   if (setup and setup.bias=="short") else "teal"

    cols = st.columns(6)
    cards = [
        (cols[0], "💰", f"{current:.2f}", "آخر سعر", "Last Price", "blue"),
        (cols[1], "📊", f"{sign}{chg_pct:.2f}%", "التغيير اليومي", "Daily Change", chg_cls),
        (cols[2], "🎯", f"{dol.price:.2f}" if dol else "—", "هدف السيولة DOL", "DOL Target", "amber"),
        (cols[3], "⚖️", bias_val, "التحيز", "Bias", bias_cls),
        (cols[4], "🏆", setup.grade if setup else "SKIP", "التقييم", "Grade",
                        {"A+":"green","A":"blue","B":"amber"}.get(setup.grade if setup else "","teal")),
        (cols[5], "📈", f"{setup.score}/13" if setup else "—", "النقاط", "Score", "purple"),
    ]
    for col, icon, val, ar, en, cls in cards:
        col.markdown(kpi_card_html(icon, val, ar, en, cls), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  KPI ROW — Radar
# ══════════════════════════════════════════════════════════════
def render_kpi_radar(df):
    n_ap   = len(df[df["Grade"]=="A+"])
    n_a    = len(df[df["Grade"]=="A"])
    n_b    = len(df[df["Grade"]=="B"])
    n_long = len(df[df["Bias"]=="Long"])
    n_skip = len(df[df["Grade"].isin(["SKIP","ERR","TIMEOUT"])])
    n_rr3  = 0
    for v in df["Potential R:R"]:
        try:
            if float(str(v).replace("1:","")) >= 3: n_rr3 += 1
        except Exception: pass

    cols = st.columns(6)
    cards = [
        (cols[0], "🔍", len(df),    "إجمالي المسح",    "Total Scanned",  "blue"),
        (cols[1], "⭐", n_ap,        "إعدادات A+",      "Grade A+ Setups","green"),
        (cols[2], "✅", n_a,         "إعدادات A",       "Grade A Setups", "blue"),
        (cols[3], "📉", n_b,         "إعدادات B",       "Grade B Setups", "amber"),
        (cols[4], "▲",  n_long,      "توجه صعودي",      "Long Bias",      "teal"),
        (cols[5], "⚡", n_rr3,       "R:R أعلى من 3",   "R:R ≥ 3",        "purple"),
    ]
    for col, icon, val, ar, en, cls in cards:
        col.markdown(kpi_card_html(icon, val, ar, en, cls), unsafe_allow_html=True)

    # Grade distribution bar
    total = max(len(df), 1)
    segs  = (["<div class='stat-seg ap'></div>"] * n_ap +
             ["<div class='stat-seg aa'></div>"] * n_a  +
             ["<div class='stat-seg bb'></div>"] * n_b  +
             ["<div class='stat-seg sk'></div>"] * n_skip)
    st.markdown(f'<div class="stat-bar">{"".join(segs[:100])}</div>',
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  DECISION LOG
# ══════════════════════════════════════════════════════════════
def render_decision_log(setup, current_price):
    if not setup:
        st.markdown("""
        <div class="dlog-card">
          <div style="padding:32px;text-align:center;">
            <div style="font-size:2.5rem;margin-bottom:12px;">📭</div>
            <div style="font-family:var(--font-ar);font-size:1rem;
                 font-weight:700;color:var(--gray-500);">لا يوجد إعداد صفقة</div>
            <div style="font-size:0.8rem;color:var(--gray-400);margin-top:6px;">
              النقاط أقل من الحد الأدنى المطلوب
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
        return

    bias_ar  = "▲ شراء  LONG"  if setup.bias=="long"  else "▼ بيع  SHORT"
    pill_html= grade_pill(setup.grade)

    html = (f'<div class="dlog-card">'
            f'<div class="dlog-card-head">'
            f'<span class="dlog-bias-label">{bias_ar}</span>'
            f'<span style="display:flex;align-items:center;gap:8px;">'
            f'{pill_html}'
            f'<span style="background:rgba(255,255,255,.2);border-radius:12px;'
            f'padding:3px 10px;font-size:0.75rem;color:#fff;">'
            f'{setup.score}/13</span></span></div>'
            f'<div class="dlog-body">')

    for entry in setup.decision_log:
        dc = ("#10B981" if entry.score_delta>0 else
              "#EF4444" if entry.score_delta<0 else "#9CA3AF")
        ds = f"+{entry.score_delta}" if entry.score_delta >= 0 else str(entry.score_delta)
        tr = entry.reasoning[:100] + ("…" if len(entry.reasoning)>100 else "")
        rh = f'<div class="dlog-risk">⚠ {entry.risk_note[:90]}</div>' if entry.risk_note else ""
        html += (f'<div class="dlog-entry">'
                 f'<div class="dlog-stage">{entry.stage}</div>'
                 f'<div class="dlog-finding">{entry.finding}</div>'
                 f'<div class="dlog-reason">{tr}</div>{rh}'
                 f'<div class="dlog-delta" style="color:{dc}">{ds} نقطة</div>'
                 f'</div>')

    pnl = ((current_price - setup.entry)/setup.entry*100
           if setup.bias=="long"
           else (setup.entry - current_price)/setup.entry*100)
    pc  = "#10B981" if pnl>=0 else "#EF4444"
    ps  = f"{'+' if pnl>=0 else ''}{pnl:.2f}%"

    html += (f'</div><div class="dlog-pnl">'
             f'<div class="dlog-pnl-lbl">الربح/الخسارة غير المحقق · Unrealised P&L</div>'
             f'<div class="dlog-pnl-val" style="color:{pc}">{ps}</div>'
             f'</div></div>')

    st.markdown(html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  TRADE TABLE
# ══════════════════════════════════════════════════════════════
def render_trade_table(setup):
    sl_dist = abs(setup.entry - setup.stop_loss)
    rows = [
        {"cls":"tl-entry","Level":"الدخول  Entry",
         "Price":f"{setup.entry:.4f}","Dist":"—","RR":"مرجع","Note":"FVG / OB midpoint"},
        {"cls":"tl-sl","Level":"وقف الخسارة  SL",
         "Price":f"{setup.stop_loss:.4f}",
         "Dist":f"{abs(setup.entry-setup.stop_loss):.4f}",
         "RR":"—","Note":"وراء منطقة Sweep"},
    ]
    for t in setup.targets:
        if t.is_tp and sl_dist > 0:
            rr = round(abs(t.price - setup.entry) / sl_dist, 2)
            rows.append({"cls":"tl-tp","Level":f"هدف  {t.label}",
                         "Price":f"{t.price:.4f}",
                         "Dist":f"{abs(t.price-setup.entry):.4f}",
                         "RR":f"1:{rr}",
                         "Note":f"+{t.level}σ من نطاق التلاعب"})

    html = ('<div class="tl-wrap"><table class="tl-table">'
            '<thead><tr>'
            '<th>المستوى</th><th>السعر</th>'
            '<th>المسافة</th><th>R:R</th><th>الملاحظة</th>'
            '</tr></thead><tbody>')
    for r in rows:
        html += (f'<tr class="{r["cls"]}">'
                 f'<td>{r["Level"]}</td>'
                 f'<td class="tl-price">{r["Price"]}</td>'
                 f'<td class="tl-price">{r["Dist"]}</td>'
                 f'<td><b>{r["RR"]}</b></td>'
                 f'<td>{r["Note"]}</td></tr>')
    html += "</tbody></table></div>"
    st.markdown(html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SINGLE STOCK VIEW
# ══════════════════════════════════════════════════════════════
def render_single(ticker, smt_ticker, cfg, run_btn):
    if "single_result" not in st.session_state:
        st.session_state.single_result = None

    if run_btn:
        with st.spinner("جارٍ التحليل…"):
            try:
                E.SWEEP_WICK_MIN = float(cfg["wick_min"])
                st.session_state.single_result = cached_run_engine(
                    ticker, smt_ticker,
                    cfg["htf_interval"], cfg["exec_interval"],
                    cfg["entry_interval"], cfg["htf_period"], cfg["exec_period"])
            except Exception as ex:
                st.error(f"خطأ في المحرك: {ex}"); return

    result = st.session_state.single_result
    if result is None:
        st.markdown("""
        <div class="placeholder-card">
          <span class="placeholder-icon">📊</span>
          <div class="placeholder-title">في انتظار التحليل</div>
          <div class="placeholder-body">
            اضبط المعاملات في شريط الأدوات أعلاه<br>
            واضغط <strong>▶ تحليل</strong> لبدء التحليل الكامل
          </div>
        </div>""", unsafe_allow_html=True)
        app_footer(); return

    setup, df_htf, df_exec, df_m5, liq_levels, swings, dol = result
    current = float(df_htf["Close"].iloc[-1])

    # KPI cards
    sec_header("📊", "المؤشرات الرئيسية", "Key Metrics")
    render_kpi_single(setup, df_htf, dol)
    st.markdown("<br>", unsafe_allow_html=True)

    # Chart + Decision Log
    sec_header("📈", "حركة السعر والمستويات", "Price Action & Levels")
    chart_col, log_col = st.columns([2.6, 1], gap="medium")
    with chart_col:
        fig = E.build_chart(df_htf, setup, liq_levels, swings, dol,
                            ticker=ticker, n_candles=cfg["n_candles"],
                            htf_interval=cfg["htf_interval"])
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar": True, "displaylogo": False,
                                "modeBarButtonsToRemove": ["select2d","lasso2d"]})
    with log_col:
        st.markdown("<br>", unsafe_allow_html=True)
        render_decision_log(setup, current)

    # Trade table
    if setup:
        st.markdown("<br>", unsafe_allow_html=True)
        sec_header("🎯", "خطة الصفقة", "Trade Setup & StdDev Targets")
        render_trade_table(setup)

    app_footer()


# ══════════════════════════════════════════════════════════════
#  RADAR TABLE
# ══════════════════════════════════════════════════════════════
def _build_styled_table(show):
    """Build colour-coded DataFrame — uses .map() (not .applymap())"""
    def sg(v):
        return {
            "A+":   "background-color:#DCFCE7;color:#15803D;font-weight:700",
            "A":    "background-color:#DBEAFE;color:#1D4ED8;font-weight:700",
            "B":    "background-color:#FEF9C3;color:#854D0E;font-weight:600",
            "SKIP": "color:#9CA3AF",
            "ERR":  "color:#EF4444",
        }.get(str(v), "color:#6B7280")

    def sb(v):
        if "Long"  in str(v): return "color:#10B981;font-weight:700"
        if "Short" in str(v): return "color:#EF4444;font-weight:700"
        return "color:#9CA3AF"

    def sr(v):
        try:
            r = float(str(v).replace("1:", ""))
            if r >= 3: return "color:#10B981;font-weight:700"
            if r >= 2: return "color:#F59E0B"
            return "color:#9CA3AF"
        except Exception: return "color:#9CA3AF"

    def sf(v):
        if "H1+M15+M5" in str(v): return "color:#10B981;font-weight:600"
        if "H1+M15"    in str(v): return "color:#F59E0B"
        return "color:#9CA3AF"

    def ss(v):
        return "color:#7C3AED;font-weight:600" if "Div" in str(v) else "color:#9CA3AF"

    # .map() — not .applymap() — pandas >= 2.1 compatibility
    return (show.style
            .map(sg, subset=["Grade"])
            .map(sb, subset=["Bias"])
            .map(sr, subset=["Potential R:R"])
            .map(sf, subset=["Fractal"])
            .map(ss, subset=["SMT Signal"])
            .set_properties(**{
                "font-family": "'Tajawal','IBM Plex Sans Arabic',sans-serif",
                "font-size":   "13px",
                "text-align":  "right",
            })
            .set_table_styles([
                {"selector": "thead th",
                 "props": ("background:#F3F4F6;color:#6B7280;font-size:11px;"
                           "font-weight:600;letter-spacing:1px;"
                           "text-transform:uppercase;padding:10px 12px;"
                           "border-bottom:2px solid #E5E7EB;text-align:right;")},
                {"selector": "tbody td",
                 "props": "padding:9px 12px;border-bottom:1px solid #F3F4F6;"},
                {"selector": "tbody tr:hover td",
                 "props": "background-color:#F9FAFB;"},
            ]))


# ══════════════════════════════════════════════════════════════
#  RADAR SCAN VIEW
# ══════════════════════════════════════════════════════════════
def render_radar(watchlist, preset, cfg, scan_btn):
    for key in ("radar_df", "radar_preset", "selected_ticker"):
        if key not in st.session_state:
            st.session_state[key] = None

    if scan_btn:
        _run_radar_scan(watchlist, cfg)

    df = st.session_state.radar_df
    if df is None:
        st.markdown("""
        <div class="placeholder-card">
          <span class="placeholder-icon">📡</span>
          <div class="placeholder-title">الرادار في وضع الاستعداد</div>
          <div class="placeholder-body">
            اختر قائمة المراقبة واضغط <strong>📡 مسح الرادار</strong><br>
            لبدء المسح المتوازي لجميع الأسهم
          </div>
        </div>""", unsafe_allow_html=True)
        app_footer(); return

    # KPI
    sec_header("📊", "نتائج المسح", "Scan Summary")
    render_kpi_radar(df)

    # Extra search filter
    s1, s2, s3 = st.columns([2, 1, 1.5])
    with s1:
        search = st.text_input("🔍 بحث بالرمز / Symbol Search", placeholder="AAPL")
    with s2:
        bias_filter = st.selectbox("التوجه / Bias", ["الكل / All", "Long", "Short"])
    with s3:
        rr_filter = st.selectbox("الحد الأدنى R:R",
                                 ["الكل / Any", "≥ 1.5", "≥ 2", "≥ 3"])

    display = df.copy()
    gf = cfg.get("grade_filter", ["A+","A"])
    if gf:
        display = display[display["Grade"].isin(gf)]
    if bias_filter != "الكل / All":
        display = display[display["Bias"] == bias_filter]
    if search:
        display = display[display["Ticker"].str.contains(search.upper(), na=False)]
    if rr_filter != "الكل / Any":
        thresh = float(rr_filter.replace("≥ ", ""))
        def _ok(v):
            try: return float(str(v).replace("1:","")) >= thresh
            except Exception: return False
        display = display[display["Potential R:R"].apply(_ok)]

    SHOW = ["Ticker","SMT","Grade","Score","Bias","Entry","SL",
            "TP1","TP2","Potential R:R","DOL","SMT Signal","Fractal","PD Array"]
    show = display[SHOW].copy()

    # Table in card wrapper
    st.markdown('<div class="table-card">'
                '<div class="table-card-header">'
                '<span class="table-card-title">🏆 الإعدادات القابلة للتنفيذ · A+ أولاً</span>'
                f'<span style="font-size:0.8rem;color:var(--gray-400)">'
                f'{len(show)} من {len(df)} إعداد</span>'
                '</div>', unsafe_allow_html=True)

    styled = _build_styled_table(show)
    st.dataframe(styled, use_container_width=True, hide_index=True, height=460)
    st.markdown("</div>", unsafe_allow_html=True)

    # Drill-down
    st.markdown("<br>", unsafe_allow_html=True)
    sec_header("🔬", "تحليل تفصيلي", "Drill Down · Full Analysis")

    if show.empty:
        st.info("لا توجد نتائج تطابق الفلاتر الحالية.")
        app_footer(); return

    d1, d2, d3 = st.columns([2.5, 1, 1])
    with d1:
        selected = st.selectbox("اختر الرمز للتحليل / Select Symbol",
                                show["Ticker"].tolist(),
                                label_visibility="visible")
    with d2:
        st.markdown("<br>", unsafe_allow_html=True)
        drill_btn = st.button("🔬 تحميل الشارت", use_container_width=True)
    with d3:
        st.markdown("<br>", unsafe_allow_html=True)
        clear_btn = st.button("✕ مسح", use_container_width=True)

    if drill_btn and selected:
        st.session_state.selected_ticker = selected
    if clear_btn:
        st.session_state.selected_ticker = None

    if st.session_state.selected_ticker:
        _render_drill(st.session_state.selected_ticker, df, watchlist, cfg)

    app_footer()


def _render_drill(tkr, radar_df, watchlist, cfg):
    smt_pair = next((s for t,s in watchlist if t==tkr), "QQQ")
    row_data = radar_df[radar_df["Ticker"]==tkr]
    grade    = row_data["Grade"].values[0] if not row_data.empty else "—"
    gc       = grade_color_hex(grade)
    pill_html = grade_pill(grade)

    with st.spinner(f"جارٍ تحميل {tkr}…"):
        try:
            result = cached_run_engine(
                tkr, smt_pair,
                cfg["htf_interval"], cfg["exec_interval"],
                cfg["entry_interval"], cfg["htf_period"], cfg["exec_period"])
            setup, df_htf, _, _, liq_levels, swings, dol = result
            current = float(df_htf["Close"].iloc[-1])
        except Exception as ex:
            st.error(f"خطأ في الشارت: {ex}"); return

    st.markdown(f"""
    <div class="drill-badge">
      <div style="display:flex;align-items:center;gap:12px;">
        <span class="drill-sym" style="color:{gc}">{tkr}</span>
        {pill_html}
      </div>
      <div class="drill-meta">
        SMT: {smt_pair} &nbsp;·&nbsp; السعر: {current:.4f}
        &nbsp;·&nbsp; {cfg['htf_interval'].upper()}
      </div>
    </div>""", unsafe_allow_html=True)

    cc, lc = st.columns([2.6, 1], gap="medium")
    with cc:
        fig = E.build_chart(df_htf, setup, liq_levels, swings, dol,
                            ticker=tkr, n_candles=cfg["n_candles"],
                            htf_interval=cfg["htf_interval"])
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar":True,"displaylogo":False})
    with lc:
        st.markdown("<br>", unsafe_allow_html=True)
        render_decision_log(setup, current)

    if setup:
        st.markdown("<br>", unsafe_allow_html=True)
        sec_header("🎯", "خطة الصفقة", "Trade Setup & Targets")
        render_trade_table(setup)


def _run_radar_scan(watchlist, cfg):
    E.SWEEP_WICK_MIN = float(cfg["wick_min"])
    total, results = len(watchlist), []
    pb = st.progress(0, text="تهيئة الرادار…")

    def scan_one(pair):
        return cached_scan_pair(pair[0], pair[1],
                                cfg["htf_interval"], cfg["exec_interval"],
                                cfg["entry_interval"], cfg["htf_period"],
                                cfg["exec_period"])

    done = 0
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(scan_one, pair): pair for pair in watchlist}
        for fut in as_completed(futures):
            tkr, smt = futures[fut]
            try:
                row = fut.result(timeout=25)
            except TimeoutError:
                row = {"Ticker":tkr,"SMT":smt,"Grade":"TIMEOUT","Score":"—",
                       "Bias":"—","Entry":"—","SL":"—","TP1":"—","TP2":"—",
                       "Potential R:R":"—","DOL":"—","SMT Signal":"—",
                       "Fractal":"—","Killzone":"—","PD Array":"—",
                       "_score_num":-2,"_grade_rank":101}
            results.append(row)
            done += 1
            g   = row.get("Grade","?")
            sym = {"A+":"⭐","A":"✅","B":"⚠️"}.get(g,"·")
            pb.progress(done/total,
                        text=f"جارٍ المسح {done}/{total} · {tkr} {sym} {g}")

    pb.empty()
    df = (pd.DataFrame(results)
          .sort_values(by=["_grade_rank","_score_num"], ascending=[True,False])
          .reset_index(drop=True))
    st.session_state.radar_df     = df
    st.session_state.radar_preset = cfg

    n_ap = len(df[df["Grade"]=="A+"])
    n_a  = len(df[df["Grade"]=="A"])
    n_b  = len(df[df["Grade"]=="B"])
    st.success(
        f"✅ اكتمل المسح · {len(df)} سهماً  ·  "
        f"A+: {n_ap}  ·  A: {n_a}  ·  B: {n_b}")


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
def main():
    # Session state init
    for k, v in [("single_result",None),("radar_df",None),
                 ("radar_preset",None),("selected_ticker",None)]:
        if k not in st.session_state:
            st.session_state[k] = v

    # Controls (no sidebar)
    mode, ticker, smt_ticker, watchlist, preset, cfg, run_btn, scan_btn = render_controls()

    # Header (after controls so mode is known)
    render_header(mode, ticker, smt_ticker, preset, len(watchlist) if watchlist else 0)

    # Content
    if mode == "single":
        render_single(ticker, smt_ticker, cfg, run_btn)
    else:
        render_radar(watchlist, preset, cfg, scan_btn)


if __name__ == "__main__":
    main()
