# app_v6.py — منصة الحبي للتداول v6 Pro
# يعمل مباشرة: streamlit run app_v6.py
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from pydantic import BaseModel
from typing import List, Optional
import random

# ==================== CONFIG ====================
st.set_page_config(page_title="منصة الحبي Pro", page_icon="ح", layout="wide", initial_sidebar_state="collapsed")

class Config:
    THEME_DARK = {
        "bg": "#0B0D16", "card": "#11141F", "brd": "#1C2136",
        "txt": "#E2E8F5", "txt2": "#8896B2", "accent": "#3B82F6",
        "green": "#22C55E", "red": "#EF4444", "amber": "#F59E0B"
    }

# ==================== MODELS ====================
class SignalRow(BaseModel):
    ticker: str
    name: str
    grade: str
    bias: str
    entry: float
    sl: float
    tp1: float
    wave: float
    rr: float
    liquidity: str
    score: int
    current: Optional[float] = None
    scan_date: str

# ==================== MOCK ENGINE ====================
# احذف هذا القسم عندما تربط engine.py الحقيقي
class MockEngine:
    def run_engine(self, ticker, market):
        # محاكاة بيانات
        base = 100 + random.uniform(-20, 20)
        return {
            "entry": round(base, 2),
            "sl": round(base * 0.97, 2),
            "tp1": round(base * 1.04, 2),
            "wave": round(base * 1.08, 2),
            "bias": random.choice(["Long", "Short"]),
            "grade": random.choice(["A+", "A", "B", "C"]),
            "liquidity": "OB",
            "rr": 2.5,
            "score": random.randint(70, 95)
        }

    def extract_row(self, data, ticker, market):
        return data

E = MockEngine()

# ==================== DATA LAYER ====================
@st.cache_data(ttl=300, show_spinner=False)
def fetch_signal(ticker: str, market: str) -> SignalRow:
    try:
        data = E.run_engine(ticker, market)
        current = data["entry"] * random.uniform(0.99, 1.01)
        return SignalRow(
            ticker=ticker,
            name=ticker,
            grade=data["grade"],
            bias=data["bias"],
            entry=data["entry"],
            sl=data["sl"],
            tp1=data["tp1"],
            wave=data["wave"],
            rr=data["rr"],
            liquidity=data["liquidity"],
            score=data["score"],
            current=round(current, 2),
            scan_date=datetime.now().strftime("%Y-%m-%d")
        )
    except Exception as e:
        return SignalRow(ticker=ticker, name=ticker, grade="ERR", bias="-",
                         entry=0, sl=0, tp1=0, wave=0, rr=0, liquidity="-", score=0,
                         scan_date=datetime.now().strftime("%Y-%m-%d"))

def scan_watchlist(tickers: List[str], market: str) -> pd.DataFrame:
    results = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(fetch_signal, t, market): t for t in tickers}
        for f in as_completed(futures):
            results.append(f.result().model_dump())
    df = pd.DataFrame(results)
    grade_order = {"A+": 0, "A": 1, "B": 2, "C": 3, "ERR": 4}
    df["rank"] = df["grade"].map(grade_order).fillna(5)
    return df.sort_values(["rank", "score"], ascending=[True, False]).reset_index(drop=True)

# ==================== UI HELPERS ====================
def market_status(market: str):
    now = datetime.now(timezone.utc)
    if market == "SA":
        # تاسي 10:00 - 15:00 بتوقيت الرياض
        is_open = 7 <= now.hour <= 12 # تقريبي
    else:
        is_open = 14 <= now.hour <= 21 # أمريكي
    return is_open, "يغلق بعد 2س 15د" if is_open else "يفتح بعد 5س"

def render_chart(entry, sl, tp1, wave, ticker):
    # Lightweight Charts مدمج
    html = f"""
    <div id="chart" style="height:400px;"></div>
    <script src="https://unpkg.com/lightweight-charts@4.1.0/dist/lightweight-charts.standalone.production.js"></script>
    <script>
    const chart = LightweightCharts.createChart(document.getElementById('chart'), {{
        layout: {{background: {{color: '#11141F'}}, textColor: '#E2E8F5'}},
        grid: {{vertLines: {{color: '#1C2136'}}, horzLines: {{color: '#1C2136'}}}},
        rightPriceScale: {{borderColor: '#1C2136'}},
    }});
    const series = chart.addCandlestickSeries();
    const data = [];
    let base = {entry};
    for(let i=0;i<80;i++){{
        base += (Math.random()-0.5)*2;
        data.push({{time: 1700000000 + i*86400, open: base, high: base+1, low: base-1, close: base+0.5}})
    }}
    series.setData(data);
    series.createPriceLine({{price: {entry}, color: '#3B82F6', lineWidth: 2, title: 'دخول'}});
    series.createPriceLine({{price: {sl}, color: '#EF4444', lineWidth: 2, title: 'وقف'}});
    series.createPriceLine({{price: {tp1}, color: '#22C55E', lineWidth: 2, title: 'هدف1'}});
    series.createPriceLine({{price: {wave}, color: '#F59E0B', lineWidth: 2, lineStyle: 2, title: 'موجة'}});
    </script>
    """
    components.html(html, height=420)

