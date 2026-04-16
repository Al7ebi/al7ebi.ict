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

# تطبيق CSS مخصص لمحاكاة التصميم الأصلي (Tailwind Style)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Kufi Arabic', sans-serif;
        direction: RTL;
        text-align: right;
    }
    
    /* خلفية داكنة للبطاقات */
    .stMetric, .trade-card {
        background-color: #161b26;
        border: 1px solid #374151;
        padding: 20px;
        border-radius: 12px;
        transition: transform 0.3s ease;
    }
    
    .trade-card:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
    }

    /* تذييل الصفحة */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #161b26;
        color: #6b7280;
        text-align: center;
        padding: 10px;
        font-size: 11px;
        border-top: 1px solid #374151;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محاكاة البيانات (Data Mockup) ---
if 'market' not in st.session_state:
    st.session_state.market = '🇸🇦 السوق السعودي'

def get_data():
    if st.session_state.market == '🇸🇦 السوق السعودي':
        return [
            {"symbol": "2222", "name": "أرامكو", "status": "نشط", "strength": 3, "entry": 28.50, "stop": 27.80, "target1": 29.50, "current": 29.10},
            {"symbol": "1120", "name": "الراجحي", "status": "نشط", "strength": 3, "entry": 95.00, "stop": 93.50, "target1": 97.00, "current": 96.20},
            {"symbol": "2010", "name": "سابك", "status": "منتظر", "strength": 2, "entry": 78.00, "stop": 76.50, "target1": 80.00, "current": 77.40},
        ]
    else:
        return [
            {"symbol": "AAPL", "name": "Apple", "status": "نشط", "strength": 3, "entry": 192.00, "stop": 188.00, "target1": 198.00, "current": 196.50},
            {"symbol": "NVDA", "name": "Nvidia", "status": "نشط", "strength": 3, "entry": 880.00, "stop": 860.00, "target1": 920.00, "current": 910.00},
        ]

# --- 3. الهيدر (Header) وحالة السوق ---
col_logo, col_info = st.columns([1, 4])
with col_logo:
    st.markdown("""
        <div style="background: linear-gradient(to bottom right, #3b82f6, #22d3ee); 
                    width: 50px; height: 50px; border-radius: 10px; 
                    display: flex; align-items: center; justify-content: center; 
                    color: white; font-weight: bold; font-size: 24px;">ح</div>
    """, unsafe_allow_html=True)
with col_info:
    st.subheader("منصة الحبي للتداول")
    st.caption("تداول ذكي • تحليل متقدم")

# تبيويب الأسواق
st.session_state.market = st.radio("اختر السوق:", ["🇸🇦 السوق السعودي", "🇺🇸 السوق الأمريكي"], horizontal=True, label_visibility="collapsed")

# حالة السوق (Status Bar)
status_col, timer_col = st.columns([2, 1])
with status_col:
    st.markdown(f"● **السوق مفتوح** | الوقت الحالي: {datetime.now().strftime('%H:%M:%S')}", unsafe_allow_html=True)
with timer_col:
    st.caption(f"آخر تحديث: {datetime.now().strftime('%H:%M:%S')}")

st.divider()

# --- 4. ملخص الصفقات (Summary Cards) ---
trades = get_data()
c1, c2, c3, c4 = st.columns(4)
c1.metric("إجمالي الصفقات", len(trades))
c2.metric("صفقات نشطة", len([t for t in trades if t['status'] == "نشط"]), delta_color="normal")
c3.metric("صفقات منتظرة", len([t for t in trades if t['status'] == "منتظر"]))
c4.metric("صفقات مغلقة", "0")

# --- 5. الفرز والبحث ---
col_search, col_filter, col_sort = st.columns([2, 1, 1])
search_query = col_search.text_input("🔍 ابحث بالرمز أو الاسم...", placeholder="مثلاً: أرامكو")
filter_strength = col_filter.selectbox("القوة", ["جميع القوة", "3 ⭐⭐⭐", "2 ⭐⭐", "1 ⭐"])
sort_by = col_sort.selectbox("ترتيب حسب", ["القوة", "الاسم"])

# --- 6. عرض الصفقات (Grid View) ---
st.write("### صفقات السوق الحالية")
cols = st.columns(3)

filtered_trades = [t for t in trades if search_query.lower() in t['name'].lower() or search_query in t['symbol']]

for i, trade in enumerate(filtered_trades):
    with cols[i % 3]:
        # حساب نسبة التقدم
        progress = min(100, max(0, int((trade['current'] - trade['entry']) / (trade['target1'] - trade['entry']) * 100))) if trade['status'] == "نشط" else 0
        
        st.markdown(f"""
            <div class="trade-card">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: bold; color: white;">{trade['symbol']} | {trade['name']}</span>
                    <span style="background: #1e293b; padding: 2px 8px; border-radius: 10px; font-size: 10px;">{trade['status']}</span>
                </div>
                <div style="margin: 10px 0; color: #9ca3af; font-size: 12px;">القوة: {'⭐' * trade['strength']}</div>
                <div style="background: #0d1117; padding: 10px; border-radius: 8px; margin-top: 10px;">
                    <table style="width: 100%; font-size: 11px; color: #d1d5db;">
                        <tr><td>الدخول</td><td style="color: white;">{trade['entry']}</td></tr>
                        <tr><td>الهدف 1</td><td style="color: #4ade80;">{trade['target1']}</td></tr>
                        <tr><td>الوقف</td><td style="color: #f87171;">{trade['stop']}</td></tr>
                    </table>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if trade['status'] == "نشط":
            st.progress(progress / 100, text=f"التقدم للهدف 1: {progress}%")

# --- 7. التذييل (Footer) ---
st.markdown(f"""
    <div class="footer">
        <p>جميع الحقوق محفوظة © 2026 منصة الحبي للتداول. هذه المنصة لأغراض تعليمية فقط ولا تتحمل أي التزامات مالية.</p>
    </div>
""", unsafe_allow_html=True)

# تحديث تلقائي (اختياري)
# time.sleep(5)
# st.rerun()
