import streamlit as st
import pandas as pd
import datetime
import random

# --- 1. إعدادات الهوية والتصميم ---
st.set_page_config(page_title="منصة الحبي للتداول", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; text-align: right; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    </style>
""", unsafe_allow_complete_html=True)

# --- 2. المحرك التحليلي (منطق الحبي الذي كتبته أنت) ---
class HabbiLogic:
    @staticmethod
    def get_score(s):
        score = 0
        if s['sweep']: score += 4
        if s['mss']: score += 3
        if s['ifvg']: score += 3
        if s['equilibrium']: score += 3
        return score

# بيانات تجريبية (نفس التي وضعتها أنت)
signals_db = [
    {
        "symbol": "BTC/USD", "sweep": True, "mss": True, "ifvg": True, "equilibrium": True,
        "high": 66000, "low": 64000, "timestamp": datetime.datetime.now() - datetime.timedelta(hours=2), "type": "شراء (Long)"
    },
    {
        "symbol": "GOLD", "sweep": True, "mss": False, "ifvg": True, "equilibrium": True,
        "high": 2360, "low": 2340, "timestamp": datetime.datetime.now() - datetime.timedelta(hours=75), "type": "بيع (Short)"
    }
]

# --- 3. الواجهة (التصميم العصري) ---
st.title("📡 منصة الحبي للتداول")

# شريط عاجل
st.info("🔥 تم رصد سحب سيولة يومي في البيتكوين .. نظام التقييم نشط الآن")

# ساعة السوق
now = datetime.datetime.now()
col_time, col_status = st.columns(2)
with col_time:
    st.write(f"🕒 {now.strftime('%I:%M %p')} | {now.strftime('%A')}")
with col_status:
    is_open = 9 <= now.hour < 17
    st.success("السوق مفتوح 🟢") if is_open else st.error("السوق مغلق 🔴")

st.write("---")

# عرض المؤشرات (3x2 Grid)
cols = st.columns(3)
indicators = [("تاسي", "12,450", "-0.4%"), ("الذهب", "2,385", "+1.2%"), ("البيتكوين", "67,200", "+4.1%")]
for i, col in enumerate(cols):
    col.metric(indicators[i][0], indicators[i][1], indicators[i][2])

st.write("### 💎 الفرص المكتشفة (قانون الـ 1 أيام)")

# معالجة الصفقات وعرضها
for s in signals_db:
    age = (datetime.datetime.now() - s['timestamp']).total_seconds() / 3600
    
    if age <= 24: # قانون الـ 1 أيام
        score = HabbiLogic.get_score(s)
        with st.expander(f"📌 {s['symbol']} - تقييم القوة: {score}/13"):
            c1, c2, c3 = st.columns(3)
            c1.write(f"**النوع:** {s['type']}")
            c2.write(f"**الهدف:** {s['high'] if s['type'] == 'شراء (Long)' else s['low']}")
            c3.write(f"**العمر:** قبل {int(age)} ساعة")
            if score >= 10:
                st.success("🔥 هذه فرصة ذهبية مكتملة الشروط!")
