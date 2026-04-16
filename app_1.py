import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. إعدادات المنصة والهوية البصرية ---
st.set_page_config(
    page_title="منصة الحبي للتداول | ICT Radar",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تطبيق CSS مخصص للحفاظ على الفخامة واللون الداكن
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Kufi Arabic', sans-serif;
        direction: RTL;
        text-align: right;
    }
    
    .stApp {
        background-color: #0d1117;
    }

    /* تصميم بطاقات الصفقات */
    .trade-card {
        background-color: #161b26;
        border: 1px solid #1f2937;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 10px;
        transition: transform 0.3s ease;
    }
    .trade-card:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
    }

    /* الهيدر */
    .main-header {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 12px;
        border-right: 5px solid #3b82f6;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. قاعدة البيانات (محاكاة) ---
# ملاحظة: يمكنك مستقبلاً ربط هذه القائمة بملف Excel أو API مباشر
if 'market_data' not in st.session_state:
    st.session_state.market_data = {
        "السوق السعودي 🇸🇦": [
            {"الرمز": "2222", "الشركة": "أرامكو", "الحالة": "نشط", "القوة": 3, "الدخول": 28.50, "الهدف": 30.50, "الوقف": 27.80, "الحالي": 29.15},
            {"الرمز": "1120", "الشركة": "الراجحي", "الحالة": "انتظار", "القوة": 3, "الدخول": 95.00, "الهدف": 102.00, "الوقف": 93.50, "الحالي": 94.80},
            {"الرمز": "2010", "الشركة": "سابك", "الحالة": "نشط", "القوة": 2, "الدخول": 78.00, "الهدف": 82.50, "الوقف": 76.80, "الحالي": 79.30},
        ],
        "السوق الأمريكي 🇺🇸": [
            {"الرمز": "AAPL", "الشركة": "Apple", "الحالة": "نشط", "القوة": 3, "الدخول": 190.00, "الهدف": 215.00, "الوقف": 185.00, "الحالي": 198.40},
            {"الرمز": "NVDA", "الشركة": "Nvidia", "الحالة": "نشط", "القوة": 3, "الدخول": 880.00, "الهدف": 950.00, "الوقف": 860.00, "الحالي": 912.00},
        ]
    }

# --- 3. الهيدر وشريط الأدوات ---
st.markdown("""
    <div class="main-header">
        <h1 style="color: white; margin:0;">منصة الحبي للتداول</h1>
        <p style="color: #60a5fa; margin:0;">رادار اقتناص الفرص بناءً على مدرسة ICT</p>
    </div>
    """, unsafe_allow_html=True)

col_m1, col_m2 = st.columns([2, 1])
with col_m1:
    market_choice = st.radio("اختر السوق المستهدف:", list(st.session_state.market_data.keys()), horizontal=True)

with col_m2:
    st.markdown(f"**الوقت الآن:** `{datetime.now().strftime('%H:%M:%S')}`")

# --- 4. ملخص الإحصائيات (Metrics) ---
current_trades = st.session_state.market_data[market_choice]
total = len(current_trades)
active = len([t for t in current_trades if t['الحالة'] == "نشط"])
waiting = total - active

m1, m2, m3, m4 = st.columns(4)
m1.metric("إجمالي الفرص", total)
m2.metric("فرص نشطة", active, delta="جاري المتابعة", delta_color="normal")
m3.metric("بانتظار الدخول", waiting)
m4.metric("الأهداف المحققة", "12", delta="فرصة ناجحة")

st.divider()

# --- 5. البحث والفلترة ---
col_s1, col_s2 = st.columns([3, 1])
search = col_s1.text_input("🔍 ابحث عن سهم محدد (الرمز أو الاسم):")
sort_opt = col_s2.selectbox("ترتيب حسب:", ["الأقوى", "الأحدث"])

# --- 6. عرض الفرص (Grid System) ---
st.subheader(f"الفرص المتاحة في {market_choice}")

# تصفية البيانات بناءً على البحث
filtered_trades = [t for t in current_trades if search.lower() in t['الشركة'].lower() or search in t['الرمز']]

if not filtered_trades:
    st.warning("لا توجد نتائج تطابق بحثك حالياً.")
else:
    cols = st.columns(3)
    for i, trade in enumerate(filtered_trades):
        with cols[i % 3]:
            # حساب نسبة التقدم للهدف
            diff_total = trade['الهدف'] - trade['الدخول']
            diff_current = trade['الحالي'] - trade['الدخول']
            progress = min(100, max(0, int((diff_current / diff_total) * 100))) if trade['الحالة'] == "نشط" else 0
            
            # عرض البطاقة باستخدام HTML داخل بايثون لجمالية التصميم
            st.markdown(f"""
                <div class="trade-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h3 style="color: white; margin: 0;">{trade['الرمز']}</h3>
                            <p style="color: #9ca3af; font-size: 13px; margin: 0;">{trade['الشركة']}</p>
                        </div>
                        <span style="background: #1e293b; color: #60a5fa; padding: 4px 10px; border-radius: 8px; font-size: 10px; font-weight: bold;">
                            {trade['الحالة']}
                        </span>
                    </div>
                    <div style="margin: 15px 0; font-size: 12px; color: #fbbf24;">
                        القوة: {'⭐' * trade['القوة']}
                    </div>
                    <div style="background: #0d1117; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; font-size: 12px;">
                            <span>الدخول: <b>{trade['الدخول']}</b></span>
                            <span style="color: #4ade80;">الهدف: <b>{trade['الهدف']}</b></span>
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-top: 5px;">
                            <span style="color: #f87171;">الوقف: <b>{trade['الوقف']}</b></span>
                            <span style="color: white;">السعر الآن: <b>{trade['الحالي']}</b></span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if trade['الحالة'] == "نشط":
                st.progress(progress / 100, text=f"نسبة الإنجاز: {progress}%")

# --- 7. التذييل (Footer) ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #1f2937;">
        <p style="color: #4b5563; font-size: 11px;">
            جميع الحقوق محفوظة © 2026 منصة الحبي للتداول<br>
            إخلاء مسؤولية: التداول ينطوي على مخاطرة، وهذه المنصة تعليمية ولا تقدم نصائح استثمارية.
        </p>
    </div>
    """, unsafe_allow_html=True)
