"""
app.py — ICT Market Maker Dashboard
Run with:  streamlit run app.py
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
    page_title="ICT Market Maker Engine",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&family=Noto+Sans+Arabic:wght@300;400;500;600&display=swap');

:root {
    --bg0:   #0d1117;
    --bg1:   #161b22;
    --bg2:   #1c2333;
    --border:#21262d;
    --cyan:  #58a6ff;
    --green: #3fb950;
    --red:   #f85149;
    --gold:  #d29922;
    --purple:#bc8cff;
    --text:  #c9d1d9;
    --muted: #484f58;
}

html, body, [class*="css"] {
    background-color: var(--bg0) !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', 'Noto Sans Arabic', monospace !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--bg1) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { font-family: 'JetBrains Mono', monospace !important; }

/* Buttons */
.stButton > button {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.5px !important;
    transition: border-color 0.2s, color 0.2s !important;
}
.stButton > button:hover {
    border-color: var(--cyan) !important;
    color: var(--cyan) !important;
}

/* Primary button */
.stButton > button[kind="primary"] {
    background: rgba(88,166,255,0.12) !important;
    border-color: var(--cyan) !important;
    color: var(--cyan) !important;
}

/* Inputs & selects */
.stSelectbox label, .stTextInput label, .stSlider label,
.stRadio label, .stCheckbox label, .stMultiSelect label {
    color: var(--muted) !important;
    font-size: 0.68rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
div[data-baseweb="select"] > div {
    background: var(--bg2) !important;
    border-color: var(--border) !important;
}

/* Metric */
div[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.4rem !important;
}

/* Dataframe */
.stDataFrame iframe { border: none !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: var(--bg1);
    border-bottom: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 1px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    color: var(--cyan) !important;
    border-bottom: 2px solid var(--cyan) !important;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Grade badges */
.badge { padding: 2px 8px; border-radius: 4px; font-family: monospace;
         font-size: 0.72rem; font-weight: 600; letter-spacing: 1px; }
.badge-ap { background:rgba(63,185,80,0.15); color:#3fb950;
            border:1px solid rgba(63,185,80,0.3); }
.badge-a  { background:rgba(88,166,255,0.15); color:#58a6ff;
            border:1px solid rgba(88,166,255,0.3); }
.badge-b  { background:rgba(210,153,34,0.15); color:#d29922;
            border:1px solid rgba(210,153,34,0.3); }
.badge-skip { background:rgba(72,79,88,0.3); color:#484f58;
              border:1px solid #21262d; }

/* Header bar */
.header-bar {
    background: linear-gradient(135deg, #161b22 0%, #1c2333 100%);
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 14px 20px;
    margin-bottom: 18px;
    position: relative;
    overflow: hidden;
}
.header-bar::before {
    content: '';
    position: absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, #58a6ff, #bc8cff, #3fb950);
}
.header-title { font-size:1.3rem; font-weight:600; color:#58a6ff;
                letter-spacing:2px; margin:0; }
.header-sub   { font-size:0.68rem; color:#484f58; letter-spacing:1px;
                margin:4px 0 0 0; }

/* Card */
.kpi-card {
    background: var(--bg1);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 16px;
}
.kpi-label { font-size:0.62rem; color:var(--muted); letter-spacing:1.5px;
             text-transform:uppercase; margin-bottom:4px; }
.kpi-value { font-size:1.5rem; font-weight:600;
             font-family:'JetBrains Mono',monospace; }

/* Decision log */
.dlog-stage { font-size:0.72rem; color:#bc8cff; letter-spacing:1px;
              font-weight:600; margin-top:12px; }
.dlog-finding { color:#c9d1d9; font-size:0.8rem; }
.dlog-reason  { color:#484f58; font-size:0.72rem; margin-top:2px; }
.dlog-risk    { color:#d29922; font-size:0.72rem; margin-top:2px; }
.dlog-score   { font-size:0.72rem; font-weight:600; }

/* Scrollbar */
::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background:var(--bg0); }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:2px; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  CACHED ENGINE CALLS
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
        setup = result[0]
        return E.extract_row(setup, ticker, smt_ticker)
    except Exception as ex:
        return {"Ticker":ticker,"SMT":smt_ticker,"Grade":"ERR","Score":"—",
                "Bias":"ERROR","Entry":"—","SL":"—","TP1":"—","TP2":"—",
                "Potential R:R":"—","DOL":"—","SMT Signal":"—",
                "Fractal":"—","Killzone":"—","PD Array":"—",
                "_score_num":-1,"_grade_rank":100}


# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════

GRADE_BADGE = {
    "A+": '<span class="badge badge-ap">A+</span>',
    "A":  '<span class="badge badge-a">A</span>',
    "B":  '<span class="badge badge-b">B</span>',
}

def grade_color(g):
    return {"A+":"#3fb950","A":"#58a6ff","B":"#d29922"}.get(g,"#484f58")

def bias_icon(b):
    return "🔺 Long" if b=="Long" else ("🔻 Short" if b=="Short" else b)


# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════

def render_sidebar():
    with st.sidebar:
        st.markdown('<div style="font-family:JetBrains Mono;font-size:0.75rem;'
                    'color:#58a6ff;letter-spacing:2px;padding:8px 0 16px;">⬡ ICT ENGINE</div>',
                    unsafe_allow_html=True)

        # ── Mode ──────────────────────────────────────────────
        st.markdown('<div style="font-size:0.62rem;color:#484f58;letter-spacing:1.5px;'
                    'text-transform:uppercase;margin-bottom:6px;">Mode</div>',
                    unsafe_allow_html=True)
        mode = st.radio("", ["Single Stock", "Radar Scan"],
                        horizontal=True, label_visibility="collapsed")

        st.divider()

        # ── Single Stock ──────────────────────────────────────
        if mode == "Single Stock":
            ticker     = st.text_input("Ticker", value="TSLA").strip().upper()
            smt_ticker = st.text_input("SMT Pair", value="QQQ").strip().upper()
        else:
            ticker     = "TSLA"
            smt_ticker = "QQQ"

        # ── Watchlist Preset ──────────────────────────────────
        if mode == "Radar Scan":
            st.markdown('<div style="font-size:0.62rem;color:#484f58;letter-spacing:1.5px;'
                        'text-transform:uppercase;margin-bottom:6px;">Watchlist</div>',
                        unsafe_allow_html=True)
            preset = st.selectbox("", list(E.WATCHLIST_PRESETS.keys()),
                                  label_visibility="collapsed")
            watchlist = E.WATCHLIST_PRESETS[preset]
            st.caption(f"{len(watchlist)} stocks")

        st.divider()

        # ── Timeframe ─────────────────────────────────────────
        st.markdown('<div style="font-size:0.62rem;color:#484f58;letter-spacing:1.5px;'
                    'text-transform:uppercase;margin-bottom:6px;">Timeframe</div>',
                    unsafe_allow_html=True)
        htf_interval = st.selectbox("HTF", ["1d","1wk","4h","1h"],
                                    index=0, label_visibility="collapsed")
        exec_interval = st.selectbox("Exec TF", ["15m","30m","1h","5m"],
                                     index=0, label_visibility="collapsed")

        # ── Period ────────────────────────────────────────────
        st.markdown('<div style="font-size:0.62rem;color:#484f58;letter-spacing:1.5px;'
                    'text-transform:uppercase;margin-bottom:6px;">Period</div>',
                    unsafe_allow_html=True)
        htf_period  = st.selectbox("HTF Period",  ["6mo","3mo","1y","2y"],
                                   index=0, label_visibility="collapsed")
        exec_period = st.selectbox("Exec Period", ["5d","10d","1mo"],
                                   index=0, label_visibility="collapsed")

        st.divider()

        # ── Engine Params ─────────────────────────────────────
        with st.expander("⚙ Engine Parameters"):
            score_min   = st.slider("Min Score",    1, 13, E.SCORE_MIN)
            wick_min    = st.slider("Min Wick %",   5, 40, int(E.SWEEP_WICK_MIN))
            n_candles   = st.slider("Chart Candles",40,150,80)

        st.divider()

        # ── Run ───────────────────────────────────────────────
        run_btn = st.button("▶  RUN ANALYSIS", type="primary",
                            use_container_width=True)

        if mode == "Radar Scan":
            scan_btn = st.button("📡  LAUNCH RADAR", use_container_width=True)
        else:
            scan_btn = False

        st.markdown(
            '<div style="font-size:0.6rem;color:#21262d;text-align:center;'
            'margin-top:20px;letter-spacing:0.5px;">Educational purposes only<br>'
            'Not financial advice</div>', unsafe_allow_html=True)

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

    st.markdown(f"""
    <div class="header-bar">
      <p class="header-title">⬡ ICT MARKET MAKER ENGINE</p>
      <p class="header-sub">
        TICKER: <span style="color:#58a6ff">{ticker}</span>
        &nbsp;·&nbsp; SMT: <span style="color:#bc8cff">{smt_ticker}</span>
        &nbsp;·&nbsp; {cfg['htf_interval']} · {cfg['exec_interval']}
        &nbsp;·&nbsp; {cfg['htf_period']}
      </p>
    </div>""", unsafe_allow_html=True)

    if "single_result" not in st.session_state:
        st.session_state.single_result = None

    if run_btn:
        with st.spinner(f"Running 6-stage analysis for {ticker}…"):
            try:
                E.SWEEP_WICK_MIN = float(cfg["wick_min"])
                result = cached_run_engine(
                    ticker, smt_ticker,
                    cfg["htf_interval"], cfg["exec_interval"],
                    cfg["entry_interval"], cfg["htf_period"], cfg["exec_period"]
                )
                st.session_state.single_result = result
            except Exception as ex:
                st.error(f"❌ {ex}")
                return

    result = st.session_state.single_result
    if result is None:
        st.info("Press **▶ RUN ANALYSIS** in the sidebar to start.")
        return

    setup, df_htf, df_exec, df_m5, liq_levels, swings, dol = result
    current = float(df_htf["Close"].iloc[-1])

    # ── KPI Row ──────────────────────────────────────────────
    c1,c2,c3,c4,c5 = st.columns(5)
    price_prev = float(df_htf["Close"].iloc[-2]) if len(df_htf)>1 else current
    chg_pct    = (current - price_prev)/price_prev*100
    chg_col    = "#3fb950" if chg_pct>=0 else "#f85149"

    for col, label, value, color in [
        (c1,"PRICE",      f"{current:.4f}","#58a6ff"),
        (c2,"CHANGE 1D",  f"{'+' if chg_pct>=0 else ''}{chg_pct:.2f}%", chg_col),
        (c3,"DOL TARGET", f"{dol.price:.4f}" if dol else "—","#bc8cff"),
        (c4,"GRADE",      setup.grade if setup else "SKIP",
                          grade_color(setup.grade) if setup else "#484f58"),
        (c5,"SCORE",      f"{setup.score}/13" if setup else "—","#d29922"),
    ]:
        col.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value" style="color:{color}">{value}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart + Decision Log ─────────────────────────────────
    chart_col, log_col = st.columns([2.4, 1], gap="medium")

    with chart_col:
        st.markdown('<div style="font-size:0.68rem;color:#484f58;letter-spacing:1.5px;'
                    'text-transform:uppercase;border-bottom:1px solid #21262d;'
                    'padding-bottom:6px;margin-bottom:10px;">◈ Price Action Chart</div>',
                    unsafe_allow_html=True)
        fig = E.build_chart(df_htf, setup, liq_levels, swings, dol,
                            ticker=ticker,
                            n_candles=cfg["n_candles"],
                            htf_interval=cfg["htf_interval"])
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar":True,
                                "displaylogo":False,
                                "modeBarButtonsToRemove":["select2d","lasso2d"]})

    with log_col:
        st.markdown('<div style="font-size:0.68rem;color:#484f58;letter-spacing:1.5px;'
                    'text-transform:uppercase;border-bottom:1px solid #21262d;'
                    'padding-bottom:6px;margin-bottom:10px;">◉ Decision Log</div>',
                    unsafe_allow_html=True)
        _render_decision_log(setup, current)

    # ── Trade Table ──────────────────────────────────────────
    if setup:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.68rem;color:#484f58;letter-spacing:1.5px;'
                    'text-transform:uppercase;border-bottom:1px solid #21262d;'
                    'padding-bottom:6px;margin-bottom:10px;">◈ Trade Setup</div>',
                    unsafe_allow_html=True)
        _render_trade_table(setup, current)


def _render_decision_log(setup, current_price):
    if not setup:
        st.markdown("""
        <div style="background:#161b22;border:1px solid #21262d;border-radius:8px;
             padding:24px;text-align:center;">
          <div style="color:#484f58;font-family:JetBrains Mono;font-size:0.78rem;
               letter-spacing:1px;">SKIP<br><br>Score below threshold.<br>
               Adjust parameters or wait<br>for better conditions.</div>
        </div>""", unsafe_allow_html=True)
        return

    bias_s = "🔺 LONG" if setup.bias=="long" else "🔻 SHORT"
    gc     = grade_color(setup.grade)

    st.markdown(f"""
    <div style="background:#161b22;border:1px solid #21262d;border-radius:8px;padding:14px;">
      <div style="display:flex;justify-content:space-between;align-items:center;
           margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid #21262d;">
        <span style="font-size:0.9rem;color:{gc};font-weight:600;
              font-family:JetBrains Mono;">{bias_s}</span>
        <span style="font-size:0.9rem;color:{gc};font-weight:600;
              font-family:JetBrains Mono;">{setup.grade} · {setup.score}/13</span>
      </div>
    """, unsafe_allow_html=True)

    for entry in setup.decision_log:
        dc = "#3fb950" if entry.score_delta>0 else ("#f85149" if entry.score_delta<0 else "#484f58")
        ds = f"+{entry.score_delta}" if entry.score_delta>=0 else str(entry.score_delta)
        st.markdown(f"""
        <div style="margin-bottom:8px;padding-bottom:8px;border-bottom:1px solid #161b22;">
          <div class="dlog-stage">{entry.stage}</div>
          <div class="dlog-finding">{entry.finding}</div>
          <div class="dlog-reason">{entry.reasoning[:90]}{"…" if len(entry.reasoning)>90 else ""}</div>
          {"<div class='dlog-risk'>⚠ " + entry.risk_note[:80] + "</div>" if entry.risk_note else ""}
          <div class="dlog-score" style="color:{dc};margin-top:3px;">{ds} pts</div>
        </div>""", unsafe_allow_html=True)

    # PnL vs current
    e  = setup.entry
    sl = setup.stop_loss
    if setup.bias == "long":
        pnl = (current_price - e) / e * 100
    else:
        pnl = (e - current_price) / e * 100
    pc = "#3fb950" if pnl>=0 else "#f85149"
    ps = f"+{pnl:.2f}%" if pnl>=0 else f"{pnl:.2f}%"

    st.markdown(f"""
    <div style="background:#0d1117;border-radius:6px;padding:10px 12px;margin-top:8px;">
      <div style="font-size:0.62rem;color:#484f58;letter-spacing:1.5px;text-transform:uppercase;">
        Unrealised P&L (current {current_price:.4f})
      </div>
      <div style="font-size:1.1rem;font-weight:600;color:{pc};
           font-family:JetBrains Mono;margin-top:2px;">{ps}</div>
    </div>
    </div>""", unsafe_allow_html=True)


def _render_trade_table(setup, current_price):
    sl_dist = abs(setup.entry - setup.stop_loss)
    rows = [{"Level":"ENTRY","Price":setup.entry,"Distance":0,"R:R":"ref",
             "Note":"FVG/OB midpoint entry"}]
    rows.append({"Level":"STOP LOSS","Price":setup.stop_loss,
                 "Distance":round(abs(setup.entry-setup.stop_loss),4),
                 "R:R":"—","Note":"Behind sweep zone"})
    for t in setup.targets:
        if t.is_tp and sl_dist>0:
            rr = round(abs(t.price-setup.entry)/sl_dist,2)
            rows.append({"Level":t.label,"Price":t.price,
                         "Distance":round(abs(t.price-setup.entry),4),
                         "R:R":f"1:{rr}","Note":f"+{t.level}σ from manipulation range"})

    df_table = pd.DataFrame(rows)

    def color_level(val):
        if "ENTRY" in str(val):     return "color: #58a6ff; font-weight:600"
        if "STOP"  in str(val):     return "color: #f85149"
        if "TP"    in str(val) or "EQ" in str(val): return "color: #3fb950"
        return ""

    styled = (df_table.style
              .applymap(color_level, subset=["Level"])
              .set_properties(**{"font-family":"JetBrains Mono","font-size":"13px"})
              .format({"Price":"{:.4f}","Distance":"{:.4f}"}))

    st.dataframe(styled, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
#  RADAR SCAN VIEW
# ══════════════════════════════════════════════════════════════

def render_radar(watchlist, preset, cfg, scan_btn):

    st.markdown(f"""
    <div class="header-bar">
      <p class="header-title">📡 RADAR SCANNER</p>
      <p class="header-sub">
        {preset} &nbsp;·&nbsp; {len(watchlist)} stocks
        &nbsp;·&nbsp; {cfg['htf_interval']} · {cfg['exec_interval']}
      </p>
    </div>""", unsafe_allow_html=True)

    if "radar_df"        not in st.session_state: st.session_state.radar_df     = None
    if "radar_preset"    not in st.session_state: st.session_state.radar_preset  = None
    if "selected_ticker" not in st.session_state: st.session_state.selected_ticker = None

    if scan_btn:
        _run_radar_scan(watchlist, cfg)

    df = st.session_state.radar_df
    if df is None:
        st.info("Press **📡 LAUNCH RADAR** in the sidebar to start the scan.")
        return

    # ── Filter & Sort ────────────────────────────────────────
    st.markdown('<div style="font-size:0.68rem;color:#484f58;letter-spacing:1.5px;'
                'text-transform:uppercase;border-bottom:1px solid #21262d;'
                'padding-bottom:6px;margin-bottom:12px;">◈ Radar Results</div>',
                unsafe_allow_html=True)

    ctrl1, ctrl2, ctrl3 = st.columns([1.5, 1, 1])
    with ctrl1:
        grade_filter = st.multiselect("Grade Filter",
                                      ["A+","A","B","C"],
                                      default=["A+","A"],
                                      label_visibility="visible")
    with ctrl2:
        bias_filter = st.selectbox("Bias", ["All","Long","Short"])
    with ctrl3:
        search = st.text_input("Search Ticker", placeholder="e.g. AAPL")

    # Apply filters
    display = df.copy()
    if grade_filter:
        display = display[display["Grade"].isin(grade_filter)]
    if bias_filter != "All":
        display = display[display["Bias"] == bias_filter]
    if search:
        display = display[display["Ticker"].str.contains(search.upper(), na=False)]

    # Drop internal sort columns
    SHOW_COLS = ["Ticker","SMT","Grade","Score","Bias","Entry","SL",
                 "TP1","TP2","Potential R:R","DOL","SMT Signal",
                 "Fractal","Killzone","PD Array"]
    show = display[SHOW_COLS].copy()

    # KPIs
    k1,k2,k3,k4,k5 = st.columns(5)
    n_aplus = len(df[df["Grade"]=="A+"])
    n_a     = len(df[df["Grade"]=="A"])
    n_b     = len(df[df["Grade"]=="B"])
    n_skip  = len(df[df["Grade"].isin(["SKIP","ERR","TIMEOUT"])])
    for col, label, val, color in [
        (k1,"Total Scanned",  len(df),     "#58a6ff"),
        (k2,"Grade A+",       n_aplus,     "#3fb950"),
        (k3,"Grade A",        n_a,         "#58a6ff"),
        (k4,"Grade B",        n_b,         "#d29922"),
        (k5,"Skip / Error",   n_skip,      "#484f58"),
    ]:
        col.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value" style="color:{color}">{val}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Interactive Table ────────────────────────────────────
    def color_grade(val):
        return {"A+":"color:#3fb950;font-weight:700",
                "A": "color:#58a6ff;font-weight:700",
                "B": "color:#d29922;font-weight:600"}.get(str(val),"color:#484f58")
    def color_bias(val):
        return "color:#3fb950" if "Long" in str(val) else "color:#f85149"

    styled_df = (show.style
                 .applymap(color_grade, subset=["Grade"])
                 .applymap(color_bias,  subset=["Bias"])
                 .set_properties(**{"font-family":"JetBrains Mono","font-size":"12px"}))

    st.dataframe(styled_df, use_container_width=True,
                 hide_index=True, height=420)

    # ── Ticker Detail on Click ───────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.68rem;color:#484f58;letter-spacing:1.5px;'
                'text-transform:uppercase;border-bottom:1px solid #21262d;'
                'padding-bottom:6px;margin-bottom:12px;">◈ Drill Down</div>',
                unsafe_allow_html=True)

    if show.empty:
        st.caption("No results match current filters.")
        return

    drill_tickers = show["Ticker"].tolist()
    col_sel, col_run = st.columns([3,1])
    with col_sel:
        selected = st.selectbox("Select stock to drill down",
                                drill_tickers, label_visibility="visible")
    with col_run:
        st.markdown("<br>", unsafe_allow_html=True)
        drill_btn = st.button("🔍 Load Chart", use_container_width=True)

    if drill_btn and selected:
        st.session_state.selected_ticker = selected

    if st.session_state.selected_ticker:
        tkr = st.session_state.selected_ticker
        # Find SMT pair from watchlist
        smt_pair = next((s for t,s in watchlist if t==tkr), "QQQ")
        row      = df[df["Ticker"]==tkr]
        grade    = row["Grade"].values[0] if not row.empty else "—"

        with st.spinner(f"Loading chart for {tkr}…"):
            try:
                result = cached_run_engine(
                    tkr, smt_pair,
                    cfg["htf_interval"], cfg["exec_interval"],
                    cfg["entry_interval"], cfg["htf_period"], cfg["exec_period"]
                )
                setup, df_htf, _, _, liq_levels, swings, dol = result
                current = float(df_htf["Close"].iloc[-1])

                gc = grade_color(grade)
                st.markdown(f"""
                <div style="background:#161b22;border:1px solid #21262d;border-radius:8px;
                     padding:10px 16px;margin-bottom:12px;display:flex;
                     justify-content:space-between;align-items:center;">
                  <span style="font-family:JetBrains Mono;font-size:1rem;
                               font-weight:600;color:{gc};">{tkr}  ·  {grade}</span>
                  <span style="font-family:JetBrains Mono;font-size:0.85rem;
                               color:#484f58;">SMT: {smt_pair}  ·  {current:.4f}</span>
                </div>""", unsafe_allow_html=True)

                chart_c, log_c = st.columns([2.4, 1], gap="medium")
                with chart_c:
                    fig = E.build_chart(df_htf, setup, liq_levels, swings, dol,
                                       ticker=tkr, n_candles=cfg["n_candles"],
                                       htf_interval=cfg["htf_interval"])
                    st.plotly_chart(fig, use_container_width=True,
                                    config={"displayModeBar":True,"displaylogo":False})
                with log_c:
                    st.markdown('<div style="font-size:0.65rem;color:#484f58;'
                                'letter-spacing:1.5px;text-transform:uppercase;'
                                'padding-bottom:6px;margin-bottom:8px;'
                                'border-bottom:1px solid #21262d;">Decision Log</div>',
                                unsafe_allow_html=True)
                    _render_decision_log(setup, current)

                if setup:
                    st.markdown("<br>", unsafe_allow_html=True)
                    _render_trade_table(setup, current)

            except Exception as ex:
                st.error(f"Chart error: {ex}")


def _run_radar_scan(watchlist, cfg):
    total = len(watchlist)
    results = []
    prog_bar = st.progress(0, text="Initialising scanner…")
    status   = st.empty()

    E.SWEEP_WICK_MIN = float(cfg["wick_min"])

    def scan_one(pair):
        tkr, smt = pair
        return cached_scan_pair(tkr, smt,
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
            prog_bar.progress(done/total,
                              text=f"Scanned {done}/{total} — {tkr} [{row.get('Grade','?')}]")

    prog_bar.empty()
    status.empty()

    df = pd.DataFrame(results)
    df = df.sort_values(by=["_grade_rank","_score_num"],
                        ascending=[True, False]).reset_index(drop=True)
    st.session_state.radar_df     = df
    st.session_state.radar_preset = cfg
    st.success(f"✅ Scan complete — {len(df)} stocks | "
               f"A+: {len(df[df['Grade']=='A+'])} | "
               f"A: {len(df[df['Grade']=='A'])} | "
               f"B: {len(df[df['Grade']=='B'])}")


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════

def main():
    sidebar_out = render_sidebar()

    if len(sidebar_out) == 8:
        mode, ticker, smt_ticker, watchlist, preset, cfg, run_btn, scan_btn = sidebar_out
    else:
        mode, ticker, smt_ticker, watchlist, preset, cfg, run_btn, scan_btn = \
            sidebar_out + (None,)*(8-len(sidebar_out))

    if mode == "Single Stock":
        render_single(ticker, smt_ticker, cfg, run_btn)
    else:
        render_radar(watchlist, preset, cfg, scan_btn)


if __name__ == "__main__":
    main()
