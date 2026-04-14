"""
app_1.py — ICT Market Maker · Luxury Financial Dashboard
Run with:  streamlit run app_1.py
Requires:  engine.py  (unchanged)
"""

import streamlit as st
import pandas as pd
import time as _time
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

import engine as E


# ══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="ICT · Market Maker Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ══════════════════════════════════════════════════════════════
#  LUXURY CSS
# ══════════════════════════════════════════════════════════════

LUXURY_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&family=Noto+Sans+Arabic:wght@300;400;500;600&display=swap');

/* ── Palette ── */
:root {
    --ink:       #0a0b0e;
    --surface-0: #0d0f14;
    --surface-1: #12151c;
    --surface-2: #181d27;
    --surface-3: #1e2535;
    --rim:       #252d3d;
    --rim-hi:    #2e3a50;

    --gold-hi:   #c8a96e;
    --gold-mid:  #a07848;
    --gold-dim:  #5a3e20;
    --gold-glow: rgba(200,169,110,0.12);

    --jade:      #3ecf8e;
    --jade-dim:  rgba(62,207,142,0.12);
    --crimson:   #e05c6a;
    --crimson-dim:rgba(224,92,106,0.12);
    --sapphire:  #5b9cf6;
    --sapphire-dim:rgba(91,156,246,0.12);
    --amethyst:  #a78bfa;

    --text-hi:   #e8dcc8;
    --text-mid:  #8a95a8;
    --text-lo:   #3e4758;

    --font-display: 'Cormorant Garamond', Georgia, serif;
    --font-mono:    'JetBrains Mono', 'Noto Sans Arabic', monospace;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    background-color: var(--surface-0) !important;
    color: var(--text-hi) !important;
}
* { box-sizing: border-box; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: var(--ink); }
::-webkit-scrollbar-thumb {
    background: var(--gold-dim);
    border-radius: 2px;
}

/* ══════════════════════════════════════
   SIDEBAR
══════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--surface-1) !important;
    border-right: 1px solid var(--rim) !important;
}
[data-testid="stSidebar"]::before {
    content: '';
    display: block;
    height: 2px;
    background: linear-gradient(90deg,
        transparent 0%,
        var(--gold-mid) 40%,
        var(--gold-hi) 60%,
        transparent 100%);
    margin-bottom: 0;
}
[data-testid="stSidebar"] * {
    font-family: var(--font-mono) !important;
}

/* Sidebar logo area */
.sb-logo {
    padding: 22px 20px 16px;
    border-bottom: 1px solid var(--rim);
    margin-bottom: 18px;
}
.sb-logo-title {
    font-family: var(--font-display) !important;
    font-size: 1.35rem;
    font-weight: 600;
    color: var(--gold-hi);
    letter-spacing: 3px;
    line-height: 1;
}
.sb-logo-sub {
    font-family: var(--font-mono) !important;
    font-size: 0.58rem;
    color: var(--text-lo);
    letter-spacing: 2.5px;
    margin-top: 5px;
    text-transform: uppercase;
}

/* Sidebar section labels */
.sb-label {
    font-size: 0.56rem;
    color: var(--text-lo);
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
    padding-left: 1px;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--rim-hi) !important;
    color: var(--text-mid) !important;
    border-radius: 3px !important;
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: 8px 14px !important;
    transition: all 0.25s ease !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: var(--gold-hi);
    transform: scaleX(0);
    transition: transform 0.3s ease;
}
.stButton > button:hover {
    border-color: var(--gold-mid) !important;
    color: var(--gold-hi) !important;
    background: var(--gold-glow) !important;
}
.stButton > button:hover::after {
    transform: scaleX(1);
}
/* Primary / CTA button */
.stButton > button[kind="primary"],
.stButton > button[data-testid*="primary"] {
    background: var(--gold-glow) !important;
    border-color: var(--gold-mid) !important;
    color: var(--gold-hi) !important;
}
.stButton > button[kind="primary"]:hover {
    background: rgba(200,169,110,0.22) !important;
    border-color: var(--gold-hi) !important;
    box-shadow: 0 0 18px rgba(200,169,110,0.18) !important;
}

/* ── Inputs ── */
.stSelectbox label, .stTextInput label,
.stSlider label, .stRadio label,
.stCheckbox label, .stMultiSelect label {
    font-family: var(--font-mono) !important;
    font-size: 0.58rem !important;
    color: var(--text-lo) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: var(--surface-2) !important;
    border-color: var(--rim) !important;
    border-radius: 3px !important;
}
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"] > div:focus-within {
    border-color: var(--gold-mid) !important;
    box-shadow: 0 0 0 1px var(--gold-dim) !important;
}

/* ── Radio ── */
div[data-testid="stRadio"] > div {
    gap: 8px !important;
}
div[data-testid="stRadio"] label {
    background: var(--surface-2) !important;
    border: 1px solid var(--rim) !important;
    border-radius: 3px !important;
    padding: 5px 12px !important;
    font-size: 0.68rem !important;
    color: var(--text-mid) !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
    border-color: var(--gold-mid) !important;
    color: var(--gold-hi) !important;
    background: var(--gold-glow) !important;
}

