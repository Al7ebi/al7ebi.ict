"""
app_1.py — ICT Market Maker · Luxury Financial Dashboard  v2
Run with:  streamlit run app_1.py
Requires:  engine.py  (unchanged)

Updates v2:
  1. .applymap -> .map  (pandas compatibility fix)
  2. Light / Dark theme toggle
  3. Compact sidebar (220px) + horizontal filter bar above radar table
  4. Font sizes +20%, KPI values enlarged to --fs-kpi: 1.90rem
  5. Arabic copyright footer: copyright جميع الحقوق محفوظة للحبي
"""

import streamlit as st
import pandas as pd
import time as _time
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

import engine as E


st.set_page_config(
    page_title="ICT Market Maker Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  THEME PALETTES
# ─────────────────────────────────────────────

DARK_PALETTE = """
    --ink:#0a0b0e; --surface-0:#0d0f14; --surface-1:#12151c;
    --surface-2:#181d27; --surface-3:#1e2535;
    --rim:#252d3d; --rim-hi:#2e3a50;
    --text-hi:#e8dcc8; --text-mid:#8a95a8; --text-lo:#3e4758;
    --inp-bg:#181d27; --inp-border:#252d3d;
    --table-bg:#12151c; --table-head:#0d0f14;
    --table-border:#181d27; --table-hover:#1e2535;
"""

LIGHT_PALETTE = """
    --ink:#f0ece6; --surface-0:#ffffff; --surface-1:#f7f3ee;
    --surface-2:#ede8e0; --surface-3:#e3ddd4;
    --rim:#d0c9be; --rim-hi:#b8ae9f;
    --text-hi:#1d1d1f; --text-mid:#4a4540; --text-lo:#888078;
    --inp-bg:#f7f3ee; --inp-border:#d0c9be;
    --table-bg:#ffffff; --table-head:#f7f3ee;
    --table-border:#ede8e0; --table-hover:#f0ece6;
"""

SHARED = """
    --gold-hi:#c8a96e; --gold-mid:#a07848; --gold-dim:#5a3e20;
    --gold-glow:rgba(200,169,110,0.14);
    --jade:#3ecf8e; --crimson:#e05c6a;
    --sapphire:#5b9cf6; --amethyst:#a78bfa;
    --font-display:'Cormorant Garamond',Georgia,serif;
    --font-mono:'JetBrains Mono','Noto Sans Arabic',monospace;
    --fs-xs:0.67rem; --fs-sm:0.78rem; --fs-md:0.94rem;
    --fs-lg:1.10rem; --fs-xl:1.32rem; --fs-kpi:1.90rem;
    --fs-head:2.04rem;
"""


def build_css(theme):
    pal = DARK_PALETTE if theme == "Luxury Dark" else LIGHT_PALETTE
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&family=Noto+Sans+Arabic:wght@300;400;500;600&display=swap');
:root{{{pal}{SHARED}}}
html,body,[class*="css"]{{background-color:var(--surface-0)!important;color:var(--text-hi)!important;font-size:16px;}}
*{{box-sizing:border-box;}}
::-webkit-scrollbar{{width:3px;height:3px;}}
::-webkit-scrollbar-track{{background:var(--ink);}}
::-webkit-scrollbar-thumb{{background:var(--gold-dim);border-radius:2px;}}

/* ── Sidebar narrow ── */
[data-testid="stSidebar"]>div:first-child{{width:220px!important;min-width:220px!important;max-width:220px!important;}}
[data-testid="stSidebar"]{{background:var(--surface-1)!important;border-right:1px solid var(--rim)!important;}}
[data-testid="stSidebar"]::before{{content:'';display:block;height:2px;background:linear-gradient(90deg,transparent,var(--gold-mid) 40%,var(--gold-hi) 60%,transparent);}}
[data-testid="stSidebar"] *{{font-family:var(--font-mono)!important;font-size:var(--fs-sm)!important;}}
.sb-logo{{padding:18px 14px 14px;border-bottom:1px solid var(--rim);margin-bottom:14px;}}
.sb-logo-title{{font-family:var(--font-display)!important;font-size:var(--fs-xl);font-weight:600;color:var(--gold-hi);letter-spacing:2px;line-height:1;}}
.sb-logo-sub{{font-size:var(--fs-xs);color:var(--text-lo);letter-spacing:2px;margin-top:4px;text-transform:uppercase;}}
.sb-label{{font-size:var(--fs-xs);color:var(--text-lo);letter-spacing:2px;text-transform:uppercase;margin-bottom:5px;}}

/* ── Buttons ── */
.stButton>button{{background:transparent!important;border:1px solid var(--rim-hi)!important;color:var(--text-mid)!important;border-radius:3px!important;font-family:var(--font-mono)!important;font-size:var(--fs-sm)!important;letter-spacing:1.5px!important;text-transform:uppercase!important;padding:9px 14px!important;transition:all .25s ease!important;position:relative!important;overflow:hidden!important;}}
.stButton>button::after{{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:var(--gold-hi);transform:scaleX(0);transition:transform .3s ease;}}
.stButton>button:hover{{border-color:var(--gold-mid)!important;color:var(--gold-hi)!important;background:var(--gold-glow)!important;}}
.stButton>button:hover::after{{transform:scaleX(1);}}
.stButton>button[kind="primary"]{{background:var(--gold-glow)!important;border-color:var(--gold-mid)!important;color:var(--gold-hi)!important;}}
.stButton>button[kind="primary"]:hover{{background:rgba(200,169,110,.22)!important;border-color:var(--gold-hi)!important;box-shadow:0 0 18px rgba(200,169,110,.18)!important;}}

/* ── Inputs ── */
.stSelectbox label,.stTextInput label,.stSlider label,.stRadio label,.stCheckbox label,.stMultiSelect label{{font-family:var(--font-mono)!important;font-size:var(--fs-xs)!important;color:var(--text-lo)!important;letter-spacing:2px!important;text-transform:uppercase!important;}}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div{{background:var(--inp-bg)!important;border-color:var(--inp-border)!important;border-radius:3px!important;color:var(--text-hi)!important;font-size:var(--fs-sm)!important;}}
div[data-baseweb="select"]>div:focus-within,div[data-baseweb="input"]>div:focus-within{{border-color:var(--gold-mid)!important;box-shadow:0 0 0 1px var(--gold-dim)!important;}}
div[data-testid="stRadio"]>div{{gap:6px!important;}}
div[data-testid="stRadio"] label{{background:var(--inp-bg)!important;border:1px solid var(--rim)!important;border-radius:3px!important;padding:5px 10px!important;font-size:var(--fs-sm)!important;color:var(--text-mid)!important;cursor:pointer!important;transition:all .2s!important;}}
div[data-testid="stRadio"] label:has(input:checked){{border-color:var(--gold-mid)!important;color:var(--gold-hi)!important;background:var(--gold-glow)!important;}}
div[data-testid="stSlider"] div[role="slider"]{{background:var(--gold-hi)!important;border:2px solid var(--ink)!important;}}
details summary{{font-family:var(--font-mono)!important;font-size:var(--fs-sm)!important;color:var(--text-mid)!important;letter-spacing:1px!important;}}
details{{background:var(--surface-2)!important;border:1px solid var(--rim)!important;border-radius:4px!important;padding:2px 8px!important;}}
div[data-testid="stProgressBar"]>div>div{{background:linear-gradient(90deg,var(--gold-dim),var(--gold-hi))!important;border-radius:2px!important;}}
hr{{border:none!important;border-top:1px solid var(--rim)!important;margin:8px 0!important;}}
div[data-testid="stInfo"],div[data-testid="stSuccess"],div[data-testid="stError"],div[data-testid="stWarning"]{{border-radius:4px!important;font-family:var(--font-mono)!important;font-size:var(--fs-md)!important;color:var(--text-hi)!important;}}
div[data-testid="stInfo"]{{background:rgba(91,156,246,.06)!important;border:1px solid rgba(91,156,246,.2)!important;}}
div[data-testid="stSuccess"]{{background:rgba(62,207,142,.06)!important;border:1px solid rgba(62,207,142,.2)!important;}}
div[data-testid="stError"]{{background:rgba(224,92,106,.06)!important;border:1px solid rgba(224,92,106,.25)!important;}}
div[data-testid="stWarning"]{{background:rgba(200,169,110,.06)!important;border:1px solid rgba(200,169,110,.25)!important;}}
.stDataFrame iframe{{border:none!important;}}

/* ── Layout components ── */
.sec-head{{display:flex;align-items:center;gap:10px;padding-bottom:8px;border-bottom:1px solid var(--rim);margin-bottom:14px;}}
.sec-head-title{{font-family:var(--font-mono);font-size:var(--fs-xs);color:var(--text-lo);letter-spacing:3px;text-transform:uppercase;}}
.sec-head-line{{flex:1;height:1px;background:linear-gradient(90deg,var(--rim),transparent);}}

.page-header{{background:var(--surface-1);border:1px solid var(--rim);border-radius:5px;padding:18px 24px 16px;margin-bottom:20px;position:relative;overflow:hidden;}}
.page-header::before{{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--gold-mid) 30%,var(--gold-hi) 50%,var(--gold-mid) 70%,transparent);}}
.page-header::after{{content:'';position:absolute;top:0;right:0;width:180px;height:100%;background:radial-gradient(ellipse at top right,rgba(200,169,110,.04) 0%,transparent 70%);pointer-events:none;}}
.ph-eyebrow{{font-family:var(--font-mono);font-size:var(--fs-xs);color:var(--gold-mid);letter-spacing:3px;text-transform:uppercase;margin-bottom:6px;}}
.ph-title{{font-family:var(--font-display);font-size:var(--fs-head);font-weight:500;color:var(--text-hi);letter-spacing:1px;line-height:1.1;margin:0 0 6px;}}
.ph-meta{{font-family:var(--font-mono);font-size:var(--fs-sm);color:var(--text-lo);letter-spacing:1px;}}

