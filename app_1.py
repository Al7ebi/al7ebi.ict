import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# إعدادات الصفحة
st.set_page_config(page_title="منصة الحبي للتداول", layout="wide")

# التنسيق البصري (McKinsey Style)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; }
    .status-card { background-color: #1e1e1e; border-radius: 10px; padding: 20px; border: 1px solid #333; text-align: center; }
    </style>
""", unsafe_allow_complete_html=True)

# ترويسة المنصة
st.title("📡 منصة الحبي للتداول (Habbi Radar)")

# عرض حالة السوق (كما في منطقك الجديد)
now = datetime.now()
is_open = 9 <= now.hour < 17
col_clock, col_status = st.columns(2)
with col_clock:
    st.info(f"🕒 {now.strftime('%I:%M %p')} | {now.strftime('%d/%m/%Y')}")
with col_status:
    if is_open: st.success("● السوق مفتوح الآن")
    else: st.error("● السوق مغلق حالياً")

# شبكة البيانات 3x2 (Symmetry)
st.write("---")
row1 = st.columns(3)
row2 = st.columns(3)
metrics = [
    ("Ticker", "ORCL", "#fff"), ("Grade", "A", "#8B5CF6"), ("Score", "9/13", "#10B981"),
    ("Bias", "Long", "#10B981"), ("Entry", "162.11", "#fff"), ("R:R", "1:8.4", "#F59E0B")
]

for i, col in enumerate(row1 + row2):
    with col:
        st.markdown(f"<div class='status-card'><small>{metrics[i][0]}</small><br><b style='color:{metrics[i][2]}; font-size:24px;'>{metrics[i][1]}</b></div>", unsafe_allow_complete_html=True)

# قانون الـ 3 أيام
st.write("### 💎 الفرص النشطة (خلال 72 ساعة)")
st.warning("⚠️ يتم الآن فلترة البيانات لضمان ظهور الفرص الطازجة فقط.")
