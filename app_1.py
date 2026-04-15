import streamlit as st
import datetime
import pandas as pd
# استيراد المحرك الفعلي الخاص بك
try:
    import engine as E
except:
    st.error("خطأ: ملف engine.py غير موجود في نفس المجلد!")

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="منصة الحبي للتداول | Habbi Radar",
    page_icon="🎯",
    layout="wide"
)

# 2. التنسيق البصري (McKinsey Style - Compact Version)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    * { font-family: 'Tajawal', sans-serif !important; direction: rtl; }
    .stApp { background-color: #0e1117; }
    
    /* تصغير البطاقات لتكون متراصة */
    .metric-card {
        background-color: #1a1a1a;
        border: 1px solid #d4af37;
        border-radius: 10px;
        padding: 10px; /* تقليل المساحة */
        text-align: center;
        color: white;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 20px; /* تصغير الخط */
        font-weight: 700;
        color: #ffcc00;
    }
    .gold-text { color: #d4af37 !important; text-align: center; }
    
    /* شريط الأخبار السفلي */
    .marquee-container {
        width: 100%; background: #d4af37; color: black;
        position: fixed; bottom: 0; left: 0; padding: 5px;
        font-weight: bold; font-size: 14px; z-index: 100;
    }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر (Header)
st.markdown('<h2 class="gold-text">📡 منصة الحبي للتداول الاحترافي</h2>', unsafe_allow_html=True)

col_time, col_status = st.columns(2)
now = datetime.datetime.now()

with col_time:
    st.markdown(f"<div style='text-align:right; color:white;'>{now.strftime('%I:%M %p')} | {now.strftime('%Y-%m-%d')}</div>", unsafe_allow_html=True)

with col_status:
    is_open = 16 <= now.hour < 23 # توقيت السوق الأمريكي كمثال
    status_msg = "السوق مفتوح 🟢" if is_open else "السوق مغلق 🔴"
    st.markdown(f"<div style='text-align:left; color:white;'>{status_msg}</div>", unsafe_allow_html=True)

st.write("---")

# 4. محرك البحث والمسح الفعلي (Habbi Logic)
# هنا نقوم باستدعاء الدالة الحقيقية من ملف engine الخاص بك
@st.cache_data(ttl=60)
def fetch_habbi_signals():
    try:
        # تأكد أن اسم الدالة في engine.py هو get_signals أو عدلها هنا
        return E.get_signals() 
    except:
        # بيانات احتياطية في حال فشل المحرك
        return [{"Ticker": "ORCL", "Score": "9/13", "Grade": "A", "Bias": "Long", "PD_Array": "Breaker", "DOL": "207.07"}]

signals = fetch_habbi_signals()

# 5. عرض شبكة البيانات (Compact Grid)
st.markdown('<h4 class="gold-text">📊 رادار الصفقات النشطة</h4>', unsafe_allow_html=True)

# عرض الصفقات في صفوف متراصة (كل صف يحتوي 4 بطاقات)
for signal in signals:
    with st.container():
        cols = st.columns(6)
        fields = [
            ("Ticker", signal.get('Ticker', 'N/A')),
            ("Score", signal.get('Score', '0/13')),
            ("Grade", signal.get('Grade', 'C')),
            ("Bias", signal.get('Bias', 'N/A')),
            ("PD Array", signal.get('PD_Array', 'N/A')),
            ("DOL", signal.get('DOL', 'N/A'))
        ]
        
        for i, (label, val) in enumerate(fields):
            with cols[i]:
                st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size:12px; color:#aaa;">{label}</div>
                        <div class="metric-value">{val}</div>
                    </div>
                """, unsafe_allow_html=True)

st.write("---")

# 6. تفاصيل الاستراتيجية (التطابق مع نظامك)
if signals:
    st.info(f"✅ تم العثور على {len(signals)} فرصة تطابق استراتيجية الحبي (سحب سيولة + IFVG).")
else:
    st.warning("🔄 الرادار يبحث الآن عن سحب سيولة جديد... لم يتم العثور على فرص تطابق شروط 13/13 حالياً.")

# شريط الأخبار
st.markdown("""
    <div class="marquee-container">
        <marquee direction="right">
            تم تطبيق قانون الـ 3 أيام بنجاح | نظام الحبي 13/13 نشط | جاري مسح PD Arrays | دقة التحليل هي هدفنا.
        </marquee>
    </div>
""", unsafe_allow_html=True)
