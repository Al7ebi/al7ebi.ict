"""
app_1.py — منصة رادار ICT الاحترافية
Professional Arabic ICT Dashboard  v3
Run: streamlit run app_1.py   |   Requires: engine.py (unchanged)
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import engine as E

# ══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="منصة رادار ICT الاحترافية",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════
#  DESIGN SYSTEM — CSS
# ══════════════════════════════════════════════════════════════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');

:root {
  --page-bg:#F0F2F5; --card-bg:#FFFFFF; --border:#E5E7EB; --border-soft:#F3F4F6;
  --blue:#4F46E5; --blue-l:#EEF2FF;
  --violet:#7C3AED; --violet-l:#F5F3FF;
  --green:#10B981; --green-l:#ECFDF5;
  --red:#EF4444;   --red-l:#FEF2F2;
  --amber:#F59E0B; --amber-l:#FFFBEB;
  --teal:#14B8A6;  --teal-l:#F0FDFA;
  --purple:#8B5CF6;--purple-l:#F5F3FF;
  --g900:#111827; --g700:#374151; --g500:#6B7280; --g400:#9CA3AF;
  --g200:#E5E7EB; --g100:#F3F4F6; --g50:#F9FAFB;
  --r-sm:8px; --r-md:12px; --r-lg:16px; --r-xl:20px;
  --sh-sm:0 1px 3px rgba(0,0,0,.08);
  --sh-md:0 4px 12px rgba(0,0,0,.09);
  --font:'Tajawal','Noto Sans Arabic',sans-serif;
}

html, body, [class*="css"] {
  background-color:var(--page-bg)!important;
  font-family:var(--font)!important;
  color:var(--g900)!important;
  direction:rtl!important;
}
* { box-sizing:border-box; }
[data-testid="collapsedControl"],
[data-testid="stSidebar"],
section[data-testid="stSidebar"] { display:none!important; }
.main .block-container { padding:0 1.25rem 3rem!important; max-width:1440px!important; }
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-thumb { background:var(--g200); border-radius:4px; }

/* ── TOP NAV ── */
.topnav {
  background:linear-gradient(135deg,#4F46E5 0%,#7C3AED 100%);
  padding:0 28px; height:64px;
  display:flex; align-items:center; justify-content:space-between;
  margin:0 -1.25rem 0;
  box-shadow:0 2px 12px rgba(79,70,229,.35);
}
.topnav-brand { display:flex; align-items:center; gap:12px; }
.topnav-logo {
  width:40px; height:40px; background:rgba(255,255,255,.18);
  border-radius:var(--r-md); display:flex; align-items:center;
  justify-content:center; font-size:1.3rem;
}
.topnav-title { font-size:1.2rem; font-weight:800; color:#fff; white-space:nowrap; }
.topnav-sub   { font-size:.68rem; color:rgba(255,255,255,.65);
                letter-spacing:1.5px; text-transform:uppercase; }
.topnav-actions { display:flex; align-items:center; gap:10px; }
.nav-badge {
  background:rgba(255,255,255,.15); border:1px solid rgba(255,255,255,.25);
  border-radius:20px; padding:4px 14px; font-size:.75rem;
  color:rgba(255,255,255,.9); white-space:nowrap;
}
.outdated-badge {
  background:#FEF2F2; border:1px solid #FECACA;
  border-radius:20px; padding:5px 14px; font-size:.8rem;
  font-weight:700; color:#DC2626;
  animation:pulse-red 2s infinite;
}
@keyframes pulse-red {
  0%,100% { box-shadow:0 0 0 0 rgba(239,68,68,0); }
  50%      { box-shadow:0 0 0 5px rgba(239,68,68,.15); }
}
.fresh-badge {
  background:#ECFDF5; border:1px solid #A7F3D0;
  border-radius:20px; padding:5px 14px;
  font-size:.8rem; font-weight:700; color:#059669;
}

/* ── CONTROL BAR ── */
.ctrl-bar {
  background:var(--card-bg); border-radius:var(--r-lg);
  box-shadow:var(--sh-sm); border:1px solid var(--border);
  padding:16px 22px; margin:18px 0 6px;
}
.ctrl-bar-title {
  font-size:.68rem; font-weight:600; color:var(--g400);
  letter-spacing:1.5px; text-transform:uppercase; margin-bottom:10px;
}

/* Widget overrides */
.stSelectbox label,.stTextInput label,.stMultiSelect label,.stSlider label,.stRadio label {
  font-family:var(--font)!important; font-size:.8rem!important;
  font-weight:500!important; color:var(--g500)!important; }
div[data-baseweb="select"]>div {
  background:var(--g50)!important; border:1px solid var(--g200)!important;
  border-radius:var(--r-sm)!important; font-family:var(--font)!important; font-size:.9rem!important; }
div[data-baseweb="select"]>div:focus-within {
  border-color:var(--blue)!important; box-shadow:0 0 0 3px rgba(79,70,229,.12)!important; }
div[data-baseweb="input"]>div {
  background:var(--g50)!important; border:1px solid var(--g200)!important;
  border-radius:var(--r-sm)!important; font-family:var(--font)!important; }
div[data-baseweb="input"]>div:focus-within {
  border-color:var(--blue)!important; box-shadow:0 0 0 3px rgba(79,70,229,.12)!important; }

/* Buttons */
.stButton>button {
  font-family:var(--font)!important; font-size:.9rem!important;
  font-weight:700!important; border-radius:var(--r-sm)!important;
  padding:10px 22px!important; transition:all .2s!important; border:none!important; }
.stButton>button:not([kind="primary"]) {
  background:var(--g100)!important; color:var(--g700)!important;
  border:1px solid var(--g200)!important; }
.stButton>button[kind="primary"] {
  background:linear-gradient(135deg,#4F46E5,#7C3AED)!important;
  color:#fff!important; box-shadow:0 4px 14px rgba(79,70,229,.4)!important; }
.stButton>button[kind="primary"]:hover {
  transform:translateY(-1px)!important; box-shadow:0 6px 18px rgba(79,70,229,.5)!important; }

/* Progress */
div[data-testid="stProgressBar"]>div>div {
  background:linear-gradient(90deg,#4F46E5,#7C3AED)!important; border-radius:4px!important; }
div[data-testid="stProgressBar"]>div {
  background:var(--g200)!important; border-radius:4px!important; }

/* ── SECTION HEADER ── */
.sec-head { display:flex; align-items:center; gap:12px; margin:22px 0 14px; }
.sec-icon {
  width:38px; height:38px; background:var(--blue-l);
  border-radius:var(--r-sm); display:flex; align-items:center;
  justify-content:center; font-size:1.05rem; flex-shrink:0;
}
.sec-ar  { font-size:1.12rem; font-weight:700; color:var(--g900); line-height:1.2; }
.sec-en  { font-size:.65rem; color:var(--g400); letter-spacing:1.2px; text-transform:uppercase; }
.sec-line{ flex:1; height:1px; background:linear-gradient(90deg,var(--g200),transparent); }

/* ── KPI GRID 3x2 ── */
.kpi-grid {
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:14px;
  margin-bottom:4px;
}
.kpi-card {
  background:var(--card-bg); border-radius:var(--r-md);
  padding:18px 18px 16px; box-shadow:var(--sh-sm);
  border:1px solid var(--border-soft);
  display:flex; align-items:center; gap:14px;
  transition:box-shadow .2s, transform .2s;
  position:relative; overflow:hidden;
}
.kpi-card:hover { box-shadow:var(--sh-md); transform:translateY(-1px); }
.kpi-card::after {
  content:''; position:absolute; right:0; top:0;
  width:4px; height:100%;
}
.kpi-card.blue::after   { background:var(--blue);   }
.kpi-card.green::after  { background:var(--green);  }
.kpi-card.red::after    { background:var(--red);    }
.kpi-card.amber::after  { background:var(--amber);  }
.kpi-card.violet::after { background:var(--violet); }
.kpi-card.teal::after   { background:var(--teal);   }
.kpi-card.purple::after { background:var(--purple); }
.kpi-icon {
  width:50px; height:50px; border-radius:var(--r-sm);
  display:flex; align-items:center; justify-content:center;
  font-size:1.3rem; flex-shrink:0;
}
.kpi-icon.blue   { background:var(--blue-l);   }
.kpi-icon.green  { background:var(--green-l);  }
.kpi-icon.red    { background:var(--red-l);    }
.kpi-icon.amber  { background:var(--amber-l);  }
.kpi-icon.violet { background:var(--violet-l); }
.kpi-icon.teal   { background:var(--teal-l);   }
.kpi-icon.purple { background:var(--purple-l); }
.kpi-body  { flex:1; text-align:right; min-width:0; }
.kpi-num   { font-size:1.9rem; font-weight:800; line-height:1; }
.kpi-num.blue   { color:var(--blue);   }
.kpi-num.green  { color:var(--green);  }
.kpi-num.red    { color:var(--red);    }
.kpi-num.amber  { color:var(--amber);  }
.kpi-num.violet { color:var(--violet); }
.kpi-num.teal   { color:var(--teal);   }
.kpi-num.purple { color:var(--purple); }
.kpi-ar { font-size:.9rem; font-weight:600; color:var(--g700); margin-top:3px; }
.kpi-en { font-size:.65rem; color:var(--g400); letter-spacing:.5px; text-transform:uppercase; }

/* ── GRADE PILLS ── */
.grade-pill {
  display:inline-flex; align-items:center; font-size:.72rem;
  font-weight:700; letter-spacing:1px; padding:4px 12px; border-radius:20px;
}
.gp-ap { background:#DCFCE7; color:#15803D; }
.gp-a  { background:#DBEAFE; color:#1D4ED8; }
.gp-b  { background:#FEF9C3; color:#854D0E; }
.gp-c  { background:#FEE2E2; color:#991B1B; }
.gp-sk { background:var(--g100); color:var(--g500); }

/* ── META BANNER ── */
.meta-banner {
  background:var(--card-bg); border:1px solid var(--border);
  border-radius:var(--r-md); padding:12px 20px;
  display:flex; align-items:center; justify-content:space-between;
  margin-bottom:14px; box-shadow:var(--sh-sm);
}
.meta-item { display:flex; align-items:center; gap:8px; }
.meta-label { font-size:.68rem; color:var(--g400); letter-spacing:1px; text-transform:uppercase; }
.meta-val   { font-size:.92rem; font-weight:700; color:var(--g700); }

/* ── DECISION LOG ── */
.dlog-wrap {
  background:var(--card-bg); border-radius:var(--r-md);
  box-shadow:var(--sh-sm); border:1px solid var(--border-soft); overflow:hidden;
}
.dlog-head {
  background:linear-gradient(135deg,#4F46E5,#7C3AED);
  padding:14px 18px; display:flex; align-items:center; justify-content:space-between;
}
.dlog-bias-txt { font-size:1.05rem; font-weight:700; color:#fff; }
.dlog-entry {
  padding:12px 18px; border-bottom:1px solid var(--border-soft);
  transition:background .15s;
}
.dlog-entry:last-child { border-bottom:none; }
.dlog-entry:hover { background:var(--g50); }
.dlog-stage { font-size:.6rem; font-weight:700; color:#6366F1;
              letter-spacing:2px; text-transform:uppercase; margin-bottom:3px; }
.dlog-find  { font-size:.88rem; font-weight:600; color:#1F2937; margin-bottom:2px; }
.dlog-rsn   { font-size:.76rem; color:var(--g500); line-height:1.55; }
.dlog-risk  { font-size:.73rem; color:#D97706; margin-top:3px; }
.dlog-pts   { font-size:.73rem; font-weight:700; margin-top:4px; }
.dlog-pnl   { background:var(--g50); padding:12px 18px; border-top:2px solid var(--border); }
.dlog-pnl-lbl { font-size:.62rem; color:var(--g400); letter-spacing:1.5px; text-transform:uppercase; }
.dlog-pnl-val { font-size:1.3rem; font-weight:800; margin-top:3px; }

/* ── TRADE TABLE ── */
.tl-wrap { background:var(--card-bg); border-radius:var(--r-md);
           box-shadow:var(--sh-sm); border:1px solid var(--border-soft); overflow:hidden; }
.tl-header-row {
  background:linear-gradient(135deg,#4F46E5,#7C3AED);
  padding:13px 20px; display:flex; align-items:center; justify-content:space-between;
}
.tl-header-title { font-size:.95rem; font-weight:700; color:#fff; font-family:var(--font); }
.tl-header-sub   { font-size:.62rem; color:rgba(255,255,255,.7);
                   letter-spacing:1.5px; text-transform:uppercase; }
.tl-table { width:100%; border-collapse:collapse; font-family:var(--font); }
.tl-table thead th {
  background:var(--g50); font-size:.68rem; font-weight:600; color:var(--g500);
  letter-spacing:1.5px; text-transform:uppercase; padding:11px 16px;
  text-align:right; border-bottom:2px solid var(--border); }
.tl-table tbody td {
  padding:12px 16px; font-size:.9rem; border-bottom:1px solid var(--border-soft); }
.tl-table tbody tr:last-child td { border-bottom:none; }
.tl-table tbody tr:hover td { background:var(--g50); }
.tl-entry td:first-child { color:#4F46E5; font-weight:700; }
.tl-sl    td:first-child { color:#EF4444; font-weight:700; }
.tl-tp    td:first-child { color:#10B981; font-weight:700; }
.tl-num { font-family:'JetBrains Mono','Courier New',monospace; font-size:.88rem; }

/* ── RADAR TABLE ── */
.tbl-card { background:var(--card-bg); border-radius:var(--r-md);
            box-shadow:var(--sh-sm); border:1px solid var(--border-soft); overflow:hidden; }
.tbl-card-hd {
  background:var(--g50); border-bottom:1px solid var(--border);
  padding:13px 20px; display:flex; align-items:center; justify-content:space-between;
}
.tbl-hd-ar  { font-size:.92rem; font-weight:700; color:var(--g700); }
.tbl-hd-cnt { font-size:.78rem; color:var(--g400); }
.stDataFrame iframe { border:none!important; }
.stDataFrame>div    { border:none!important; border-radius:0!important; }

/* ── STAT BAR ── */
.stat-bar { display:flex; gap:2px; height:7px; border-radius:4px; overflow:hidden; margin:8px 0 22px; }
.sap { background:#10B981; } .saa { background:#4F46E5; }
.sbb { background:#F59E0B; } .ssk { background:var(--g200); }

/* ── DRILL BADGE ── */
.drill-badge {
  background:linear-gradient(135deg,#EEF2FF,#F5F3FF);
  border:1px solid #C7D2FE; border-radius:var(--r-md);
  padding:13px 20px; display:flex; align-items:center;
  justify-content:space-between; margin-bottom:14px;
}
.drill-sym  { font-size:1.5rem; font-weight:800; color:var(--blue); letter-spacing:1px; }
.drill-meta { font-size:.75rem; color:var(--g500); }

/* ── ALERTS ── */
div[data-testid="stInfo"]    { background:#EEF2FF!important; border:1px solid #C7D2FE!important;
  border-radius:var(--r-sm)!important; color:var(--g700)!important; font-family:var(--font)!important; }
div[data-testid="stSuccess"] { background:#ECFDF5!important; border:1px solid #A7F3D0!important;
  border-radius:var(--r-sm)!important; color:var(--g700)!important; font-family:var(--font)!important; }
div[data-testid="stError"]   { background:#FEF2F2!important; border:1px solid #FECACA!important;
  border-radius:var(--r-sm)!important; color:var(--g700)!important; font-family:var(--font)!important; }

/* ── PLACEHOLDER ── */
.ph-card {
  background:var(--card-bg); border-radius:var(--r-xl);
  border:2px dashed var(--g200); padding:56px 24px;
  text-align:center; box-shadow:var(--sh-sm);
}
.ph-icon  { font-size:3rem; display:block; margin-bottom:14px; }
.ph-title { font-size:1.15rem; font-weight:700; color:#4B5563; margin-bottom:8px; }
.ph-body  { font-size:.88rem; color:var(--g400); line-height:1.8; }

/* ── FOOTER ── */
.app-footer {
  margin-top:52px; padding:22px 0 10px;
  border-top:1px solid var(--g200); text-align:center;
}
.app-footer-ar { font-size:1rem; font-weight:700; color:var(--blue); margin-bottom:4px; }
.app-footer-en { font-size:.65rem; color:var(--g400); letter-spacing:1.5px; text-transform:uppercase; }

hr { border:none!important; border-top:1px solid var(--g200)!important; margin:6px 0!important; }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════
_SS = {
    "single_result": None, "single_ts": None,
    "single_ticker": "",   "radar_df": None,
    "radar_ts": None,      "radar_preset": None,
    "selected_ticker": None,
}
for _k, _v in _SS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ══════════════════════════════════════════════════════════════
#  CACHED ENGINE  (engine.py logic unchanged)
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
        res = E.run_engine(ticker, smt_ticker,
                           htf_interval=htf_interval,
                           exec_interval=exec_interval,
                           entry_interval=entry_interval,
                           htf_period=htf_period,
                           exec_period=exec_period)
        return E.extract_row(res[0], ticker, smt_ticker)
    except Exception:
        return {"Ticker": ticker, "SMT": smt_ticker, "Grade": "ERR",
                "Score": "—", "Bias": "ERROR", "Entry": "—", "SL": "—",
                "TP1": "—", "TP2": "—", "Potential R:R": "—",
                "DOL": "—", "SMT Signal": "—", "Fractal": "—",
                "Killzone": "—", "PD Array": "—",
                "_score_num": -1, "_grade_rank": 100}


# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════
def grade_hex(g):
    return {"A+":"#10B981","A":"#4F46E5","B":"#F59E0B","C":"#EF4444"}.get(g,"#9CA3AF")

def grade_pill_html(g):
    cls = {"A+":"gp-ap","A":"gp-a","B":"gp-b","C":"gp-c"}.get(g,"gp-sk")
    return f'<span class="grade-pill {cls}">{g}</span>'

def _to_rr(v):
    try: return float(str(v).replace("1:",""))
    except Exception: return 0.0

def sec_header(icon, ar, en=""):
    en_html = f"<div class='sec-en'>{en}</div>" if en else ""
    st.markdown(
        f'<div class="sec-head">'
        f'<div class="sec-icon">{icon}</div>'
        f'<div><div class="sec-ar">{ar}</div>{en_html}</div>'
        f'<div class="sec-line"></div>'
        f'</div>', unsafe_allow_html=True)

def kpi(icon, num, ar, en, cls):
    return (f'<div class="kpi-card {cls}">'
            f'<div class="kpi-icon {cls}">{icon}</div>'
            f'<div class="kpi-body">'
            f'<div class="kpi-num {cls}">{num}</div>'
            f'<div class="kpi-ar">{ar}</div>'
            f'<div class="kpi-en">{en}</div>'
            f'</div></div>')

def freshness_badge(ts):
    if ts is None:
        return '<span class="nav-badge">&#8212;</span>'
    ts_utc = ts.astimezone(timezone.utc) if ts.tzinfo else ts.replace(tzinfo=timezone.utc)
    age_m  = (datetime.now(timezone.utc) - ts_utc).total_seconds() / 60
    ts_str = ts_utc.strftime("%H:%M UTC")
    if age_m > 240:
        return (f'<span class="outdated-badge">'
                f'&#9888;&#65039; تحليل قديم ({int(age_m//60)}h {int(age_m%60)}m)'
                f'</span>')
    return f'<span class="fresh-badge">&#9989; محدّث · {ts_str}</span>'

def app_footer():
    st.markdown(
        '<div class="app-footer">'
        '<div class="app-footer-ar">&#169; جميع الحقوق محفوظة للحبي</div>'
        '<div class="app-footer-en">'
        'ICT Professional Radar Platform · Educational Use Only · Not Financial Advice'
        '</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  TOP NAV BAR  (Home + Refresh)
# ══════════════════════════════════════════════════════════════
def render_topnav(mode, ticker, smt, preset, n_sym):
    mode_badge = "تحليل منفرد · Single" if mode == "single" else "مسح الرادار · Radar"
    ctx_badge  = f"{ticker} / {smt}" if mode == "single" else f"{preset} · {n_sym} رمز"
    ts         = st.session_state.get("single_ts" if mode == "single" else "radar_ts")
    fresh_html = freshness_badge(ts)

    st.markdown(
        f'<div class="topnav">'
        f'<div class="topnav-brand">'
        f'<div class="topnav-logo">&#128225;</div>'
        f'<div><div class="topnav-title">منصة رادار ICT الاحترافية</div>'
        f'<div class="topnav-sub">Professional ICT Radar Platform</div></div>'
        f'</div>'
        f'<div class="topnav-actions">'
        f'{fresh_html}'
        f'<span class="nav-badge">{mode_badge}</span>'
        f'<span class="nav-badge">{ctx_badge}</span>'
        f'</div></div>', unsafe_allow_html=True)

    nb1, nb2, _ = st.columns([1, 1, 10])
    with nb1:
        if st.button("🏠 رئيسية", use_container_width=True):
            for k, v in _SS.items():
                st.session_state[k] = v
            st.rerun()
    with nb2:
        if st.button("🔄 تحديث", use_container_width=True):
            cached_run_engine.clear()
            cached_scan_pair.clear()
            if mode == "single":
                st.session_state.single_result = None
                st.session_state.single_ts     = None
            else:
                st.session_state.radar_df = None
                st.session_state.radar_ts = None
            st.rerun()


# ══════════════════════════════════════════════════════════════
#  CONTROL BAR  (horizontal, no sidebar)
# ══════════════════════════════════════════════════════════════
def render_controls():
    st.markdown(
        '<div class="ctrl-bar">'
        '<div class="ctrl-bar-title">&#9881; إعدادات التحليل — Analysis Settings</div>',
        unsafe_allow_html=True)

    # Row 1 — Mode · Symbol · SMT · Watchlist · HTF · Exec · Period
    c1,c2,c3,c4,c5,c6,c7 = st.columns([1.1,1.1,0.9,1.8,0.9,0.9,0.9])
    with c1:
        raw  = st.radio("النوع / Mode", ["&#128200; سهم واحد","&#128225; رادار"],
                        horizontal=False, label_visibility="visible")
        mode = "single" if "سهم" in raw else "radar"
    with c2:
        ticker = st.text_input("الرمز / Symbol", value="TSLA",
                               placeholder="TSLA").strip().upper()
    with c3:
        smt_ticker = st.text_input("SMT Pair", value="QQQ",
                                   placeholder="QQQ").strip().upper()
    with c4:
        preset    = st.selectbox("قائمة المراقبة / Watchlist",
                                 list(E.WATCHLIST_PRESETS.keys()),
                                 disabled=(mode == "single"))
        watchlist = E.WATCHLIST_PRESETS[preset]
    with c5:
        htf_interval  = st.selectbox("الإطار / HTF",  ["1d","1wk","4h","1h"])
    with c6:
        exec_interval = st.selectbox("تنفيذ / Exec",  ["15m","30m","1h","5m"])
    with c7:
        htf_period    = st.selectbox("الفترة / Period",["6mo","3mo","1y","2y"])

    # Row 2 — Exec Period · Score · Wick · Candles · Grade Filter · Buttons
    d1,d2,d3,d4,d5,d6 = st.columns([1,1.1,1.1,1,1.8,1.6])
    with d1:
        exec_period = st.selectbox("Exec Period", ["5d","10d","1mo"])
    with d2:
        score_min = st.slider("الحد الأدنى للنقاط", 1, 13, E.SCORE_MIN)
    with d3:
        wick_min  = st.slider("Wick % Min", 5, 40, int(E.SWEEP_WICK_MIN))
    with d4:
        n_candles = st.slider("عدد الشموع", 40, 150, 80)
    with d5:
        grade_filter = st.multiselect("فلتر Grade",["A+","A","B","C"],default=["A+","A"])
    with d6:
        bc1,bc2 = st.columns(2)
        with bc1:
            run_btn  = st.button("&#9654; تحليل", type="primary",
                                 use_container_width=True, disabled=(mode=="radar"))
        with bc2:
            scan_btn = st.button("&#128225; مسح",
                                 use_container_width=True, disabled=(mode=="single"))

    st.markdown("</div>", unsafe_allow_html=True)
    cfg = dict(htf_interval=htf_interval, exec_interval=exec_interval,
               entry_interval="5m", htf_period=htf_period,
               exec_period=exec_period, score_min=score_min,
               wick_min=wick_min, n_candles=n_candles,
               grade_filter=grade_filter)
    return mode, ticker, smt_ticker, watchlist, preset, cfg, run_btn, scan_btn


# ══════════════════════════════════════════════════════════════
#  META BANNER  (symbol + timestamp + freshness badge)
# ══════════════════════════════════════════════════════════════
def render_meta_banner(ticker, smt, ts):
    ts_str = ts.strftime("%Y-%m-%d  %H:%M UTC") if ts else "—"
    ts_utc = ts.astimezone(timezone.utc) if (ts and ts.tzinfo) else (
             ts.replace(tzinfo=timezone.utc) if ts else None)
    if ts_utc:
        age_m = (datetime.now(timezone.utc) - ts_utc).total_seconds() / 60
        badge = (f'<span class="outdated-badge">&#9888;&#65039; تحليل قديم '
                 f'({int(age_m//60)}h {int(age_m%60)}m)</span>'
                 if age_m > 240 else
                 '<span class="fresh-badge">&#9989; محدّث · Fresh</span>')
    else:
        badge = '<span class="nav-badge">—</span>'

    st.markdown(
        f'<div class="meta-banner">'
        f'<div style="display:flex;gap:28px;align-items:center;flex-wrap:wrap;">'
        f'<div class="meta-item">'
        f'<span style="font-size:1.1rem;">&#128204;</span>'
        f'<div><div class="meta-label">الرمز · Symbol</div>'
        f'<div class="meta-val">{ticker} <span style="color:#9CA3AF;font-weight:400">/ {smt}</span></div>'
        f'</div></div>'
        f'<div class="meta-item">'
        f'<span style="font-size:1.1rem;">&#128336;</span>'
        f'<div><div class="meta-label">وقت التحليل · Timestamp</div>'
        f'<div class="meta-val" style="font-size:.85rem;">{ts_str}</div>'
        f'</div></div></div>'
        f'{badge}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  KPI GRIDS
# ══════════════════════════════════════════════════════════════
def render_kpi_single(setup, df_htf, dol):
    cur   = float(df_htf["Close"].iloc[-1])
    prev  = float(df_htf["Close"].iloc[-2]) if len(df_htf) > 1 else cur
    chg   = (cur - prev) / prev * 100
    sign  = "+" if chg >= 0 else ""
    chg_c = "green" if chg >= 0 else "red"
    bias_val = "صعودي &#9650;" if (setup and setup.bias=="long")  else \
               "هبوطي &#9660;" if (setup and setup.bias=="short") else "—"
    bias_c   = "green" if (setup and setup.bias=="long") else \
               "red"   if (setup and setup.bias=="short") else "teal"
    grade_c  = {"A+":"green","A":"blue","B":"amber"}.get(
                setup.grade if setup else "", "teal")
    cards = (
        kpi("&#128176;", f"{cur:.2f}",        "آخر سعر",        "Last Price",  "blue")  +
        kpi("&#128202;", f"{sign}{chg:.2f}%",  "التغيير اليومي", "Daily Change", chg_c) +
        kpi("&#127919;", f"{dol.price:.2f}" if dol else "—",
                                               "هدف السيولة",    "DOL Target",  "amber") +
        kpi("&#9878;&#65039;", bias_val,       "التحيز",         "Bias",        bias_c) +
        kpi("&#127942;", setup.grade if setup else "SKIP",
                                               "التقييم",        "Grade",       grade_c) +
        kpi("&#128200;", f"{setup.score}/13" if setup else "—",
                                               "النقاط",         "Score",       "violet")
    )
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)


def render_kpi_radar(df):
    n_ap   = len(df[df["Grade"]=="A+"])
    n_a    = len(df[df["Grade"]=="A"])
    n_b    = len(df[df["Grade"]=="B"])
    n_long = len(df[df["Bias"]=="Long"])
    n_skip = len(df[df["Grade"].isin(["SKIP","ERR","TIMEOUT"])])
    n_rr3  = sum(1 for v in df["Potential R:R"] if _to_rr(v) >= 3)
    cards = (
        kpi("&#128269;", len(df),   "إجمالي المسح",  "Total Scanned",   "blue")  +
        kpi("&#11088;",  n_ap,       "إعدادات A+",    "Grade A+ Setups", "green") +
        kpi("&#9989;",   n_a,        "إعدادات A",     "Grade A Setups",  "blue")  +
        kpi("&#9888;&#65039;", n_b,  "إعدادات B",     "Grade B Setups",  "amber") +
        kpi("&#9650;",   n_long,     "توجه صعودي",    "Long Bias",       "teal")  +
        kpi("&#9889;",   n_rr3,      "R:R أعلى من 3", "R:R >= 3",        "violet")
    )
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)
    segs = (["<div class='stat-seg sap'></div>"] * n_ap +
            ["<div class='stat-seg saa'></div>"] * n_a  +
            ["<div class='stat-seg sbb'></div>"] * n_b  +
            ["<div class='stat-seg ssk'></div>"] * n_skip)
    st.markdown(f'<div class="stat-bar">{"".join(segs[:100])}</div>',
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  DECISION LOG
# ══════════════════════════════════════════════════════════════
def render_decision_log(setup, current_price):
    if not setup:
        st.markdown(
            '<div class="dlog-wrap"><div style="padding:32px;text-align:center;">'
            '<div style="font-size:2.5rem;margin-bottom:12px;">&#128141;</div>'
            '<div style="font-size:1rem;font-weight:700;color:#6B7280;">لا يوجد إعداد صفقة</div>'
            '<div style="font-size:.8rem;color:#9CA3AF;margin-top:6px;">'
            'النقاط أقل من الحد الأدنى</div>'
            '</div></div>', unsafe_allow_html=True)
        return

    bias_ar  = "&#9650; شراء LONG"  if setup.bias=="long"  else "&#9660; بيع SHORT"
    pill_html = grade_pill_html(setup.grade)

    html = (f'<div class="dlog-wrap">'
            f'<div class="dlog-head">'
            f'<span class="dlog-bias-txt">{bias_ar}</span>'
            f'<span style="display:flex;align-items:center;gap:8px;">{pill_html}'
            f'<span style="background:rgba(255,255,255,.2);border-radius:12px;'
            f'padding:3px 10px;font-size:.75rem;color:#fff;">'
            f'{setup.score}/13</span></span></div>')

    for entry in setup.decision_log:
        dc = ("#10B981" if entry.score_delta>0 else
              "#EF4444" if entry.score_delta<0 else "#9CA3AF")
        ds = f"+{entry.score_delta}" if entry.score_delta >= 0 else str(entry.score_delta)
        tr = entry.reasoning[:105] + ("…" if len(entry.reasoning) > 105 else "")
        rh = f'<div class="dlog-risk">&#9888; {entry.risk_note[:90]}</div>' if entry.risk_note else ""
        html += (f'<div class="dlog-entry">'
                 f'<div class="dlog-stage">{entry.stage}</div>'
                 f'<div class="dlog-find">{entry.finding}</div>'
                 f'<div class="dlog-rsn">{tr}</div>{rh}'
                 f'<div class="dlog-pts" style="color:{dc}">{ds} نقطة</div>'
                 f'</div>')

    pnl = ((current_price - setup.entry)/setup.entry*100
           if setup.bias=="long"
           else (setup.entry - current_price)/setup.entry*100)
    pc  = "#10B981" if pnl >= 0 else "#EF4444"
    ps  = f"{'+' if pnl>=0 else ''}{pnl:.2f}%"
    html += (f'<div class="dlog-pnl">'
             f'<div class="dlog-pnl-lbl">الربح / الخسارة غير المحقق · Unrealised P&L</div>'
             f'<div class="dlog-pnl-val" style="color:{pc}">{ps}</div>'
             f'</div></div>')
    st.markdown(html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  TRADE TABLE  (with symbol + timestamp + outdated badge)
# ══════════════════════════════════════════════════════════════
def render_trade_table(setup, ticker, ts):
    sl_dist = abs(setup.entry - setup.stop_loss)
    ts_str  = ts.strftime("%Y-%m-%d %H:%M UTC") if ts else "—"

    # Build outdated indicator for the header
    if ts:
        ts_utc = ts.astimezone(timezone.utc) if ts.tzinfo else ts.replace(tzinfo=timezone.utc)
        age_m  = (datetime.now(timezone.utc) - ts_utc).total_seconds() / 60
        ts_badge = (f'<span style="background:#FEF2F2;border:1px solid #FECACA;'
                    f'border-radius:12px;padding:2px 10px;font-size:.7rem;color:#DC2626;">'
                    f'&#9888;&#65039; قديم</span>' if age_m > 240 else
                    f'<span style="background:#ECFDF5;border:1px solid #A7F3D0;'
                    f'border-radius:12px;padding:2px 10px;font-size:.7rem;color:#059669;">'
                    f'&#9989; محدّث</span>')
    else:
        ts_badge = ""

    rows = [
        {"cls":"tl-entry","Level":"الدخول  Entry",
         "Price":f"{setup.entry:.4f}","Dist":"—","RR":"مرجع","Note":"FVG / OB midpoint"},
        {"cls":"tl-sl","Level":"وقف الخسارة  Stop Loss",
         "Price":f"{setup.stop_loss:.4f}",
         "Dist":f"{abs(setup.entry-setup.stop_loss):.4f}","RR":"—","Note":"وراء منطقة Sweep"},
    ]
    for t in setup.targets:
        if t.is_tp and sl_dist > 0:
            rr = round(abs(t.price - setup.entry) / sl_dist, 2)
            rows.append({
                "cls":"tl-tp","Level":f"هدف  {t.label}",
                "Price":f"{t.price:.4f}",
                "Dist":f"{abs(t.price-setup.entry):.4f}",
                "RR":f"1:{rr}","Note":f"+{t.level}σ من نطاق التلاعب"})

    html = (f'<div class="tl-wrap">'
            f'<div class="tl-header-row">'
            f'<div>'
            f'<div class="tl-header-title">&#127919; خطة الصفقة · Trade Plan</div>'
            f'<div class="tl-header-sub">Trade Setup &amp; StdDev Targets</div>'
            f'</div>'
            f'<div style="display:flex;gap:18px;align-items:center;">'
            f'<div style="text-align:center;">'
            f'<div class="tl-header-sub">الرمز</div>'
            f'<div style="font-size:1rem;font-weight:800;color:#fff;">{ticker}</div>'
            f'</div>'
            f'<div style="text-align:center;">'
            f'<div class="tl-header-sub">التوقيت</div>'
            f'<div style="font-size:.78rem;color:rgba(255,255,255,.85);">{ts_str}</div>'
            f'</div>'
            f'<div>{ts_badge}</div>'
            f'</div></div>'
            f'<table class="tl-table"><thead><tr>'
            f'<th>المستوى</th><th>السعر</th><th>المسافة</th><th>R:R</th><th>الملاحظة</th>'
            f'</tr></thead><tbody>')
    for r in rows:
        html += (f'<tr class="{r["cls"]}">'
                 f'<td>{r["Level"]}</td>'
                 f'<td class="tl-num">{r["Price"]}</td>'
                 f'<td class="tl-num">{r["Dist"]}</td>'
                 f'<td><b>{r["RR"]}</b></td>'
                 f'<td>{r["Note"]}</td></tr>')
    html += "</tbody></table></div>"
    st.markdown(html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  RADAR TABLE  (.map not .applymap)
# ══════════════════════════════════════════════════════════════
def _styled_radar(show):
    def sg(v):
        return {"A+":"background-color:#DCFCE7;color:#15803D;font-weight:700",
                "A": "background-color:#DBEAFE;color:#1D4ED8;font-weight:700",
                "B": "background-color:#FEF9C3;color:#854D0E;font-weight:600",
                "SKIP":"color:#9CA3AF","ERR":"color:#EF4444"}.get(str(v),"color:#6B7280")
    def sb(v):
        if "Long"  in str(v): return "color:#10B981;font-weight:700"
        if "Short" in str(v): return "color:#EF4444;font-weight:700"
        return "color:#9CA3AF"
    def sr(v):
        r = _to_rr(v)
        return ("color:#10B981;font-weight:700" if r>=3 else
                "color:#F59E0B" if r>=2 else "color:#9CA3AF")
    def sf(v):
        return ("color:#10B981;font-weight:600" if "H1+M15+M5" in str(v) else
                "color:#F59E0B" if "H1+M15" in str(v) else "color:#9CA3AF")
    def ss(v):
        return "color:#7C3AED;font-weight:600" if "Div" in str(v) else "color:#9CA3AF"

    # .map() — NOT .applymap()
    return (show.style
            .map(sg, subset=["Grade"])
            .map(sb, subset=["Bias"])
            .map(sr, subset=["Potential R:R"])
            .map(sf, subset=["Fractal"])
            .map(ss, subset=["SMT Signal"])
            .set_properties(**{"font-family":"'Tajawal',sans-serif",
                               "font-size":"13px","text-align":"right"})
            .set_table_styles([
                {"selector":"thead th",
                 "props":"background:#F9FAFB;color:#6B7280;font-size:11px;"
                         "font-weight:600;letter-spacing:1px;text-transform:uppercase;"
                         "padding:10px 14px;border-bottom:2px solid #E5E7EB;text-align:right;"},
                {"selector":"tbody td",
                 "props":"padding:10px 14px;border-bottom:1px solid #F3F4F6;"},
                {"selector":"tbody tr:hover td","props":"background-color:#F9FAFB;"},
            ]))


# ══════════════════════════════════════════════════════════════
#  SINGLE STOCK VIEW
# ══════════════════════════════════════════════════════════════
def render_single(ticker, smt_ticker, cfg, run_btn):
    if run_btn:
        with st.spinner("جارٍ تشغيل المحرك الكامل…"):
            try:
                E.SWEEP_WICK_MIN = float(cfg["wick_min"])
                result = cached_run_engine(
                    ticker, smt_ticker,
                    cfg["htf_interval"], cfg["exec_interval"],
                    cfg["entry_interval"], cfg["htf_period"], cfg["exec_period"])
                st.session_state.single_result = result
                st.session_state.single_ts     = datetime.now(timezone.utc)
                st.session_state.single_ticker = ticker
            except Exception as ex:
                st.error(f"خطأ في المحرك: {ex}"); return

    result = st.session_state.single_result
    if result is None:
        st.markdown(
            '<div class="ph-card">'
            '<span class="ph-icon">&#128202;</span>'
            '<div class="ph-title">في انتظار التحليل · Awaiting Analysis</div>'
            '<div class="ph-body">اضبط المعاملات في شريط الأدوات أعلاه<br>'
            'واضغط <strong>&#9654; تحليل</strong> لبدء التحليل</div>'
            '</div>', unsafe_allow_html=True)
        app_footer(); return

    setup, df_htf, df_exec, df_m5, liq_levels, swings, dol = result
    current = float(df_htf["Close"].iloc[-1])
    ts      = st.session_state.single_ts
    sym     = st.session_state.single_ticker or ticker

    render_meta_banner(sym, smt_ticker, ts)
    sec_header("&#128202;", "المؤشرات الرئيسية", "Key Metrics")
    render_kpi_single(setup, df_htf, dol)
    st.markdown("<br>", unsafe_allow_html=True)

    sec_header("&#128200;", "حركة السعر والمستويات", "Price Action & Levels")
    cc, lc = st.columns([2.6, 1], gap="medium")
    with cc:
        fig = E.build_chart(df_htf, setup, liq_levels, swings, dol,
                            ticker=sym, n_candles=cfg["n_candles"],
                            htf_interval=cfg["htf_interval"])
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar":True,"displaylogo":False,
                                "modeBarButtonsToRemove":["select2d","lasso2d"]})
    with lc:
        st.markdown("<br>", unsafe_allow_html=True)
        render_decision_log(setup, current)

    if setup:
        st.markdown("<br>", unsafe_allow_html=True)
        render_trade_table(setup, sym, ts)

    app_footer()


# ══════════════════════════════════════════════════════════════
#  RADAR SCAN VIEW
# ══════════════════════════════════════════════════════════════
def render_radar(watchlist, preset, cfg, scan_btn):
    if scan_btn:
        _run_scan(watchlist, cfg)

    df = st.session_state.radar_df
    if df is None:
        st.markdown(
            '<div class="ph-card">'
            '<span class="ph-icon">&#128225;</span>'
            '<div class="ph-title">الرادار في وضع الاستعداد · Radar Standby</div>'
            '<div class="ph-body">اختر قائمة المراقبة واضغط <strong>&#128225; مسح</strong></div>'
            '</div>', unsafe_allow_html=True)
        app_footer(); return

    sec_header("&#128202;", "نتائج المسح", "Scan Summary")
    render_kpi_radar(df)

    f1, f2, f3 = st.columns([2, 1, 1])
    with f1: search      = st.text_input("&#128269; بحث بالرمز / Symbol Search", placeholder="AAPL")
    with f2: bias_filter = st.selectbox("التوجه / Bias", ["الكل","Long","Short"])
    with f3: rr_filter   = st.selectbox("الحد الأدنى R:R", ["الكل","&#8805; 1.5","&#8805; 2","&#8805; 3"])

    display = df.copy()
    gf = cfg.get("grade_filter", ["A+","A"])
    if gf:              display = display[display["Grade"].isin(gf)]
    if bias_filter != "الكل": display = display[display["Bias"] == bias_filter]
    if search:          display = display[display["Ticker"].str.contains(search.upper(), na=False)]
    rr_map = {"&#8805; 1.5":1.5,"&#8805; 2":2.0,"&#8805; 3":3.0}
    if rr_filter in rr_map:
        thr = rr_map[rr_filter]
        display = display[display["Potential R:R"].apply(lambda v: _to_rr(v) >= thr)]

    SHOW = ["Ticker","SMT","Grade","Score","Bias","Entry","SL",
            "TP1","TP2","Potential R:R","DOL","SMT Signal","Fractal","PD Array"]
    show = display[SHOW].copy()

    st.markdown(
        f'<div class="tbl-card">'
        f'<div class="tbl-card-hd">'
        f'<span class="tbl-hd-ar">&#127942; الإعدادات القابلة للتنفيذ · A+ أولاً</span>'
        f'<span class="tbl-hd-cnt">{len(show)} من {len(df)} إعداد</span>'
        f'</div>', unsafe_allow_html=True)
    st.dataframe(_styled_radar(show), use_container_width=True,
                 hide_index=True, height=468)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec_header("&#128300;", "تحليل تفصيلي", "Drill Down · Full Analysis")

    if show.empty:
        st.info("لا توجد نتائج تطابق الفلاتر الحالية.")
        app_footer(); return

    d1, d2, d3 = st.columns([2.5, 1, 1])
    with d1: selected  = st.selectbox("اختر الرمز / Select Symbol", show["Ticker"].tolist())
    with d2:
        st.markdown("<br>", unsafe_allow_html=True)
        drill_btn = st.button("&#128300; تحميل الشارت", use_container_width=True)
    with d3:
        st.markdown("<br>", unsafe_allow_html=True)
        clear_btn = st.button("&#10005; مسح", use_container_width=True)

    if drill_btn and selected: st.session_state.selected_ticker = selected
    if clear_btn:               st.session_state.selected_ticker = None

    if st.session_state.selected_ticker:
        _render_drill(st.session_state.selected_ticker, df, watchlist, cfg)

    app_footer()


def _render_drill(tkr, radar_df, watchlist, cfg):
    smt_pair = next((s for t,s in watchlist if t==tkr), "QQQ")
    row_data = radar_df[radar_df["Ticker"]==tkr]
    grade    = row_data["Grade"].values[0] if not row_data.empty else "—"
    gc       = grade_hex(grade)

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

    ts = st.session_state.get("radar_ts")
    pill_html = grade_pill_html(grade)
    st.markdown(
        f'<div class="drill-badge">'
        f'<div style="display:flex;align-items:center;gap:12px;">'
        f'<span class="drill-sym" style="color:{gc}">{tkr}</span>{pill_html}'
        f'</div>'
        f'<div class="drill-meta">SMT: {smt_pair} &nbsp;&#183;&nbsp; '
        f'{current:.4f} &nbsp;&#183;&nbsp; {cfg["htf_interval"].upper()}</div>'
        f'</div>', unsafe_allow_html=True)

    render_meta_banner(tkr, smt_pair, ts)
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
        render_trade_table(setup, tkr, ts)


def _run_scan(watchlist, cfg):
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
            sym = {"A+":"&#11088;","A":"&#9989;","B":"&#9888;&#65039;"}.get(g,"&#183;")
            pb.progress(done/total,
                        text=f"مسح {done}/{total} · {tkr} {sym} {g}")

    pb.empty()
    df = (pd.DataFrame(results)
            .sort_values(by=["_grade_rank","_score_num"], ascending=[True,False])
            .reset_index(drop=True))
    st.session_state.radar_df    = df
    st.session_state.radar_preset = cfg
    st.session_state.radar_ts    = datetime.now(timezone.utc)
    n_ap = len(df[df["Grade"]=="A+"])
    n_a  = len(df[df["Grade"]=="A"])
    n_b  = len(df[df["Grade"]=="B"])
    st.success(f"&#9989; اكتمل المسح · {len(df)} رمزاً  ·  A+: {n_ap}  ·  A: {n_a}  ·  B: {n_b}")


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
def main():
    mode, ticker, smt_ticker, watchlist, preset, cfg, run_btn, scan_btn = render_controls()
    n_sym = len(watchlist) if watchlist else 0
    render_topnav(mode, ticker, smt_ticker, preset, n_sym)
    st.markdown("<br>", unsafe_allow_html=True)
    if mode == "single":
        render_single(ticker, smt_ticker, cfg, run_btn)
    else:
        render_radar(watchlist, preset, cfg, scan_btn)


if __name__ == "__main__":
    main()
