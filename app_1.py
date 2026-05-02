import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة (يجب أن تكون أول سطر برمجي)
st.set_page_config(layout="wide", page_title="AL-HABBI ICT Platform")

# 2. دالة تحويل القيم (للحماية من الأخطاء الحسابية)
def _to_rr(value):
    try:
        return float(value)
    except:
        return 0.0

# 3. دالة رأس الصفحة (الشعار والوقت)
def render_header(container):
    with container:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.title("AL-HABBI ICT")
        with col2:
            st.write(f"الوقت الحالي: {datetime.now().strftime('%H:%M:%S')}")
        st.markdown("---")

# 4. دالة الإحصائيات (التي أصلحناها لعدم ظهور KeyError)
def render_kpi_radar(df):
    n_total = len(df)[cite: 1]
    
    # التأكد من وجود العمود قبل الحساب
    if "Potential R:R" in df.columns:[cite: 1]
        n_rr3 = sum(1 for v in df["Potential R:R"] if _to_rr(v) >= 3)[cite: 1]
    else:
        n_rr3 = 0[cite: 1]

    col1, col2, col3 = st.columns(3)[cite: 1]
    with col1:
        st.metric("إجمالي العملات", n_total)[cite: 1]
    with col2:
        st.metric("فرص R:R >= 3", n_rr3)[cite: 1]
    with col3:
        win_rate = (n_rr3 / n_total * 100) if n_total > 0 else 0[cite: 1]
        st.metric("كثافة الفرص", f"{win_rate:.1f}%")[cite: 1]

# 5. الدالة الرئيسية لتشغيل التطبيق
def main():
    # حجز مكان الرأس في أعلى الصفحة[cite: 1]
    header_spot = st.empty()[cite: 1]
    render_header(header_spot)[cite: 1]
    
    # القائمة الجانبية للتحكم
    st.sidebar.header("لوحة التحكم")
    scan_btn = st.sidebar.button("تشغيل رادار ICT")
    
    if scan_btn:
        # هنا نضع بيانات تجريبية للتأكد من عمل الكود
        # في ملفك الأصلي، البيانات تأتي من محرك التحليل engine.py
        data = {
            "Symbol": ["BTC/USDT", "ETH/USDT", "SOL/USDT"],
            "Potential R:R": [3.5, 1.2, 4.0]
        }
        df_results = pd.DataFrame(data)
        
        # عرض الإحصائيات الآمنة
        render_kpi_radar(df_results)[cite: 1]
        
        # عرض الجدول
        st.table(df_results)[cite: 1]

if __name__ == "__main__":
    main()[cite: 1]
