from pathlib import Path
Path('output').mkdir(exist_ok=True)
code = '''import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="منصة الحبي للتداول", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
html, body, [class*="css"] { direction: rtl; text-align: right; font-family: 'Noto Kufi Arabic', 'Segoe UI', sans-serif; }
html { font-size: 19px; }
.stApp { background: #0d1117; color: #e5e7eb; }
.block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 100% !important; }
.shell { background:#161b26; border:1px solid #263244; border-radius:18px; box-shadow:0 8px 24px rgba(0,0,0,0.18); }
.top-shell { padding: 1rem 1.1rem; margin-bottom: 0.9rem; }
.iconbtn { width: 46px; height: 46px; border-radius: 14px; background: #1e2536; display: flex; align-items: center; justify-content: center; color: #aab3c5; font-size: 1.1rem; border: 1px solid #2b3550; }
.brand-badge { width: 56px; height: 56px; border-radius: 16px; background: linear-gradient(135deg,#2f80ed,#29b6f6); display:flex; align-items:center; justify-content:center; color:white; font-size:1.8rem; font-weight:800; box-shadow:0 10px 28px rgba(41,182,246,0.28); }
.brand-title { font-size:1.8rem; line-height:1.2; font-weight:900; color:#fff; margin:0; }
.brand-sub { color:#7a8497; font-size:0.93rem; margin-top:0.15rem; }
.clock-box { color:#aab3c5; font-size:1.05rem; font-weight:700; letter-spacing:0.5px; }
.tabs-shell { margin-bottom:0.65rem; border-bottom:1px solid #232c3b; padding:0 0.5rem; }
.market-tab { display:inline-flex; align-items:center; gap:0.45rem; color:#7b8498; font-size:1.05rem; font-weight:800; padding:0.95rem 0.3rem 0.8rem 0.3rem; margin-left:1.25rem; border-bottom:3px solid transparent; }
.market-tab.active { color:#3b82f6; border-bottom-color:#3b82f6; }
.status-shell { background:#0f1520; border:1px solid #243041; border-radius:16px; padding:0.95rem 1rem; margin-bottom:1rem; }
.status-dot { width:13px; height:13px; border-radius:999px; background:#ef4444; display:inline-block; margin-left:0.5rem; box-shadow:0 0 0 6px rgba(239,68,68,0.12); }
.status-text { color:#f87171; font-size:1.05rem; font-weight:900; }
.status-meta { color:#7b8498; font-size:0.95rem; }
.metric-card { background:#161b26; border:1px solid #263244; border-radius:18px; box-shadow:0 8px 24px rgba(0,0,0,0.10); padding:1rem 1.1rem; min-height:112px; }
.metric-label { color:#7b8498; font-size:0.98rem; margin-bottom:0.4rem; }
.metric-value { font-size:2.1rem; font-weight:900; line-height:1; }
.input-wrap .stTextInput > div > div > input, .input-wrap .stSelectbox > div > div > div, .input-wrap .stTextArea > div > div > textarea { background:#1e2536 !important; color:#e5e7eb !important; border:1px solid #334155 !important; border-radius:14px !important; padding:0.95rem 1rem !important; font-size:1rem !important; }
.input-wrap label { display:none !important; }
.card-shell { background:#161b26; border:1px solid #263244; border-radius:18px; box-shadow:0 8px 24px rgba(0,0,0,0.12); padding:1rem; min-height:280px; }
.symbol { font-size:1.15rem; font-weight:900; color:#fff; }
.company { color:#97a3b8; font-size:0.98rem; }
.badge { display:inline-block; padding:0.28rem 0.68rem; border-radius:999px; font-size:0.8rem; font-weight:800; }
.badge-active { background:rgba(34,197,94,0.16); color:#4ade80; }
.badge-waiting { background:rgba(250,204,21,0.14); color:#facc15; }
.badge-closed { background:rgba(148,163,184,0.12); color:#9ca3af; }
.badge-up { background:rgba(34,197,94,0.16); color:#4ade80; }
.badge-down { background:rgba(239,68,68,0.16); color:#f87171; }
.small-label { color:#7b8498; font-size:0.82rem; }
.small-value { color:#fff; font-size:0.98rem; font-weight:800; }
.progress-track { height:10px; background:#0d1117; border-radius:999px; overflow:hidden; }
.progress-fill { height:100%; border-radius:999px; background:linear-gradient(90deg,#22c55e,#3b82f6); }
.empty-shell { min-height:290px; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#6f7b90; margin-top:0.9rem; background:#161b26; border:1px solid #263244; border-radius:18px; }
.empty-icon { font-size:4rem; line-height:1; opacity:0.5; }
.footer-shell { margin-top:1rem; padding:0.85rem 1rem; color:#6f7b90; font-size:0.92rem; text-align:center; background:#161b26; border:1px solid #263244; border-radius:18px; }
.divider-gap { height:60px; }
.icon-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }
.icon-item { background:#161b26; border:1px solid #263244; border-radius:18px; padding:14px 10px; text-align:center; }
.icon-circle { width:56px; height:56px; border-radius:18px; margin:0 auto 8px; background:#1e2536; display:flex; align-items:center; justify-content:center; color:#fff; font-size:1.5rem; border:1px solid #2b3550; }
.icon-title { font-size:0.95rem; font-weight:800; color:#fff; line-height:1.25; }
.icon-short { font-size:0.78rem; color:#7b8498; margin-top:3px; }
.chat-box { background:#161b26; border:1px solid #263244; border-radius:18px; padding:16px; }
.msg { padding:12px 14px; border-radius:14px; margin:10px 0; }
.msg-user { background:#1e2536; border:1px solid #334155; }
.msg-bot { background:#0f1520; border:1px solid #243041; }
</style>
""", unsafe_allow_html=True)

for k, v in [("market", "saudi"), ("sort_by", "strength"), ("filter_strength", "all"), ("view_mode", "grid"), ("search", ""), ("trend_filter", "all"), ("selected_symbol", None)]:
    st.session_state.setdefault(k, v)

saudi = [
    {"symbol":"2222","name":"أرامكو","status":"active","strength":3,"entry":28.50,"current":29.10,"stop":27.80,"t1":29.50,"t2":30.20,"t3":31.00,"date":"2025-01-15","direction":"صاعد"},
    {"symbol":"1120","name":"الراجحي","status":"active","strength":3,"entry":95.00,"current":96.20,"stop":93.50,"t1":97.00,"t2":99.00,"t3":102.00,"date":"2025-01-14","direction":"صاعد"},
    {"symbol":"2010","name":"سابك","status":"waiting","strength":2,"entry":78.00,"current":77.40,"stop":76.50,"t1":80.00,"t2":82.00,"t3":85.00,"date":"2025-01-13","direction":"هابط"},
    {"symbol":"7010","name":"STC","status":"active","strength":2,"entry":42.00,"current":43.10,"stop":41.00,"t1":43.50,"t2":45.00,"t3":47.00,"date":"2025-01-12","direction":"صاعد"},
    {"symbol":"4200","name":"الدواء","status":"waiting","strength":1,"entry":55.00,"current":54.20,"stop":53.80,"t1":57.00,"t2":59.00,"t3":62.00,"date":"2025-01-10","direction":"هابط"},
    {"symbol":"1180","name":"الأهلي","status":"closed","strength":2,"entry":38.00,"current":39.50,"stop":37.00,"t1":39.50,"t2":41.00,"t3":43.00,"date":"2025-01-09","direction":"صاعد"},
]

us = [
    {"symbol":"AAPL","name":"Apple","status":"active","strength":3,"entry":192.00,"current":196.50,"stop":188.00,"t1":198.00,"t2":205.00,"t3":212.00,"date":"2025-01-15","direction":"صاعد"},
    {"symbol":"MSFT","name":"Microsoft","status":"active","strength":3,"entry":415.00,"current":422.00,"stop":408.00,"t1":425.00,"t2":435.00,"t3":450.00,"date":"2025-01-14","direction":"صاعد"},
    {"symbol":"TSLA","name":"Tesla","status":"waiting","strength":2,"entry":250.00,"current":247.00,"stop":242.00,"t1":260.00,"t2":275.00,"t3":290.00,"date":"2025-01-13","direction":"هابط"},
    {"symbol":"NVDA","name":"Nvidia","status":"active","strength":3,"entry":880.00,"current":910.00,"stop":860.00,"t1":920.00,"t2":960.00,"t3":1000.00,"date":"2025-01-12","direction":"صاعد"},
    {"symbol":"AMZN","name":"Amazon","status":"closed","strength":2,"entry":178.00,"current":185.00,"stop":174.00,"t1":185.00,"t2":192.00,"t3":200.00,"date":"2025-01-10","direction":"صاعد"},
]

def get_trades():
    return saudi if st.session_state.market == "saudi" else us

def get_progress(t):
    if t["status"] == "waiting": return 0
    rng = t["t1"] - t["entry"]
    return 0 if rng == 0 else max(0, min(100, ((t["current"] - t["entry"]) / rng) * 100))

def get_pnl(t):
    d = t["current"] - t["entry"]
    return d, (d / t["entry"]) * 100

def apply_filters(df):
    q = st.session_state.search.lower().strip()
    if q:
        df = df[df["symbol"].str.lower().str.contains(q) | df["name"].str.lower().str.contains(q)]
    fs = st.session_state.filter_strength
    if fs != "all": df = df[df["strength"] == int(fs)]
    tr = st.session_state.trend_filter
    if tr != "all": df = df[df["direction"] == tr]
    sb = st.session_state.sort_by
    if sb == "strength": df = df.sort_values(["strength", "date"], ascending=[False, False])
    elif sb == "progress": df = df.assign(_p=df.apply(lambda r: get_progress(r.to_dict()), axis=1)).sort_values(["_p", "date"], ascending=[False, False]).drop(columns=["_p"])
    else: df = df.sort_values("name")
    return df

def badge_for_direction(d):
    return "badge-up" if d == "صاعد" else "badge-down"

st.markdown(f"""
<div class="top-shell">
  <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem;">
    <div style="display:flex;align-items:center;gap:0.8rem;">
      <div class="iconbtn">🔔</div>
      <div class="iconbtn">🔊</div>
      <div class="iconbtn">☼</div>
      <div class="clock-box">{datetime.now().strftime("%H:%M:%S")}</div>
    </div>
    <div class="brand-wrap">
      <div style="text-align:right;">
        <div class="brand-title">منصة الحبي للتداول</div>
        <div class="brand-sub">تداول ذكي • تحليل متقدم</div>
      </div>
      <div class="brand-badge">ح</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tabs-shell">
  <span class="market-tab">السوق الأمريكي US</span>
  <span class="market-tab active">السوق السعودي SA</span>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="status-shell">
  <div style="display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;">
    <div><span class="status-dot"></span><span class="status-text">السوق مغلق - يفتح بعد 6س 40د</span></div>
    <div class="status-meta">آخر تحديث: {datetime.now().strftime("%H:%M:%S")} • التحديث كل 5 دقائق</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-wrap">', unsafe_allow_html=True)
col_f1, col_f2, col_f3, col_f4 = st.columns([2.8, 2.0, 2.0, 5.2])
with col_f4:
    st.text_input("", placeholder="ابحث بالرمز أو الاسم...", key="search", label_visibility="collapsed")
with col_f3:
    st.session_state.sort_by = st.selectbox("", ["strength", "progress", "name"], format_func=lambda x: {"strength":"ترتيب بالقوة", "progress":"ترتيب بالتقدم", "name":"ترتيب أبجدي"}[x], label_visibility="collapsed")
with col_f2:
    st.session_state.filter_strength = st.selectbox("", ["all", 3, 2, 1], format_func=lambda x: "جميع القوة" if x == "all" else f"قوة {x}", label_visibility="collapsed")
with col_f1:
    st.session_state.trend_filter = st.selectbox("", ["all", "صاعد", "هابط"], format_func=lambda x: "جميع الاتجاهات" if x == "all" else ("اتجاه صاعد" if x == "صاعد" else "اتجاه هابط"), label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

st.write("")
filtered = apply_filters(pd.DataFrame(get_trades()).copy())

m1, m2, m3, m4 = st.columns(4)
vals = [
    (m4, "إجمالي الصفقات", len(filtered), "#ffffff"),
    (m3, "صفقات نشطة", int((filtered["status"] == "active").sum()) if len(filtered) else 0, "#4ade80"),
    (m2, "صفقات منتظرة", int((filtered["status"] == "waiting").sum()) if len(filtered) else 0, "#facc15"),
    (m1, "صفقات مغلقة", int((filtered["status"] == "closed").sum()) if len(filtered) else 0, "#9ca3af"),
]
for c, label, val, color in vals:
    c.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value" style="color:{color}">{val}</div></div>', unsafe_allow_html=True)

st.write("")
icon_items = [("🔔", "تنبيهات", "NTF"), ("🔊", "صوت", "AUD"), ("☼", "مظهر", "THM"), ("↕", "فلتر", "FLT")]
st.markdown('<div class="icon-grid">' + ''.join([f'<div class="icon-item"><div class="icon-circle">{i}</div><div class="icon-title">{t}</div><div class="icon-short">{s}</div></div>' for i,t,s in icon_items]) + '</div>', unsafe_allow_html=True)

st.write("")

if len(filtered) == 0:
    st.markdown('<div class="empty-shell"><div class="empty-icon">🗃️</div><div style="margin-top:0.9rem;font-size:1.1rem;">لا توجد صفقات مطابقة للبحث</div></div>', unsafe_allow_html=True)
else:
    if st.session_state.view_mode == "table":
        rows = []
        for _, r in filtered.iterrows():
            _, p = get_pnl(r.to_dict())
            rows.append([r["symbol"], r["name"], r["date"], "نشط" if r["status"] == "active" else "منتظر" if r["status"] == "waiting" else "مغلق", r["direction"], "⭐" * int(r["strength"]), f'{r["entry"]:.2f}', f'{r["current"]:.2f}', f'{p:+.2f}%', f'{r["stop"]:.2f}', f'{r["t1"]:.2f}', f'{r["t2"]:.2f}', f'{r["t3"]:.2f}'])
        st.dataframe(pd.DataFrame(rows, columns=["الرمز", "الاسم", "التاريخ", "الحالة", "الاتجاه", "القوة", "الدخول", "الحالي", "ربح/خسارة", "وقف", "هدف1", "هدف2", "هدف3"]), use_container_width=True, hide_index=True)
    else:
        cols = st.columns(4)
        for i, (_, r) in enumerate(filtered.iterrows()):
            t = r.to_dict()
            _, p = get_pnl(t)
            status_class = "badge-active" if t["status"] == "active" else "badge-waiting" if t["status"] == "waiting" else "badge-closed"
            status_text = "نشط" if t["status"] == "active" else "منتظر" if t["status"] == "waiting" else "مغلق"
            dir_class = badge_for_direction(t["direction"])
            with cols[i % 4]:
                st.markdown(f"""
<div class="card-shell">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;">
    <div>
      <div class="symbol">{t['symbol']}</div>
      <div class="company">{t['name']}</div>
      <div style="margin-top:0.35rem;color:#768299;font-size:0.8rem;">{t['date']}</div>
    </div>
    <div style="text-align:left;">
      <span class="badge {status_class}">{status_text}</span>
      <div style="margin-top:0.35rem;"><span class="badge {dir_class}">{t['direction']}</span></div>
      <div style="margin-top:0.4rem;color:#94a3b8;font-size:0.85rem;">{'⭐' * int(t['strength'])}</div>
    </div>
  </div>
  <div style="margin-top:0.85rem;display:flex;justify-content:space-between;align-items:center;gap:0.5rem;">
    <div class="small-label">التقدم نحو الهدف 1</div>
    <div style="color:{'#4ade80' if p >= 0 else '#f87171'};font-weight:900;">{p:+.2f}%</div>
  </div>
  <div class="progress-track"><div class="progress-fill" style="width:{get_progress(t)}%;"></div></div>
  <div style="margin-top:0.9rem;display:grid;grid-template-columns:repeat(2,1fr);gap:0.5rem;">
    <div><div class="small-label">نقطة الدخول</div><div class="small-value">{t['entry']:.2f}</div></div>
    <div><div class="small-label">وقف الخسارة</div><div class="small-value" style="color:#f87171;">{t['stop']:.2f}</div></div>
    <div><div class="small-label">الهدف 1</div><div class="small-value" style="color:#4ade80;">{t['t1']:.2f}</div></div>
    <div><div class="small-label">السعر الحالي</div><div class="small-value">{t['current']:.2f}</div></div>
  </div>
  <div style="margin-top:0.8rem;display:grid;grid-template-columns:repeat(2,1fr);gap:0.5rem;">
    <div><div class="small-label">الهدف 2</div><div class="small-value" style="color:#4ade80;">{t['t2']:.2f}</div></div>
    <div><div class="small-label">الهدف 3</div><div class="small-value" style="color:#22d3ee;">{t['t3']:.2f}</div></div>
  </div>
  <div style="margin-top:0.9rem;display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;">
    <div class="shell" style="padding:10px 12px;text-align:center;">طلب تحليل الصفقة</div>
    <div class="shell" style="padding:10px 12px;text-align:center;">تواصل لتحليل الصفقه</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider-gap"></div>', unsafe_allow_html=True)
st.markdown('<div class="empty-shell"><div class="empty-icon">📦</div><div style="margin-top:0.8rem;font-size:1.02rem;">لا توجد صفقات مطابقة للبحث</div></div>', unsafe_allow_html=True)
st.markdown('<div class="footer-shell">جميع الحقوق محفوظة © 2025 منصة الحبي للتداول. هذه المنصة لأغراض تعليمية فقط ولا تتحمل أي التزامات مالية.</div>', unsafe_allow_html=True)
'''
Path('output/app.py').write_text(code, encoding='utf-8')
print('saved')
