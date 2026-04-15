"""
app_1.py — منصة الحبي للتداول  v4
Run: streamlit run app_1.py   |   Requires: engine.py (unchanged)
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import engine as E

st.set_page_config(
    page_title="منصة الحبي للتداول",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════
_SS = {
    "theme":           "light",
    "single_result":   None,
    "single_ts":       None,
    "single_ticker":   "",
    "radar_df":        None,
    "radar_ts":        None,
    "radar_preset":    None,
    "selected_ticker": None,
}
for _k, _v in _SS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

DARK = st.session_state.theme == "dark"

# ═══════════════════════════════════════════════════════════
#  THEME TOKENS
# ═══════════════════════════════════════════════════════════
if DARK:
    THEME = dict(
        page_bg="#0F1117", card_bg="#1A1D2E", card2_bg="#22263A",
        border="#2E3250", border_soft="#252847",
        text_hi="#F1F5FB", text_mid="#9CA3BC", text_lo="#555A78",
        inp_bg="#1E2235", inp_border="#2E3250",
        tbl_bg="#1A1D2E", tbl_head="#151828", tbl_row_hover="#1F2340",
        g50="#151828", g100="#1E2235", g200="#252847",
        sh_sm="0 1px 4px rgba(0,0,0,.4)",
        sh_md="0 4px 16px rgba(0,0,0,.5)",
        divider="#2E3250",
    )
else:
    THEME = dict(
        page_bg="#F0F2F6", card_bg="#FFFFFF", card2_bg="#F9FAFB",
        border="#E5E7EB", border_soft="#F3F4F6",
        text_hi="#111827", text_mid="#374151", text_lo="#9CA3AF",
        inp_bg="#F9FAFB", inp_border="#E5E7EB",
        tbl_bg="#FFFFFF", tbl_head="#F9FAFB", tbl_row_hover="#F3F4F6",
        g50="#F9FAFB", g100="#F3F4F6", g200="#E5E7EB",
        sh_sm="0 1px 3px rgba(0,0,0,.07)",
        sh_md="0 4px 14px rgba(0,0,0,.09)",
        divider="#E5E7EB",
    )

T = THEME

# ═══════════════════════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════════════════════
def get_css():
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');
:root {{
  --page-bg:{T["page_bg"]}; --card-bg:{T["card_bg"]}; --card2:{T["card2_bg"]};
  --border:{T["border"]}; --bsoft:{T["border_soft"]};
  --txt-hi:{T["text_hi"]}; --txt-mid:{T["text_mid"]}; --txt-lo:{T["text_lo"]};
  --inp-bg:{T["inp_bg"]}; --inp-brd:{T["inp_border"]};
  --tbl-bg:{T["tbl_bg"]}; --tbl-head:{T["tbl_head"]}; --tbl-hover:{T["tbl_row_hover"]};
  --g50:{T["g50"]}; --g100:{T["g100"]}; --g200:{T["g200"]};
  --sh-sm:{T["sh_sm"]}; --sh-md:{T["sh_md"]}; --divider:{T["divider"]};
  --blue:#4F46E5; --blue-l:{"#1E2052" if DARK else "#EEF2FF"};
  --violet:#7C3AED; --violet-l:{"#200D47" if DARK else "#F5F3FF"};
  --green:#10B981; --green-l:{"#052E1C" if DARK else "#ECFDF5"};
  --red:#EF4444;   --red-l:{"#2D0A0A" if DARK else "#FEF2F2"};
  --amber:#F59E0B; --amber-l:{"#2D1A00" if DARK else "#FFFBEB"};
  --teal:#14B8A6;  --teal-l:{"#042E2A" if DARK else "#F0FDFA"};
  --purple:#8B5CF6;--purple-l:{"#1D0D3E" if DARK else "#F5F3FF"};
  --font:'Tajawal','Noto Sans Arabic',sans-serif;
  --r-sm:8px; --r-md:12px; --r-lg:16px; --r-xl:20px;
}}
html,body,[class*="css"]{{
  background-color:var(--page-bg)!important;
  font-family:var(--font)!important;
  color:var(--txt-hi)!important;
  direction:rtl!important;
}}
*{{box-sizing:border-box;}}
[data-testid="collapsedControl"],
[data-testid="stSidebar"],
section[data-testid="stSidebar"]{{display:none!important;}}
.main .block-container{{padding:0 1.25rem 3rem!important;max-width:1440px!important;}}
::-webkit-scrollbar{{width:5px;height:5px;}}
::-webkit-scrollbar-thumb{{background:var(--g200);border-radius:4px;}}

/* ── Ticker ── */
@keyframes ticker-scroll {{
  0%   {{ transform: translateX(0); }}
  100% {{ transform: translateX(-50%); }}
}}
.ticker-wrap {{
  background:{"#111827" if DARK else "#1E2235"};
  overflow:hidden; white-space:nowrap; padding:0; height:34px;
  display:flex; align-items:center;
}}
.ticker-inner {{
  display:inline-block;
  animation:ticker-scroll 38s linear infinite;
  will-change:transform;
}}
.ticker-inner:hover {{ animation-play-state:paused; }}
.tick-item {{
  display:inline-flex; align-items:center; gap:8px;
  padding:0 28px; font-size:.78rem; font-weight:500;
  color:rgba(255,255,255,.85);
  border-right:1px solid rgba(255,255,255,.1);
}}
.tick-up   {{ color:#34D399; }}
.tick-down {{ color:#F87171; }}
.tick-sym  {{ color:#93C5FD; font-weight:700; }}

/* ── Header ── */
.main-header {{
  background:{"linear-gradient(135deg,#0F1A3A 0%,#1B1060 60%,#2D0E5B 100%)" if DARK
              else "linear-gradient(135deg,#1E1B4B 0%,#4F46E5 60%,#7C3AED 100%)"};
  padding:22px 28px 16px;
  margin:0 -1.25rem 0;
  display:flex; align-items:center; justify-content:space-between;
}}
.brand-row {{ display:flex; align-items:center; gap:14px; }}
.brand-logo {{
  width:48px; height:48px;
  background:rgba(255,255,255,.15);
  border-radius:var(--r-lg);
  display:flex; align-items:center; justify-content:center;
  font-size:1.5rem;
}}
.brand-name {{ font-size:1.45rem; font-weight:800; color:#fff; line-height:1.1; }}
.brand-sub  {{ font-size:.68rem; color:rgba(255,255,255,.6);
               letter-spacing:1.5px; text-transform:uppercase; margin-top:2px; }}
.header-right {{ display:flex; align-items:center; gap:10px; }}
.nav-pill {{
  background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.2);
  border-radius:20px; padding:5px 14px; font-size:.75rem;
  color:rgba(255,255,255,.88); white-space:nowrap; cursor:default;
}}

/* Market clock */
.market-clock {{
  background:rgba(0,0,0,.25); border:1px solid rgba(255,255,255,.15);
  border-radius:var(--r-lg); padding:10px 16px;
  display:flex; align-items:center; gap:14px;
}}
.clock-dot {{
  width:11px; height:11px; border-radius:50%; flex-shrink:0;
}}
.clock-dot.open  {{ background:#34D399; box-shadow:0 0 0 0 rgba(52,211,153,.6);
                    animation:pulse-green 1.8s infinite; }}
.clock-dot.closed{{ background:#F87171; box-shadow:0 0 0 0 rgba(248,113,113,.5);
                    animation:pulse-red 1.8s infinite; }}
@keyframes pulse-green {{
  0%,100%{{ box-shadow:0 0 0 0 rgba(52,211,153,.5); }}
  50%    {{ box-shadow:0 0 0 6px rgba(52,211,153,.0); }}
}}
@keyframes pulse-red {{
  0%,100%{{ box-shadow:0 0 0 0 rgba(248,113,113,.5); }}
  50%    {{ box-shadow:0 0 0 6px rgba(248,113,113,.0); }}
}}
.clock-status {{ font-size:.82rem; font-weight:700; color:#fff; white-space:nowrap; }}
.clock-countdown {{ font-size:.72rem; color:rgba(255,255,255,.6); white-space:nowrap; }}
.clock-time {{ font-size:1.05rem; font-weight:800; color:#fff; white-space:nowrap; }}
.clock-date {{ font-size:.68rem; color:rgba(255,255,255,.55); }}

/* ── Ctrl bar ── */
.ctrl-bar {{
  background:var(--card-bg); border-radius:var(--r-lg);
  box-shadow:var(--sh-sm); border:1px solid var(--border);
  padding:16px 22px; margin:18px 0 6px;
}}
.ctrl-bar-title {{
  font-size:.68rem; font-weight:600; color:var(--txt-lo);
  letter-spacing:1.5px; text-transform:uppercase; margin-bottom:10px;
}}
.stSelectbox label,.stTextInput label,
.stMultiSelect label,.stSlider label,.stRadio label {{
  font-family:var(--font)!important; font-size:.8rem!important;
  font-weight:500!important; color:var(--txt-lo)!important; }}
div[data-baseweb="select"]>div {{
  background:var(--inp-bg)!important; border:1px solid var(--inp-brd)!important;
  border-radius:var(--r-sm)!important; font-family:var(--font)!important;
  font-size:.9rem!important; color:var(--txt-hi)!important; }}
div[data-baseweb="select"]>div:focus-within {{
  border-color:var(--blue)!important;
  box-shadow:0 0 0 3px rgba(79,70,229,.15)!important; }}
div[data-baseweb="input"]>div {{
  background:var(--inp-bg)!important; border:1px solid var(--inp-brd)!important;
  border-radius:var(--r-sm)!important; font-family:var(--font)!important;
  color:var(--txt-hi)!important; }}
div[data-baseweb="input"]>div:focus-within {{
  border-color:var(--blue)!important;
  box-shadow:0 0 0 3px rgba(79,70,229,.15)!important; }}

/* Buttons */
.stButton>button {{
  font-family:var(--font)!important; font-size:.9rem!important;
  font-weight:700!important; border-radius:var(--r-sm)!important;
  padding:10px 22px!important; transition:all .2s!important;
  border:none!important; }}
.stButton>button:not([kind="primary"]) {{
  background:var(--g100)!important; color:var(--txt-mid)!important;
  border:1px solid var(--g200)!important; }}
.stButton>button[kind="primary"] {{
  background:linear-gradient(135deg,#4F46E5,#7C3AED)!important;
  color:#fff!important; box-shadow:0 4px 14px rgba(79,70,229,.4)!important; }}
.stButton>button[kind="primary"]:hover {{
  transform:translateY(-1px)!important;
  box-shadow:0 6px 18px rgba(79,70,229,.5)!important; }}

/* Progress */
div[data-testid="stProgressBar"]>div>div {{
  background:linear-gradient(90deg,#4F46E5,#7C3AED)!important; border-radius:4px!important; }}
div[data-testid="stProgressBar"]>div {{
  background:var(--g200)!important; border-radius:4px!important; }}

/* ── Section header ── */
.sec-head {{ display:flex; align-items:center; gap:12px; margin:22px 0 14px; }}
.sec-icon {{
  width:38px; height:38px; background:var(--blue-l);
  border-radius:var(--r-sm); display:flex; align-items:center;
  justify-content:center; font-size:1.05rem; flex-shrink:0;
}}
.sec-ar  {{ font-size:1.12rem; font-weight:700; color:var(--txt-hi); line-height:1.2; }}
.sec-en  {{ font-size:.65rem; color:var(--txt-lo);
            letter-spacing:1.2px; text-transform:uppercase; }}
.sec-line{{ flex:1; height:1px;
            background:linear-gradient(90deg,var(--divider),transparent); }}

/* ── KPI grid 3x2 ── */
.kpi-grid {{
  display:grid; grid-template-columns:repeat(3,1fr);
  gap:14px; margin-bottom:4px;
}}
.kpi-card {{
  background:var(--card-bg); border-radius:var(--r-md);
  padding:18px 18px 16px; box-shadow:var(--sh-sm);
  border:1px solid var(--bsoft);
  display:flex; align-items:center; gap:14px;
  transition:box-shadow .2s,transform .2s;
  position:relative; overflow:hidden;
}}
.kpi-card:hover{{box-shadow:var(--sh-md);transform:translateY(-1px);}}
.kpi-card::after{{
  content:''; position:absolute; right:0; top:0; width:4px; height:100%;
}}
.kpi-card.blue::after  {{background:var(--blue);}}
.kpi-card.green::after {{background:var(--green);}}
.kpi-card.red::after   {{background:var(--red);}}
.kpi-card.amber::after {{background:var(--amber);}}
.kpi-card.violet::after{{background:var(--violet);}}
.kpi-card.teal::after  {{background:var(--teal);}}
.kpi-card.purple::after{{background:var(--purple);}}
.kpi-icon {{
  width:50px; height:50px; border-radius:var(--r-sm);
  display:flex; align-items:center; justify-content:center;
  font-size:1.3rem; flex-shrink:0;
}}
.kpi-icon.blue  {{background:var(--blue-l);}}
.kpi-icon.green {{background:var(--green-l);}}
.kpi-icon.red   {{background:var(--red-l);}}
.kpi-icon.amber {{background:var(--amber-l);}}
.kpi-icon.violet{{background:var(--violet-l);}}
.kpi-icon.teal  {{background:var(--teal-l);}}
.kpi-icon.purple{{background:var(--purple-l);}}
.kpi-body  {{flex:1;text-align:right;min-width:0;}}
.kpi-num   {{font-size:1.9rem;font-weight:800;line-height:1;}}
.kpi-num.blue  {{color:var(--blue);}}
.kpi-num.green {{color:var(--green);}}
.kpi-num.red   {{color:var(--red);}}
.kpi-num.amber {{color:var(--amber);}}
.kpi-num.violet{{color:var(--violet);}}
.kpi-num.teal  {{color:var(--teal);}}
.kpi-num.purple{{color:var(--purple);}}
.kpi-ar {{font-size:.9rem;font-weight:600;color:var(--txt-hi);margin-top:3px;}}
.kpi-en {{font-size:.65rem;color:var(--txt-lo);letter-spacing:.5px;text-transform:uppercase;}}

/* ── Grade pills ── */
.grade-pill{{
  display:inline-flex;align-items:center;font-size:.72rem;
  font-weight:700;letter-spacing:1px;padding:4px 12px;border-radius:20px;
}}
.gp-ap{{background:{"#052E1C" if DARK else "#DCFCE7"};color:{"#34D399" if DARK else "#15803D"};}}
.gp-a {{background:{"#1E2052" if DARK else "#DBEAFE"};color:{"#818CF8" if DARK else "#1D4ED8"};}}
.gp-b {{background:{"#2D1A00" if DARK else "#FEF9C3"};color:{"#FBBF24" if DARK else "#854D0E"};}}
.gp-c {{background:{"#2D0A0A" if DARK else "#FEE2E2"};color:{"#F87171" if DARK else "#991B1B"};}}
.gp-sk{{background:var(--g100);color:var(--txt-lo);}}

/* ── Meta banner ── */
.meta-banner {{
  background:var(--card-bg); border:1px solid var(--border);
  border-radius:var(--r-md); padding:12px 20px;
  display:flex; align-items:center; justify-content:space-between;
  margin-bottom:14px; box-shadow:var(--sh-sm);
}}
.meta-label{{font-size:.68rem;color:var(--txt-lo);letter-spacing:1px;text-transform:uppercase;}}
.meta-val  {{font-size:.92rem;font-weight:700;color:var(--txt-mid);}}
.outdated-badge{{
  background:{"#2D0A0A" if DARK else "#FEF2F2"};
  border:1px solid {"#7F1D1D" if DARK else "#FECACA"};
  border-radius:20px;padding:5px 14px;font-size:.8rem;
  font-weight:700;color:{"#F87171" if DARK else "#DC2626"};
  animation:pulse-danger 2s infinite;
}}
@keyframes pulse-danger{{
  0%,100%{{box-shadow:0 0 0 0 rgba(239,68,68,0);}}
  50%    {{box-shadow:0 0 0 5px rgba(239,68,68,.15);}}
}}
.fresh-badge{{
  background:{"#052E1C" if DARK else "#ECFDF5"};
  border:1px solid {"#065F46" if DARK else "#A7F3D0"};
  border-radius:20px;padding:5px 14px;
  font-size:.8rem;font-weight:700;
  color:{"#34D399" if DARK else "#059669"};
}}
.expired-badge{{
  background:{"#1F1300" if DARK else "#FFF7ED"};
  border:1px solid {"#78350F" if DARK else "#FED7AA"};
  border-radius:20px;padding:5px 14px;
  font-size:.8rem;font-weight:700;
  color:{"#FBBF24" if DARK else "#92400E"};
}}

/* ── Decision log ── */
.dlog-wrap{{
  background:var(--card-bg);border-radius:var(--r-md);
  box-shadow:var(--sh-sm);border:1px solid var(--bsoft);overflow:hidden;
}}
.dlog-head{{
  background:linear-gradient(135deg,#4F46E5,#7C3AED);
  padding:14px 18px;display:flex;align-items:center;justify-content:space-between;
}}
.dlog-bias-txt{{font-size:1.05rem;font-weight:700;color:#fff;}}
.dlog-entry{{
  padding:12px 18px;border-bottom:1px solid var(--bsoft);transition:background .15s;
}}
.dlog-entry:last-child{{border-bottom:none;}}
.dlog-entry:hover{{background:var(--g50);}}
.dlog-stage{{font-size:.6rem;font-weight:700;color:#818CF8;
             letter-spacing:2px;text-transform:uppercase;margin-bottom:3px;}}
.dlog-find {{font-size:.88rem;font-weight:600;color:var(--txt-hi);margin-bottom:2px;}}
.dlog-rsn  {{font-size:.76rem;color:var(--txt-lo);line-height:1.55;}}
.dlog-risk {{font-size:.73rem;color:#FBBF24;margin-top:3px;}}
.dlog-pts  {{font-size:.73rem;font-weight:700;margin-top:4px;}}
.dlog-pnl  {{background:var(--g50);padding:12px 18px;border-top:2px solid var(--divider);}}
.dlog-pnl-lbl{{font-size:.62rem;color:var(--txt-lo);letter-spacing:1.5px;text-transform:uppercase;}}
.dlog-pnl-val{{font-size:1.3rem;font-weight:800;margin-top:3px;}}

/* ── Trade table ── */
.tl-wrap{{background:var(--card-bg);border-radius:var(--r-md);
          box-shadow:var(--sh-sm);border:1px solid var(--bsoft);overflow:hidden;}}
.tl-header-row{{
  background:linear-gradient(135deg,#4F46E5,#7C3AED);
  padding:13px 20px;display:flex;align-items:center;justify-content:space-between;
}}
.tl-header-title{{font-size:.95rem;font-weight:700;color:#fff;font-family:var(--font);}}
.tl-header-sub{{font-size:.62rem;color:rgba(255,255,255,.65);
                letter-spacing:1.5px;text-transform:uppercase;}}
.tl-table{{width:100%;border-collapse:collapse;font-family:var(--font);}}
.tl-table thead th{{
  background:var(--tbl-head);font-size:.68rem;font-weight:600;color:var(--txt-lo);
  letter-spacing:1.5px;text-transform:uppercase;padding:11px 16px;
  text-align:right;border-bottom:2px solid var(--border);}}
.tl-table tbody td{{
  padding:12px 16px;font-size:.9rem;
  border-bottom:1px solid var(--bsoft);color:var(--txt-mid);}}
.tl-table tbody tr:last-child td{{border-bottom:none;}}
.tl-table tbody tr:hover td{{background:var(--tbl-hover);}}
.tl-entry td:first-child{{color:#818CF8;font-weight:700;}}
.tl-sl    td:first-child{{color:#F87171;font-weight:700;}}
.tl-tp    td:first-child{{color:#34D399;font-weight:700;}}
.tl-num{{font-family:'JetBrains Mono','Courier New',monospace;font-size:.88rem;}}

/* ── Radar table ── */
.tbl-card{{background:var(--card-bg);border-radius:var(--r-md);
           box-shadow:var(--sh-sm);border:1px solid var(--bsoft);overflow:hidden;}}
.tbl-card-hd{{
  background:var(--g50);border-bottom:1px solid var(--border);
  padding:13px 20px;display:flex;align-items:center;justify-content:space-between;
}}
.tbl-hd-ar {{font-size:.92rem;font-weight:700;color:var(--txt-hi);}}
.tbl-hd-cnt{{font-size:.78rem;color:var(--txt-lo);}}
.stDataFrame iframe{{border:none!important;}}
.stDataFrame>div{{border:none!important;border-radius:0!important;}}

/* ── Stat bar ── */
.stat-bar{{display:flex;gap:2px;height:7px;border-radius:4px;overflow:hidden;margin:8px 0 22px;}}
.sap{{background:#10B981;}} .saa{{background:#4F46E5;}}
.sbb{{background:#F59E0B;}} .ssk{{background:var(--g200);}}

/* ── Drill badge ── */
.drill-badge{{
  background:{"linear-gradient(135deg,#1E2052,#200D47)" if DARK
              else "linear-gradient(135deg,#EEF2FF,#F5F3FF)"};
  border:1px solid {"#3730A3" if DARK else "#C7D2FE"};
  border-radius:var(--r-md); padding:13px 20px;
  display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;
}}
.drill-sym {{font-size:1.5rem;font-weight:800;color:var(--blue);letter-spacing:1px;}}
.drill-meta{{font-size:.75rem;color:var(--txt-lo);}}

/* ── Alerts ── */
div[data-testid="stInfo"]   {{background:{"#1E2052" if DARK else "#EEF2FF"}!important;
  border:1px solid {"#3730A3" if DARK else "#C7D2FE"}!important;
  border-radius:var(--r-sm)!important;color:var(--txt-hi)!important;font-family:var(--font)!important;}}
div[data-testid="stSuccess"]{{background:{"#052E1C" if DARK else "#ECFDF5"}!important;
  border:1px solid {"#065F46" if DARK else "#A7F3D0"}!important;
  border-radius:var(--r-sm)!important;color:var(--txt-hi)!important;font-family:var(--font)!important;}}
div[data-testid="stError"]  {{background:{"#2D0A0A" if DARK else "#FEF2F2"}!important;
  border:1px solid {"#7F1D1D" if DARK else "#FECACA"}!important;
  border-radius:var(--r-sm)!important;color:var(--txt-hi)!important;font-family:var(--font)!important;}}

/* ── Placeholder ── */
.ph-card{{
  background:var(--card-bg);border-radius:var(--r-xl);
  border:2px dashed var(--g200);padding:56px 24px;
  text-align:center;box-shadow:var(--sh-sm);
}}
.ph-icon {{font-size:3rem;display:block;margin-bottom:14px;}}
.ph-title{{font-size:1.15rem;font-weight:700;color:var(--txt-mid);margin-bottom:8px;}}
.ph-body {{font-size:.88rem;color:var(--txt-lo);line-height:1.8;}}

/* ── Footer ── */
.app-footer{{
  margin-top:52px;padding:22px 0 10px;
  border-top:1px solid var(--divider);text-align:center;
}}
.app-footer-ar{{font-size:1rem;font-weight:700;color:var(--blue);margin-bottom:4px;}}
.app-footer-en{{font-size:.65rem;color:var(--txt-lo);letter-spacing:1.5px;text-transform:uppercase;}}

hr{{border:none!important;border-top:1px solid var(--divider)!important;margin:6px 0!important;}}
</style>"""

