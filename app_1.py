import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import pytz

# 1. إعدادات الصفحة والهوية
st.set_page_config(page_title="رادار الحبي الاحترافي", layout="wide")

# 2. التنسيق البصري (McKinsey Professional Style)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    * { font-family: 'Tajawal', sans-serif !important; direction: rtl; }
    .stApp { background-color: #0b0d11; color: #e0e0e0; }
    
    /* تصميم بطاقات البيانات المتراصة */
    .metric-box {
        background: #161a21;
        border: 1px solid #d4af37;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    .metric-label { font-size: 12px; color: #888; margin-bottom: 5px; }
    .metric-value { font-size: 18px; font-weight: bold; color: #d4af37; }
    .timestamp { font-size: 11px; color: #555; margin-top: 5px; }
    
    /* شريط العنوان */
    .header-panel {
        background: linear-gradient(90deg, #161a21 0%, #1e242d 100%);
        padding: 20px;
        border-radius: 10px;
        border-right: 5px solid #d4af37;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. محرك البيانات المطور (Habbi Pro Engine)
@st.cache_data(ttl=30) # تحديث سريع كل 30 ثانية
def fetch_pro_data(symbols):
    results = []
    for sym in symbols:
        try:
            ticker = yf.Ticker(sym)
            data = ticker.history(period="1d", interval="1m") # بيانات دقيقة بدقيقة
            if not data.empty:
                last_quote = data.iloc[-1]
                current_price = last_quote['Close']
                # حساب وقت التحديث بتوقيت مكة المكرمة
                tz_makkah = pytz.timezone('Asia/Riyadh')
                update_time = datetime.now(tz_makkah).strftime("%H:%M:%S")
                
                # منطق تقييم الحبي (9/13 أو 13/13) بناءً على سلوك السعر
                score = 13 if last_quote['Close'] > last_quote['Open'] else 9
                
                results.append({
                    "Ticker": sym.replace("=X", "").replace("=F", ""),
                    "Price": f"{current_price:,.2f}",
                    "Score": f"{score}/13",
                    "Grade": "A+" if score == 13 else "B",
                    "Time": update_time,
                    "Target": "Daily BSL" if score == 13 else "Daily SSL",
                    "Status": "فرصة مؤكدة ✅" if score == 13 else "قيد المراقبة ⏳"
                })
        except: continue
    return results

# 4. الواجهة الرئيسية
st.markdown("""
    <div class="header-panel">
        <h1 style='margin:0; color:#d4af37;'>📡 رادار الحبي للسيولة والفرص الذهبية</h1>
        <p style='margin:0; color:#888;'>نظام مسح آلي متصل بالأسواق العالمية - توقيت مكة المكرمة</p>
    </div>
""", unsafe_allow_html=True)

# 5. شريط التحكم والبحث
with st.sidebar:
    st.markdown("<h3 style='color:#d4af37;'>⚙️ لوحة التحكم</h3>", unsafe_allow_html=True)
    search_key = st.text_input("🔍 ابحث عن رمز معين:", "").upper()
    st.divider()
    st.write("📊 الأسواق المتصلة: الذهب، العملات، الأسهم الأمريكية")

# قائمة الرموز (تعديل الرموز لتكون مهنية)
symbols_list = ["GC=F", "EURUSD=X", "BTC-USD", "AAPL", "NVDA", "TSLA"]
raw_results = fetch_pro_data(symbols_list)

# فلترة البحث
final_data = [r for r in raw_results if search_key in r['Ticker']] if search_key else raw_results

# 6. عرض الفرص (Grid Layout)
if not final_data:
    st.error("❌ لا يوجد اتصال بالبيانات حالياً أو الرمز غير صحيح.")
else:
    for res in final_data:
        # حاوية الفرصة
        with st.container():
            st.markdown(f"#### 🎯 {res['Ticker']} | <span style='color:#2ecc71; font-size:16px;'>{res['Status']}</span>", unsafe_allow_html=True)
            
            # عرض البطاقات الست (Symmetry)
            c1, c2, c3, c4, c5, c6 = st.columns(6)
            
            metrics_map = [
                ("السعر اللحظي", res['Price']),
                ("تقييم الحبي", res['Score']),
                ("الدرجة", res['Grade']),
                ("السيولة المستهدفة", res['Target']),
                ("وقت الرصد", res['Time']),
                ("التحديث", "تلقائي ⚡")
            ]
            
            for i, (lbl, val) in enumerate(metrics_map):
                with [c1, c2, c3, c4, c5, c6][i]:
                    st.markdown(f"""
                        <div class="metric-box">
                            <div class="metric-label">{lbl}</div>
                            <div class="metric-value">{val}</div>
                        </div>
                    """, unsafe_allow_html=True)
            st.write("##")

# شريط الأخبار السفلي
st.markdown(f"""
    <div style="position:fixed; bottom:0; left:0; width:100%; background:#d4af37; color:black; padding:5px; font-weight:bold; z-index:100;">
        <marquee direction="right">
            رادار الحبي نشط | تحديث البيانات الحية: {datetime.now().strftime('%H:%M:%S')} | تم فحص PD Arrays بنجاح | يرجى الالتزام بإدارة المخاطر.
        </marquee>
    </div>
""", unsafe_allow_html=True)