# ==================== MAIN APP ====================
if "theme" not in st.session_state: st.session_state.theme = "dark"
if "market" not in st.session_state: st.session_state.market = "US"
if "df" not in st.session_state: st.session_state.df = None

theme = Config.THEME_DARK

# CSS محترف مختصر
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@500;700;900&display=swap');
html,body{{font-family:'Tajawal',sans-serif;direction:rtl;background:{theme['bg']};color:{theme['txt']}}}
.header{{display:flex;justify-content:space-between;align-items:center;padding:14px 24px;background:{theme['card']};border-bottom:1px solid {theme['brd']}}}
.logo{{font-size:1.4rem;font-weight:900;color:{theme['accent']}}}
.card{{background:{theme['card']};border:1px solid {theme['brd']};border-radius:14px;padding:16px;margin-bottom:12px}}
.stat{{text-align:center}}.stat-v{{font-size:2rem;font-weight:900}}
.badge{{padding:4px 10px;border-radius:12px;font-size:0.75rem;font-weight:700}}
.badge-a{{background:rgba(34,197,94,.15);color:{theme['green']}}}
.badge-b{{background:rgba(245,158,11,.15);color:{theme['amber']}}}
</style>
""", unsafe_allow_html=True)

# Header
is_open, cd = market_status(st.session_state.market)
st.markdown(f"""
<div class="header">
  <div class="logo">ح منصة الحبي Pro</div>
  <div>{'🟢 مفتوح' if is_open else '🔴 مغلق'} · {cd}</div>
</div>
""", unsafe_allow_html=True)

# Controls
c1, c2, c3, c4 = st.columns([1,1,1,2])
with c1:
    if st.button("🇸🇦 سعودي", use_container_width=True, type="primary" if st.session_state.market=="SA" else "secondary"):
        st.session_state.market = "SA"; st.rerun()
with c2:
    if st.button("🇺🇸 أمريكي", use_container_width=True, type="primary" if st.session_state.market=="US" else "secondary"):
        st.session_state.market = "US"; st.rerun()
with c3:
    market_code = "2222.SR" if st.session_state.market=="SA" else "QQQ"
    tickers = ["2222","1120","2010","7010","1180"] if st.session_state.market=="SA" else ["AAPL","MSFT","NVDA","TSLA","AMD"]
with c4:
    if st.button("📡 مسح الرادار الآن", type="primary", use_container_width=True):
        with st.spinner("جاري المسح..."):
            st.session_state.df = scan_watchlist(tickers, market_code)
            st.success(f"تم مسح {len(tickers)} سهم")

# Stats
if st.session_state.df is not None and not st.session_state.df.empty:
    df = st.session_state.df
    total, active = len(df), len(df[df["grade"].isin(["A+","A"])])
    c1,c2,c3,c4 = st.columns(4)
    for col, label, val in [(c1,"الإجمالي",total),(c2,"نشط",active),(c3,"منتظر",len(df[df['grade']=='B'])),(c4,"قوة",f"{df['score'].mean():.0f}%")]:
        with col: st.markdown(f"<div class='card stat'><div>{label}</div><div class='stat-v'>{val}</div></div>", unsafe_allow_html=True)

# Table
if st.session_state.df is not None:
    df = st.session_state.df
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    for i, row in df.iterrows():
        color = theme['green'] if row['bias']=="Long" else theme['red']
        badge = "badge-a" if row['grade'] in ["A+","A"] else "badge-b"
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:60px 100px 1fr 90px 90px 90px 80px; padding:10px 0; border-bottom:1px solid {theme['brd']}">
          <div>{i+1}</div>
          <div style="font-weight:800">{row['ticker']}</div>
          <div><span class="badge {badge}">{row['grade']}</span></div>
          <div style="color:{color}">{row['entry']}</div>
          <div>{row['current']}</div>
          <div style="color:{theme['red']}">{row['sl']}</div>
          <div style="color:{theme['green']}">{row['tp1']}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # تفاصيل أول سهم
    if not df.empty:
        first = df.iloc[0]
        st.markdown(f"<div class='card'><h3>تحليل {first['ticker']} — {first['grade']}</h3></div>", unsafe_allow_html=True)
        render_chart(first['entry'], first['sl'], first['tp1'], first['wave'], first['ticker'])

else:
    st.info("اضغط مسح الرادار لبدء التحليل")