# ═══════════════════════════════════════════════════════════
#  CACHED ENGINE  (unchanged)
# ═══════════════════════════════════════════════════════════
@st.cache_data(ttl=300, show_spinner=False)
def cached_run_engine(ticker, smt_ticker, htf_interval, exec_interval,
                      entry_interval, htf_period, exec_period):
    return E.run_engine(ticker, smt_ticker,
                        htf_interval=htf_interval, exec_interval=exec_interval,
                        entry_interval=entry_interval, htf_period=htf_period,
                        exec_period=exec_period)

@st.cache_data(ttl=300, show_spinner=False)
def cached_scan_pair(ticker, smt_ticker, htf_interval, exec_interval,
                     entry_interval, htf_period, exec_period):
    try:
        res = E.run_engine(ticker, smt_ticker,
                           htf_interval=htf_interval, exec_interval=exec_interval,
                           entry_interval=entry_interval, htf_period=htf_period,
                           exec_period=exec_period)
        return E.extract_row(res[0], ticker, smt_ticker)
    except Exception:
        return {"Ticker":ticker,"SMT":smt_ticker,"Grade":"ERR","Score":"—",
                "Bias":"ERROR","Entry":"—","SL":"—","TP1":"—","TP2":"—",
                "Potential R:R":"—","DOL":"—","SMT Signal":"—","Fractal":"—",
                "Killzone":"—","PD Array":"—","_score_num":-1,"_grade_rank":100}

