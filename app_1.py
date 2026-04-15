import streamlit as st
import datetime
import pandas as pd

# 1. نظام التبديل بين الأبيض والأسود (Theme Logic)
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

def change_theme():
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# إعدادات الألوان بناءً على اختيارك
if st.session_state.theme == 'dark':
    bg, txt, card_bg, border = "#0e1117", "#ffffff", "#1a1a1a", "#d4af37"
else:
    bg, txt, card_bg, border = "#ffffff", "#000000", "#f0f2f5", "#cccccc"

st.set_page_config(page_title="منصة الحبي | Habbi Radar", layout="wide")

# 2. التنسيق البصري (McKinsey Style)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    * {{ font-family: 'Tajawal', sans-serif !important; direction: rtl; }}
    .stApp {{ background-color: {bg}; color: {txt}; }}
    .metric-card {{
        background-color: {card_bg}; border: 1px solid {border};
        border-radius: 8px; padding: 10px; text-align: center; margin-bottom: 10px;
    }}
    .gold-text {{ color: #d4af37 !important; text-align: center; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# 3. الشريط الجانبي (Sidebar) - واجهة التحكم
with st.sidebar:
    st.markdown("<h2 class='gold-text'>لوحة التحكم</h2>", unsafe_allow_html=True)
    st.button("☀️/🌙 تبديل المظهر (أبيض/أسود)", on_click=change_theme)
    st.write("---")
    search_query = st.text_input("🔍 ابحث بالرمز أو الاسم (مثلاً: ORCL أو الذهب)", "").upper()
    st.write("---")
    st.write("⚙️ إعدادات الرادار:")
    st.checkbox("تفعيل قانون الـ 3 أيام", value=True)

# 4. محاكاة بيانات المحرك (استبدلها بـ E.get_signals() لاحقاً)
raw_data = [
    {"Ticker": "ORCL", "Score": "13/13", "Grade": "A+", "Bias": "Long", "PD_Array": "FVG", "DOL": "207.07"},
    {"Ticker": "XAUUSD", "Score": "9/13", "Grade": "B", "Bias": "Short", "PD_Array": "Breaker", "DOL": "2340.5"},
    {"Ticker": "NVDA", "Score": "11/13", "Grade": "A", "Bias": "Long", "PD_Array": "Order Block", "DOL": "950.2"},
    {"Ticker": "TASI", "Score": "7/13", "Grade": "C", "Bias": "Neutral", "PD_Array": "N/A", "DOL": "12500"}
]

# منطق البحث (الفلترة)
if search_query:
    filtered_data = [s for s in raw_data if search_query in s['Ticker']]
else:
    filtered_data = raw_data

# 5. عرض الهيدر وحالة السوق
st.markdown('<h2 class="gold-text">📡 رادار الحبي للسيولة</h2>', unsafe_allow_html=True)

col_t, col_s = st.columns(2)
with col_t:
    st.write(f"🕒 {datetime.datetime.now().strftime('%I:%M %p')} | {datetime.datetime.now().strftime('%Y-%m-%d')}")
with col_s:
    # يمكنك تعديل توقيت السوق هنا
    is_open = 16 <= datetime.datetime.now().hour < 23
    st.write(f"وضع السوق: {'مفتوح 🟢' if is_open else 'مغلق 🔴'}")

st.write("---")

# 6. عرض النتائج بأسلوب الشبكة (Grid)
if not filtered_data:
    st.warning("⚠️ لا توجد نتائج مطابقة لبحثك.")
else:
    for signal in filtered_data:
        st.markdown(f"### 🎯 تحليل: {signal['Ticker']}")
        cols = st.columns(6)
        metrics = [
            ("الرمز", signal['Ticker']), ("التقييم", signal['Score']), ("الدرجة", signal['Grade']),
            ("الاتجاه", signal['Bias']), ("المنطقة", signal['PD_Array']), ("الهدف", signal['DOL'])
        ]
        for i, (label, val) in enumerate(metrics):
            with cols[i]:
                st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size:12px; color:#888;">{label}</div>
                        <div style="font-size:18px; font-weight:bold; color:#d4af37;">{val}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.write("---")

# شريط الأخبار السفلي
st.markdown('<marquee style="background:#d4af37; color:black; padding:5px;">جاري فحص السيولة... تم تفعيل رادار الحبي بنجاح | نظام البحث نشط الآن</marquee>', unsafe_allow_html=True)
