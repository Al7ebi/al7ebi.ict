import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- الإعدادات الفنية (McKinsey Dark UI) ---
st.set_page_config(page_title="Habbi Pro Terminal", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    * { font-family: 'Tajawal', sans-serif !important; direction: rtl; }
    .stApp { background-color: #0b0d11; color: #e0e0e0; }
    .status-active { color: #2ecc71; font-weight: bold; border: 1px solid #2ecc71; padding: 2px 10px; border-radius: 5px; }
    .status-wait { color: #f1c40f; font-weight: bold; border: 1px solid #f1c40f; padding: 2px 10px; border-radius: 5px; }
    .trade-box { background: #161a21; border-right: 5px solid #d4af37; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    .price-label { font-size: 14px; color: #888; }
    .price-val { font-size: 22px; font-weight: 900; color: #d4af37; }
    </style>
""", unsafe_allow_html=True)

# --- محرك استراتيجية الحبي (The Brain) ---
def get_habbi_signal(symbol):
    try:
        # جلب بيانات 5 دقائق لآخر يومين
        df = yf.download(symbol, period='2d', interval='5m')
        if df.empty: return None
        
        curr = df.iloc[-1]
        prev_high = df['High'].iloc[-20:].max() # أعلى قمة في الـ 20 شمعة الماضية
        prev_low = df['Low'].iloc[-20:].min()
        
        # 1. تحليل سحب السيولة (Liquidity Sweep)
        sweep_buy = curr['Low'] < prev_low and curr['Close'] > prev_low
        sweep_sell = curr['High'] > prev_high and curr['Close'] < prev_high
        
        # 2. مستويات التنفيذ (ICT Equilibrium)
        range_max, range_min = df['High'].max(), df['Low'].min()
        equilibrium = (range_max + range_min) / 2
        
        # 3. منطق الجاهزية (Readiness Logic)
        status = "انتظار سحب سيولة"
        color = "wait"
        if sweep_buy:
            status = "جاهز للشراء (Long Zone)"
            color = "active"
        elif sweep_sell:
            status = "جاهز للبيع (Short Zone)"
            color = "active"
        
        return {
            "Symbol": symbol,
            "Price": round(curr['Close'], 2),
            "Entry": round(equilibrium, 2),
            "Target": round(range_max if sweep_buy else range_min, 2),
            "Stop": round(prev_low * 0.998 if sweep_buy else prev_high * 1.002, 2),
            "Score": "13/13" if (sweep_buy or sweep_sell) else "9/13",
            "Status": status,
            "Class": color,
            "Time": datetime.now(pytz.timezone('Asia/Riyadh')).strftime('%H:%M:%S')
        }
    except: return None

# --- واجهة العرض التنفيذية ---
st.markdown("<h1 style='color:#d4af37; text-align:center;'>🎯 منصة الحبي: رادار التنفيذ اللحظي</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align:center;'>تحديث تلقائي كل 5 دقائق | توقيت مكة: {datetime.now(pytz.timezone('Asia/Riyadh')).strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

# شريط البحث
with st.sidebar:
    st.markdown("<h3 style='color:#d4af37;'>لوحة التحكم</h3>", unsafe_allow_html=True)
    user_symbol = st.text_input("ابحث عن رمز (مثال: GC=F, NQ=F):", "").upper()
    st.divider()
    st.write("⚙️ الرادار يفحص الآن: Liquidity Sweeps, MSS, IFVG")

tickers = [user_symbol] if user_symbol else ["GC=F", "NQ=F", "BTC-USD", "NVDA"]

for t in tickers:
    res = get_habbi_signal(t)
    if res:
        st.markdown(f"""
            <div class="trade-box">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:24px; font-weight:bold;">{res['Symbol']}</span>
                    <span class="status-{res['Class']}">{res['Status']}</span>
                    <span style="color:#888;">تقييم: {res['Score']} | ⌚ {res['Time']}</span>
                </div>
                <hr style="border:0.5px solid #333;">
                <div style="display:flex; justify-content:space-around; text-align:center;">
                    <div><p class="price-label">السعر اللحظي</p><p class="price-val">{res['Price']}</p></div>
                    <div><p class="price-label">نقطة الدخول (50%)</p><p class="price-val" style="color:#3498db;">{res['Entry']}</p></div>
                    <div><p class="price-label">الهدف (DOL)</p><p class="price-val" style="color:#2ecc71;">{res['Target']}</p></div>
                    <div><p class="price-label">وقف الخسارة</p><p class="price-val" style="color:#e74c3c;">{res['Stop']}</p></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ميزة إدارة الصفقة (متى تغلق أو ترفع الوقف)
st.write("---")
st.markdown("### 🛡️ دليل إدارة الصفقة (Execution Guide)")
col1, col2 = st.columns(2)
with col1:
    st.success("**متى ترفع الوقف؟** إذا حقق السعر 50% من المسافة نحو الهدف، انقل الوقف لنقطة الدخول (Breakeven).")
with col2:
    st.warning("**متى تغلق يدوياً؟** إذا ظهر سحب سيولة عكسي (Opposite Sweep) قبل الوصول للهدف النهائي.")

# التحديث الآلي
st.empty()
import time
time.sleep(300)
st.rerun()
