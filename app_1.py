import streamlit as st
from datetime import datetime
import engine as habbi_engine
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الحبي للتداول", page_icon="🦅", layout="wide")

# 2. تصميم الـ CSS الفاخر 
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    
    html, body, [data-testid="stSidebar"], .stApp {
        font-family: 'Tajawal', sans-serif;
        direction: RTL;
        text-align: right;
    }

    .promo-header {
        background: linear-gradient(90deg, #020617 0%, #1e293b 100%);
        padding: 50px;
        border-radius: 20px;
        text-align: center;
        color: white;
        border: 1px solid #3b82f6;
        margin-bottom: 25px;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        transition: 0.3s;
    }
    .metric-card:hover {
        border-color: #3b82f6;
        transform: translateY(-5px);
    }
    
    .ticker {
        background: #3b82f6;
        color: white;
        padding: 10px;
        border-radius: 10px;
        font-weight: bold;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. قسم البرومو
st.markdown("""
    <div class="promo-header">
        <h1 style="font-size: 48px; margin-bottom: 10px;">🦅 منصة الحبي للتداول</h1>
        <p style="font-size: 20px; opacity: 0.8;">تحليل ذكي يعتمد على خوارزميات ICT وسلوك السعر الحقيقي</p>
        <div style="margin-top: 20px;">
            <span style="background: #3b82f6; padding: 5px 15px; border-radius: 20px;">نظام Habbi Golden Setup</span>
            <span style="background: #1e40af; padding: 5px 15px; border-radius: 20px; margin-right: 10px;">بدون Killzones</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. استدعاء البيانات من المحرك (هنا كان الخطأ وتم إصلاحه)
analysis = habbi_engine.habbi_brain.analyze_habbi_golden()
ticker_text = f"🚨 تم رصد إشارة {analysis['symbol']} - {analysis['sweep']} | الدخول من منطقة Equilibrium: {analysis['entry']} 🚨"

# شريط الأنباء العاجلة
st.markdown(f"""
    <div class="ticker">
        <marquee direction="right" scrollamount="6">{ticker_text}</marquee>
    </div>
""", unsafe_allow_html=True)

# 5. حالة السوق والوقت
col_m1, col_m2 = st.columns([2, 1])
with col_m1:
    st.markdown("""
        <div style="background: #10B981; color: white; padding: 15px; border-radius: 12px; text-align: center;">
            <h3 style="margin:0;">السوق مفتوح حالياً | Market OPEN</h3>
            <p style="margin:5px 0 0 0;">الوقت المتبقي لتغير الحالة: 02:15:40</p>
        </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
        <div style="background: #1e293b; color: #60A5FA; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #3b82f6;">
            <h3 style="margin:0;">{datetime.now().strftime("%I:%M:%S %p")}</h3>
            <p style="margin:5px 0 0 0; color: white;">{datetime.now().strftime("%A, %d %B")}</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. شبكة الإحصائيات مع الفلتر
if habbi_engine.habbi_brain.is_fresh(analysis['time']):
    st.subheader("📊 لوحة بيانات التحليل اللحظي")
    
    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    def draw_stat(col, title, val, sub):
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <div style="color: #60A5FA; font-size: 16px;">{title}</div>
                    <div style="font-size: 26px; font-weight: bold; margin: 10px 0;">{val}</div>
                    <div style="font-size: 12px; opacity: 0.6;">{sub}</div>
                </div>
            """, unsafe_allow_html=True)

    draw_stat(c1, "الزوج المكتشف", analysis['symbol'], "بناءً على سيولة اليوم")
    draw_stat(c2, "حالة السيولة", analysis['sweep'], "Liquidity Sweep Step")
    draw_stat(c3, "هيكل السوق", analysis['mss'], "Market Structure Shift")
    draw_stat(c4, "نقطة الدخول (50%)", analysis['entry'], "Equilibrium Price")
    draw_stat(c5, "الهدف النهائي", analysis['target'], "External Liquidity")
    draw_stat(c6, "صلاحية الإشارة", "نشطة", "تحديث تلقائي (أقل من 24 ساعة)")
else:
    st.warning("⚠️ لا توجد إشارات حديثة متوافقة مع شروط الحبي خلال الـ 24 ساعة الماضية.")

# 7. التذييل
st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #333; opacity: 0.7;">
        حقوق النشر محفوظة © منصة الحبي للتداول | برعاية <br>
        <a href="https://quantomoption.com/" style="color: #3b82f6; text-decoration: none;">www.quantomoption.com</a>
    </div>
""", unsafe_allow_html=True)