/* ── Sliders ── */
div[data-testid="stSlider"] div[role="slider"] {
    background: var(--gold-hi) !important;
    border: 2px solid var(--ink) !important;
}
div[data-testid="stSlider"] div[data-testid="stSlider"] > div > div > div {
    background: linear-gradient(90deg, var(--gold-dim), var(--gold-hi)) !important;
}

/* ── Expander ── */
details summary {
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    color: var(--text-mid) !important;
    letter-spacing: 1px !important;
}
details {
    background: var(--surface-2) !important;
    border: 1px solid var(--rim) !important;
    border-radius: 4px !important;
    padding: 2px 8px !important;
}

/* ── Progress bar ── */
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, var(--gold-dim), var(--gold-hi)) !important;
    border-radius: 2px !important;
}

/* ── Dividers ── */
hr {
    border: none !important;
    border-top: 1px solid var(--rim) !important;
    margin: 10px 0 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--rim) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-lo) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border: none !important;
    padding: 8px 16px !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    color: var(--gold-hi) !important;
    border-bottom-color: var(--gold-hi) !important;
}

/* ── Alerts ── */
div[data-testid="stInfo"] {
    background: rgba(91,156,246,0.06) !important;
    border: 1px solid rgba(91,156,246,0.2) !important;
    border-radius: 4px !important;
    font-family: var(--font-mono) !important;
    font-size: 0.78rem !important;
}
div[data-testid="stSuccess"] {
    background: rgba(62,207,142,0.06) !important;
    border: 1px solid rgba(62,207,142,0.2) !important;
    border-radius: 4px !important;
    font-family: var(--font-mono) !important;
    font-size: 0.78rem !important;
}
div[data-testid="stError"] {
    background: rgba(224,92,106,0.06) !important;
    border: 1px solid rgba(224,92,106,0.25) !important;
    border-radius: 4px !important;
    font-family: var(--font-mono) !important;
    font-size: 0.78rem !important;
}

/* ── DataFrames ── */
.stDataFrame iframe { border: none !important; }
.stDataFrame > div { border-radius: 4px !important; }

/* ══════════════════════════════════════
   REUSABLE COMPONENTS
══════════════════════════════════════ */

/* Section header */
.sec-head {
    display: flex;
    align-items: center;
    gap: 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--rim);
    margin-bottom: 14px;
}
.sec-head-title {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    color: var(--text-lo);
    letter-spacing: 3px;
    text-transform: uppercase;
}
.sec-head-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--rim), transparent);
}

/* Page header */
.page-header {
    background: var(--surface-1);
    border: 1px solid var(--rim);
    border-radius: 5px;
    padding: 18px 24px 16px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg,
        transparent, var(--gold-mid) 30%,
        var(--gold-hi) 50%, var(--gold-mid) 70%, transparent);
}
.page-header::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 180px; height: 100%;
    background: radial-gradient(ellipse at top right,
        rgba(200,169,110,0.04) 0%, transparent 70%);
    pointer-events: none;
}
.ph-eyebrow {
    font-family: var(--font-mono);
    font-size: 0.55rem;
    color: var(--gold-mid);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.ph-title {
    font-family: var(--font-display);
    font-size: 1.7rem;
    font-weight: 500;
    color: var(--text-hi);
    letter-spacing: 1px;
    line-height: 1.1;
    margin: 0 0 6px 0;
}
.ph-meta {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: var(--text-lo);
    letter-spacing: 1px;
}

/* KPI card */
.kpi-wrap {
    background: var(--surface-1);
    border: 1px solid var(--rim);
    border-radius: 4px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s;
}
.kpi-wrap:hover { border-color: var(--rim-hi); }
.kpi-wrap::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
}
.kpi-label {
    font-family: var(--font-mono);
    font-size: 0.55rem;
    color: var(--text-lo);
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.kpi-value {
    font-family: var(--font-mono);
    font-size: 1.45rem;
    font-weight: 500;
    line-height: 1;
}
.kpi-sub {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    color: var(--text-lo);
    margin-top: 3px;
}

/* Grade pill */
.grade-pill {
    display: inline-block;
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 2px;
    padding: 3px 10px;
    border-radius: 2px;
}
.grade-ap {
    background: rgba(62,207,142,0.1);
    color: #3ecf8e;
    border: 1px solid rgba(62,207,142,0.25);
}
.grade-a {
    background: rgba(91,156,246,0.1);
    color: #5b9cf6;
    border: 1px solid rgba(91,156,246,0.25);
}
.grade-b {
    background: rgba(200,169,110,0.1);
    color: #c8a96e;
    border: 1px solid rgba(200,169,110,0.2);
}
.grade-skip {
    background: rgba(62,71,88,0.3);
    color: #3e4758;
    border: 1px solid rgba(62,71,88,0.4);
}

/* Radar table row colour */
.row-ap { background: rgba(62,207,142,0.04) !important; }
.row-a  { background: rgba(91,156,246,0.04) !important; }
.row-b  { background: rgba(200,169,110,0.04) !important; }

/* Decision log panel */
.dlog-panel {
    background: var(--surface-1);
    border: 1px solid var(--rim);
    border-radius: 4px;
    padding: 14px 16px;
    height: 100%;
}
.dlog-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 10px;
    margin-bottom: 10px;
    border-bottom: 1px solid var(--rim);
}
.dlog-bias {
    font-family: var(--font-display);
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 1px;
}
.dlog-score-badge {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-mid);
    letter-spacing: 1px;
}
.dlog-entry {
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--surface-2);
}
.dlog-entry:last-child { border-bottom: none; margin-bottom: 0; }
.dlog-stage-label {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    color: var(--amethyst);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 3px;
}
.dlog-finding {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--text-hi);
    margin-bottom: 2px;
}
.dlog-reason {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-lo);
    line-height: 1.5;
    margin-bottom: 2px;
}
.dlog-risk {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: #c8a96e;
    opacity: 0.85;
}
.dlog-delta {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 600;
    margin-top: 3px;
}
.dlog-pnl-block {
    background: var(--surface-0);
    border-radius: 3px;
    padding: 10px 12px;
    margin-top: 10px;
}
.dlog-pnl-label {
    font-family: var(--font-mono);
    font-size: 0.55rem;
    color: var(--text-lo);
    letter-spacing: 2px;
    text-transform: uppercase;
}
.dlog-pnl-value {
    font-family: var(--font-mono);
    font-size: 1.15rem;
    font-weight: 600;
    margin-top: 2px;
}

