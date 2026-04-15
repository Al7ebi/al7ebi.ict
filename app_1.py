import streamlit as st
import pandas as pd
import datetime
import time

# --- إعدادات الصفحة العامة ---
st.set_page_config(
    page_title="منصة الحبي للتداول",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- تنسيق CSS مخصص للواجهة (Dark Theme & RTL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #374151;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #111827;
        color: #9ca3af;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        border-top: 1px solid #374151;
    }
    </style>
    """, unsafe_allow_html=True)

# --- منطق توقيت السوق ---
def get_market_status(market):
    now = datetime.datetime.now()
    # مثال مبسط لمنطق التوقيت (يمكن ربطه ببيانات حية)
    if market == "السوق السعودي":
        opening = now.replace(hour=10, minute=0, second=0)
        closing = now.replace(hour=15, minute=0, second=0)
    else: # السوق الأمريكي
        opening = now.replace(hour=16, minute=30, second=0)
        closing = now.replace(hour=23, minute=0, second=0)
    
    if opening <= now <= (closing - datetime.timedelta(hours=1)):
        return "🟢 مفتوح", "#10b981"
    elif (closing - datetime.timedelta(hours=1)) < now <= closing:
        return "🟠 يغلق قريباً", "#f59e0b"
    else:
        return "🔴 مغلق", "#ef4444"

# --- العناوين الرئيسية ---
st.title("📊 منصة الحبي للتداول")
st.divider()

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.header("إعدادات المنصة")
    market_choice = st.selectbox("اختر السوق المستهدف:", ["السوق السعودي", "السوق الأمريكي"])
    status_text, status_color = get_market_status(market_choice)
    
    st.markdown(f"### حالة السوق: <span style='color:{status_color}'>{status_text}</span>", unsafe_allow_html=True)
    st.info(f"آخر تحديث للبيانات: {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    # تنبيهات صوتية (محاكاة)
    st.toggle("تفعيل التنبيهات الصوتية (الرادار)", value=True)

# --- لوحة التحكم العلوية (Metrics) ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("عدد الصفقات النشطة", "12", "+2")
with col2:
    st.metric("الصفقات المنتظرة", "5", "-1")
with col3:
    st.metric("متوسط القوة", "2.8 / 3")
with col4:
    st.metric("أداء الاستراتيجية اليوم", "85%", "4%")

# --- إدارة الصفقات (Grid Management) ---
st.subheader(f"🗂️ إدارة صفقات {market_choice}")

# محاكاة بيانات الصفقات
data = {
    'الرمز': ['2222', '1120', '7010', '4300'],
    'الشركة': ['أرامكو', 'الراجحي', 'اس تي سي', 'دار الأركان'],
    'نقطة الدخول': [32.10, 85.50, 38.20, 14.10],
    'وقف الخسارة': [31.50, 83.00, 37.00, 13.80],
    'القوة': [3, 2, 3, 1],
    'الهدف 1': [34.00, 90.00, 41.00, 15.50],
    'التقدم (%)': [75, 40, 10, 0]
}
df = pd.DataFrame(data)

# شريط البحث والفرز
search_col, filter_col = st.columns([2, 1])
with search_col:
    search_term = st.text_input("🔍 ابحث عن رمز أو شركة...")
with filter_col:
    sort_option = st.selectbox("ترتيب حسب:", ["الأقوى (الاستراتيجية)", "الأكثر تقدماً", "الأحدث"])

# عرض الصفقات في بطاقات منظمة
for index, row in df.iterrows():
    with st.container():
        c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 2, 1])
        with c1:
            st.markdown(f"**{row['الرمز']}**\n\n{row['الشركة']}")
        with c2:
            st.write(f"دخول: {row['نقطة الدخول']}")
            st.write(f"وقف: {row['وقف الخسارة']}")
        with c3:
            st.write(f"القوة: {'⭐' * row['القوة']}")
        with c4:
            st.write(f"التقدم نحو الهدف الأول ({row['الهدف 1']})")
            st.progress(row['التقدم (%)'] / 100)
        with c5:
            if st.button(f"تفاصيل {row['الرمز']}", key=row['الرمز']):
                st.toast(f"فتح تفاصيل {row['الشركة']}...")
        st.divider()

# --- قسم الصفقات المنتظرة ---
with st.expander("⏳ عرض الصفقات المنتظرة وأسباب الانتظار"):
    st.warning("الرمز 1180: بانتظار اختراق مستويات السيولة (RSI > 60)")
    st.warning("الرمز 2010: بانتظار تأكيد شمعة الارتداد")

# --- التذييل القانوني ---
st.markdown("""
    <div class="footer">
        <p>جميع الحقوق محفوظة لـ <b>منصة الحبي للتداول</b> © 2026</p>
        <p>تنبيه: المنصة لأغراض تعليمية فقط. المعلومات المقدمة لا تعتبر نصيحة مالية، ولا تتحمل المنصة أي التزامات مالية ناتجة عن التداول.</p>
    </div>
    """, unsafe_allow_html=True)

# --- تحديث دوري (محاكاة) ---
# ملاحظة: في Streamlit يتم استخدام fragment أو empty لتحديث أجزاء معينة
# هذا الكود سيقوم بإعادة التشغيل كل 300 ثانية (5 دقائق)
# st.empty() 
# time.sleep(300)
# st.rerun()
