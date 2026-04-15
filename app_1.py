import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time

st.set_page_config(
page_title="منصة الحبي للتداول",
layout="wide",
initial_sidebar_state="expanded"
)

CSS مخصص
st.markdown("""

""", unsafe_allow_html=True)

===== العنوان والعناصر الأساسية =====
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
st.title("🇸🇦 منصة الحبي للتداول")
st.caption("تداول ذكي • تحليل متقدم")

with col2:
now = datetime.now()
st.metric("⏰ الوقت", now.strftime("%H:%M:%S"))

with col3:
refresh_btn = st.button("🔄 تحديث", key="refresh")

===== البيانات =====
saudi_trades = [
{"الرمز": "2222", "الاسم": "أرامكو", "التاريخ": "2025-01-15", "الحالة": "نشط", "القوة": 3, "نقطة الدخول": 28.50, "السعر الحالي": 29.10, "وقف الخسارة": 27.80, "الهدف1": 29.50, "الهدف2": 30.20, "الهدف3": 31.00},
{"الرمز": "1120", "الاسم": "الراجحي", "التاريخ": "2025-01-14", "الحالة": "نشط", "القوة": 3, "نقطة الدخول": 95.00, "السعر الحالي": 96.20, "وقف الخسارة": 93.50, "الهدف1": 97.00, "الهدف2": 99.00, "الهدف3": 102.00},
{"الرمز": "2010", "الاسم": "سابك", "التاريخ": "2025-01-13", "الحالة": "منتظر", "القوة": 2, "نقطة الدخول": 78.00, "السعر الحالي": 77.40, "وقف الخسارة": 76.50, "الهدف1": 80.00, "الهدف2": 82.00, "الهدف3": 85.00},
{"الرمز": "7010", "الاسم": "STC", "التاريخ": "2025-01-12", "الحالة": "نشط", "القوة": 2, "نقطة الدخول": 42.00, "السعر الحالي": 43.10, "وقف الخسارة": 41.00, "الهدف1": 43.50, "الهدف2": 45.00, "الهدف3": 47.00},
{"الرمز": "4200", "الاسم": "الدواء", "التاريخ": "2025-01-10", "الحالة": "منتظر", "القوة": 1, "نقطة الدخول": 55.00, "السعر الحالي": 54.20, "وقف الخسارة": 53.80, "الهدف1": 57.00, "الهدف2": 59.00, "الهدف3": 62.00},
{"الرمز": "1180", "الاسم": "الأهلي", "التاريخ": "2025-01-09", "الحالة": "مغلق", "القوة": 2, "نقطة الدخول": 38.00, "السعر الحالي": 39.50, "وقف الخسارة": 37.00, "الهدف1": 39.50, "الهدف2": 41.00, "الهدف3": 43.00},
]

us_trades = [
{"الرمز": "AAPL", "الاسم": "Apple", "التاريخ": "2025-01-15", "الحالة": "نشط", "القوة": 3, "نقطة الدخول": 192.00, "السعر الحالي": 196.50, "وقف الخسارة": 188.00, "الهدف1": 198.00, "الهدف2": 205.00, "الهدف3": 212.00},
{"الرمز": "MSFT", "الاسم": "Microsoft", "التاريخ": "2025-01-14", "الحالة": "نشط", "القوة": 3, "نقطة الدخول": 415.00, "السعر الحالي": 422.00, "وقف الخسارة": 408.00, "الهدف1": 425.00, "الهدف2": 435.00, "الهدف3": 450.00},
{"الرمز": "TSLA", "الاسم": "Tesla", "التاريخ": "2025-01-13", "الحالة": "منتظر", "القوة": 2, "نقطة الدخول": 250.00, "السعر الحالي": 247.00, "وقف الخسارة": 242.00, "الهدف1": 260.00, "الهدف2": 275.00, "الهدف3": 290.00},
{"الرمز": "NVDA", "الاسم": "Nvidia", "التاريخ": "2025-01-12", "الحالة": "نشط", "القوة": 3, "نقطة الدخول": 880.00, "السعر الحالي": 910.00, "وقف الخسارة": 860.00, "الهدف1": 920.00, "الهدف2": 960.00, "الهدف3": 1000.00},
]

===== Sidebar =====
with st.sidebar:
st.header("⚙️ الإعدادات")