.kpi-wrap{{background:var(--surface-1);border:1px solid var(--rim);border-radius:4px;padding:18px 18px 14px;position:relative;overflow:hidden;transition:border-color .25s;}}
.kpi-wrap:hover{{border-color:var(--rim-hi);}}
.kpi-label{{font-family:var(--font-mono);font-size:var(--fs-xs);color:var(--text-lo);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:8px;}}
.kpi-value{{font-family:var(--font-mono);font-size:var(--fs-kpi);font-weight:500;line-height:1;}}
.kpi-sub{{font-family:var(--font-mono);font-size:var(--fs-xs);color:var(--text-lo);margin-top:5px;}}

.grade-pill{{display:inline-block;font-family:var(--font-mono);font-size:var(--fs-sm);font-weight:600;letter-spacing:2px;padding:3px 10px;border-radius:2px;}}
.grade-ap{{background:rgba(62,207,142,.1);color:#3ecf8e;border:1px solid rgba(62,207,142,.25);}}
.grade-a{{background:rgba(91,156,246,.1);color:#5b9cf6;border:1px solid rgba(91,156,246,.25);}}
.grade-b{{background:rgba(200,169,110,.1);color:#c8a96e;border:1px solid rgba(200,169,110,.2);}}
.grade-skip{{background:rgba(62,71,88,.3);color:#3e4758;border:1px solid rgba(62,71,88,.4);}}

.dlog-panel{{background:var(--surface-1);border:1px solid var(--rim);border-radius:4px;padding:14px 16px;height:100%;}}
.dlog-header{{display:flex;justify-content:space-between;align-items:center;padding-bottom:10px;margin-bottom:10px;border-bottom:1px solid var(--rim);}}
.dlog-bias{{font-family:var(--font-display);font-size:var(--fs-xl);font-weight:600;letter-spacing:1px;}}
.dlog-score-badge{{font-family:var(--font-mono);font-size:var(--fs-sm);color:var(--text-mid);letter-spacing:1px;}}
.dlog-entry{{margin-bottom:10px;padding-bottom:10px;border-bottom:1px solid var(--surface-2);}}
.dlog-entry:last-child{{border-bottom:none;margin-bottom:0;}}
.dlog-stage-label{{font-family:var(--font-mono);font-size:var(--fs-xs);color:var(--amethyst);letter-spacing:2px;text-transform:uppercase;margin-bottom:3px;}}
.dlog-finding{{font-family:var(--font-mono);font-size:var(--fs-md);color:var(--text-hi);margin-bottom:2px;}}
.dlog-reason{{font-family:var(--font-mono);font-size:var(--fs-sm);color:var(--text-lo);line-height:1.5;margin-bottom:2px;}}
.dlog-risk{{font-family:var(--font-mono);font-size:var(--fs-xs);color:#c8a96e;opacity:.9;}}
.dlog-delta{{font-family:var(--font-mono);font-size:var(--fs-sm);font-weight:600;margin-top:3px;}}
.dlog-pnl-block{{background:var(--surface-0);border-radius:3px;padding:10px 12px;margin-top:10px;}}
.dlog-pnl-label{{font-family:var(--font-mono);font-size:var(--fs-xs);color:var(--text-lo);letter-spacing:2px;text-transform:uppercase;}}
.dlog-pnl-value{{font-family:var(--font-mono);font-size:var(--fs-xl);font-weight:600;margin-top:2px;}}

.tl-table{{width:100%;border-collapse:separate;border-spacing:0 3px;font-family:var(--font-mono);font-size:var(--fs-md);}}
.tl-table th{{font-size:var(--fs-xs);letter-spacing:2px;text-transform:uppercase;color:var(--text-lo);padding:5px 10px;text-align:left;font-weight:400;}}
.tl-table td{{padding:8px 10px;background:var(--surface-2);color:var(--text-mid);}}
.tl-table tr:first-child td{{border-radius:3px 3px 0 0;}}
.tl-table tr:last-child td{{border-radius:0 0 3px 3px;}}
.tl-entry td{{color:#5b9cf6!important;font-weight:600;}}
.tl-sl td{{color:#e05c6a!important;}}
.tl-tp td{{color:#3ecf8e!important;}}

.skip-placeholder{{background:var(--surface-1);border:1px solid var(--rim);border-radius:4px;padding:32px 20px;text-align:center;}}
.skip-icon{{font-family:var(--font-display);font-size:2.5rem;color:var(--text-lo);display:block;margin-bottom:12px;}}
.skip-title{{font-family:var(--font-display);font-size:var(--fs-xl);color:var(--text-lo);margin-bottom:6px;}}
.skip-body{{font-family:var(--font-mono);font-size:var(--fs-sm);color:var(--text-lo);line-height:1.7;letter-spacing:.5px;}}

.drill-badge{{display:flex;justify-content:space-between;align-items:center;background:var(--surface-1);border:1px solid var(--rim);border-radius:4px;padding:12px 18px;margin-bottom:14px;}}
.drill-ticker{{font-family:var(--font-display);font-size:var(--fs-head);font-weight:600;letter-spacing:2px;}}
.drill-meta{{font-family:var(--font-mono);font-size:var(--fs-sm);color:var(--text-lo);letter-spacing:1px;}}

.stat-bar{{display:flex;gap:1px;margin:12px 0 16px;}}
.stat-seg{{flex:1;height:3px;border-radius:1px;background:var(--rim);transition:background .4s;}}
.stat-seg.filled-ap{{background:#3ecf8e;}}
.stat-seg.filled-a{{background:#5b9cf6;}}
.stat-seg.filled-b{{background:#c8a96e;}}
.stat-seg.filled-sk{{background:#3e4758;}}

.app-footer{{font-family:var(--font-mono);font-size:var(--fs-md);color:var(--gold-mid);letter-spacing:1.5px;text-align:center;padding:22px 0 14px;border-top:1px solid var(--gold-dim);margin-top:32px;direction:rtl;}}
.app-footer .footer-en{{font-size:var(--fs-xs);color:var(--text-lo);letter-spacing:1px;margin-top:5px;direction:ltr;display:block;text-transform:uppercase;}}
</style>
"""


# ─────────────────────────────────────────────
#  CACHED ENGINE
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def grade_color(g):
    return {"A+":"#3ecf8e","A":"#5b9cf6","B":"#c8a96e","C":"#6b7585"}.get(g,"#3e4758")

def grade_pill(g):
    css = {"A+":"grade-ap","A":"grade-a","B":"grade-b"}.get(g,"grade-skip")
    return f'<span class="grade-pill {css}">{g}</span>'

def sec_header(title):
    st.markdown(f'<div class="sec-head"><span class="sec-head-title">{title}</span>'
                '<div class="sec-head-line"></div></div>', unsafe_allow_html=True)

def kpi_card(col, label, value, color, sub=""):
    sub_html = f"<div class='kpi-sub'>{sub}</div>" if sub else ""
    col.markdown(f'<div class="kpi-wrap"><div class="kpi-label">{label}</div>'
                 f'<div class="kpi-value" style="color:{color}">{value}</div>'
                 f'{sub_html}</div>', unsafe_allow_html=True)

def _app_footer():
    st.markdown(
        '<div class="app-footer">'
        '\u00a9 \u062c\u0645\u064a\u0639 \u0627\u0644\u062d\u0642\u0648\u0642 \u0645\u062d\u0641\u0648\u0638\u0629 \u0644\u0644\u062d\u0628\u064a'
        '<span class="footer-en">ICT Market Maker Engine &middot; Educational use only &middot; Not financial advice</span>'
        '</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR  (compact 220 px)
# ─────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sb-logo"><div class="sb-logo-title">&#9672; ICT</div>'
                    '<div class="sb-logo-sub">Market Maker Intel</div></div>',
                    unsafe_allow_html=True)

        # Theme toggle
        st.markdown('<div class="sb-label">Theme</div>', unsafe_allow_html=True)
        theme = st.radio("__theme__", ["Luxury Dark", "Minimal Light"],
                         horizontal=False, label_visibility="collapsed",
                         key="app_theme")

        st.divider()

        # Mode
        st.markdown('<div class="sb-label">Mode</div>', unsafe_allow_html=True)
        mode = st.radio("__mode__", ["Single Stock", "Radar Scan"],
                        horizontal=False, label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)

        if mode == "Single Stock":
            st.markdown('<div class="sb-label">Symbol</div>', unsafe_allow_html=True)
            ticker = st.text_input("__tkr__", value="TSLA",
                                   label_visibility="collapsed").strip().upper()
            st.markdown('<div class="sb-label">SMT Pair</div>', unsafe_allow_html=True)
            smt_ticker = st.text_input("__smt__", value="QQQ",
                                       label_visibility="collapsed").strip().upper()
        else:
            ticker, smt_ticker = "TSLA", "QQQ"

        if mode == "Radar Scan":
            st.markdown('<div class="sb-label">Watchlist</div>', unsafe_allow_html=True)
            preset    = st.selectbox("__wl__", list(E.WATCHLIST_PRESETS.keys()),
                                     label_visibility="collapsed")
            watchlist = E.WATCHLIST_PRESETS[preset]
            st.markdown(f'<div class="sb-label" style="margin-top:4px;">'
                        f'{len(watchlist)} symbols</div>', unsafe_allow_html=True)
        else:
            watchlist, preset = None, None

        st.divider()

        st.markdown('<div class="sb-label">HTF</div>', unsafe_allow_html=True)
        htf_interval = st.selectbox("__htf__", ["1d","1wk","4h","1h"],
                                    label_visibility="collapsed")
        st.markdown('<div class="sb-label">Exec TF</div>', unsafe_allow_html=True)
        exec_interval = st.selectbox("__exec__", ["15m","30m","1h","5m"],
                                     label_visibility="collapsed")
        st.markdown('<div class="sb-label">HTF Period</div>', unsafe_allow_html=True)
        htf_period = st.selectbox("__hp__", ["6mo","3mo","1y","2y"],
                                  label_visibility="collapsed")
        st.markdown('<div class="sb-label">Exec Period</div>', unsafe_allow_html=True)
        exec_period = st.selectbox("__ep__", ["5d","10d","1mo"],
                                   label_visibility="collapsed")

        st.divider()

        with st.expander("&#9881;  Params"):
            score_min = st.slider("Min Score",  1, 13, E.SCORE_MIN)
            wick_min  = st.slider("Min Wick %", 5, 40, int(E.SWEEP_WICK_MIN))
            n_candles = st.slider("Candles",    40, 150, 80)

        st.markdown("<br>", unsafe_allow_html=True)

        run_btn  = st.button("&#9654;  Run Analysis", type="primary",
                             use_container_width=True)
        scan_btn = (st.button("&#9673;  Launch Radar", use_container_width=True)
                    if mode == "Radar Scan" else False)

    cfg = dict(htf_interval=htf_interval, exec_interval=exec_interval,
               entry_interval="5m", htf_period=htf_period,
               exec_period=exec_period, score_min=score_min,
               wick_min=wick_min, n_candles=n_candles)

    if mode == "Radar Scan":
        return mode, ticker, smt_ticker, watchlist, preset, cfg, run_btn, scan_btn, theme
    return mode, ticker, smt_ticker, None, None, cfg, run_btn, scan_btn, theme


# ─────────────────────────────────────────────
#  SINGLE STOCK
# ─────────────────────────────────────────────

def render_single(ticker, smt_ticker, cfg, run_btn):
    st.markdown(f'<div class="page-header">'
                f'<div class="ph-eyebrow">6-Stage Protocol &middot; ICT Smart Money</div>'
                f'<h1 class="ph-title">{ticker}'
                f'<span style="color:var(--gold-mid);font-size:1.1rem;'
                f'font-family:var(--font-mono);letter-spacing:3px;">'
                f'&nbsp;/&nbsp;{smt_ticker}</span></h1>'
                f'<div class="ph-meta">{cfg["htf_interval"].upper()}'
                f' &middot; {cfg["exec_interval"].upper()}'
                f' &nbsp;&middot;&nbsp; {cfg["htf_period"]}'
                f' &nbsp;&middot;&nbsp; Min Score: {cfg["score_min"]}'
                f'</div></div>', unsafe_allow_html=True)

    if "single_result" not in st.session_state:
        st.session_state.single_result = None

    if run_btn:
        with st.spinner(""):
            try:
                E.SWEEP_WICK_MIN = float(cfg["wick_min"])
                st.session_state.single_result = cached_run_engine(
                    ticker, smt_ticker,
                    cfg["htf_interval"], cfg["exec_interval"],
                    cfg["entry_interval"], cfg["htf_period"], cfg["exec_period"])
            except Exception as ex:
                st.error(f"Engine error: {ex}"); return

    result = st.session_state.single_result
    if result is None:
        st.markdown('<div class="skip-placeholder"><span class="skip-icon">&#9672;</span>'
                    '<div class="skip-title">Awaiting Analysis</div>'
                    '<div class="skip-body">Configure parameters in the sidebar<br>'
                    'and press <strong>Run Analysis</strong> to begin.</div></div>',
                    unsafe_allow_html=True)
        _app_footer(); return

    setup, df_htf, df_exec, df_m5, liq_levels, swings, dol = result
    current    = float(df_htf["Close"].iloc[-1])
    price_prev = float(df_htf["Close"].iloc[-2]) if len(df_htf) > 1 else current
    chg_pct    = (current - price_prev) / price_prev * 100
    chg_col    = "#3ecf8e" if chg_pct >= 0 else "#e05c6a"
    sign       = "+" if chg_pct >= 0 else ""

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    kpi_card(k1, "Last Price",  f"{current:.4f}",          "#5b9cf6")
    kpi_card(k2, "Change 1D",   f"{sign}{chg_pct:.2f}%",   chg_col, "vs prior close")
    kpi_card(k3, "DOL Target",  f"{dol.price:.4f}" if dol else "—",
             "#c8a96e", f"{dol.kind}" if dol else "")
    kpi_card(k4, "Bias",
             "Long"  if (setup and setup.bias=="long")  else
             "Short" if (setup and setup.bias=="short") else "—",
             "#3ecf8e" if (setup and setup.bias=="long") else
             "#e05c6a" if setup else "#3e4758")
    kpi_card(k5, "Grade",
             setup.grade if setup else "SKIP",
             grade_color(setup.grade if setup else "SKIP"))
    kpi_card(k6, "Score",
             f"{setup.score}/13" if setup else "—",
             "#c8a96e" if setup else "#3e4758", "confidence")

    st.markdown("<br>", unsafe_allow_html=True)

    chart_col, log_col = st.columns([2.5, 1], gap="medium")
    with chart_col:
        sec_header("Price Action &middot; DOL &middot; PD Arrays")
        fig = E.build_chart(df_htf, setup, liq_levels, swings, dol,
                            ticker=ticker, n_candles=cfg["n_candles"],
                            htf_interval=cfg["htf_interval"])
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar":True,"displaylogo":False,
                                "modeBarButtonsToRemove":["select2d","lasso2d"]})
    with log_col:
        sec_header("Decision Log")
        _render_decision_log(setup, current)

    if setup:
        st.markdown("<br>", unsafe_allow_html=True)
        sec_header("Trade Setup &middot; StdDev Targets")
        _render_trade_table(setup, current)

    _app_footer()


def _render_decision_log(setup, current_price):
    if not setup:
        st.markdown('<div class="dlog-panel"><div class="skip-placeholder"'
                    ' style="border:none;padding:20px 10px;">'
                    '<span class="skip-icon" style="font-size:1.8rem;">&#8212;</span>'
                    '<div class="skip-title" style="font-size:0.9rem;">No Setup</div>'
                    '<div class="skip-body">Score below minimum threshold.</div>'
                    '</div></div>', unsafe_allow_html=True)
        return

    gc        = grade_color(setup.grade)
    bias_sym  = "&#9650; LONG" if setup.bias == "long" else "&#9660; SHORT"
    bias_col  = "#3ecf8e" if setup.bias == "long" else "#e05c6a"
    pill_html = grade_pill(setup.grade)

    html = (f'<div class="dlog-panel">'
            f'<div class="dlog-header">'
            f'<span class="dlog-bias" style="color:{bias_col}">{bias_sym}</span>'
            f'<span class="dlog-score-badge">{pill_html}&nbsp;&nbsp;{setup.score}/13</span>'
            f'</div>')

    for entry in setup.decision_log:
        dc  = ("#3ecf8e" if entry.score_delta>0 else
               "#e05c6a" if entry.score_delta<0 else "#3e4758")
        ds  = f"+{entry.score_delta}" if entry.score_delta >= 0 else str(entry.score_delta)
        tr  = entry.reasoning[:95] + ("&#8230;" if len(entry.reasoning) > 95 else "")
        rh  = (f'<div class="dlog-risk">&#9670; {entry.risk_note[:85]}</div>'
               if entry.risk_note else "")
        html += (f'<div class="dlog-entry">'
                 f'<div class="dlog-stage-label">{entry.stage}</div>'
                 f'<div class="dlog-finding">{entry.finding}</div>'
                 f'<div class="dlog-reason">{tr}</div>{rh}'
                 f'<div class="dlog-delta" style="color:{dc}">{ds} pts</div>'
                 f'</div>')

    pnl = ((current_price - setup.entry) / setup.entry * 100
           if setup.bias == "long"
           else (setup.entry - current_price) / setup.entry * 100)
    pc  = "#3ecf8e" if pnl >= 0 else "#e05c6a"
    ps  = f"{'+' if pnl>=0 else ''}{pnl:.2f}%"

    html += (f'<div class="dlog-pnl-block">'
             f'<div class="dlog-pnl-label">Unrealised P&amp;L &middot; {current_price:.4f}</div>'
             f'<div class="dlog-pnl-value" style="color:{pc}">{ps}</div>'
             f'</div></div>')
    st.markdown(html, unsafe_allow_html=True)


def _render_trade_table(setup, current_price):
    sl_dist = abs(setup.entry - setup.stop_loss)
    rows = [
        {"cls":"tl-entry","Level":"Entry",
         "Price":f"{setup.entry:.4f}","Distance":"&#8212;",
         "RR":"ref","Note":"FVG / OB midpoint"},
        {"cls":"tl-sl","Level":"Stop Loss",
         "Price":f"{setup.stop_loss:.4f}",
         "Distance":f"{abs(setup.entry-setup.stop_loss):.4f}",
         "RR":"&#8212;","Note":"Behind sweep zone"},
    ]
    for t in setup.targets:
        if t.is_tp and sl_dist > 0:
            rr = round(abs(t.price - setup.entry) / sl_dist, 2)
            rows.append({"cls":"tl-tp","Level":t.label,
                         "Price":f"{t.price:.4f}",
                         "Distance":f"{abs(t.price-setup.entry):.4f}",
                         "RR":f"1:{rr}","Note":f"+{t.level}&#963; StdDev"})

    html = ('<table class="tl-table"><thead><tr>'
            '<th>Level</th><th>Price</th><th>Distance</th>'
            '<th>R:R</th><th>Note</th></tr></thead><tbody>')
    for r in rows:
        html += (f'<tr class="{r["cls"]}">'
                 f'<td>{r["Level"]}</td><td>{r["Price"]}</td>'
                 f'<td>{r["Distance"]}</td><td>{r["RR"]}</td>'
                 f'<td>{r["Note"]}</td></tr>')
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  RADAR SCAN
# ─────────────────────────────────────────────

def render_radar(watchlist, preset, cfg, scan_btn):
    st.markdown(f'<div class="page-header">'
                f'<div class="ph-eyebrow">Parallel Market Scan &middot; Smart Money</div>'
                f'<h1 class="ph-title">Radar Scanner</h1>'
                f'<div class="ph-meta">{preset} &nbsp;&middot;&nbsp; {len(watchlist)} symbols'
                f' &nbsp;&middot;&nbsp; {cfg["htf_interval"].upper()}'
                f' &middot; {cfg["exec_interval"].upper()}</div></div>',
                unsafe_allow_html=True)

    for key in ("radar_df","radar_preset","selected_ticker"):
        if key not in st.session_state:
            st.session_state[key] = None

    if scan_btn:
        _run_radar_scan(watchlist, cfg)

    df = st.session_state.radar_df
    if df is None:
        st.markdown('<div class="skip-placeholder"><span class="skip-icon">&#9673;</span>'
                    '<div class="skip-title">Radar Offline</div>'
                    '<div class="skip-body">Select a watchlist and press'
                    ' <strong>Launch Radar</strong>.</div></div>', unsafe_allow_html=True)
        _app_footer(); return

    # ── Horizontal filter bar ──────────────────────────────────
    sec_header("Filters &middot; Sort &middot; Search")
    f1, f2, f3, f4 = st.columns([2, 1.2, 1.2, 1.4])
    with f1:
        grade_filter = st.multiselect("Grade", ["A+","A","B","C"],
                                      default=["A+","A"])
    with f2:
        bias_filter = st.selectbox("Bias", ["All","Long","Short"])
    with f3:
        rr_filter = st.selectbox("Min R:R", ["Any","≥ 1.5","≥ 2","≥ 3"])
    with f4:
        search = st.text_input("Symbol", placeholder="e.g. AAPL")

    display = df.copy()
    if grade_filter:
        display = display[display["Grade"].isin(grade_filter)]
    if bias_filter != "All":
        display = display[display["Bias"] == bias_filter]
    if search:
        display = display[display["Ticker"].str.contains(search.upper(), na=False)]
    if rr_filter != "Any":
        thresh = float(rr_filter.replace("≥ ", ""))
        def _rr_ok(v):
            try: return float(str(v).replace("1:", "")) >= thresh
            except Exception: return False
        display = display[display["Potential R:R"].apply(_rr_ok)]

    SHOW = ["Ticker","SMT","Grade","Score","Bias","Entry","SL",
            "TP1","TP2","Potential R:R","DOL","SMT Signal",
            "Fractal","Killzone","PD Array"]
    show = display[SHOW].copy()

    # KPIs
    st.markdown("<br>", unsafe_allow_html=True)
    n_ap   = len(df[df["Grade"]=="A+"])
    n_a    = len(df[df["Grade"]=="A"])
    n_b    = len(df[df["Grade"]=="B"])
    n_skip = len(df[df["Grade"].isin(["SKIP","ERR","TIMEOUT"])])
    n_long = len(df[df["Bias"]=="Long"])

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    kpi_card(k1,"Scanned",   len(df), "#5b9cf6")
    kpi_card(k2,"Grade A+",  n_ap,    "#3ecf8e","elite")
    kpi_card(k3,"Grade A",   n_a,     "#5b9cf6","strong")
    kpi_card(k4,"Grade B",   n_b,     "#c8a96e","developing")
    kpi_card(k5,"Long Bias", n_long,  "#3ecf8e")
    kpi_card(k6,"Skip/Err",  n_skip,  "#3e4758")

    segs = (["<div class='stat-seg filled-ap'></div>"]*n_ap +
            ["<div class='stat-seg filled-a'></div>"]*n_a +
            ["<div class='stat-seg filled-b'></div>"]*n_b +
            ["<div class='stat-seg filled-sk'></div>"]*n_skip)
    st.markdown(f'<div class="stat-bar">{"".join(segs[:70])}</div>',
                unsafe_allow_html=True)

    sec_header("Actionable Setups &middot; A+ First")

    # ── FIX #1: .map() instead of deprecated .applymap() ─────
    def sg(v):
        return {"A+":"color:#3ecf8e;font-weight:700;background:rgba(62,207,142,.08)",
                "A": "color:#5b9cf6;font-weight:700;background:rgba(91,156,246,.08)",
                "B": "color:#c8a96e;font-weight:600;background:rgba(200,169,110,.07)",
                "SKIP":"color:#3e4758","ERR":"color:#e05c6a"}.get(str(v),"color:#484f58")
    def sb(v):
        if "Long"  in str(v): return "color:#3ecf8e;font-weight:600"
        if "Short" in str(v): return "color:#e05c6a;font-weight:600"
        return "color:#3e4758"
    def sr(v):
        try:
            r = float(str(v).replace("1:",""))
            return ("color:#3ecf8e;font-weight:600" if r>=3 else
                    "color:#c8a96e" if r>=2 else "color:#5a6478")
        except Exception: return "color:#3e4758"
    def sf(v):
        if "H1+M15+M5" in str(v): return "color:#3ecf8e"
        if "H1+M15"    in str(v): return "color:#c8a96e"
        return "color:#3e4758"
    def ss(v):
        return "color:#a78bfa;font-weight:600" if "Div" in str(v) else "color:#3e4758"

    styled = (show.style
              .map(sg, subset=["Grade"])
              .map(sb, subset=["Bias"])
              .map(sr, subset=["Potential R:R"])
              .map(sf, subset=["Fractal"])
              .map(ss, subset=["SMT Signal"])
              .set_properties(**{"font-family":"JetBrains Mono,monospace",
                                 "font-size":"13px"})
              .set_table_styles([
                  {"selector":"thead th",
                   "props":"font-size:11px;letter-spacing:1.5px;"
                           "text-transform:uppercase;padding:9px 10px;"},
                  {"selector":"tbody tr:hover td",
                   "props":"opacity:.85;"},
                  {"selector":"tbody td",
                   "props":"padding:8px 10px;"},
              ]))

    st.dataframe(styled, use_container_width=True, hide_index=True, height=460)

    # Drill-down
    st.markdown("<br>", unsafe_allow_html=True)
    sec_header("Drill Down &middot; Full Analysis")

    if show.empty:
        st.markdown('<div class="skip-body" style="text-align:center;padding:16px;">'
                    'No results match current filters.</div>', unsafe_allow_html=True)
        _app_footer(); return

    dc1, dc2 = st.columns([3, 1])
    with dc1:
        selected = st.selectbox("Select symbol", show["Ticker"].tolist())
    with dc2:
        st.markdown("<br>", unsafe_allow_html=True)
        drill_btn = st.button("&#9672;  Load Chart", use_container_width=True)

    if drill_btn and selected:
        st.session_state.selected_ticker = selected

    if st.session_state.selected_ticker:
        _render_drill_down(st.session_state.selected_ticker, df, watchlist, cfg)

    _app_footer()


def _render_drill_down(tkr, radar_df, watchlist, cfg):
    smt_pair = next((s for t,s in watchlist if t==tkr), "QQQ")
    row_data = radar_df[radar_df["Ticker"]==tkr]
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
            st.error(f"Chart error: {ex}"); return

    pill_html = grade_pill(grade)
    st.markdown(f'<div class="drill-badge">'
                f'<div><span class="drill-ticker" style="color:{gc}">{tkr}</span>'
                f'&nbsp;&nbsp;{pill_html}</div>'
                f'<div class="drill-meta">SMT: {smt_pair} &nbsp;&middot;&nbsp; '
                f'{current:.4f} &nbsp;&middot;&nbsp; {cfg["htf_interval"].upper()}</div>'
                f'</div>', unsafe_allow_html=True)

    cc, lc = st.columns([2.5, 1], gap="medium")
    with cc:
        sec_header("Price Action Chart")
        fig = E.build_chart(df_htf, setup, liq_levels, swings, dol,
                            ticker=tkr, n_candles=cfg["n_candles"],
                            htf_interval=cfg["htf_interval"])
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar":True,"displaylogo":False})
    with lc:
        sec_header("Decision Log")
        _render_decision_log(setup, current)

    if setup:
        st.markdown("<br>", unsafe_allow_html=True)
        sec_header("Trade Setup &middot; StdDev Targets")
        _render_trade_table(setup, current)


def _run_radar_scan(watchlist, cfg):
    E.SWEEP_WICK_MIN = float(cfg["wick_min"])
    total, results = len(watchlist), []
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
                row = {"Ticker":tkr,"SMT":smt,"Grade":"TIMEOUT","Score":"—",
                       "Bias":"—","Entry":"—","SL":"—","TP1":"—","TP2":"—",
                       "Potential R:R":"—","DOL":"—","SMT Signal":"—",
                       "Fractal":"—","Killzone":"—","PD Array":"—",
                       "_score_num":-2,"_grade_rank":101}
            results.append(row)
            done += 1
            g = row.get("Grade","?")
            sym = {"A+":"◈","A":"◆","B":"◇"}.get(g,"·")
            pb.progress(done/total, text=f"Scanning {done}/{total} · {tkr} {sym} {g}")

    pb.empty()
    df = pd.DataFrame(results).sort_values(
        by=["_grade_rank","_score_num"], ascending=[True,False]
    ).reset_index(drop=True)
    st.session_state.radar_df     = df
    st.session_state.radar_preset = cfg

    n_ap = len(df[df["Grade"]=="A+"])
    n_a  = len(df[df["Grade"]=="A"])
    n_b  = len(df[df["Grade"]=="B"])
    st.success(f"Scan complete · {len(df)} symbols · A+: {n_ap} · A: {n_a} · B: {n_b}")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    out = render_sidebar()
    (mode, ticker, smt_ticker, watchlist, preset,
     cfg, run_btn, scan_btn, theme) = out

    # Inject theme-aware CSS after sidebar so theme value is known
    st.markdown(build_css(theme), unsafe_allow_html=True)

    if mode == "Single Stock":
        render_single(ticker, smt_ticker, cfg, run_btn)
    else:
        render_radar(watchlist, preset, cfg, scan_btn)


if __name__ == "__main__":
    main()
