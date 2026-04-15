
import streamlit as st
import pandas as pd
from datetime import datetime, time
import pytz

# إعدادات الصفحة
st.set_page_config(
    page_title="منصة الحبي للتداول",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS مخصص
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        direction: rtl;
    }
    body {
        background-color: #0d1117;
        color: #e5e7eb;
        font-family: 'Arial', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# ===== البيانات =====
saudi_trades = [
    {"symbol": "2222", "name": "أرامكو", "status": "نشط", "strength": 3, "entry": 28.50, "stopLoss": 27.80, "target1": 29.50, "target2": 30.20, "target3": 31.00, "current": 29.10},
    {"symbol": "1120", "name": "الراجحي", "status": "نشط", "strength": 3, "entry": 95.00, "stopLoss": 93.50, "target1": 97.00, "target2": 99.00, "target3": 102.00, "current": 96.20},
    {"symbol": "2010", "name": "سابك", "status": "منتظر", "strength": 2, "entry": 78.00, "stopLoss": 76.50, "target1": 80.00, "target2": 82.00, "target3": 85.00, "current": 77.40},
    {"symbol": "7010", "name": "STC", "status": "نشط", "strength": 2, "entry": 42.00, "stopLoss": 41.00, "target1": 43.50, "target2": 45.00, "target3": 47.00, "current": 43.10},
    {"symbol": "1180", "name": "الأهلي", "status": "مغلق", "strength": 2, "entry": 38.00, "stopLoss": 37.00, "target1": 39.50, "target2": 41.00, "target3": 43.00, "current": 39.50},
]

us_trades = [
    {"symbol": "AAPL", "name": "آبل", "status": "نشط", "strength": 3, "entry": 192.00, "stopLoss": 188.00, "target1": 198.00, "target2": 205.00, "target3": 212.00, "current": 196.50},
    {"symbol": "MSFT", "name": "مايكروسوفت", "status": "نشط", "strength": 3, "entry": 415.00, "stopLoss": 408.00, "target1": 425.00, "target2": 435.00, "target3": 450.00, "current": 422.00},
    {"symbol": "TSLA", "name": "تسلا", "status": "منتظر", "strength": 2, "entry": 250.00, "stopLoss": 242.00, "target1": 260.00, "target2": 275.00, "target3": 290.00, "current": 247.00},
    {"symbol": "NVDA", "name": "إنفيديا", "status": "نشط", "strength": 3, "entry": 880.00, "stopLoss": 860.00, "target1": 920.00, "target2": 960.00, "target3": 1000.00, "current": 910.00},
    {"symbol": "AMZN", "name": "أمازون", "status": "مغلق", "strength": 2, "entry": 178.00, "stopLoss": 174.00, "target1": 185.00, "target2": 192.00, "target3": 200.00, "current": 185.00},
]

# ===== الدالات =====
def get_market_status(market):
    """الحصول على حالة السوق"""
    if market == "saudi":
        tz = pytz.timezone('Asia/Riyadh')
        open_time, close_time = 10, 15
    else:
        tz = pytz.timezone('America/New_York')
        open_time, close_time = 9.5, 16
    
    now = datetime.now(tz)
    hour = now.hour + now.minute / 60
    
    if open_time <= hour < close_time:
        if close_time - hour <= 1:
            return "🟠 يغلق قريباً", "orange"
        return "🟢 السوق مفتوح", "green"
    return "🔴 السوق مغلق", "red"

def calculate_progress(entry, current, target1):
    """حساب التقدم نحو الهدف الأول"""
    if target1 == entry:
        return 0
    progress = ((current - entry) / (target1 - entry)) * 100
    return max(0, min(100, progress))

def calculate_pnl(entry, current):
    """حساب الربح والخسارة"""
    diff = current - entry
    pct = (diff / entry) * 100
    return diff, pct

# ===== الواجهة =====
st.markdown("<h1 style='text-align: right; color: #3b82f6;'>📈 منصة الحبي للتداول</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: right; color: #9ca3af;'>تداول ذكي • تحليل متقدم</p>", unsafe_allow_html=True)

# تبديل السوق
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    market = st.radio("اختر السوق", ["🇸🇦 السعودي", "🇺🇸 الأمريكي"], key="market")
with col2:
    market_type = "saudi" if "السعودي" in market else "us"
    status, color = get_market_status(market_type)
    st.markdown(f"<p style='color: {color};'>{status}</p>", unsafe_allow_html=True)

# الفلاتر
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    search = st.text_input("🔍 بحث بالرمز أو الاسم")
with col2:
    status_filter = st.selectbox("الحالة", ["جميع الحالات", "نشط", "منتظر", "مغلق"])
with col3:
    strength_filter = st.selectbox("القوة", ["جميع القوة", "⭐⭐⭐", "⭐⭐", "⭐"])
with col4:
    sort_by = st.selectbox("الترتيب", ["بالقوة", "بالتقدم", "أبجدي"])

# اختيار البيانات
trades = saudi_trades if market_type == "saudi" else us_trades

# تطبيق الفلاتر
if search:
    trades = [t for t in trades if search.lower() in t["symbol"].lower() or search in t["name"]]

if status_filter != "جميع الحالات":
    trades = [t for t in trades if t["status"] == status_filter]

strength_map = {"⭐⭐⭐": 3, "⭐⭐": 2, "⭐": 1}
if strength_filter != "جميع القوة":
    trades = [t for t in trades if t["strength"] == strength_map[strength_filter]]

# الترتيب
if sort_by == "بالقوة":
    trades = sorted(trades, key=lambda x: x["strength"], reverse=True)
elif sort_by == "بالتقدم":
    trades = sorted(trades, key=lambda x: calculate_progress(x["entry"], x["current"], x["target1"]), reverse=True)
elif sort_by == "أبجدي":
    trades = sorted(trades, key=lambda x: x["name"])

# عرض الملخص
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("إجمالي الصفقات", len(trades))
with col2:
    st.metric("صفقات نشطة", len([t for t in trades if t["status"] == "نشط"]))
with col3:
    st.metric("صفقات منتظرة", len([t for t in trades if t["status"] == "منتظر"]))
with col4:
    st.metric("صفقات مغلقة", len([t for t in trades if t["status"] == "مغلق"]))

# عرض الصفقات
st.markdown("---")
if trades:
    for trade in trades:
        diff, pct = calculate_pnl(trade["entry"], trade["current"])
        progress = calculate_progress(trade["entry"], trade["current"], trade["target1"])
        
        # تحديد الألوان
        status_colors = {
            "نشط": "#10b981",
            "منتظر": "#f59e0b",
            "مغلق": "#6b7280"
        }
        status_color = status_colors[trade["status"]]
        
        # البطاقة
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"<h3 style='color: #3b82f6;'>{trade['symbol']} - {trade['name']}</h3>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<p style='color: {status_color}; font-weight: bold;'>{trade['status']} {'⭐' * trade['strength']}</p>", unsafe_allow_html=True)
            
            # التقدم
            if trade["status"] == "نشط":
                st.progress(progress / 100, text=f"التقدم: {progress:.0f}%")
                
                # PnL
                color = "#10b981" if pct >= 0 else "#ef4444"
                st.markdown(f"<p style='color: {color}; font-weight: bold;'>الربح/الخسارة: {pct:+.2f}% ({diff:+.2f})</p>", unsafe_allow_html=True)
            
            # الأسعار
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("الدخول", f"{trade['entry']:.2f}")
            with col2:
                st.metric("وقف الخسارة", f"{trade['stopLoss']:.2f}")
            with col3:
                st.metric("الهدف 1", f"{trade['target1']:.2f}")
            with col4:
                st.metric("الهدف 2", f"{trade['target2']:.2f}")
            with col5:
                st.metric("الهدف 3", f"{trade['target3']:.2f}")
            
            st.markdown("---")
else:
    st.warning("لا توجد صفقات مطابقة للبحث")

# التذييل
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6b7280; font-size: 12px;'>جميع الحقوق محفوظة © 2025 منصة الحبي للتداول. هذه المنصة لأغراض تعليمية فقط</p>", unsafe_allow_html=True)