market = st.radio("اختر السوق:", ["🇸🇦 السوق السعودي", "🇺🇸 السوق الأمريكي"])

st.divider()

search = st.text_input("🔍 ابحث بالرمز أو الاسم:")

strength_filter = st.selectbox("تصفية بالقوة:", ["الكل", "⭐⭐⭐", "⭐⭐", "⭐"])

sort_option = st.selectbox("ترتيب حسب:", ["القوة", "التقدم", "الاسم"])

view_mode = st.radio("طريقة العرض:", ["🎴 بطاقات", "📊 جدول"])

===== معالجة البيانات =====
trades_data = saudi_trades if "السوق السعودي" in market else us_trades

df = pd.DataFrame(trades_data)

حساب الربح/الخسارة
df["الربح/الخسارة %"] = ((df["السعر الحالي"] - df["نقطة الدخول"]) / df["نقطة الدخول"] * 100).round(2)

تصفية
if search:
df = df[df["الرمز"].str.contains(search, case=False) | df["الاسم"].str.contains(search, case=False)]

strength_map = {"الكل": 0, "⭐": 1, "⭐⭐": 2, "⭐⭐⭐": 3}
if strength_filter != "الكل":
df = df[df["القوة"] == strength_map[strength_filter]]

ترتيب
if sort_option == "القوة":
df = df.sort_values("القوة", ascending=False)
elif sort_option == "التقدم":
df["التقدم"] = ((df["السعر الحالي"] - df["نقطة الدخول"]) / (df["الهدف1"] - df["نقطة الدخول"]) * 100).clip(0, 100)
df = df.sort_values("التقدم", ascending=False)
elif sort_option == "الاسم":
df = df.sort_values("الاسم")

===== الإحصائيات =====
st.divider()
col1, col2, col3, col4 = st.columns(4)

with col1:
st.metric("📊 إجمالي الصفقات", len(df))

with col2:
active = len(df[df["الحالة"] == "نشط"])
st.metric("✅ صفقات نشطة", active, delta=f"+{active}")

with col3:
waiting = len(df[df["الحالة"] == "منتظر"])
st.metric("⏳ صفقات منتظرة", waiting)

with col4:
closed = len(df[df["الحالة"] == "مغلق"])
st.metric("❌ صفقات مغلقة", closed)

===== عرض البيانات =====
st.divider()
st.subheader(f"📈 الصفقات - {market}")

if view_mode == "📊 جدول":
st.dataframe(
df[["الرمز", "الاسم", "التاريخ", "الحالة", "القوة", "نقطة الدخول", "السعر الح��لي", "الربح/الخسارة %", "وقف الخسارة", "الهدف1"]],
use_container_width=True,
hide_index=True
)
else:
# عرض البطاقات
cols = st.columns(2)
for idx, row in df.iterrows():
with cols[idx % 2]:
with st.container(border=True):
col1, col2 = st.columns([2, 1])
with col1:
st.subheader(f"{row['الرمز']} - {row['الاسم']}")
with col2:
if row["الحالة"] == "نشط":
st.success(row["الحالة"])
elif row["الحالة"] == "منتظر":
st.warning(row["الحالة"])
else:
st.info(row["الحالة"])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("نقطة الدخول", f"${row['نقطة الدخول']:.2f}")
            with col2:
                st.metric("السعر الحالي", f"${row['السعر الحالي']:.2f}")
            with col3:
                color = "green" if row["ال��بح/الخسارة %"] >= 0 else "red"
                st.metric("الربح/الخسارة", f"{row['الربح/الخسارة %']:.2f}%")
            
            st.text(f"🎯 الهدف 1: {row['الهدف1']} | الهدف 2: {row['الهدف2']} | الهدف 3: {row['الهدف3']}")
            st.text(f"🛑 وقف الخسارة: {row['وقف الخسارة']}")

===== Footer =====
st.divider()
st.caption("© 2025 منصة الحبي للتداول - لأغراض تعليمية فقط")

python # app.py - منصة الحبي للت��اول (Streamlit) import streamlit as st import pandas as pd from datetime import datetime, timedelta import time st.set_page_config( page_title="منصة الحبي للتداول", layout="wide", initial_sidebar_state="expanded" ) # CSS مخصص st.markdown("""