/* Trade levels table */
.tl-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 3px;
    font-family: var(--font-mono);
    font-size: 0.75rem;
}
.tl-table th {
    font-size: 0.55rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-lo);
    padding: 4px 10px;
    text-align: left;
    font-weight: 400;
}
.tl-table td {
    padding: 7px 10px;
    background: var(--surface-2);
    color: var(--text-mid);
}
.tl-table tr:first-child td { border-radius: 3px 3px 0 0; }
.tl-table tr:last-child td  { border-radius: 0 0 3px 3px; }
.tl-entry td { color: #5b9cf6 !important; font-weight: 600; }
.tl-sl    td { color: #e05c6a !important; }
.tl-tp    td { color: #3ecf8e !important; }

/* Skip placeholder */
.skip-placeholder {
    background: var(--surface-1);
    border: 1px solid var(--rim);
    border-radius: 4px;
    padding: 32px 20px;
    text-align: center;
}
.skip-icon {
    font-family: var(--font-display);
    font-size: 2.5rem;
    color: var(--text-lo);
    display: block;
    margin-bottom: 12px;
}
.skip-title {
    font-family: var(--font-display);
    font-size: 1.1rem;
    color: var(--text-lo);
    margin-bottom: 6px;
}
.skip-body {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-lo);
    line-height: 1.7;
    letter-spacing: 0.5px;
}

/* Drill-down ticker badge */
.drill-badge {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--surface-1);
    border: 1px solid var(--rim);
    border-radius: 4px;
    padding: 12px 18px;
    margin-bottom: 14px;
}
.drill-ticker {
    font-family: var(--font-display);
    font-size: 1.4rem;
    font-weight: 600;
    letter-spacing: 2px;
}
.drill-meta {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: var(--text-lo);
    letter-spacing: 1px;
}

/* Radar stat bar */
.stat-bar {
    display: flex;
    gap: 1px;
    margin: 12px 0 16px;
}
.stat-seg {
    flex: 1;
    height: 3px;
    border-radius: 1px;
    background: var(--rim);
    transition: background 0.4s;
}
.stat-seg.filled-ap { background: #3ecf8e; }
.stat-seg.filled-a  { background: #5b9cf6; }
.stat-seg.filled-b  { background: #c8a96e; }
.stat-seg.filled-sk { background: #3e4758; }

/* Footer */
.app-footer {
    font-family: var(--font-mono);
    font-size: 0.52rem;
    color: var(--text-lo);
    letter-spacing: 1.5px;
    text-align: center;
    padding: 20px 0 8px;
    border-top: 1px solid var(--rim);
    margin-top: 30px;
    opacity: 0.6;
}
</style>
"""

st.markdown(LUXURY_CSS, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  CACHED ENGINE CALLS  (unchanged logic)
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

def grade_color(g):
    return {"A+": "#3ecf8e", "A": "#5b9cf6",
            "B":  "#c8a96e", "C": "#6b7585"}.get(g, "#3e4758")

def grade_pill(g):
    css = {"A+": "grade-ap", "A": "grade-a",
           "B":  "grade-b"}.get(g, "grade-skip")
    return f'<span class="grade-pill {css}">{g}</span>'

def bias_html(b):
    if b == "Long":
        return f'<span style="color:#3ecf8e;font-weight:600">▲ {b}</span>'
    if b == "Short":
        return f'<span style="color:#e05c6a;font-weight:600">▼ {b}</span>'
    return f'<span style="color:#3e4758">{b}</span>'

def sec_header(title):
    st.markdown(f"""
    <div class="sec-head">
      <span class="sec-head-title">{title}</span>
      <div class="sec-head-line"></div>
    </div>""", unsafe_allow_html=True)

def kpi_card(col, label, value, color, sub=""):
    col.markdown(f"""
    <div class="kpi-wrap">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value" style="color:{color}">{value}</div>
      {"<div class='kpi-sub'>" + sub + "</div>" if sub else ""}
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════

def render_sidebar():
    with st.sidebar:

        # ── Logo ──────────────────────────────────────────────
        st.markdown("""
        <div class="sb-logo">
          <div class="sb-logo-title">◈ ICT ENGINE</div>
          <div class="sb-logo-sub">Market Maker Intelligence</div>
        </div>""", unsafe_allow_html=True)

        # ── Mode ──────────────────────────────────────────────
        st.markdown('<div class="sb-label">Mode</div>', unsafe_allow_html=True)
        mode = st.radio("", ["Single Stock", "Radar Scan"],
                        horizontal=True, label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Ticker inputs ─────────────────────────────────────
        if mode == "Single Stock":
            st.markdown('<div class="sb-label">Symbol</div>', unsafe_allow_html=True)
            ticker     = st.text_input("", value="TSLA",
                                       label_visibility="collapsed").strip().upper()
            st.markdown('<div class="sb-label">SMT Pair</div>', unsafe_allow_html=True)
            smt_ticker = st.text_input("smt", value="QQQ",
                                       label_visibility="collapsed").strip().upper()
        else:
            ticker, smt_ticker = "TSLA", "QQQ"

        # ── Watchlist (Radar only) ─────────────────────────────
        if mode == "Radar Scan":
            st.markdown('<div class="sb-label">Watchlist</div>', unsafe_allow_html=True)
            preset    = st.selectbox("wl", list(E.WATCHLIST_PRESETS.keys()),
                                     label_visibility="collapsed")
            watchlist = E.WATCHLIST_PRESETS[preset]
            st.markdown(f'<div class="sb-label" style="margin-top:4px;">'
                        f'{len(watchlist)} symbols loaded</div>',
                        unsafe_allow_html=True)
        else:
            watchlist, preset = None, None

        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()

        # ── Timeframes ────────────────────────────────────────
        st.markdown('<div class="sb-label">HTF Interval</div>', unsafe_allow_html=True)
        htf_interval = st.selectbox("htf", ["1d", "1wk", "4h", "1h"],
                                    label_visibility="collapsed")
        st.markdown('<div class="sb-label">Exec Interval</div>', unsafe_allow_html=True)
        exec_interval = st.selectbox("exec", ["15m", "30m", "1h", "5m"],
                                     label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Periods ───────────────────────────────────────────
        st.markdown('<div class="sb-label">HTF Period</div>', unsafe_allow_html=True)
        htf_period = st.selectbox("hp", ["6mo", "3mo", "1y", "2y"],
                                  label_visibility="collapsed")
        st.markdown('<div class="sb-label">Exec Period</div>', unsafe_allow_html=True)
        exec_period = st.selectbox("ep", ["5d", "10d", "1mo"],
                                   label_visibility="collapsed")

        st.divider()

        # ── Engine params ─────────────────────────────────────
        with st.expander("⚙  Engine Parameters"):
            score_min = st.slider("Min Score",    1, 13, E.SCORE_MIN)
            wick_min  = st.slider("Min Wick %",   5, 40, int(E.SWEEP_WICK_MIN))
            n_candles = st.slider("Chart Candles",40, 150, 80)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── CTA buttons ───────────────────────────────────────
        run_btn = st.button("▶  Run Analysis", type="primary",
                            use_container_width=True)
        if mode == "Radar Scan":
            scan_btn = st.button("◉  Launch Radar", use_container_width=True)
        else:
            scan_btn = False

        # ── Footer ────────────────────────────────────────────
        st.markdown("""
        <div style="font-family:var(--font-mono);font-size:0.52rem;
             color:#1e2535;text-align:center;margin-top:24px;
             letter-spacing:1px;line-height:1.8;">
          Educational use only<br>Not financial advice
        </div>""", unsafe_allow_html=True)

    cfg = dict(htf_interval=htf_interval, exec_interval=exec_interval,
               entry_interval="5m", htf_period=htf_period,
               exec_period=exec_period, score_min=score_min,
               wick_min=wick_min, n_candles=n_candles)

    if mode == "Radar Scan":
        return mode, ticker, smt_ticker, watchlist, preset, cfg, run_btn, scan_btn
    return mode, ticker, smt_ticker, None, None, cfg, run_btn, scan_btn


# ══════════════════════════════════════════════════════════════
#  SINGLE STOCK VIEW
# ══════════════════════════════════════════════════════════════

def render_single(ticker, smt_ticker, cfg, run_btn):

    # ── Page header ───────────────────────────────────────────
    st.markdown(f"""
    <div class="page-header">
      <div class="ph-eyebrow">6-Stage Protocol · ICT Smart Money</div>
      <h1 class="ph-title">{ticker}
        <span style="color:var(--gold-mid);font-size:1rem;
              font-family:var(--font-mono);letter-spacing:3px;">
          &nbsp;/&nbsp;{smt_ticker}
        </span>
      </h1>
      <div class="ph-meta">
        {cfg['htf_interval'].upper()} · {cfg['exec_interval'].upper()}
        &nbsp;·&nbsp; Period: {cfg['htf_period']}
        &nbsp;·&nbsp; Min Score: {cfg['score_min']}
      </div>
    </div>""", unsafe_allow_html=True)

    if "single_result" not in st.session_state:
        st.session_state.single_result = None

    if run_btn:
        with st.spinner(""):
            try:
                E.SWEEP_WICK_MIN = float(cfg["wick_min"])
                result = cached_run_engine(
                    ticker, smt_ticker,
                    cfg["htf_interval"], cfg["exec_interval"],
                    cfg["entry_interval"], cfg["htf_period"], cfg["exec_period"])
                st.session_state.single_result = result
            except Exception as ex:
                st.error(f"Engine error: {ex}")
                return

    result = st.session_state.single_result
    if result is None:
        st.markdown("""
        <div class="skip-placeholder">
          <span class="skip-icon">◈</span>
          <div class="skip-title">Awaiting Analysis</div>
          <div class="skip-body">
            Configure parameters in the sidebar<br>
            and press <strong>Run Analysis</strong> to begin.
          </div>
        </div>""", unsafe_allow_html=True)
        return

    setup, df_htf, df_exec, df_m5, liq_levels, swings, dol = result
    current    = float(df_htf["Close"].iloc[-1])
    price_prev = float(df_htf["Close"].iloc[-2]) if len(df_htf) > 1 else current
    chg_pct    = (current - price_prev) / price_prev * 100

    # ── KPI row ───────────────────────────────────────────────
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    chg_col = "#3ecf8e" if chg_pct >= 0 else "#e05c6a"
    sign    = "+" if chg_pct >= 0 else ""

    kpi_card(k1, "Last Price",  f"{current:.4f}",    "#5b9cf6")
    kpi_card(k2, "Change 1D",   f"{sign}{chg_pct:.2f}%", chg_col,
             "vs prior close")
    kpi_card(k3, "DOL Target",
             f"{dol.price:.4f}" if dol else "—",
             "#c8a96e",
             f"{dol.kind}" if dol else "")
    kpi_card(k4, "Bias",
             "Long" if (setup and setup.bias == "long") else
             "Short" if (setup and setup.bias == "short") else "—",
             "#3ecf8e" if (setup and setup.bias == "long") else
             "#e05c6a" if setup else "#3e4758")
    kpi_card(k5, "Grade",
             setup.grade if setup else "SKIP",
             grade_color(setup.grade if setup else "SKIP"))
    kpi_card(k6, "Score",
             f"{setup.score}/13" if setup else "—",
             "#c8a96e" if setup else "#3e4758",
             "confidence")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart  +  Decision Log ────────────────────────────────
    chart_col, log_col = st.columns([2.5, 1], gap="medium")

    with chart_col:
        sec_header("Price Action · DOL · PD Arrays")
        fig = E.build_chart(df_htf, setup, liq_levels, swings, dol,
                            ticker=ticker,
                            n_candles=cfg["n_candles"],
                            htf_interval=cfg["htf_interval"])
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar": True,
                                "displaylogo":    False,
                                "modeBarButtonsToRemove": ["select2d", "lasso2d"]})

    with log_col:
        sec_header("Decision Log")
        _render_decision_log(setup, current)

    # ── Trade Levels ──────────────────────────────────────────
    if setup:
        st.markdown("<br>", unsafe_allow_html=True)
        sec_header("Trade Setup · Standard Deviation Targets")
        _render_trade_table(setup, current)

    _app_footer()


def _render_decision_log(setup, current_price):
    if not setup:
        st.markdown("""
        <div class="dlog-panel">
          <div class="skip-placeholder" style="border:none;padding:20px 10px;">
            <span class="skip-icon" style="font-size:1.8rem;">—</span>
            <div class="skip-title" style="font-size:0.9rem;">No Setup</div>
            <div class="skip-body">Score below minimum threshold.</div>
          </div>
        </div>""", unsafe_allow_html=True)
        return

    gc       = grade_color(setup.grade)
    bias_sym = "▲ LONG" if setup.bias == "long" else "▼ SHORT"
    bias_col = "#3ecf8e" if setup.bias == "long" else "#e05c6a"
    pill_html = grade_pill(setup.grade)

    html = f"""
    <div class="dlog-panel">
      <div class="dlog-header">
        <span class="dlog-bias" style="color:{bias_col}">{bias_sym}</span>
        <span class="dlog-score-badge">
          {pill_html}&nbsp;&nbsp;{setup.score}/13
        </span>
      </div>
    """

    for entry in setup.decision_log:
        dc = ("#3ecf8e" if entry.score_delta > 0 else
              "#e05c6a" if entry.score_delta < 0 else "#3e4758")
        ds = f"+{entry.score_delta}" if entry.score_delta >= 0 else str(entry.score_delta)
        trunc_reason = entry.reasoning[:95] + ("…" if len(entry.reasoning) > 95 else "")
        risk_html = (f'<div class="dlog-risk">◆ {entry.risk_note[:85]}</div>'
                     if entry.risk_note else "")
        html += f"""
        <div class="dlog-entry">
          <div class="dlog-stage-label">{entry.stage}</div>
          <div class="dlog-finding">{entry.finding}</div>
          <div class="dlog-reason">{trunc_reason}</div>
          {risk_html}
          <div class="dlog-delta" style="color:{dc}">{ds} pts</div>
        </div>"""

    # P&L
    pnl = ((current_price - setup.entry) / setup.entry * 100
           if setup.bias == "long"
           else (setup.entry - current_price) / setup.entry * 100)
    pc  = "#3ecf8e" if pnl >= 0 else "#e05c6a"
    ps  = f"{'+' if pnl>=0 else ''}{pnl:.2f}%"

    html += f"""
      <div class="dlog-pnl-block">
        <div class="dlog-pnl-label">Unrealised P&amp;L · {current_price:.4f}</div>
        <div class="dlog-pnl-value" style="color:{pc}">{ps}</div>
      </div>
    </div>"""

    st.markdown(html, unsafe_allow_html=True)


def _render_trade_table(setup, current_price):
    sl_dist = abs(setup.entry - setup.stop_loss)
    rows    = []

    rows.append({"cls": "tl-entry", "Level": "Entry",
                 "Price": f"{setup.entry:.4f}", "Distance": "—",
                 "R:R": "ref", "Note": "FVG / OB midpoint"})
    rows.append({"cls": "tl-sl", "Level": "Stop Loss",
                 "Price": f"{setup.stop_loss:.4f}",
                 "Distance": f"{abs(setup.entry - setup.stop_loss):.4f}",
                 "R:R": "—", "Note": "Behind sweep zone"})

    for t in setup.targets:
        if t.is_tp and sl_dist > 0:
            rr = round(abs(t.price - setup.entry) / sl_dist, 2)
            rows.append({"cls": "tl-tp", "Level": t.label,
                         "Price": f"{t.price:.4f}",
                         "Distance": f"{abs(t.price - setup.entry):.4f}",
                         "R:R": f"1:{rr}",
                         "Note": f"+{t.level}σ · StdDev target"})

    html = """
    <table class="tl-table">
      <thead>
        <tr>
          <th>Level</th><th>Price</th>
          <th>Distance</th><th>R:R</th><th>Note</th>
        </tr>
      </thead>
      <tbody>"""
    for r in rows:
        html += f"""
        <tr class="{r['cls']}">
          <td>{r['Level']}</td><td>{r['Price']}</td>
          <td>{r['Distance']}</td><td>{r['R:R']}</td>
          <td>{r['Note']}</td>
        </tr>"""
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  RADAR SCAN VIEW
# ══════════════════════════════════════════════════════════════

def render_radar(watchlist, preset, cfg, scan_btn):

    st.markdown(f"""
    <div class="page-header">
      <div class="ph-eyebrow">Parallel Market Scan · Smart Money</div>
      <h1 class="ph-title">Radar Scanner</h1>
      <div class="ph-meta">
        {preset} &nbsp;·&nbsp; {len(watchlist)} symbols
        &nbsp;·&nbsp; {cfg['htf_interval'].upper()} · {cfg['exec_interval'].upper()}
      </div>
    </div>""", unsafe_allow_html=True)

    for key in ("radar_df", "radar_preset", "selected_ticker"):
        if key not in st.session_state:
            st.session_state[key] = None

    if scan_btn:
        _run_radar_scan(watchlist, cfg)

    df = st.session_state.radar_df
    if df is None:
        st.markdown("""
        <div class="skip-placeholder">
          <span class="skip-icon">◉</span>
          <div class="skip-title">Radar Offline</div>
          <div class="skip-body">
            Select a watchlist and press <strong>Launch Radar</strong><br>
            to begin the parallel market scan.
          </div>
        </div>""", unsafe_allow_html=True)
        return

    # ── Filters ───────────────────────────────────────────────
    sec_header("Filter · Sort · Search")
    fc1, fc2, fc3 = st.columns([2, 1, 1])
    with fc1:
        grade_filter = st.multiselect(
            "Grade", ["A+", "A", "B", "C"],
            default=["A+", "A"], label_visibility="visible")
    with fc2:
        bias_filter = st.selectbox("Bias", ["All", "Long", "Short"])
    with fc3:
        search = st.text_input("Symbol", placeholder="AAPL")

    display = df.copy()
    if grade_filter:
        display = display[display["Grade"].isin(grade_filter)]
    if bias_filter != "All":
        display = display[display["Bias"] == bias_filter]
    if search:
        display = display[display["Ticker"].str.contains(search.upper(), na=False)]

    SHOW_COLS = ["Ticker", "SMT", "Grade", "Score", "Bias",
                 "Entry", "SL", "TP1", "TP2", "Potential R:R",
                 "DOL", "SMT Signal", "Fractal", "Killzone", "PD Array"]
    show = display[SHOW_COLS].copy()

    # ── KPI row ───────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    n_ap   = len(df[df["Grade"] == "A+"])
    n_a    = len(df[df["Grade"] == "A"])
    n_b    = len(df[df["Grade"] == "B"])
    n_skip = len(df[df["Grade"].isin(["SKIP", "ERR", "TIMEOUT"])])
    n_long = len(df[df["Bias"] == "Long"])

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    kpi_card(k1, "Total Scanned", len(df),    "#5b9cf6")
    kpi_card(k2, "Grade A+",      n_ap,       "#3ecf8e", "elite setups")
    kpi_card(k3, "Grade A",       n_a,        "#5b9cf6", "strong setups")
    kpi_card(k4, "Grade B",       n_b,        "#c8a96e", "developing")
    kpi_card(k5, "Long Bias",     n_long,     "#3ecf8e")
    kpi_card(k6, "Skip / Error",  n_skip,     "#3e4758")

    # ── Visual grade distribution bar ─────────────────────────
    total = max(len(df), 1)
    segs = []
    for g, css in [("A+","ap"),("A","a"),("B","b")]:
        cnt = len(df[df["Grade"] == g])
        segs += [f'<div class="stat-seg filled-{css}"></div>'] * max(cnt, 0)
    segs += ['<div class="stat-seg filled-sk"></div>'] * max(n_skip, 0)
    st.markdown(f'<div class="stat-bar">{"".join(segs[:70])}</div>',
                unsafe_allow_html=True)

    # ── Styled Radar Table ────────────────────────────────────
    sec_header("Actionable Setups · A+ First")

    def style_grade(val):
        return {"A+": "color:#3ecf8e;font-weight:700;background:rgba(62,207,142,0.07)",
                "A":  "color:#5b9cf6;font-weight:700;background:rgba(91,156,246,0.07)",
                "B":  "color:#c8a96e;font-weight:600;background:rgba(200,169,110,0.06)",
                "SKIP": "color:#3e4758", "ERR": "color:#e05c6a",
                }.get(str(val), "color:#484f58")

    def style_bias(val):
        if "Long"  in str(val): return "color:#3ecf8e;font-weight:600"
        if "Short" in str(val): return "color:#e05c6a;font-weight:600"
        return "color:#3e4758"

    def style_rr(val):
        try:
            ratio = float(str(val).replace("1:", ""))
            if ratio >= 3:   return "color:#3ecf8e;font-weight:600"
            if ratio >= 2:   return "color:#c8a96e"
            return "color:#5a6478"
        except Exception:
            return "color:#3e4758"

    def style_fractal(val):
        if "H1+M15+M5" in str(val):
            return "color:#3ecf8e"
        if "H1+M15" in str(val):
            return "color:#c8a96e"
        return "color:#3e4758"

    def style_smt(val):
        if "Div" in str(val):
            return "color:#a78bfa;font-weight:600"
        return "color:#3e4758"

    styled = (show.style
              .applymap(style_grade,   subset=["Grade"])
              .applymap(style_bias,    subset=["Bias"])
              .applymap(style_rr,      subset=["Potential R:R"])
              .applymap(style_fractal, subset=["Fractal"])
              .applymap(style_smt,     subset=["SMT Signal"])
              .set_properties(**{
                  "font-family": "JetBrains Mono, monospace",
                  "font-size":   "11.5px",
                  "background":  "#12151c",
              })
              .set_table_styles([
                  {"selector": "thead th",
                   "props": "background:#0d0f14;color:#3e4758;font-size:10px;"
                            "letter-spacing:1.5px;text-transform:uppercase;"
                            "padding:8px 10px;"},
                  {"selector": "tbody tr:hover td",
                   "props": "background:#1e2535 !important;"},
                  {"selector": "tbody td",
                   "props": "border-bottom:1px solid #181d27;padding:7px 10px;"},
              ]))

    st.dataframe(styled, use_container_width=True,
                 hide_index=True, height=440)

    # ── Drill-Down ────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    sec_header("Drill Down · Full Analysis")

    if show.empty:
        st.markdown('<div class="skip-body" style="text-align:center;padding:16px;">'
                    'No results match current filters.</div>',
                    unsafe_allow_html=True)
        return

    dcol1, dcol2 = st.columns([3, 1])
    with dcol1:
        selected = st.selectbox(
            "Select symbol", show["Ticker"].tolist(),
            label_visibility="visible")
    with dcol2:
        st.markdown("<br>", unsafe_allow_html=True)
        drill_btn = st.button("◈  Load Chart", use_container_width=True)

    if drill_btn and selected:
        st.session_state.selected_ticker = selected

    if st.session_state.selected_ticker:
        _render_drill_down(st.session_state.selected_ticker, df,
                           watchlist, cfg)

    _app_footer()


def _render_drill_down(tkr, radar_df, watchlist, cfg):
    smt_pair = next((s for t, s in watchlist if t == tkr), "QQQ")
    row_data = radar_df[radar_df["Ticker"] == tkr]
    grade    = row_data["Grade"].values[0] if not row_data.empty else "—"
    gc       = grade_color(grade)

    with st.spinner(""):
        try:
            result = cached_run_engine(
                tkr, smt_pair,
                cfg["htf_interval"], cfg["exec_interval"],
                cfg["entry_interval"], cfg["htf_period"], cfg["exec_period"])
            setup, df_htf, _, _, liq_levels, swings, dol = result
            current = float(df_htf["Close"].iloc[-1])
        except Exception as ex:
            st.error(f"Chart error: {ex}")
            return

    pill_html = grade_pill(grade)
    st.markdown(f"""
    <div class="drill-badge">
      <div>
        <span class="drill-ticker" style="color:{gc}">{tkr}</span>
        &nbsp;&nbsp;{pill_html}
      </div>
      <div class="drill-meta">
        SMT: {smt_pair} &nbsp;·&nbsp; {current:.4f}
        &nbsp;·&nbsp; {cfg['htf_interval'].upper()}
      </div>
    </div>""", unsafe_allow_html=True)

    cc, lc = st.columns([2.5, 1], gap="medium")
    with cc:
        sec_header("Price Action Chart")
        fig = E.build_chart(df_htf, setup, liq_levels, swings, dol,
                            ticker=tkr,
                            n_candles=cfg["n_candles"],
                            htf_interval=cfg["htf_interval"])
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar": True,
                                "displaylogo":    False})
    with lc:
        sec_header("Decision Log")
        _render_decision_log(setup, current)

    if setup:
        st.markdown("<br>", unsafe_allow_html=True)
        sec_header("Trade Setup · Standard Deviation Targets")
        _render_trade_table(setup, current)


def _run_radar_scan(watchlist, cfg):
    E.SWEEP_WICK_MIN = float(cfg["wick_min"])
    total   = len(watchlist)
    results = []
    pb = st.progress(0, text="Initialising radar…")

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
                row = {"Ticker": tkr, "SMT": smt, "Grade": "TIMEOUT",
                       "Score": "—", "Bias": "—", "Entry": "—",
                       "SL": "—", "TP1": "—", "TP2": "—",
                       "Potential R:R": "—", "DOL": "—",
                       "SMT Signal": "—", "Fractal": "—",
                       "Killzone": "—", "PD Array": "—",
                       "_score_num": -2, "_grade_rank": 101}
            results.append(row)
            done += 1
            g = row.get("Grade", "?")
            gc_sym = {"A+": "◈", "A": "◆", "B": "◇"}.get(g, "·")
            pb.progress(done / total,
                        text=f"Scanning {done}/{total}  ·  {tkr} {gc_sym} {g}")

    pb.empty()

    df = pd.DataFrame(results)
    df = df.sort_values(by=["_grade_rank", "_score_num"],
                        ascending=[True, False]).reset_index(drop=True)
    st.session_state.radar_df     = df
    st.session_state.radar_preset = cfg

    n_ap = len(df[df["Grade"] == "A+"])
    n_a  = len(df[df["Grade"] == "A"])
    n_b  = len(df[df["Grade"] == "B"])
    st.success(
        f"Scan complete · {len(df)} symbols  "
        f"·  A+: {n_ap}  ·  A: {n_a}  ·  B: {n_b}")


# ══════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════

def _app_footer():
    st.markdown("""
    <div class="app-footer">
      ICT MARKET MAKER ENGINE &nbsp;·&nbsp; EDUCATIONAL USE ONLY
      &nbsp;·&nbsp; NOT FINANCIAL ADVICE
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════

def main():
    out = render_sidebar()
    mode, ticker, smt_ticker, watchlist, preset, cfg, run_btn, scan_btn = \
        out if len(out) == 8 else out + (None,) * (8 - len(out))

    if mode == "Single Stock":
        render_single(ticker, smt_ticker, cfg, run_btn)
    else:
        render_radar(watchlist, preset, cfg, scan_btn)


if __name__ == "__main__":
    main()