# ═══════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════
def grade_hex(g):
    return {"A+":"#10B981","A":"#4F46E5","B":"#F59E0B","C":"#EF4444"}.get(g,"#9CA3AF")

def grade_pill_html(g):
    cls = {"A+":"gp-ap","A":"gp-a","B":"gp-b","C":"gp-c"}.get(g,"gp-sk")
    return f'<span class="grade-pill {cls}">{g}</span>'

def _to_rr(v):
    try: return float(str(v).replace("1:",""))
    except Exception: return 0.0

def age_minutes(ts):
    if ts is None: return 9999
    utc = ts.astimezone(timezone.utc) if ts.tzinfo else ts.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - utc).total_seconds() / 60

def freshness_badge_html(ts, expired_limit_days=3):
    m = age_minutes(ts)
    if m >= expired_limit_days * 24 * 60:
        return ('<span class="expired-badge">&#128683; منتهية الصلاحية · Expired</span>')
    if m > 240:
        h,mn = int(m//60), int(m%60)
        return (f'<span class="outdated-badge">&#9888;&#65039; قديم ({h}h {mn}m)</span>')
    ts_str = ts.astimezone(timezone.utc).strftime("%H:%M UTC") if ts else "—"
    return f'<span class="fresh-badge">&#9989; محدّث · {ts_str}</span>'

def sec_header(icon, ar, en=""):
    en_h = f'<div class="sec-en">{en}</div>' if en else ""
    st.markdown(
        f'<div class="sec-head"><div class="sec-icon">{icon}</div>'
        f'<div><div class="sec-ar">{ar}</div>{en_h}</div>'
        f'<div class="sec-line"></div></div>', unsafe_allow_html=True)

def kpi_html(icon, num, ar, en, cls):
    return (f'<div class="kpi-card {cls}">'
            f'<div class="kpi-icon {cls}">{icon}</div>'
            f'<div class="kpi-body">'
            f'<div class="kpi-num {cls}">{num}</div>'
            f'<div class="kpi-ar">{ar}</div>'
            f'<div class="kpi-en">{en}</div>'
            f'</div></div>')

def app_footer():
    st.markdown(
        '<div class="app-footer">'
        '<div class="app-footer-ar">&#169; جميع الحقوق محفوظة للحبي</div>'
        '<div class="app-footer-en">'
        'منصة الحبي للتداول · للأغراض التعليمية فقط · ليس نصيحة مالية'
        '</div></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  MARKET CLOCK  (US/Eastern)
# ═══════════════════════════════════════════════════════════
def get_market_status():
    """Returns (is_open, status_ar, countdown_label, countdown_ar, day_str, time_str)"""
    try:
        import pytz
        et = pytz.timezone("US/Eastern")
        now_et = datetime.now(et)
    except Exception:
        now_et = datetime.now(timezone.utc)

    wd   = now_et.weekday()        # 0=Mon … 6=Sun
    h,m  = now_et.hour, now_et.minute

    OPEN_H,  OPEN_M  = 9,  30
    CLOSE_H, CLOSE_M = 16, 0

    is_weekday = wd < 5
    after_open  = (h, m) >= (OPEN_H,  OPEN_M)
    before_close= (h, m) <  (CLOSE_H, CLOSE_M)
    is_open = is_weekday and after_open and before_close

    def to_sec(hh, mm): return hh * 3600 + mm * 60
    now_sec  = to_sec(h, m) + now_et.second

    if is_open:
        remaining = to_sec(CLOSE_H, CLOSE_M) - now_sec
        remaining = max(remaining, 0)
        hh, rem   = divmod(remaining, 3600)
        mm, ss    = divmod(rem, 60)
        countdown_label = "يغلق بعد"
        countdown_ar    = f"{hh:02d}:{mm:02d}:{ss:02d}"
        status_ar = "السوق مفتوح"
    else:
        # next open
        if not is_weekday:
            days_until = (7 - wd) % 7
            if days_until == 0: days_until = 7
        else:
            days_until = 0
        open_sec = to_sec(OPEN_H, OPEN_M)
        if is_weekday and not after_open:
            diff = open_sec - now_sec
        else:
            diff = (days_until or 1) * 86400 + open_sec - now_sec
        diff = max(diff, 0)
        hh, rem = divmod(diff, 3600)
        mm, ss  = divmod(rem, 60)
        countdown_label = "يفتح بعد"
        countdown_ar    = f"{hh:02d}:{mm:02d}:{ss:02d}"
        status_ar = "السوق مغلق"

    # Arabic days
    DAYS_AR = ["الإثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]
    day_str  = DAYS_AR[wd]
    date_str = now_et.strftime("%d/%m/%Y")
    hour12   = now_et.strftime("%I:%M:%S")
    ampm     = "ص" if now_et.hour < 12 else "م"
    time_str = f"{hour12} {ampm}"

    return is_open, status_ar, countdown_label, countdown_ar, f"{day_str} {date_str}", time_str

# ═══════════════════════════════════════════════════════════
#  SCROLLING TICKER
# ═══════════════════════════════════════════════════════════
def render_ticker(radar_df):
    """Build a scrolling news ticker from scan results."""
    if radar_df is None or radar_df.empty:
        items = [
            ("TSLA","توصية: تحليل جاري","—","—"),
            ("NVDA","البروتوكول نشط","—","—"),
            ("AAPL","ICT Market Maker","—","—"),
        ]
    else:
        top = radar_df[radar_df["Grade"].isin(["A+","A"])].head(12)
        if top.empty:
            top = radar_df.head(8)
        items = []
        for _, row in top.iterrows():
            bias = "شراء ▲" if row.get("Bias","") == "Long" else "بيع ▼" if row.get("Bias","") == "Short" else "—"
            items.append((str(row.get("Ticker","?")),
                          f"{row.get('Grade','?')} · {bias}",
                          str(row.get("Entry","—")),
                          str(row.get("Potential R:R","—"))))

    parts = []
    for sym, label, entry, rr in items:
        bias_cls = "tick-up" if "▲" in label else "tick-down" if "▼" in label else ""
        parts.append(
            f'<span class="tick-item">'
            f'<span class="tick-sym">{sym}</span>'
            f'<span class="{bias_cls}">{label}</span>'
            f'<span style="color:rgba(255,255,255,.5);">دخول {entry} | R:R {rr}</span>'
            f'</span>')

    # Double the items for seamless loop
    ticker_html = "".join(parts * 2)
    st.markdown(
        f'<div class="ticker-wrap">'
        f'<div class="ticker-inner">{ticker_html}</div>'
        f'</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  HEADER  (brand + market clock + ticker)
# ═══════════════════════════════════════════════════════════
def render_header(mode, ticker_sym, smt, preset, n_sym):
    is_open, status_ar, cd_lbl, cd_ar, day_date, time_str = get_market_status()
    dot_cls = "open" if is_open else "closed"
    mode_lbl = "تحليل منفرد" if mode == "single" else "مسح الرادار"
    ctx_lbl  = f"{ticker_sym} / {smt}" if mode == "single" else f"{preset} · {n_sym} رمز"

    st.markdown(f"""
<div class="main-header">
  <div class="brand-row">
    <div class="brand-logo">💹</div>
    <div>
      <div class="brand-name">منصة الحبي للتداول</div>
      <div class="brand-sub">Al-Hubbi Trading Platform · ICT Protocol</div>
    </div>
  </div>
  <div class="header-right">
    <div class="market-clock">
      <div class="clock-dot {dot_cls}"></div>
      <div>
        <div class="clock-status">{status_ar}</div>
        <div class="clock-countdown">{cd_lbl}: <strong>{cd_ar}</strong></div>
      </div>
      <div style="border-right:1px solid rgba(255,255,255,.15);height:32px;margin:0 4px;"></div>
      <div>
        <div class="clock-time">{time_str}</div>
        <div class="clock-date">{day_date}</div>
      </div>
    </div>
    <span class="nav-pill">{mode_lbl}</span>
    <span class="nav-pill">{ctx_lbl}</span>
  </div>
</div>""", unsafe_allow_html=True)

    # Scrolling ticker
    render_ticker(st.session_state.get("radar_df"))

    # Home + Refresh + Theme toggle
    nb1, nb2, nb3, _ = st.columns([1, 1, 1.2, 8])
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
                st.session_state.single_ts = None
            else:
                st.session_state.radar_df = None
                st.session_state.radar_ts = None
            st.rerun()
    with nb3:
        theme_lbl = "☀️ وضع نهاري" if DARK else "🌙 وضع ليلي"
        if st.button(theme_lbl, use_container_width=True):
            st.session_state.theme = "light" if DARK else "dark"
            st.rerun()

# ═══════════════════════════════════════════════════════════
#  CONTROL BAR
# ═══════════════════════════════════════════════════════════
def render_controls():
    st.markdown(
        '<div class="ctrl-bar">'
        '<div class="ctrl-bar-title">&#9881; إعدادات التحليل — Analysis Settings</div>',
        unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6,c7 = st.columns([1.1,1.1,0.9,1.8,0.9,0.9,0.9])
    with c1:
        raw  = st.radio("النوع / Mode", ["سهم واحد","رادار"],
                        horizontal=False, label_visibility="visible")
        mode = "single" if "سهم" in raw else "radar"
    with c2:
        ticker = st.text_input("الرمز / Symbol", value="TSLA",
                               placeholder="TSLA").strip().upper()
    with c3:
        smt_ticker = st.text_input("SMT Pair", value="QQQ").strip().upper()
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

    d1,d2,d3,d4,d5,d6 = st.columns([1,1.1,1.1,1,1.8,1.6])
    with d1:
        exec_period  = st.selectbox("Exec Period", ["5d","10d","1mo"])
    with d2:
        score_min    = st.slider("الحد الأدنى للنقاط", 1, 13, E.SCORE_MIN)
    with d3:
        wick_min     = st.slider("Wick % Min", 5, 40, int(E.SWEEP_WICK_MIN))
    with d4:
        n_candles    = st.slider("عدد الشموع", 40, 150, 80)
    with d5:
        grade_filter = st.multiselect("فلتر Grade",["A+","A","B","C"],default=["A+","A"])
    with d6:
        bc1,bc2 = st.columns(2)
        with bc1:
            run_btn  = st.button("▶ تحليل", type="primary",
                                 use_container_width=True, disabled=(mode=="radar"))
        with bc2:
            scan_btn = st.button("📡 مسح", use_container_width=True,
                                 disabled=(mode=="single"))

    st.markdown("</div>", unsafe_allow_html=True)
    cfg = dict(htf_interval=htf_interval, exec_interval=exec_interval,
               entry_interval="5m", htf_period=htf_period,
               exec_period=exec_period, score_min=score_min,
               wick_min=wick_min, n_candles=n_candles,
               grade_filter=grade_filter)
    return mode, ticker, smt_ticker, watchlist, preset, cfg, run_btn, scan_btn

# ═══════════════════════════════════════════════════════════
#  META BANNER  (+3-day expiry check)
# ═══════════════════════════════════════════════════════════
def render_meta_banner(ticker_sym, smt, ts):
    ts_str = ts.strftime("%Y-%m-%d  %H:%M UTC") if ts else "—"
    badge  = freshness_badge_html(ts, expired_limit_days=3)
    st.markdown(
        f'<div class="meta-banner">'
        f'<div style="display:flex;gap:28px;align-items:center;flex-wrap:wrap;">'
        f'<div style="display:flex;align-items:center;gap:8px;">'
        f'<span style="font-size:1.1rem;">📌</span>'
        f'<div><div class="meta-label">الرمز · Symbol</div>'
        f'<div class="meta-val">{ticker_sym} <span style="color:var(--txt-lo);font-weight:400">/ {smt}</span></div>'
        f'</div></div>'
        f'<div style="display:flex;align-items:center;gap:8px;">'
        f'<span style="font-size:1.1rem;">🕐</span>'
        f'<div><div class="meta-label">وقت التحليل · Timestamp</div>'
        f'<div class="meta-val" style="font-size:.85rem;">{ts_str}</div>'
        f'</div></div></div>{badge}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  KPI GRIDS
# ═══════════════════════════════════════════════════════════
def render_kpi_single(setup, df_htf, dol):
    cur   = float(df_htf["Close"].iloc[-1])
    prev  = float(df_htf["Close"].iloc[-2]) if len(df_htf) > 1 else cur
    chg   = (cur - prev) / prev * 100
    sign  = "+" if chg >= 0 else ""
    chg_c = "green" if chg >= 0 else "red"
    bias_v = ("صعودي ▲" if (setup and setup.bias=="long") else
              "هبوطي ▼" if (setup and setup.bias=="short") else "—")
    bias_c = ("green" if (setup and setup.bias=="long") else
              "red"   if (setup and setup.bias=="short") else "teal")
    grade_c= {"A+":"green","A":"blue","B":"amber"}.get(
               setup.grade if setup else "", "teal")
    cards = (
        kpi_html("💰", f"{cur:.2f}",          "آخر سعر",        "Last Price",  "blue")  +
        kpi_html("📊", f"{sign}{chg:.2f}%",    "التغيير اليومي", "Daily Change", chg_c) +
        kpi_html("🎯", f"{dol.price:.2f}" if dol else "—",
                                                "هدف السيولة",    "DOL Target",  "amber") +
        kpi_html("⚖️", bias_v,                  "التحيز",         "Bias",        bias_c) +
        kpi_html("🏆", setup.grade if setup else "SKIP",
                                                "التقييم",        "Grade",       grade_c) +
        kpi_html("📈", f"{setup.score}/13" if setup else "—",
                                                "النقاط",         "Score",       "violet")
    )
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)

def render_kpi_radar(df):
    n_ap  = len(df[df["Grade"]=="A+"])
    n_a   = len(df[df["Grade"]=="A"])
    n_b   = len(df[df["Grade"]=="B"])
    n_lng = len(df[df["Bias"]=="Long"])
    n_sk  = len(df[df["Grade"].isin(["SKIP","ERR","TIMEOUT"])])
    n_rr3 = sum(1 for v in df["Potential R:R"] if _to_rr(v) >= 3)
    cards = (
        kpi_html("🔍", len(df),  "إجمالي المسح",  "Total Scanned",   "blue")  +
        kpi_html("⭐", n_ap,      "إعدادات A+",    "Grade A+ Setups", "green") +
        kpi_html("✅", n_a,       "إعدادات A",     "Grade A Setups",  "blue")  +
        kpi_html("⚠️", n_b,       "إعدادات B",     "Grade B Setups",  "amber") +
        kpi_html("▲",  n_lng,     "توجه صعودي",    "Long Bias",       "teal")  +
        kpi_html("⚡", n_rr3,     "R:R ≥ 3",       "R:R ≥ 3",         "violet")
    )
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)
    segs = (["<div class='stat-seg sap'></div>"] * n_ap +
            ["<div class='stat-seg saa'></div>"] * n_a  +
            ["<div class='stat-seg sbb'></div>"] * n_b  +
            ["<div class='stat-seg ssk'></div>"] * n_sk)
    st.markdown(f'<div class="stat-bar">{"".join(segs[:100])}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  DECISION LOG
# ═══════════════════════════════════════════════════════════
def render_decision_log(setup, current_price):
    if not setup:
        st.markdown(
            '<div class="dlog-wrap"><div style="padding:32px;text-align:center;">'
            '<div style="font-size:2.5rem;margin-bottom:12px;">📭</div>'
            '<div style="font-size:1rem;font-weight:700;color:var(--txt-lo);">'
            'لا يوجد إعداد صفقة</div>'
            '<div style="font-size:.8rem;color:var(--txt-lo);margin-top:6px;">'
            'النقاط أقل من الحد الأدنى</div>'
            '</div></div>', unsafe_allow_html=True)
        return

    bias_ar   = "▲ شراء LONG"  if setup.bias=="long"  else "▼ بيع SHORT"
    pill_html = grade_pill_html(setup.grade)

    html = (f'<div class="dlog-wrap">'
            f'<div class="dlog-head">'
            f'<span class="dlog-bias-txt">{bias_ar}</span>'
            f'<span style="display:flex;align-items:center;gap:8px;">{pill_html}'
            f'<span style="background:rgba(255,255,255,.2);border-radius:12px;'
            f'padding:3px 10px;font-size:.75rem;color:#fff;">{setup.score}/13</span>'
            f'</span></div>')

    for entry in setup.decision_log:
        dc  = ("#34D399" if entry.score_delta>0 else
               "#F87171" if entry.score_delta<0 else "#6B7280")
        ds  = f"+{entry.score_delta}" if entry.score_delta >= 0 else str(entry.score_delta)
        tr  = entry.reasoning[:105] + ("…" if len(entry.reasoning)>105 else "")
        rh  = f'<div class="dlog-risk">⚠ {entry.risk_note[:90]}</div>' if entry.risk_note else ""
        html += (f'<div class="dlog-entry">'
                 f'<div class="dlog-stage">{entry.stage}</div>'
                 f'<div class="dlog-find">{entry.finding}</div>'
                 f'<div class="dlog-rsn">{tr}</div>{rh}'
                 f'<div class="dlog-pts" style="color:{dc}">{ds} نقطة</div>'
                 f'</div>')

    pnl = ((current_price - setup.entry)/setup.entry*100
           if setup.bias=="long"
           else (setup.entry - current_price)/setup.entry*100)
    pc  = "#34D399" if pnl >= 0 else "#F87171"
    ps  = f"{'+ ' if pnl>=0 else ''}{pnl:.2f}%"
    html += (f'<div class="dlog-pnl">'
             f'<div class="dlog-pnl-lbl">الربح / الخسارة غير المحقق · Unrealised P&L</div>'
             f'<div class="dlog-pnl-val" style="color:{pc}">{ps}</div>'
             f'</div></div>')
    st.markdown(html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  TRADE TABLE  (symbol + timestamp + expiry check)
# ═══════════════════════════════════════════════════════════
def render_trade_table(setup, ticker_sym, ts):
    sl_dist = abs(setup.entry - setup.stop_loss)
    ts_str  = ts.strftime("%Y-%m-%d %H:%M UTC") if ts else "—"
    m = age_minutes(ts)
    if m >= 3 * 24 * 60:
        ts_badge = ('<span style="background:#2D1A00;border:1px solid #78350F;'
                   'border-radius:12px;padding:2px 10px;font-size:.7rem;color:#FBBF24;">'
                   '⏰ منتهية الصلاحية</span>')
    elif m > 240:
        ts_badge = ('<span style="background:#2D0A0A;border:1px solid #7F1D1D;'
                   'border-radius:12px;padding:2px 10px;font-size:.7rem;color:#F87171;">'
                   '⚠️ قديم</span>')
    else:
        ts_badge = ('<span style="background:#052E1C;border:1px solid #065F46;'
                   'border-radius:12px;padding:2px 10px;font-size:.7rem;color:#34D399;">'
                   '✅ محدّث</span>')

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
            rows.append({"cls":"tl-tp","Level":f"هدف  {t.label}",
                         "Price":f"{t.price:.4f}",
                         "Dist":f"{abs(t.price-setup.entry):.4f}",
                         "RR":f"1:{rr}","Note":f"+{t.level}σ من نطاق التلاعب"})

    html = (f'<div class="tl-wrap">'
            f'<div class="tl-header-row">'
            f'<div><div class="tl-header-title">🎯 خطة الصفقة · Trade Plan</div>'
            f'<div class="tl-header-sub">Trade Setup &amp; StdDev Targets</div></div>'
            f'<div style="display:flex;gap:18px;align-items:center;">'
            f'<div style="text-align:center;">'
            f'<div class="tl-header-sub">الرمز</div>'
            f'<div style="font-size:1rem;font-weight:800;color:#fff;">{ticker_sym}</div>'
            f'</div>'
            f'<div style="text-align:center;">'
            f'<div class="tl-header-sub">التوقيت</div>'
            f'<div style="font-size:.78rem;color:rgba(255,255,255,.82);">{ts_str}</div>'
            f'</div>'
            f'<div>{ts_badge}</div>'
            f'</div></div>'
            f'<table class="tl-table"><thead><tr>'
            f'<th>المستوى</th><th>السعر</th><th>المسافة</th><th>R:R</th><th>الملاحظة</th>'
            f'</tr></thead><tbody>')
    for r in rows:
        html += (f'<tr class="{r["cls"]}">'
                 f'<td>{r["Level"]}</td><td class="tl-num">{r["Price"]}</td>'
                 f'<td class="tl-num">{r["Dist"]}</td><td><b>{r["RR"]}</b></td>'
                 f'<td>{r["Note"]}</td></tr>')
    html += "</tbody></table></div>"
    st.markdown(html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  RADAR TABLE  (.map not .applymap)
# ═══════════════════════════════════════════════════════════
def _styled_radar(show, is_dark):
    ap_bg  = "#052E1C" if is_dark else "background-color:#DCFCE7"
    a_bg   = "#1E2052" if is_dark else "background-color:#DBEAFE"
    b_bg   = "#2D1A00" if is_dark else "background-color:#FEF9C3"

    def sg(v):
        m = {"A+":f"background-color:{ap_bg};color:{'#34D399' if is_dark else '#15803D'};font-weight:700",
             "A": f"background-color:{a_bg};color:{'#818CF8' if is_dark else '#1D4ED8'};font-weight:700",
             "B": f"background-color:{b_bg};color:{'#FBBF24' if is_dark else '#854D0E'};font-weight:600",
             "SKIP":"color:#6B7280","ERR":f"color:{'#F87171' if is_dark else '#EF4444'}"}
        return m.get(str(v), "color:#6B7280")
    def sb(v):
        if "Long"  in str(v): return f"color:{'#34D399' if is_dark else '#10B981'};font-weight:700"
        if "Short" in str(v): return f"color:{'#F87171' if is_dark else '#EF4444'};font-weight:700"
        return "color:#6B7280"
    def sr(v):
        r = _to_rr(v)
        return (f"color:{'#34D399' if is_dark else '#10B981'};font-weight:700" if r>=3 else
                f"color:{'#FBBF24' if is_dark else '#F59E0B'}" if r>=2 else "color:#6B7280")
    def sf(v):
        return (f"color:{'#34D399' if is_dark else '#10B981'};font-weight:600"
                if "H1+M15+M5" in str(v) else
                f"color:{'#FBBF24' if is_dark else '#F59E0B'}"
                if "H1+M15" in str(v) else "color:#6B7280")
    def ss(v):
        return f"color:{'#A78BFA' if is_dark else '#7C3AED'};font-weight:600" if "Div" in str(v) else "color:#6B7280"

    tbl_bg   = T["tbl_bg"]
    tbl_head = T["tbl_head"]
    border   = T["border"]

    return (show.style
            .map(sg, subset=["Grade"])
            .map(sb, subset=["Bias"])
            .map(sr, subset=["Potential R:R"])
            .map(sf, subset=["Fractal"])
            .map(ss, subset=["SMT Signal"])
            .set_properties(**{"font-family":"'Tajawal',sans-serif",
                               "font-size":"13px","text-align":"right",
                               "background-color":tbl_bg})
            .set_table_styles([
                {"selector":"thead th",
                 "props":f"background:{tbl_head};color:var(--txt-lo);font-size:11px;"
                         "font-weight:600;letter-spacing:1px;text-transform:uppercase;"
                         "padding:10px 14px;text-align:right;"},
                {"selector":"tbody td","props":"padding:10px 14px;"},
                {"selector":"tbody tr:hover td",
                 "props":f"background-color:{T['tbl_row_hover']};"},
            ]))

# ═══════════════════════════════════════════════════════════
#  SINGLE STOCK VIEW
# ═══════════════════════════════════════════════════════════
def render_single(ticker_sym, smt_ticker, cfg, run_btn):
    # 3-day expiry check on existing result
    ts_existing = st.session_state.get("single_ts")
    if ts_existing and age_minutes(ts_existing) >= 3 * 24 * 60:
        st.warning("⏰ البيانات المحفوظة منتهية الصلاحية (أكثر من 3 أيام). يرجى إعادة التحليل.")

    if run_btn:
        with st.spinner("جارٍ تشغيل المحرك الكامل…"):
            try:
                E.SWEEP_WICK_MIN = float(cfg["wick_min"])
                result = cached_run_engine(
                    ticker_sym, smt_ticker,
                    cfg["htf_interval"], cfg["exec_interval"],
                    cfg["entry_interval"], cfg["htf_period"], cfg["exec_period"])
                st.session_state.single_result  = result
                st.session_state.single_ts      = datetime.now(timezone.utc)
                st.session_state.single_ticker  = ticker_sym
            except Exception as ex:
                st.error(f"خطأ في المحرك: {ex}"); return

    result = st.session_state.single_result
    if result is None:
        st.markdown(
            '<div class="ph-card"><span class="ph-icon">📊</span>'
            '<div class="ph-title">في انتظار التحليل · Awaiting Analysis</div>'
            '<div class="ph-body">اضبط المعاملات واضغط <strong>▶ تحليل</strong></div>'
            '</div>', unsafe_allow_html=True)
        app_footer(); return

    setup, df_htf, df_exec, df_m5, liq_levels, swings, dol = result
    current = float(df_htf["Close"].iloc[-1])
    ts      = st.session_state.single_ts
    sym     = st.session_state.single_ticker or ticker_sym

    render_meta_banner(sym, smt_ticker, ts)
    sec_header("📊", "المؤشرات الرئيسية", "Key Metrics")
    render_kpi_single(setup, df_htf, dol)
    st.markdown("<br>", unsafe_allow_html=True)

    sec_header("📈", "حركة السعر والمستويات", "Price Action & Levels")
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

# ═══════════════════════════════════════════════════════════
#  RADAR VIEW
# ═══════════════════════════════════════════════════════════
def render_radar(watchlist, preset, cfg, scan_btn):
    if scan_btn: _run_scan(watchlist, cfg)

    # 3-day expiry check
    ts_radar = st.session_state.get("radar_ts")
    if ts_radar and age_minutes(ts_radar) >= 3 * 24 * 60:
        st.warning("⏰ نتائج المسح منتهية الصلاحية (أكثر من 1 أيام). يرجى إعادة المسح.")

    df = st.session_state.radar_df
    if df is None:
        st.markdown(
            '<div class="ph-card"><span class="ph-icon">📡</span>'
            '<div class="ph-title">الرادار في وضع الاستعداد · Radar Standby</div>'
            '<div class="ph-body">اختر قائمة المراقبة واضغط <strong>📡 مسح</strong></div>'
            '</div>', unsafe_allow_html=True)
        app_footer(); return

    sec_header("📊", "نتائج المسح", "Scan Summary")
    render_kpi_radar(df)

    f1,f2,f3 = st.columns([2,1,1])
    with f1: search      = st.text_input("🔍 بحث بالرمز", placeholder="AAPL")
    with f2: bias_filter = st.selectbox("التوجه / Bias", ["الكل","Long","Short"])
    with f3: rr_filter   = st.selectbox("الحد الأدنى R:R", ["الكل","≥ 1.5","≥ 2","≥ 3"])

    display = df.copy()
    gf = cfg.get("grade_filter", ["A+","A"])
    if gf:              display = display[display["Grade"].isin(gf)]
    if bias_filter != "الكل": display = display[display["Bias"] == bias_filter]
    if search:          display = display[display["Ticker"].str.contains(search.upper(), na=False)]
    rr_map = {"≥ 1.5":1.5,"≥ 2":2.0,"≥ 3":3.0}
    if rr_filter in rr_map:
        thr = rr_map[rr_filter]
        display = display[display["Potential R:R"].apply(lambda v: _to_rr(v) >= thr)]

    SHOW = ["Ticker","SMT","Grade","Score","Bias","Entry","SL",
            "TP1","TP2","Potential R:R","DOL","SMT Signal","Fractal","PD Array"]
    show = display[SHOW].copy()

    st.markdown(
        f'<div class="tbl-card"><div class="tbl-card-hd">'
        f'<span class="tbl-hd-ar">🏆 الإعدادات القابلة للتنفيذ · A+ أولاً</span>'
        f'<span class="tbl-hd-cnt">{len(show)} من {len(df)} إعداد</span>'
        f'</div>', unsafe_allow_html=True)
    st.dataframe(_styled_radar(show, DARK), use_container_width=True,
                 hide_index=True, height=468)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec_header("🔬", "تحليل تفصيلي", "Drill Down · Full Analysis")
    if show.empty:
        st.info("لا توجد نتائج تطابق الفلاتر."); app_footer(); return

    d1,d2,d3 = st.columns([2.5,1,1])
    with d1: selected  = st.selectbox("اختر الرمز / Select Symbol", show["Ticker"].tolist())
    with d2:
        st.markdown("<br>", unsafe_allow_html=True)
        drill_btn = st.button("🔬 تحميل الشارت", use_container_width=True)
    with d3:
        st.markdown("<br>", unsafe_allow_html=True)
        clear_btn = st.button("✕ مسح", use_container_width=True)

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
        f'<div class="drill-meta">SMT: {smt_pair} · {current:.4f} · {cfg["htf_interval"].upper()}</div>'
        f'</div>', unsafe_allow_html=True)

    render_meta_banner(tkr, smt_pair, ts)
    cc, lc = st.columns([2.6,1], gap="medium")
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
                       "Fractal":"—","PD Array":"—",
                       "_score_num":-2,"_grade_rank":101}
            results.append(row)
            done += 1
            g   = row.get("Grade","?")
            sym = {"A+":"⭐","A":"✅","B":"⚠️"}.get(g,"·")
            pb.progress(done/total, text=f"مسح {done}/{total} · {tkr} {sym} {g}")
    pb.empty()
    df = (pd.DataFrame(results)
            .sort_values(by=["_grade_rank","_score_num"], ascending=[True,False])
            .reset_index(drop=True))
    st.session_state.radar_df     = df
    st.session_state.radar_preset = cfg
    st.session_state.radar_ts     = datetime.now(timezone.utc)
    n_ap = len(df[df["Grade"]=="A+"])
    n_a  = len(df[df["Grade"]=="A"])
    n_b  = len(df[df["Grade"]=="B"])
    st.success(f"✅ اكتمل المسح · {len(df)} رمزاً · A+: {n_ap} · A: {n_a} · B: {n_b}")

# ═══════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════
def main():
    st.markdown(get_css(), unsafe_allow_html=True)
    mode, ticker, smt_ticker, watchlist, preset, cfg, run_btn, scan_btn = render_controls()
    render_header(mode, ticker, smt_ticker, preset, len(watchlist) if watchlist else 0)
    st.markdown("<br>", unsafe_allow_html=True)
    if mode == "single":
        render_single(ticker, smt_ticker, cfg, run_btn)
    else:
        render_radar(watchlist, preset, cfg, scan_btn)

if __name__ == "__main__":
    main()
