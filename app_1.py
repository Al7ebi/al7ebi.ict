"""
app.py — منصة الحبي للتداول
النسخة المحسّنة: متجاوبة مع الجوال، سريعة، تصميم احترافي
"""

import streamlit as st
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import pandas as pd
import habbi_engine as E

# ══════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="منصة الحبي للتداول",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════
for k, v in {
    "theme":          "dark",
    "single_result":  None,
    "single_ts":      None,
    "single_ticker":  "TSLA",
    "single_smt":     "QQQ",
    "radar_df":       None,
    "radar_ts":       None,
    "drill":          None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

DARK = st.session_state.theme == "dark"

# ══════════════════════════════════════════════════════
#  DESIGN TOKENS
# ══════════════════════════════════════════════════════
if DARK:
    BG     = "#0B0D14"
    CARD   = "#12151F"
    CARD2  = "#181D2A"
    BRD    = "#1E2535"
    TXT    = "#E8EDF5"
    TXT2   = "#8B98A9"
    TXT3   = "#3A4558"
    INP    = "#181D2A"
    INPB   = "#1E2535"
    TBLH   = "#0B0D14"
    TBLHOV = "#181D2A"
    HDR    = "linear-gradient(135deg,#060810 0%,#0C1220 60%,#101828 100%)"
else:
    BG     = "#F0F2F6"
    CARD   = "#FFFFFF"
    CARD2  = "#F9FAFB"
    BRD    = "#E5E7EB"
    TXT    = "#111827"
    TXT2   = "#374151"
    TXT3   = "#9CA3AF"
    INP    = "#F9FAFB"
    INPB   = "#E5E7EB"
    TBLH   = "#F9FAFB"
    TBLHOV = "#F3F4F6"
    HDR    = "linear-gradient(135deg,#1E1B4B 0%,#2563EB 60%,#4F46E5 100%)"

BLUE   = "#3B82F6"
GREEN  = "#10B981"
RED    = "#EF4444"
AMBER  = "#F59E0B"
VIOLET = "#8B5CF6"
TEAL   = "#14B8A6"

# ══════════════════════════════════════════════════════
#  GLOBAL CSS — Mobile First
# ══════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');

/* ── Reset ── */
:root {{
  --bg:{BG}; --card:{CARD}; --card2:{CARD2};
  --brd:{BRD}; --txt:{TXT}; --txt2:{TXT2}; --txt3:{TXT3};
  --inp:{INP}; --inpb:{INPB}; --tblh:{TBLH}; --tblhov:{TBLHOV};
  --blue:{BLUE}; --green:{GREEN}; --red:{RED};
  --amber:{AMBER}; --violet:{VIOLET}; --teal:{TEAL};
  --font:'Tajawal','Noto Sans Arabic',sans-serif;
  --r:10px; --r2:14px; --r3:20px;
  --sh:0 1px 4px rgba(0,0,0,{"0.5" if DARK else "0.08"});
  --sh2:0 4px 16px rgba(0,0,0,{"0.6" if DARK else "0.12"});
}}
html,body,[class*="css"]{{
  background:{BG}!important;
  font-family:var(--font)!important;
  color:var(--txt)!important;
  direction:rtl!important;
}}
*{{box-sizing:border-box;margin:0;padding:0;}}
[data-testid="collapsedControl"],
[data-testid="stSidebar"],
section[data-testid="stSidebar"]{{display:none!important;}}
.main .block-container{{
  padding:0 clamp(12px,3vw,24px) 60px!important;
  max-width:1440px!important;
}}
::-webkit-scrollbar{{width:4px;height:4px;}}
::-webkit-scrollbar-thumb{{background:var(--brd);border-radius:4px;}}

/* ── HEADER ── */
.habbi-hdr{{
  background:{HDR};
  padding:clamp(14px,2.5vw,22px) clamp(16px,3vw,28px);
  margin:0 clamp(-12px,-3vw,-24px) 0;
  display:flex; align-items:center; justify-content:space-between;
  flex-wrap:wrap; gap:12px;
  border-bottom:1px solid rgba(59,130,246,0.2);
}}
.hdr-brand{{display:flex;align-items:center;gap:12px;}}
.hdr-logo{{
  width:clamp(38px,6vw,48px); height:clamp(38px,6vw,48px);
  background:rgba(255,255,255,0.14); border-radius:12px;
  display:flex; align-items:center; justify-content:center;
  font-size:clamp(1.2rem,3vw,1.5rem); flex-shrink:0;
}}
.hdr-name{{
  font-size:clamp(1.1rem,3.5vw,1.45rem);
  font-weight:800; color:#fff; line-height:1.15;
}}
.hdr-sub{{
  font-size:clamp(0.58rem,1.5vw,0.65rem);
  color:rgba(255,255,255,0.55); letter-spacing:1.5px;
  text-transform:uppercase; margin-top:2px;
}}
.hdr-right{{
  display:flex; align-items:center; gap:8px; flex-wrap:wrap;
}}

/* Market clock */
.mkt-clk{{
  background:rgba(0,0,0,0.28); border:1px solid rgba(255,255,255,0.12);
  border-radius:12px; padding:8px 13px;
  display:flex; align-items:center; gap:10px;
}}
.mkt-dot{{
  width:9px; height:9px; border-radius:50%; flex-shrink:0;
}}
.dot-open {{background:#4ADE80;animation:pg 1.8s infinite;}}
.dot-closed{{background:#F87171;animation:pr 1.8s infinite;}}
@keyframes pg{{0%,100%{{box-shadow:0 0 0 0 rgba(74,222,128,.5)}}50%{{box-shadow:0 0 0 5px rgba(74,222,128,0)}}}}
@keyframes pr{{0%,100%{{box-shadow:0 0 0 0 rgba(248,113,113,.5)}}50%{{box-shadow:0 0 0 5px rgba(248,113,113,0)}}}}
.mkt-info{{}}
.mkt-st{{font-size:clamp(0.72rem,1.8vw,0.82rem);font-weight:700;color:#fff;}}
.mkt-cd{{font-size:clamp(0.62rem,1.5vw,0.7rem);color:rgba(255,255,255,0.55);}}
.mkt-sep{{width:1px;height:28px;background:rgba(255,255,255,0.14);flex-shrink:0;}}
.mkt-time-v{{font-size:clamp(0.85rem,2.2vw,1rem);font-weight:800;color:#fff;letter-spacing:.5px;}}
.mkt-date-v{{font-size:clamp(0.6rem,1.4vw,0.67rem);color:rgba(255,255,255,0.5);}}

/* ── TICKER ── */
@keyframes tkmove{{0%{{transform:translateX(0)}}100%{{transform:translateX(-50%)}}}}
.ticker-wrap{{
  background:{"#060810" if DARK else "#1E1B4B"};
  overflow:hidden; height:33px;
  display:flex; align-items:center;
  margin:0 clamp(-12px,-3vw,-24px);
}}
.ticker-track{{
  display:inline-block;
  animation:tkmove 40s linear infinite;
  white-space:nowrap;
}}
.ticker-track:hover{{animation-play-state:paused;}}
.tk-item{{
  display:inline-flex; align-items:center; gap:6px;
  padding:0 22px; font-size:0.76rem; font-weight:500;
  color:rgba(255,255,255,0.82);
  border-left:1px solid rgba(255,255,255,0.08);
}}
.tk-sym{{color:#93C5FD;font-weight:700;}}
.tk-up {{color:#4ADE80;}} .tk-dn{{color:#F87171;}}

/* ── NAV ROW ── */
.nav-row{{
  display:flex; gap:8px; padding:10px 0 4px; flex-wrap:wrap;
}}
.stButton>button{{
  font-family:var(--font)!important; font-size:clamp(0.78rem,2vw,0.9rem)!important;
  font-weight:700!important; border-radius:10px!important;
  padding:clamp(7px,1.5vw,10px) clamp(12px,2.5vw,20px)!important;
  transition:all .2s!important; border:none!important;
  min-height:40px!important;
}}
.stButton>button:not([kind="primary"]){{
  background:var(--card2)!important; color:var(--txt2)!important;
  border:1px solid var(--brd)!important;
}}
.stButton>button[kind="primary"]{{
  background:linear-gradient(135deg,#1D4ED8,#4F46E5)!important;
  color:#fff!important; box-shadow:0 4px 14px rgba(29,78,216,0.4)!important;
}}
.stButton>button[kind="primary"]:hover{{transform:translateY(-1px)!important;}}

/* ── CTRL BAR ── */
.ctrl-bar{{
  background:var(--card); border-radius:14px;
  box-shadow:var(--sh); border:1px solid var(--brd);
  padding:clamp(12px,2vw,16px) clamp(14px,2.5vw,20px);
  margin:14px 0 6px;
}}
.ctrl-lbl{{
  font-size:0.62rem; font-weight:600; color:var(--txt3);
  letter-spacing:2px; text-transform:uppercase; margin-bottom:8px;
}}

/* Streamlit widget overrides */
.stSelectbox label,.stTextInput label,.stMultiSelect label,
.stSlider label,.stRadio label{{
  font-family:var(--font)!important;
  font-size:clamp(0.72rem,1.8vw,0.8rem)!important;
  font-weight:500!important; color:var(--txt3)!important;
}}
div[data-baseweb="select"]>div{{
  background:var(--inp)!important; border:1px solid var(--inpb)!important;
  border-radius:10px!important; font-family:var(--font)!important;
  font-size:clamp(0.8rem,2vw,0.9rem)!important; color:var(--txt)!important;
  min-height:40px!important;
}}
div[data-baseweb="select"]>div:focus-within{{
  border-color:var(--blue)!important;
  box-shadow:0 0 0 3px rgba(59,130,246,0.18)!important;
}}
div[data-baseweb="input"]>div{{
  background:var(--inp)!important; border:1px solid var(--inpb)!important;
  border-radius:10px!important; font-family:var(--font)!important;
  color:var(--txt)!important; min-height:40px!important;
}}
div[data-baseweb="input"]>div:focus-within{{
  border-color:var(--blue)!important;
  box-shadow:0 0 0 3px rgba(59,130,246,0.18)!important;
}}
div[data-testid="stProgressBar"]>div>div{{
  background:linear-gradient(90deg,#1D4ED8,#4F46E5)!important;border-radius:4px!important;
}}
div[data-testid="stProgressBar"]>div{{
  background:var(--brd)!important;border-radius:4px!important;
}}

/* ── SEC HEADER ── */
.sec-hd{{
  display:flex; align-items:center; gap:10px;
  margin:clamp(16px,3vw,22px) 0 clamp(10px,2vw,14px);
}}
.sec-ico{{
  width:34px; height:34px;
  background:rgba(59,130,246,{"0.2" if DARK else "0.1"});
  border-radius:9px; display:flex; align-items:center;
  justify-content:center; font-size:0.95rem; flex-shrink:0;
}}
.sec-ar{{font-size:clamp(0.95rem,2.5vw,1.1rem);font-weight:700;color:var(--txt);}}
.sec-en{{font-size:0.62rem;color:var(--txt3);letter-spacing:1.2px;text-transform:uppercase;}}
.sec-ln{{flex:1;height:1px;background:linear-gradient(90deg,var(--brd),transparent);}}

/* ── KPI GRID 3×2 — responsive ── */
.kpi-grid{{
  display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));
  gap:clamp(8px,1.5vw,13px);
  margin-bottom:4px;
}}
@media(max-width:600px){{
  .kpi-grid{{grid-template-columns:repeat(2,minmax(0,1fr));}}
}}
.kpi-c{{
  background:var(--card); border-radius:14px;
  padding:clamp(13px,2vw,17px) clamp(12px,2vw,16px) clamp(11px,1.8vw,14px);
  box-shadow:var(--sh); border:1px solid var(--brd);
  display:flex; align-items:center; gap:clamp(10px,1.5vw,13px);
  transition:box-shadow .2s,transform .2s;
  position:relative; overflow:hidden;
}}
.kpi-c:hover{{box-shadow:var(--sh2);transform:translateY(-1px);}}
.kpi-c::after{{
  content:''; position:absolute; right:0; top:0;
  width:4px; height:100%;
  border-radius:0 14px 14px 0;
}}
.kpi-c.bl::after{{background:{BLUE};}}
.kpi-c.gr::after{{background:{GREEN};}}
.kpi-c.rd::after{{background:{RED};}}
.kpi-c.am::after{{background:{AMBER};}}
.kpi-c.vl::after{{background:{VIOLET};}}
.kpi-c.tl::after{{background:{TEAL};}}
.kpi-ico{{
  width:clamp(40px,7vw,48px); height:clamp(40px,7vw,48px);
  border-radius:10px; display:flex; align-items:center;
  justify-content:center; font-size:clamp(1.1rem,2.5vw,1.3rem);
  flex-shrink:0;
}}
.kpi-ico.bl{{background:rgba(59,130,246,{"0.18" if DARK else "0.1"});}}
.kpi-ico.gr{{background:rgba(16,185,129,{"0.18" if DARK else "0.1"});}}
.kpi-ico.rd{{background:rgba(239,68,68,{"0.18" if DARK else "0.1"});}}
.kpi-ico.am{{background:rgba(245,158,11,{"0.18" if DARK else "0.1"});}}
.kpi-ico.vl{{background:rgba(139,92,246,{"0.18" if DARK else "0.1"});}}
.kpi-ico.tl{{background:rgba(20,184,166,{"0.18" if DARK else "0.1"});}}
.kpi-body{{flex:1;text-align:right;min-width:0;}}
.kpi-num{{font-size:clamp(1.5rem,4vw,1.9rem);font-weight:800;line-height:1;}}
.kpi-num.bl{{color:{BLUE};}} .kpi-num.gr{{color:{GREEN};}}
.kpi-num.rd{{color:{RED};}}  .kpi-num.am{{color:{AMBER};}}
.kpi-num.vl{{color:{VIOLET};}} .kpi-num.tl{{color:{TEAL};}}
.kpi-ar{{font-size:clamp(0.78rem,2vw,0.9rem);font-weight:600;color:var(--txt);margin-top:3px;}}
.kpi-en{{font-size:0.62rem;color:var(--txt3);letter-spacing:.5px;text-transform:uppercase;}}

/* ── GRADE PILLS ── */
.gpill{{
  display:inline-flex;align-items:center;
  font-size:0.7rem;font-weight:700;letter-spacing:1px;
  padding:3px 11px;border-radius:20px;
}}
.gp-ap{{background:{"#052E1C" if DARK else "#DCFCE7"};color:{"#4ADE80" if DARK else "#15803D"};}}
.gp-a {{background:{"#172554" if DARK else "#DBEAFE"};color:{"#93C5FD" if DARK else "#1D4ED8"};}}
.gp-b {{background:{"#2D1A00" if DARK else "#FEF9C3"};color:{"#FCD34D" if DARK else "#854D0E"};}}
.gp-sk{{background:var(--card2);color:var(--txt3);}}

/* ── META BANNER ── */
.meta-bn{{
  background:var(--card); border:1px solid var(--brd);
  border-radius:14px; padding:clamp(10px,1.8vw,13px) clamp(14px,2.5vw,18px);
  display:flex; align-items:center; justify-content:space-between;
  margin-bottom:13px; box-shadow:var(--sh); flex-wrap:wrap; gap:10px;
}}
.meta-lbl{{font-size:0.64rem;color:var(--txt3);letter-spacing:1.2px;text-transform:uppercase;}}
.meta-val{{font-size:clamp(0.82rem,2vw,0.9rem);font-weight:700;color:var(--txt2);}}
.badge-ok {{background:{"#052E1C" if DARK else "#ECFDF5"};border:1px solid {"#166534" if DARK else "#A7F3D0"};border-radius:20px;padding:4px 12px;font-size:0.76rem;font-weight:700;color:{"#4ADE80" if DARK else "#059669"};}}
.badge-old{{background:{"#2D0A0A" if DARK else "#FEF2F2"};border:1px solid {"#7F1D1D" if DARK else "#FECACA"};border-radius:20px;padding:4px 12px;font-size:0.76rem;font-weight:700;color:{"#F87171" if DARK else "#DC2626"};}}
.badge-exp{{background:{"#1F1300" if DARK else "#FFFBEB"};border:1px solid {"#78350F" if DARK else "#FDE68A"};border-radius:20px;padding:4px 12px;font-size:0.76rem;font-weight:700;color:{"#FCD34D" if DARK else "#92400E"};}}

/* ── DECISION LOG ── */
.dlog{{background:var(--card);border-radius:14px;box-shadow:var(--sh);border:1px solid var(--brd);overflow:hidden;}}
.dlog-hd{{background:linear-gradient(135deg,#1D4ED8,#4F46E5);padding:12px 16px;display:flex;align-items:center;justify-content:space-between;}}
.dlog-bias{{font-size:clamp(0.9rem,2.2vw,1.05rem);font-weight:700;color:#fff;}}
.dlog-e{{padding:clamp(9px,1.8vw,12px) clamp(14px,2.5vw,17px);border-bottom:1px solid var(--brd);transition:background .14s;}}
.dlog-e:last-child{{border-bottom:none;}}
.dlog-e:hover{{background:var(--card2);}}
.dlog-stage{{font-size:0.58rem;font-weight:700;color:#818CF8;letter-spacing:2px;text-transform:uppercase;margin-bottom:3px;}}
.dlog-find{{font-size:clamp(0.8rem,2vw,0.86rem);font-weight:600;color:var(--txt);margin-bottom:2px;}}
.dlog-rsn {{font-size:clamp(0.7rem,1.8vw,0.74rem);color:var(--txt3);line-height:1.55;}}
.dlog-risk{{font-size:0.69rem;color:{AMBER};margin-top:3px;}}
.dlog-pts {{font-size:0.7rem;font-weight:700;margin-top:4px;}}
.dlog-pnl {{background:var(--card2);padding:11px 16px;border-top:2px solid var(--brd);}}
.dlog-pnl-l{{font-size:0.6rem;color:var(--txt3);letter-spacing:1.8px;text-transform:uppercase;}}
.dlog-pnl-v{{font-size:clamp(1.1rem,3vw,1.28rem);font-weight:800;margin-top:2px;}}

/* ── TRADE TABLE ── */
.tl-card{{background:var(--card);border-radius:14px;box-shadow:var(--sh);border:1px solid var(--brd);overflow:hidden;}}
.tl-hdr{{background:linear-gradient(135deg,#1D4ED8,#4F46E5);padding:11px 17px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;}}
.tl-hdr-t{{font-size:clamp(0.82rem,2vw,0.93rem);font-weight:700;color:#fff;}}
.tl-hdr-s{{font-size:0.6rem;color:rgba(255,255,255,0.65);letter-spacing:1.5px;text-transform:uppercase;}}
.tl-table{{width:100%;border-collapse:collapse;font-family:var(--font);}}
.tl-table thead th{{background:var(--tblh);font-size:clamp(0.6rem,1.5vw,0.65rem);font-weight:600;color:var(--txt3);letter-spacing:1.5px;text-transform:uppercase;padding:9px 14px;text-align:right;border-bottom:2px solid var(--brd);white-space:nowrap;}}
.tl-table tbody td{{padding:clamp(8px,1.8vw,11px) 14px;font-size:clamp(0.8rem,2vw,0.88rem);border-bottom:1px solid var(--brd);color:var(--txt2);}}
.tl-table tbody tr:last-child td{{border-bottom:none;}}
.tl-table tbody tr:hover td{{background:var(--tblhov);}}
.tl-entry td:first-child{{color:{BLUE};font-weight:700;}}
.tl-sl    td:first-child{{color:{RED};font-weight:700;}}
.tl-tp    td:first-child{{color:{GREEN};font-weight:700;}}
.tl-ext   td:first-child{{color:{AMBER};font-weight:700;}}
.tl-num{{font-family:'JetBrains Mono','Courier New',monospace;font-size:clamp(0.78rem,2vw,0.86rem);}}

/* ── RADAR TABLE ── */
.tbl-card{{background:var(--card);border-radius:14px;box-shadow:var(--sh);border:1px solid var(--brd);overflow:hidden;}}
.tbl-hdr{{background:var(--card2);border-bottom:1px solid var(--brd);padding:11px 17px;display:flex;align-items:center;justify-content:space-between;}}
.tbl-hdr-ar{{font-size:clamp(0.82rem,2vw,0.9rem);font-weight:700;color:var(--txt);}}
.tbl-hdr-ct{{font-size:0.74rem;color:var(--txt3);}}
.stDataFrame iframe{{border:none!important;}}
.stDataFrame>div{{border:none!important;border-radius:0!important;}}

/* ── STAT BAR ── */
.sbar{{display:flex;gap:2px;height:5px;border-radius:3px;overflow:hidden;margin:6px 0 18px;}}

/* ── DRILL BADGE ── */
.drill-bd{{background:{"linear-gradient(135deg,#0F1D4A,#1A1060)" if DARK else "linear-gradient(135deg,#EFF6FF,#F0EDFF)"};border:1px solid {"#1E3A8A" if DARK else "#C7D2FE"};border-radius:14px;padding:11px 17px;display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;flex-wrap:wrap;gap:8px;}}
.drill-sym{{font-size:clamp(1.2rem,3.5vw,1.45rem);font-weight:800;color:{BLUE};}}
.drill-meta{{font-size:0.72rem;color:var(--txt3);}}

/* ── PLACEHOLDER ── */
.ph-card{{background:var(--card);border-radius:18px;border:2px dashed var(--brd);padding:clamp(36px,6vw,52px) 22px;text-align:center;box-shadow:var(--sh);}}
.ph-ico {{font-size:2.6rem;display:block;margin-bottom:12px;}}
.ph-tt  {{font-size:clamp(0.95rem,2.5vw,1.1rem);font-weight:700;color:var(--txt2);margin-bottom:7px;}}
.ph-body{{font-size:clamp(0.8rem,2vw,0.86rem);color:var(--txt3);line-height:1.8;}}

/* ── ALERTS ── */
div[data-testid="stInfo"]   {{background:{"#172354" if DARK else "#EFF6FF"}!important;border:1px solid {"#1E3A8A" if DARK else "#BFDBFE"}!important;border-radius:10px!important;color:var(--txt)!important;font-family:var(--font)!important;}}
div[data-testid="stSuccess"]{{background:{"#052E1C" if DARK else "#F0FDF4"}!important;border:1px solid {"#166534" if DARK else "#A7F3D0"}!important;border-radius:10px!important;color:var(--txt)!important;font-family:var(--font)!important;}}
div[data-testid="stError"]  {{background:{"#2D0A0A" if DARK else "#FEF2F2"}!important;border:1px solid {"#7F1D1D" if DARK else "#FECACA"}!important;border-radius:10px!important;color:var(--txt)!important;font-family:var(--font)!important;}}
div[data-testid="stWarning"]{{background:{"#1F1300" if DARK else "#FFFBEB"}!important;border:1px solid {"#78350F" if DARK else "#FDE68A"}!important;border-radius:10px!important;color:var(--txt)!important;font-family:var(--font)!important;}}

/* ── FOOTER ── */
.hb-footer{{margin-top:48px;padding:18px 0 8px;border-top:1px solid var(--brd);text-align:center;}}
.ft-ar{{font-size:clamp(0.88rem,2.2vw,0.98rem);font-weight:700;color:{BLUE};margin-bottom:3px;}}
.ft-en{{font-size:0.62rem;color:var(--txt3);letter-spacing:1.8px;text-transform:uppercase;}}
.ft-link{{color:{BLUE};text-decoration:none;font-weight:700;}}
hr{{border:none!important;border-top:1px solid var(--brd)!important;margin:6px 0!important;}}

/* ── Mobile tweaks ── */
@media(max-width:768px){{
  .habbi-hdr{{flex-direction:column;align-items:flex-start;}}
  .hdr-right{{width:100%;justify-content:flex-start;}}
  .mkt-clk{{width:100%;}}
}}
@media(max-width:480px){{
  .tl-table thead th,.tl-table tbody td{{padding:7px 10px;}}
}}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  CACHED ENGINE
# ══════════════════════════════════════════════════════
@st.cache_data(ttl=300, show_spinner=False)
def _run(ticker, smt):
    return E.run_habbi(ticker, smt)

@st.cache_data(ttl=300, show_spinner=False)
def _row(ticker, smt):
    try:
        res = E.run_habbi(ticker, smt)
        return E.extract_row(res[0], ticker, smt)
    except Exception:
        return E.extract_row(None, ticker, smt)


# ══════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════
def _ghex(g):
    return {
        "A+": GREEN, "A": BLUE, "B": AMBER, "C": RED
    }.get(g, TXT3)

def _gpill(g):
    c = {"A+":"gp-ap","A":"gp-a","B":"gp-b"}.get(g,"gp-sk")
    return f'<span class="gpill {c}">{g}</span>'

def _age(ts):
    if ts is None: return 9999
    u = ts.astimezone(timezone.utc) if ts.tzinfo else ts.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - u).total_seconds() / 60

def _fbadge(ts, days=3):
    m = _age(ts)
    if ts is None:       return '<span class="badge-exp">—</span>'
    if m >= days*24*60:  return '<span class="badge-exp">⏰ منتهية الصلاحية</span>'
    if m > 240:          return f'<span class="badge-old">⚠️ قديم ({int(m//60)}h)</span>'
    s = ts.astimezone(timezone.utc).strftime("%H:%M UTC")
    return f'<span class="badge-ok">✅ محدّث · {s}</span>'

def _is_exp(ts, days=3):
    return _age(ts) >= days * 24 * 60

def _rr(v):
    try: return float(str(v).replace("1:",""))
    except: return 0.0

def sec_hdr(icon, ar, en=""):
    e = f'<div class="sec-en">{en}</div>' if en else ""
    st.markdown(
        f'<div class="sec-hd"><div class="sec-ico">{icon}</div>'
        f'<div><div class="sec-ar">{ar}</div>{e}</div>'
        f'<div class="sec-ln"></div></div>',
        unsafe_allow_html=True)

def kpi(icon, num, ar, en, cls):
    return (
        f'<div class="kpi-c {cls}">'
        f'<div class="kpi-ico {cls}">{icon}</div>'
        f'<div class="kpi-body">'
        f'<div class="kpi-num {cls}">{num}</div>'
        f'<div class="kpi-ar">{ar}</div>'
        f'<div class="kpi-en">{en}</div>'
        f'</div></div>')

def footer():
    st.markdown(
        '<div class="hb-footer">'
        '<div class="ft-ar">© جميع الحقوق محفوظة للحبي</div>'
        '<div class="ft-en">Habbi Trading Platform · Educational Use · Not Financial Advice</div>'
        '<div style="margin-top:6px;font-size:0.72rem;color:' + TXT3 + ';">'
        'برعاية <a href="https://quantomoption.com/" class="ft-link" target="_blank">quantomoption.com</a>'
        '</div></div>',
        unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  MARKET CLOCK
# ══════════════════════════════════════════════════════
def _clock():
    try:
        import pytz
        et  = pytz.timezone("US/Eastern")
        now = datetime.now(et)
    except Exception:
        now = datetime.now(timezone.utc)

    wd = now.weekday(); h,m,s = now.hour, now.minute, now.second
    is_open = wd < 5 and (h,m) >= (9,30) and (h,m) < (16,0)

    def ts(hh, mm): return hh*3600 + mm*60
    ns = ts(h,m) + s

    if is_open:
        rem = max(ts(16,0) - ns, 0)
        hh, r = divmod(rem, 3600); mm2, ss = divmod(r, 60)
        lbl, cd = "يغلق بعد", f"{hh:02d}:{mm2:02d}:{ss:02d}"
        status, dot = "السوق مفتوح", "dot-open"
    else:
        if wd < 5 and (h,m) < (9,30):
            nxt = max(ts(9,30) - ns, 1)
        else:
            days = (7 - wd) % 7 or 1
            nxt  = days * 86400 + ts(9,30) - ns % 86400
        nxt = max(int(nxt), 1)
        hh, r = divmod(nxt, 3600); mm2, ss = divmod(r, 60)
        lbl, cd = "يفتح بعد", f"{hh:02d}:{mm2:02d}:{ss:02d}"
        status, dot = "السوق مغلق", "dot-closed"

    DAYS = ["الإثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]
    ampm = "ص" if h<12 else "م"
    h12  = h%12 or 12
    return is_open, status, lbl, cd, f"{h12:02d}:{m:02d}:{s:02d} {ampm}", \
           f"{DAYS[wd]}  {now.strftime('%d/%m/%Y')}", dot


# ══════════════════════════════════════════════════════
#  TICKER BAR
# ══════════════════════════════════════════════════════
def _ticker(radar_df):
    if radar_df is not None and not radar_df.empty:
        top = radar_df[radar_df["Grade"].isin(["A+","A"])].head(14)
        if top.empty: top = radar_df.head(10)
        items = []
        for _, row in top.iterrows():
            sym   = str(row.get("الرمز", "?"))
            bias  = str(row.get("الاتجاه", "—"))
            entry = row.get("الدخول", "—")
            rr    = row.get("أفضل R:R", "—")
            liq   = row.get("نوع السيولة", "—")
            bc    = "tk-up" if "شراء" in bias else "tk-dn"
            items.append(
                f'<span class="tk-item">'
                f'<span class="tk-sym">{sym}</span>'
                f'<span class="{bc}">{bias}</span>'
                f'<span style="color:rgba(255,255,255,.5)">دخول {entry}</span>'
                f'<span style="color:#FCD34D">R:R {rr}</span>'
                f'<span style="color:rgba(255,255,255,.35)">{liq}</span>'
                f'</span>')
    else:
        items = [
            '<span class="tk-item"><span class="tk-sym">TSLA</span><span class="tk-up">شراء ▲</span><span style="color:rgba(255,255,255,.5)">Habbi Golden Setup نشط</span></span>',
            '<span class="tk-item"><span class="tk-sym">NVDA</span><span class="tk-dn">بيع ▼</span><span style="color:rgba(255,255,255,.5)">Daily Sweep مكتمل</span></span>',
            '<span class="tk-item"><span class="tk-sym">AAPL</span><span class="tk-up">شراء ▲</span><span style="color:rgba(255,255,255,.5)">IFVG · 50% EQ</span></span>',
            '<span class="tk-item"><span class="tk-sym">SPY</span><span style="color:#93C5FD">انتظار MSS على H1</span></span>',
        ]
    inner = "".join(items * 2)
    st.markdown(
        f'<div class="ticker-wrap"><div class="ticker-track">{inner}</div></div>',
        unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  HEADER  +  NAV BUTTONS
# ══════════════════════════════════════════════════════
def render_header(mode, ticker, smt, preset, n_sym):
    is_open, status, cd_lbl, cd, time_s, date_s, dot = _clock()
    mode_lbl = "تحليل منفرد" if mode == "single" else "مسح الرادار"
    ctx_lbl  = f"{ticker} / {smt}" if mode == "single" \
               else f"{preset} · {n_sym} رمز"
    ts_key   = "single_ts" if mode == "single" else "radar_ts"
    fresh    = _fbadge(st.session_state.get(ts_key))

    st.markdown(f"""
<div class="habbi-hdr">
  <div class="hdr-brand">
    <div class="hdr-logo">💹</div>
    <div>
      <div class="hdr-name">منصة الحبي للتداول</div>
      <div class="hdr-sub">Habbi Golden Setup · ICT Price Action Only</div>
    </div>
  </div>
  <div class="hdr-right">
    <div class="mkt-clk">
      <div class="mkt-dot {dot}"></div>
      <div class="mkt-info">
        <div class="mkt-st">{status}</div>
        <div class="mkt-cd">{cd_lbl}: <b>{cd}</b></div>
      </div>
      <div class="mkt-sep"></div>
      <div>
        <div class="mkt-time-v">{time_s}</div>
        <div class="mkt-date-v">{date_s}</div>
      </div>
    </div>
    {fresh}
    <span style="background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:20px;padding:4px 12px;font-size:.72rem;color:rgba(255,255,255,.88);">{mode_lbl}</span>
    <span style="background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:20px;padding:4px 12px;font-size:.72rem;color:rgba(255,255,255,.88);">{ctx_lbl}</span>
  </div>
</div>""", unsafe_allow_html=True)

    _ticker(st.session_state.get("radar_df"))

    n1, n2, n3, _ = st.columns([1, 1, 1.2, 7])
    with n1:
        if st.button("🏠 رئيسية", use_container_width=True):
            for k, v in {
                "single_result": None, "single_ts": None,
                "radar_df": None, "radar_ts": None, "drill": None
            }.items():
                st.session_state[k] = v
            st.rerun()
    with n2:
        if st.button("🔄 تحديث", use_container_width=True):
            _run.clear(); _row.clear()
            if mode == "single":
                st.session_state.single_result = None
                st.session_state.single_ts = None
            else:
                st.session_state.radar_df = None
                st.session_state.radar_ts = None
            st.rerun()
    with n3:
        lbl = "☀️ نهاري" if DARK else "🌙 ليلي"
        if st.button(lbl, use_container_width=True):
            st.session_state.theme = "light" if DARK else "dark"
            st.rerun()


# ══════════════════════════════════════════════════════
#  CONTROL BAR
# ══════════════════════════════════════════════════════
def render_controls():
    st.markdown(
        '<div class="ctrl-bar">'
        '<div class="ctrl-lbl">⚙ إعدادات التحليل — Analysis Settings</div>',
        unsafe_allow_html=True)

    c1,c2,c3,c4,c5,c6,c7 = st.columns([1.1,1.1,0.9,1.9,0.9,0.9,0.9])
    with c1:
        raw  = st.radio("النوع", ["سهم واحد","رادار"], horizontal=False)
        mode = "single" if "سهم" in raw else "radar"
    with c2:
        ticker = st.text_input("الرمز / Symbol", value="TSLA").strip().upper()
    with c3:
        smt    = st.text_input("SMT Pair", value="QQQ").strip().upper()
    with c4:
        preset    = st.selectbox("قائمة المراقبة",
                                  list(E.WATCHLISTS.keys()),
                                  disabled=(mode=="single"))
        watchlist = E.WATCHLISTS[preset]
    with c5:
        htf_tf = st.selectbox("HTF",  ["1d","1wk","4h","1h"])
    with c6:
        n_can  = st.slider("الشموع", 40, 150, 80)
    with c7:
        gf     = st.multiselect("Grade", ["A+","A","B","C"], default=["A+","A"])

    d1, d2, d3 = st.columns([1,1,2])
    with d1:
        min_sc = st.slider("الحد الأدنى للنقاط", 1, 13, E.SCORE_MIN)
    with d2:
        min_wk = st.slider("Wick % Min", 5, 40, int(E.SWEEP_WICK_MIN))
    with d3:
        b1, b2 = st.columns(2)
        with b1:
            run_btn  = st.button("▶ تحليل", type="primary",
                                  use_container_width=True,
                                  disabled=(mode=="radar"))
        with b2:
            scan_btn = st.button("📡 مسح الرادار",
                                  use_container_width=True,
                                  disabled=(mode=="single"))

    st.markdown("</div>", unsafe_allow_html=True)
    cfg = dict(min_sc=min_sc, min_wk=min_wk, n_can=n_can,
               gf=gf, htf_tf=htf_tf)
    return mode, ticker, smt, watchlist, preset, cfg, run_btn, scan_btn


# ══════════════════════════════════════════════════════
#  META BANNER
# ══════════════════════════════════════════════════════
def meta_banner(ticker, smt, ts):
    ts_s  = ts.strftime("%Y-%m-%d  %H:%M UTC") if ts else "—"
    badge = _fbadge(ts)
    st.markdown(
        f'<div class="meta-bn">'
        f'<div style="display:flex;gap:22px;align-items:center;flex-wrap:wrap;">'
        f'<div style="display:flex;align-items:center;gap:8px;">'
        f'<span style="font-size:1rem;">📌</span>'
        f'<div><div class="meta-lbl">الرمز · Symbol</div>'
        f'<div class="meta-val">{ticker} <span style="color:var(--txt3);font-weight:400">/ {smt}</span></div>'
        f'</div></div>'
        f'<div style="display:flex;align-items:center;gap:8px;">'
        f'<span style="font-size:1rem;">🕐</span>'
        f'<div><div class="meta-lbl">وقت التحليل · Timestamp</div>'
        f'<div class="meta-val" style="font-size:.82rem;">{ts_s}</div>'
        f'</div></div></div>{badge}</div>',
        unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  KPI GRIDS
# ══════════════════════════════════════════════════════
def kpi_single(setup, df_d, dol):
    cur   = float(df_d["Close"].iloc[-1])
    prev  = float(df_d["Close"].iloc[-2]) if len(df_d) > 1 else cur
    chg   = (cur - prev) / prev * 100
    sign  = "+" if chg >= 0 else ""
    cc    = "gr" if chg >= 0 else "rd"
    bv    = ("صعودي ▲" if (setup and setup.bias=="long") else
             "هبوطي ▼" if (setup and setup.bias=="short") else "—")
    bc    = ("gr" if (setup and setup.bias=="long") else
             "rd" if (setup and setup.bias=="short") else "tl")
    gc    = {"A+":"gr","A":"bl","B":"am"}.get(
             setup.grade if setup else "", "tl")
    liq_t = setup.liquidity_type if setup else "—"
    cards = (
        kpi("💰", f"{cur:.2f}",          "آخر سعر",        "Last Price",    "bl") +
        kpi("📊", f"{sign}{chg:.2f}%",   "التغيير اليومي", "Daily Change",  cc)  +
        kpi("🎯", f"{dol.price:.2f}" if dol else "—", "هدف DOL","DOL Target","am") +
        kpi("⚖️", bv,                    "التحيز",          "Bias",          bc)  +
        kpi("🏆", setup.grade if setup else "SKIP","التقييم","Grade",         gc)  +
        kpi("🔥", liq_t,                 "نوع السيولة",     "Liq Type",      "vl")
    )
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)

def kpi_radar(df):
    n_ap  = len(df[df["Grade"]=="A+"])
    n_a   = len(df[df["Grade"]=="A"])
    n_b   = len(df[df["Grade"]=="B"])
    n_lng = len(df[df["الاتجاه"].str.contains("شراء", na=False)])
    n_sk  = len(df[df["Grade"].isin(["SKIP","ERR","TIMEOUT"])])
    n_rr3 = sum(1 for v in df["أفضل R:R"] if _rr(v) >= 3)
    cards = (
        kpi("🔍", len(df), "إجمالي المسح",  "Total Scanned",  "bl") +
        kpi("⭐", n_ap,    "إعدادات A+",     "Grade A+",       "gr") +
        kpi("✅", n_a,     "إعدادات A",      "Grade A",        "bl") +
        kpi("⚠️", n_b,    "إعدادات B",      "Grade B",        "am") +
        kpi("▲",  n_lng,  "توجه صعودي",     "Long Bias",      "tl") +
        kpi("⚡", n_rr3,  "R:R أعلى من 3",  "R:R ≥ 3",        "vl")
    )
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)

    # Stat bar
    total = max(len(df), 1)
    ap_w = round(n_ap/total*100); a_w = round(n_a/total*100)
    b_w  = round(n_b/total*100);  sk_w = max(100-ap_w-a_w-b_w, 0)
    seg  = lambda w,c: f'<div style="flex:{w};height:5px;background:{c};"></div>' if w else ""
    st.markdown(
        f'<div class="sbar">'
        f'{seg(ap_w, GREEN)}{seg(a_w, BLUE)}{seg(b_w, AMBER)}{seg(sk_w, BRD)}'
        f'</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  DECISION LOG
# ══════════════════════════════════════════════════════
def render_dlog(setup, cur_price):
    if not setup:
        st.markdown(
            '<div class="dlog"><div style="padding:26px;text-align:center;">'
            '<div style="font-size:2.2rem;margin-bottom:10px;">📭</div>'
            '<div style="font-size:0.95rem;font-weight:700;color:var(--txt3);">لا يوجد إعداد صفقة</div>'
            '<div style="font-size:0.78rem;color:var(--txt3);margin-top:5px;">النقاط أقل من الحد الأدنى</div>'
            '</div></div>', unsafe_allow_html=True)
        return

    bias_col = "#4ADE80" if setup.bias=="long" else "#F87171"
    bias_ar  = "▲ شراء LONG" if setup.bias=="long" else "▼ بيع SHORT"
    pill     = _gpill(setup.grade)

    html = (f'<div class="dlog">'
            f'<div class="dlog-hd">'
            f'<span class="dlog-bias" style="color:{bias_col}">{bias_ar}</span>'
            f'<span style="display:flex;align-items:center;gap:7px;">{pill}'
            f'<span style="background:rgba(255,255,255,.18);border-radius:11px;'
            f'padding:2px 9px;font-size:.72rem;color:#fff;">{setup.score}</span>'
            f'</span></div>')

    for lg in setup.logs:
        dc  = ("#4ADE80" if lg.pts > 0 else "#F87171" if lg.pts < 0 else "#6B7280")
        ds  = f"+{lg.pts}" if lg.pts >= 0 else str(lg.pts)
        tr  = lg.reason[:110] + ("…" if len(lg.reason) > 110 else "")
        rh  = f'<div class="dlog-risk">⚠ {lg.risk[:90]}</div>' if lg.risk else ""
        html += (f'<div class="dlog-e">'
                 f'<div class="dlog-stage">{lg.stage}</div>'
                 f'<div class="dlog-find">{lg.finding}</div>'
                 f'<div class="dlog-rsn">{tr}</div>{rh}'
                 f'<div class="dlog-pts" style="color:{dc}">{ds} نقطة</div>'
                 f'</div>')

    pnl = ((cur_price-setup.entry)/setup.entry*100 if setup.bias=="long"
           else (setup.entry-cur_price)/setup.entry*100)
    pc  = "#4ADE80" if pnl >= 0 else "#F87171"
    ps  = f"{'+' if pnl>=0 else ''}{pnl:.2f}%"
    html += (f'<div class="dlog-pnl">'
             f'<div class="dlog-pnl-l">الربح/الخسارة غير المحقق · Unrealised P&L</div>'
             f'<div class="dlog-pnl-v" style="color:{pc}">{ps}</div>'
             f'</div></div>')
    st.markdown(html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  TRADE TABLE
# ══════════════════════════════════════════════════════
def render_trade_table(setup, ticker, ts):
    sl_d = abs(setup.entry - setup.sl)
    ts_s = ts.strftime("%Y-%m-%d %H:%M UTC") if ts else "—"
    m    = _age(ts)
    ts_b = ('<span style="background:#052E1C;border:1px solid #166534;border-radius:10px;padding:2px 9px;font-size:.66rem;color:#4ADE80;">✅ محدّث</span>'
            if m <= 240 else
            '<span style="background:#2D0A0A;border:1px solid #7F1D1D;border-radius:10px;padding:2px 9px;font-size:.66rem;color:#F87171;">⚠️ قديم</span>'
            if m < 3*24*60 else
            '<span style="background:#1F1300;border:1px solid #78350F;border-radius:10px;padding:2px 9px;font-size:.66rem;color:#FCD34D;">⏰ منتهي</span>')

    rows = [
        {"cls":"tl-entry","L":"الدخول · Entry",    "P":f"{setup.entry:.4f}","D":"—","RR":"مرجع","N":"50% EQ · IFVG"},
        {"cls":"tl-sl",   "L":"وقف الخسارة · SL",  "P":f"{setup.sl:.4f}",
         "D":f"{sl_d:.4f}","RR":"—","N":"وراء منطقة السحب"},
    ]
    for t in setup.targets:
        rr  = abs(t.price - setup.entry) / max(sl_d, 1e-9)
        cls = "tl-ext" if t.kind in ("ext_liq","ext_ext") else "tl-tp"
        rows.append({"cls":cls,"L":t.label,"P":f"{t.price:.4f}",
                     "D":f"{abs(t.price-setup.entry):.4f}",
                     "RR":f"1:{rr:.1f}","N":f"level {t.level:.0f}"})

    html = (f'<div class="tl-card">'
            f'<div class="tl-hdr">'
            f'<div><div class="tl-hdr-t">🎯 خطة الصفقة · Trade Plan</div>'
            f'<div class="tl-hdr-s">Habbi Golden Setup</div></div>'
            f'<div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap;">'
            f'<div style="text-align:center;">'
            f'<div class="tl-hdr-s">الرمز</div>'
            f'<div style="font-size:.95rem;font-weight:800;color:#fff;">{ticker}</div></div>'
            f'<div style="text-align:center;">'
            f'<div class="tl-hdr-s">التوقيت</div>'
            f'<div style="font-size:.74rem;color:rgba(255,255,255,.8);">{ts_s}</div></div>'
            f'<div>{ts_b}</div></div></div>'
            f'<table class="tl-table"><thead><tr>'
            f'<th>المستوى</th><th>السعر</th>'
            f'<th>المسافة</th><th>R:R</th><th>ملاحظة</th>'
            f'</tr></thead><tbody>')
    for r in rows:
        html += (f'<tr class="{r["cls"]}">'
                 f'<td>{r["L"]}</td>'
                 f'<td class="tl-num">{r["P"]}</td>'
                 f'<td class="tl-num">{r["D"]}</td>'
                 f'<td><b>{r["RR"]}</b></td>'
                 f'<td>{r["N"]}</td></tr>')
    html += "</tbody></table></div>"
    st.markdown(html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  RADAR TABLE  ← .map() not .applymap()
# ══════════════════════════════════════════════════════
def _style_radar(show):
    def sg(v):
        m = {"A+":f"background-color:{'#052E1C' if DARK else '#DCFCE7'};color:{'#4ADE80' if DARK else '#15803D'};font-weight:700",
             "A": f"background-color:{'#172554' if DARK else '#DBEAFE'};color:{'#93C5FD' if DARK else '#1D4ED8'};font-weight:700",
             "B": f"background-color:{'#2D1A00' if DARK else '#FEF9C3'};color:{'#FCD34D' if DARK else '#854D0E'};font-weight:600",
             "SKIP":"color:#6B7280","ERR":f"color:{'#F87171' if DARK else '#DC2626'}"}
        return m.get(str(v), "color:#6B7280")
    def sb(v):
        if "شراء" in str(v): return f"color:{'#4ADE80' if DARK else '#16A34A'};font-weight:700"
        if "بيع"  in str(v): return f"color:{'#F87171' if DARK else '#DC2626'};font-weight:700"
        return "color:#6B7280"
    def sr(v):
        r = _rr(v)
        if r >= 3: return f"color:{'#4ADE80' if DARK else '#16A34A'};font-weight:700"
        if r >= 2: return f"color:{'#FCD34D' if DARK else '#D97706'}"
        return "color:#6B7280"
    def sm(v):
        if "MSS" in str(v): return f"color:{'#4ADE80' if DARK else '#16A34A'};font-weight:600"
        if "BOS" in str(v): return f"color:{'#FCD34D' if DARK else '#D97706'}"
        return "color:#6B7280"

    # .map() — NOT .applymap()
    return (show.style
            .map(sg, subset=["Grade"])
            .map(sb, subset=["الاتجاه"])
            .map(sr, subset=["أفضل R:R"])
            .map(sm, subset=["MSS"])
            .set_properties(**{
                "font-family": "'Tajawal',sans-serif",
                "font-size":   "13px",
                "text-align":  "right",
                "background-color": CARD,
            })
            .set_table_styles([
                {"selector": "thead th",
                 "props": (f"background:{TBLH};color:{TXT3};font-size:11px;"
                           "font-weight:600;letter-spacing:1.2px;"
                           "text-transform:uppercase;padding:10px 13px;"
                           f"border-bottom:2px solid {BRD};text-align:right;")},
                {"selector": "tbody td",
                 "props": "padding:9px 13px;"},
                {"selector": "tbody tr:hover td",
                 "props": f"background-color:{TBLHOV};"},
            ]))


# ══════════════════════════════════════════════════════
#  SINGLE STOCK VIEW
# ══════════════════════════════════════════════════════
def render_single(ticker, smt, cfg, run_btn):
    ts_ex = st.session_state.single_ts
    if ts_ex and _is_exp(ts_ex):
        st.warning("⏰ التحليل المحفوظ منتهي الصلاحية (أكثر من 3 أيام). اضغط تحليل.")

    if run_btn:
        with st.spinner("جارٍ تشغيل استراتيجية الحبي…"):
            try:
                E.SWEEP_WICK_MIN = float(cfg["min_wk"])
                res = _run(ticker, smt)
                st.session_state.single_result = res
                st.session_state.single_ts     = datetime.now(timezone.utc)
                st.session_state.single_ticker = ticker
                st.session_state.single_smt    = smt
            except Exception as ex:
                st.error(f"خطأ: {ex}"); return

    res = st.session_state.single_result
    if res is None:
        st.markdown(
            '<div class="ph-card"><span class="ph-ico">📊</span>'
            '<div class="ph-tt">في انتظار التحليل · Awaiting Analysis</div>'
            '<div class="ph-body">اضبط الرمز في شريط الإعدادات أعلاه<br>'
            'واضغط <b>▶ تحليل</b> لبدء البروتوكول الكامل</div>'
            '</div>', unsafe_allow_html=True)
        footer(); return

    if _is_exp(st.session_state.single_ts):
        st.markdown(
            '<div class="ph-card"><span class="ph-ico">⏰</span>'
            '<div class="ph-tt">تحليل منتهي الصلاحية · Expired</div>'
            '<div class="ph-body">أقدم من 3 أيام — تم الإخفاء تلقائياً<br>'
            'اضغط <b>🔄 تحديث</b> ثم <b>▶ تحليل</b></div>'
            '</div>', unsafe_allow_html=True)
        footer(); return

    setup, df_d, df_h1, df_m15, liq_lvls, sw_d, dol = res
    cur   = float(df_d["Close"].iloc[-1])
    ts    = st.session_state.single_ts
    sym   = st.session_state.single_ticker or ticker
    smt_s = st.session_state.single_smt    or smt

    meta_banner(sym, smt_s, ts)
    sec_hdr("📊", "المؤشرات الرئيسية", "Key Metrics")
    kpi_single(setup, df_d, dol)
    st.markdown("<br>", unsafe_allow_html=True)

    sec_hdr("📈", "حركة السعر والمستويات", "Price Action & Levels")
    cc, lc = st.columns([2.6, 1], gap="medium")
    with cc:
        fig = E.build_chart(df_d, setup, liq_lvls, sw_d, dol,
                             ticker=sym, n=cfg["n_can"], tf=cfg["htf_tf"])
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar": True, "displaylogo": False,
                                "modeBarButtonsToRemove": ["select2d","lasso2d"]})
    with lc:
        st.markdown("<br>", unsafe_allow_html=True)
        render_dlog(setup, cur)

    if setup:
        st.markdown("<br>", unsafe_allow_html=True)
        render_trade_table(setup, sym, ts)
    footer()


# ══════════════════════════════════════════════════════
#  RADAR VIEW
# ══════════════════════════════════════════════════════
def render_radar(watchlist, preset, cfg, scan_btn):
    if scan_btn: _do_scan(watchlist, cfg)

    ts_r = st.session_state.radar_ts
    if ts_r and _is_exp(ts_r):
        st.warning("⏰ نتائج الرادار منتهية الصلاحية. اضغط 🔄 ثم 📡 مسح.")

    df = st.session_state.radar_df
    if df is None:
        st.markdown(
            '<div class="ph-card"><span class="ph-ico">📡</span>'
            '<div class="ph-tt">الرادار في وضع الاستعداد · Radar Standby</div>'
            '<div class="ph-body">اختر قائمة المراقبة واضغط <b>📡 مسح الرادار</b></div>'
            '</div>', unsafe_allow_html=True)
        footer(); return

    if _is_exp(ts_r):
        st.markdown(
            '<div class="ph-card"><span class="ph-ico">⏰</span>'
            '<div class="ph-tt">نتائج منتهية الصلاحية · Expired</div>'
            '<div class="ph-body">أقدم من 3 أيام — مُخفاة تلقائياً</div>'
            '</div>', unsafe_allow_html=True)
        footer(); return

    sec_hdr("📊", "نتائج المسح", "Scan Summary")
    kpi_radar(df)

    f1, f2, f3 = st.columns([2, 1, 1])
    with f1: srch = st.text_input("🔍 بحث بالرمز", placeholder="AAPL")
    with f2: bf   = st.selectbox("الاتجاه", ["الكل","شراء ▲","بيع ▼"])
    with f3: rrf  = st.selectbox("Min R:R",  ["الكل","≥ 1.5","≥ 2","≥ 3"])

    disp = df.copy()
    gf = cfg.get("gf", ["A+","A"])
    if gf:           disp = disp[disp["Grade"].isin(gf)]
    if bf != "الكل": disp = disp[disp["الاتجاه"] == bf]
    if srch:         disp = disp[disp["الرمز"].str.contains(srch.upper(), na=False)]
    rrm = {"≥ 1.5": 1.5, "≥ 2": 2.0, "≥ 3": 3.0}
    if rrf in rrm:
        thr  = rrm[rrf]
        disp = disp[disp["أفضل R:R"].apply(lambda v: _rr(v) >= thr)]

    SHOW = ["الرمز","SMT","Grade","Score","الاتجاه","الدخول","SL",
            "TP1","الموجة (Ext)","أفضل R:R","نوع السيولة","MSS","IFVG 50%"]
    show = disp[[c for c in SHOW if c in disp.columns]].copy()

    st.markdown(
        f'<div class="tbl-card"><div class="tbl-hdr">'
        f'<span class="tbl-hdr-ar">🏆 الإعدادات الذهبية · A+ أولاً</span>'
        f'<span class="tbl-hdr-ct">{len(show)} من {len(df)}</span>'
        f'</div>', unsafe_allow_html=True)
    st.dataframe(_style_radar(show), use_container_width=True,
                 hide_index=True, height=470)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec_hdr("🔬", "تحليل تفصيلي", "Drill Down")

    if show.empty:
        st.info("لا نتائج تطابق الفلاتر الحالية.")
        footer(); return

    d1, d2, d3 = st.columns([2.5, 1, 1])
    with d1:
        sel = st.selectbox("اختر الرمز للتحليل", show["الرمز"].tolist())
    with d2:
        st.markdown("<br>", unsafe_allow_html=True)
        dbtn = st.button("🔬 تحميل الشارت", use_container_width=True)
    with d3:
        st.markdown("<br>", unsafe_allow_html=True)
        clr  = st.button("✕ مسح", use_container_width=True)

    if dbtn and sel: st.session_state.drill = sel
    if clr:          st.session_state.drill = None
    if st.session_state.drill:
        _drill(st.session_state.drill, df, watchlist, cfg)
    footer()


def _drill(tkr, df, watchlist, cfg):
    smt_p = next((s for t,s in watchlist if t==tkr), "QQQ")
    row   = df[df["الرمز"]==tkr]
    grade = row["Grade"].values[0] if not row.empty else "—"
    gc    = _ghex(grade)
    pill  = _gpill(grade)
    ts_r  = st.session_state.radar_ts

    with st.spinner(f"تحميل {tkr}…"):
        try:
            res = _run(tkr, smt_p)
            setup, df_d, df_h1, df_m15, liq_lvls, sw_d, dol = res
            cur = float(df_d["Close"].iloc[-1])
        except Exception as ex:
            st.error(f"خطأ: {ex}"); return

    st.markdown(
        f'<div class="drill-bd">'
        f'<div style="display:flex;align-items:center;gap:10px;">'
        f'<span class="drill-sym" style="color:{gc}">{tkr}</span>{pill}'
        f'</div>'
        f'<div class="drill-meta">SMT: {smt_p} · {cur:.4f} · {cfg["htf_tf"].upper()}</div>'
        f'</div>', unsafe_allow_html=True)

    meta_banner(tkr, smt_p, ts_r)
    cc, lc = st.columns([2.6, 1], gap="medium")
    with cc:
        fig = E.build_chart(df_d, setup, liq_lvls, sw_d, dol,
                             ticker=tkr, n=cfg["n_can"], tf=cfg["htf_tf"])
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar": True, "displaylogo": False})
    with lc:
        st.markdown("<br>", unsafe_allow_html=True)
        render_dlog(setup, cur)
    if setup:
        st.markdown("<br>", unsafe_allow_html=True)
        render_trade_table(setup, tkr, ts_r)


def _do_scan(watchlist, cfg):
    E.SWEEP_WICK_MIN = float(cfg["min_wk"])
    total, results = len(watchlist), []
    pb = st.progress(0, text="تهيئة الرادار…")

    def one(pair): return _row(pair[0], pair[1])

    done = 0
    with ThreadPoolExecutor(max_workers=4) as pool:
        futs = {pool.submit(one, p): p for p in watchlist}
        for fut in as_completed(futs):
            tkr, smt = futs[fut]
            try:   r = fut.result(timeout=25)
            except TimeoutError:
                r = E.extract_row(None, tkr, smt); r["Grade"] = "TIMEOUT"
            results.append(r)
            done += 1
            g   = r.get("Grade","?")
            sym = {"A+":"⭐","A":"✅","B":"⚠️"}.get(g,"·")
            pb.progress(done/total, text=f"مسح {done}/{total} · {tkr} {sym} {g}")

    pb.empty()
    df = (pd.DataFrame(results)
            .sort_values(by=["_r","_s"], ascending=[True, False])
            .reset_index(drop=True))
    st.session_state.radar_df = df
    st.session_state.radar_ts = datetime.now(timezone.utc)

    n_ap = len(df[df["Grade"]=="A+"])
    n_a  = len(df[df["Grade"]=="A"])
    n_b  = len(df[df["Grade"]=="B"])
    st.success(
        f"✅ اكتمل المسح · {len(df)} رمزاً  ·  "
        f"A+: {n_ap}  ·  A: {n_a}  ·  B: {n_b}")


# ══════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════
def main():
    mode, ticker, smt, watchlist, preset, cfg, run_btn, scan_btn = render_controls()
    render_header(mode, ticker, smt, preset,
                  len(watchlist) if watchlist else 0)
    st.markdown("<br>", unsafe_allow_html=True)

    if mode == "single":
        render_single(ticker, smt, cfg, run_btn)
    else:
        render_radar(watchlist, preset, cfg, scan_btn)


if __name__ == "__main__":
    main()
