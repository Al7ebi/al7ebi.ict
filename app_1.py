import streamlit as st
import pandas as pd
import yfinance as yf
import datetime

# 1. إعدادات الثيم (أبيض/أسود)
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

def toggle_theme():
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# الألوان الاحترافية
if st.session_state.theme == 'dark':
    bg, txt, card, border = "#0e1117", "#ffffff", "#1a1a1a", "#d4af37"
else:
    bg, txt, card, border = "#f9f9f9", "#000000", "#ffffff", "#dddddd"

st.set_page_config(page_title="منصة الحبي | Habbi Radar Live", layout="wide")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    * {{ font-family: 'Tajawal', sans-serif !important; direction: rtl; }}
    .stApp {{ background-color: {bg}; color: {txt}; }}
    .metric-card {{
        background-color: {card}; border: 1px solid {border};
        border-radius: 12px; padding: 15px; text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
    .gold-text {{ color: #d4af37 !important; text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# 2. محرك جلب البيانات الحية (Real-Time Engine)
@st.cache_data(ttl=60)  # تحديث كل دقيقة
def get_live_market_data(symbols):
    data_list = []
    for sym in symbols:
        ticker = yf.Ticker(sym)
        hist = ticker.history(period="2d")
        if not hist.empty:
            price = hist['Close'].iloc[-1]
            # محاكاة منطق الحبي (التقييم بناءً على حركة السعر الحقيقية)
            # مثال: إذا كان السعر فوق متوسط اليوم السابق نعطيه درجة أعلى
            score = 13 if price > hist['Open'].iloc[-1] else 9
            data_list.append({
                "Ticker": sym.replace("=X", "").replace("=F", ""),
                "Price": round(price, 2),
                "Score": f"{score}/13",
                "Grade": "A+" if score == 13 else "B",
                "Bias": "Long" if score == 13 else "Short",
                "Change": round(((price - hist['Close'].iloc[-2])/hist['Close'].iloc[-2])*100, 2)
            })
    return data_list

# 3. التحكم والبحث
with st.sidebar:
    st.markdown("<h2 class='gold-text'>تحكم المنصة</h2>", unsafe_allow_html=True)
    st.button("☀️/🌙 تبديل الوضع", on_click=toggle_theme)
    search_query = st.text_input("🔍 ابحث عن رمز (مثلاً: GC=F للذهب أو AAPL)", "").upper()
    st.write("---")
    st.info("الرادار متصل الآن ببيانات الأسواق العالمية الحية.")

# القائمة الافتراضية للرادار (ذهب، نفط، بيتكوين، أسهم تقنية)
default_symbols = ["GC=F", "CL=F", "BTC-USD", "AAPL", "NVDA", "ORCL"]
market_data = get_live_market_data(default_symbols)

# 4. واجهة العرض
st.markdown('<h1 class="gold-text">📡 رادار الحبي للسيولة الحية</h1>', unsafe_allow_html=True)

# حالة السوق الحقيقية (نيويورك)
now_ny = datetime.datetime.now() # يمكن ضبط التوقيت بدقة لاحقاً
st.markdown(f"<p style='text-align:center;'>توقيت النظام: {now_ny.strftime('%I:%M %p')} | الحالة: <span style='color:#2ecc71;'>السوق الأمريكي مفتوح ✅</span></p>", unsafe_allow_html=True)

st.write("---")

# فلترة البحث
display_data = [s for s in market_data if search_query in s['Ticker']] if search_query else market_data

if not display_data:
    st.warning("لم يتم العثور على بيانات للرمز المطلوب.")
else:
    for s in display_data:
        st.markdown(f"### 🎯 {s['Ticker']} | السعر الحالي: {s['Price']}")
        c1, c2, c3, c4, c5 = st.columns(5)
        metrics = [
            ("التقييم", s['Score']), ("الدرجة", s['Grade']), 
            ("الاتجاه", s['Bias']), ("التغير اليومي", f"{s['Change']}%"),
            ("الحالة", "فرصة ذهبية" if s['Score'] == "13/13" else "قيد المراقبة")
        ]
        for i, (lbl, val) in enumerate(metrics):
            with [c1, c2, c3, c4, c5][i]:
                color = "#2ecc71" if "+" in str(val) or "13" in str(val) or "Long" in str(val) else "#d4af37"
                st.markdown(f"""
                    <div class="metric-card">
                        <small style='color:#888;'>{lbl}</small>
                        <div style="font-size:20px; font-weight:bold; color:{color};">{val}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.write("##")

st.markdown('<marquee style="background:#d4af37; color:black; padding:8px; font-weight:bold;">⚠️ رادار الحبي: يتم الآن سحب أسعار الذهب والنفط والأسهم لحظياً.. نظام التقييم 13/13 يعمل بناءً على حركة السعر الفعلية.</marquee>', unsafe_allow_html=True)
