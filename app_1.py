import streamlit as st
from datetime import datetime
import engine as habbi_engine
import pandas as pd

# 1. إعدادات الغرفة الاحترافية
st.set_page_config(page_title="غرفة تداول الحبي الذكية", layout="wide", initial_sidebar_state="expanded")

# 2. تصميم الـ UI (نظام الغرف والتنسيق الزجاجي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    
    html, body, [data-testid="stSidebar"], .stApp {
        font-family: 'Tajawal', sans-serif;
        direction: RTL; text-align: right;
        background-color: #05070a;
    }

    /* القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        border-left: 1px solid #1f2937;
    }

    /* بطاقة الغرفة الذكية */
    .trading-room-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .trading-room-card:hover {
        border-color: #3b82f6;
        background: rgba(59, 130, 246, 0.05);
    }

    /* مؤشرات الحالة */
    .status-badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 3. القائمة الجانبية (Sidebar) - مركز التحكم
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2502/2502164.png", width=80) # شعار افتراضي
    st.title("غرفة التداول")
    st.markdown("---")
    room_selection = st.radio("اختر القسم:", ["📊 لوحة الرادار", "🔥 إشارات الذهب", "📅 سجل الصفقات", "⚙️ الإعدادات"])
    st.markdown("---")
    st.info("قاعدة الـ 72 ساعة نشطة")
    if st.button("تحديث البيانات الحية"):
        st.rerun()

# 4. الجزء العلوي (Top Header)
t_col1, t_col2 = st.columns([3, 1])
with t_col1:
    st.markdown(f"## {room_selection}")
with t_col2:
    st.markdown(f"<div style='text-align:left; color:#60A5FA;'>{datetime.now().strftime('%I:%M %p')}</div>", unsafe_allow_html=True)

# 5. محتوى الغرفة (Main Dashboard)
analysis = habbi_engine.habbi_brain.analyze_habbi_golden()

if room_selection == "📊 لوحة الرادار":
    # شريط التنبيهات العلوي
    st.markdown(f"""
        <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid #3b82f6; padding: 10px; border-radius: 8px; margin-bottom: 20px;">
            <marquee direction="right">🚨 تنبيه ذكي: {analysis['symbol']} يقترب من منطقة السيولة اليومية - Habbi Golden Setup قيد التشكل 🚨</marquee>
        </div>
    """, unsafe_allow_html=True)

    # تقسيم الشاشة (يسار: التحليل ، يمين: قائمة المراقبة)
    main_col, watch_col = st.columns([3, 1])

    with main_col:
        st.markdown("### 🖥️ شاشة التحليل المركزي")
        # محاكاة لشارت أو تحليل فني
        st.markdown(f"""
            <div class="trading-room-card" style="height: 300px; display: flex; align-items: center; justify-content: center; border-style: dashed;">
                <div style="text-align: center;">
                    <h1 style="color: #3b82f6; margin:0;">{analysis['symbol']}</h1>
                    <p>Habbi Golden Strategy - {analysis['mss']}</p>
                    <h2 style="color: #10B981;">{analysis['entry']}</h2>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # تفاصيل الصفقة الحالية (شبكة البيانات)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='trading-room-card'><b>نقطة الدخول</b><br><h3 style='color:#3b82f6;'>{analysis['entry']}</h3></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='trading-room-card'><b>الهدف الأول</b><br><h3 style='color:#10B981;'>{analysis['target']}</h3></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='trading-room-card'><b>السيولة</b><br><h5>{analysis['sweep']}</h5></div>", unsafe_allow_html=True)

    with watch_col:
        st.markdown("### 🔔 إشارات حية")
        pairs = [("XAUUSD", "A+"), ("EURUSD", "A"), ("GBPUSD", "B"), ("BTCUSD", "A")]
        for p, grade in pairs:
            st.markdown(f"""
                <div class="trading-room-card" style="padding: 10px;">
                    <span style="float:left;" class="status-badge">Grade: {grade}</span>
                    <b>{p}</b><br>
                    <small style="color: #60A5FA;">Status: Monitoring</small>
                </div>
            """, unsafe_allow_html=True)

elif room_selection == "🔥 إشارات الذهب":
    st.success("هذا القسم مخصص لاستراتيجية الذهب حصراً.")
    st.table(pd.DataFrame([analysis]))

# 6. التذييل الاحترافي
st.markdown("---")
st.markdown("""
    <div style="display: flex; justify-content: space-between; opacity: 0.6; font-size: 13px;">
        <div>جميع الحقوق محفوظة لمنصة الحبي © 2026</div>
        <div>برعاية: <a href="https://quantomoption.com/" style="color: #3b82f6; text-decoration: none;">Quantom Option</a></div>
    </div>
""", unsafe_allow_html=True)
