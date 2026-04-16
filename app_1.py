import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- 1. إعدادات الصفحة والهوية البصرية ---
st.set_page_config(
    page_title="منصة الحبي للتداول",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تطبيق التنسيق الاحترافي (McKinsey Style & Dark UI)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700&display=swap');
    
    /* تنسيق الحاوية الرئيسية */
    .main { background-color: #0d1117; color: #e5e7eb; }
    html, body, [class*="css"] {
        font-family: 'Noto Kufi Arabic', sans-serif;
        direction: RTL; text-align: right;
    }

    /* تصميم البطاقات (Trade Cards) */
    .trade-card {
        background-color: #161b26;
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .trade-card:hover {
        border-color: #3b82f6;
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }

    /* تخصيص الـ Metrics */
    [data-testid="stMetricValue"] { color: white; font-weight: bold; }
    
    /* شريط الحالة */
    .status-bar {
        background-color: #0f1520;
        border: 1px solid #1f2937;
        padding: 10px 20px;
        border-radius: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    /* التذييل */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 11px;
        padding: 20px;
        border-top: 1px solid #1f2937;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. منطق البيانات (Backend Logic) ---
# ملاحظة: هنا يمكنك لاحقاً ربط المنصة ببيانات حقيقية عبر API
def load_data(market_type):
    if market_type == "🇸🇦 السوق السعودي":
        data = [
            {"الرمز": "2222", "الاسم": "أرامكو", "الحالة": "نشط", "القوة": 3, "الدخول": 28.50, "الهدف": 29.50, "الوقف": 27.80, "الحالي": 29.10},
            {"الرمز": "1120", "الاسم": "الراجحي", "الحالة": "نشط", "القوة": 3, "الدخول": 95.00, "الهدف": 97.00, "الوقف": 93.50, "الحالي": 96.20},
            {"الرمز": "2010", "الاسم": "سابك", "الحالة": "منتظر", "القوة": 2, "الدخول": 78.00, "الهدف": 80.00, "الوقف": 76.50, "الحالي": 77.40},
        ]
    else:
        data = [
            {"الرمز": "AAPL", "الاسم": "Apple", "الحالة": "نشط", "القوة": 3, "الدخول": 192.00, "الهدف": 198.00, "الوقف": 188.00, "الحالي": 196.50},
            {"الرمز": "NVDA", "الاسم": "Nvidia", "الحالة": "نشط", "القوة": 3, "الدخول": 880.00, "الهدف": 920.00, "الوقف": 860.00, "الحالي": 910.00},
        ]
    return pd.DataFrame(data)

# --- 3. واجهة المستخدم (Header) ---
col_head1, col_head2 = st.columns([4, 1])
with col_head1:
    st.title("منصة الحبي للتداول")
    st.caption("تحليل ذكي • تداول متقدم • استراتيجيات ICT")

with col_head2:
    st.markdown(f"""<div style="text-align:left; font-family:monospace; color:#9ca3af; margin-top:20px;">
                {datetime.now().strftime('%H:%M:%S')}</div>""", unsafe_allow_html=True)

# تبيويب الأسواق
market = st.radio("اختر السوق", ["🇸🇦 السوق السعودي", "🇺🇸 السوق الأمريكي"], horizontal=True, label_visibility="collapsed")
df = load_data(market)

# شريط الحالة
st.markdown(f"""
    <div class="status-bar">
        <div><span style="color:#4ade80;">●</span> السوق مفتوح حالياً</div>
        <div style="font-size:12px; color:#6b7280;">آخر تحديث للأسعار: {datetime.now().strftime('%H:%M:%S')}</div>
    </div>
""", unsafe_allow_html=True)

# --- 4. الإحصائيات السريعة ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("إجمالي الصفقات", len(df))
c2.metric("نشطة", len(df[df['الحالة']=="نشط"]), delta="↑")
c3.metric("بانتظار الدخول", len(df[df['الحالة']=="منتظر"]))
c4.metric("مكتملة", "0")

st.write("---")

# --- 5. البحث والفلترة ---
col_search, col_filter, col_view = st.columns([2, 1, 1])
search = col_search.text_input("🔍 ابحث بالرمز أو الاسم...", placeholder="أدخل اسم الشركة")
view_mode = col_view.selectbox("نمط العرض", ["بطاقات احترافية", "جدول بيانات"])

# منطق الفلترة
filtered_df = df[df['الاسم'].str.contains(search) | df['الرمز'].str.contains(search)]

# --- 6. عرض النتائج ---
if view_mode == "بطاقات احترافية":
    cols = st.columns(3)
    for i, row in enumerate(filtered_df.to_dict('records')):
        with cols[i % 3]:
            # حساب نسبة التقدم للهدف
            progress = min(100, max(0, int((row['الحالي'] - row['الدخول']) / (row['الهدف'] - row['الدخول']) * 100))) if row['الحالة'] == "نشط" else 0
            color = "#4ade80" if row['الحالي'] >= row['الدخول'] else "#f87171"
            
            st.markdown(f"""
                <div class="trade-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 1.1rem; font-weight: bold;">{row['الرمز']}</span>
                        <span style="font-size: 0.8rem; background: #1e293b; padding: 2px 10px; border-radius: 20px;">{row['الحالة']}</span>
                    </div>
                    <div style="color: #9ca3af; font-size: 0.8rem; margin-bottom: 15px;">{row['الاسم']} | {'⭐' * row['القوة']}</div>
                    <div style="background: #0d1117; padding: 12px; border-radius: 8px;">
                        <div style="display: flex; justify-content: space-between; font-size: 12px;">
                            <span>الدخول: <b>{row['الدخول']}</b></span>
                            <span style="color:{color};">الحالي: <b>{row['الحالي']}</b></span>
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-top:5px;">
                            <span style="color:#4ade80;">الهدف: <b>{row['الهدف']}</b></span>
                            <span style="color:#f87171;">الوقف: <b>{row['الوقف']}</b></span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if row['الحالة'] == "نشط":
                st.progress(progress / 100, text=f"التقدم نحو الهدف: {progress}%")
else:
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# --- 7. التذييل ---
st.markdown(f"""
    <div class="footer">
        <p>جميع الحقوق محفوظة © 2026 منصة الحبي للتداول</p>
        <p style="opacity: 0.6;">تنبيه: التداول ينطوي على مخاطر عالية، وهذه البيانات للأغراض التعليمية فقط.</p>
    </div>
""", unsafe_allow_html=True)

# تحديث تلقائي بسيط
if st.button("تحديث يدوي للبيانات"):
    st.rerun()
