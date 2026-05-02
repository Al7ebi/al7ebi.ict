import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="AL-HABBI ICT PLATFORM",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Institutional UI
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stMetric { background-color: #111111; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #222; }
    .stTable { background-color: #050505; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- CORE UTILITIES ---
def _to_rr(value):
    try:
        if isinstance(value, str):
            value = value.replace('x', '').strip()
        return float(value)
    except:
        return 0.0

def format_currency(val):
    return f"${val:,.2f}"

# --- COMPONENTS ---
def render_header(container):
    with container:
        col1, col2, col3 = st.columns([2, 3, 2])
        with col1:
            st.title("AL-HABBI ICT")
            st.caption("Institutional Grade Trading Suite")
        with col2:
            st.info("Market Status: OPEN | Session: London/NY Overlap")
        with col3:
            st.metric("Server Time", datetime.now().strftime("%H:%M:%S"))
        st.markdown("---")

# --- DATA ENGINE SIMULATION ---
def get_market_data():
    symbols = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "ADA/USDT", "DOT/USDT"]
    data = []
    for s in symbols:
        data.append({
            "Symbol": s,
            "Price": np.random.uniform(10, 60000),
            "Change %": np.random.uniform(-5, 5),
            "ICT Context": np.random.choice(["Premium", "Discount", "Equilibrium"]),
            "PD Array": np.random.choice(["FVG", "OB", "Breaker", "Mitigation"]),
            "Potential R:R": np.random.uniform(1, 8)
        })
    return pd.DataFrame(data)

# (الأسطر من 100 إلى 600 تشمل بقية الدوال الفرعية وإعدادات النماذج الفنية)
# سيتم إكمال بقية الملف في الرسالة القادمة مباشرة# --- RADAR ENGINE & ANALYTICS ---
def render_kpi_radar(df):
    """
    دالة الإحصائيات المصلحة (السطر 811 وما حوله)
    """
    n_total = len(df)
    
    # صمام الأمان لمنع خطأ KeyError
    if "Potential R:R" in df.columns:
        n_rr3 = sum(1 for v in df["Potential R:R"] if _to_rr(v) >= 3)
    else:
        n_rr3 = 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("إجمالي العملات الممسوحة", n_total)
    with col2:
        st.metric("فرص عالية الجودة (3+ RR)", n_rr3)
    with col3:
        win_rate = (n_rr3 / n_total * 100) if n_total > 0 else 0
        st.metric("كثافة إشارات ICT", f"{win_rate:.1f}%")

def render_radar_view(df_results):
    st.header("ICT Institutional Radar")
    
    # استدعاء الإحصائيات المصلحة
    render_kpi_radar(df_results)
    
    # تنسيق الجدول النهائي بأسلوب Bloomberg
    st.dataframe(
        df_results.style.format({
            "Price": "{:,.2f}",
            "Change %": "{:+.2f}%",
            "Potential R:R": "{:.1f}x"
        }).applymap(
            lambda x: "color: #00ff00" if "Premium" in str(x) else "color: #ff4b4b",
            subset=["ICT Context"]
        )
    )

# --- MAIN EXECUTION LOOP ---
def main():
    # إنشاء حاوية الرأس
    header_container = st.empty()
    render_header(header_container)
    
    # القائمة الجانبية (Sidebar)
    with st.sidebar:
        st.image("https://via.placeholder.com/150/000000/FFFFFF?text=AL-HABBI+ICT", width=150)
        st.title("Navigation")
        mode = st.radio("Select Module", ["Radar Scanner", "Chart Analysis", "Settings"])
        
        st.markdown("---")
        st.subheader("Scanner Settings")
        scan_btn = st.button("RUN INSTITUTIONAL SCAN")

    if mode == "Radar Scanner":
        if scan_btn:
            with st.spinner("Fetching Institutional Flow Data..."):
                time.sleep(1) # محاكاة معالجة البيانات
                df_market = get_market_data()
                render_radar_view(df_market)
        else:
            st.info("الرجاء الضغط على زر المسح لبدء تحليل السيولة.")
            
    elif mode == "Chart Analysis":
        st.subheader("Advanced Charting (Coming Soon)")
        st.write("سيتم ربط هذا القسم بـ TradingView لاحقاً.")

# تشغيل التطبيق
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"حدث خطأ غير متوقع: {e}")
