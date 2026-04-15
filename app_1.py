import streamlit as st
from datetime import datetime
import pytz
import time

# 1. إعدادات المنصة الأساسية
st.set_page_config(page_title="Habbi Pro Terminal", layout="wide", initial_sidebar_state="expanded")

# 2. هندسة التصميم (McKinsey & Gold Edition CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    
    /* التنسيق العام */
    * { font-family: 'Tajawal', sans-serif !important; direction: rtl; }
    .stApp { background-color: #0b0d11; color: #e0e0e0; }
    
    /* بطاقة التداول الاحترافية */
    .trade-card {
        background: linear-gradient(145deg, #161a21, #1c2229);
        border: 1px solid #333;
        border-right: 5px solid #d4af37;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }
    
    /* مؤشرات الحالة */
    .status-ready { color: #2ecc71; background: rgba(46, 204, 113, 0.1); padding: 5px 15px; border-radius: 50px; font-weight: bold; border: 1px solid #2ecc71; }
    .status-hold { color: #f1c40f; background: rgba(241, 196, 15, 0.1); padding: 5px 15px; border-radius: 50px; font-weight: bold; border: 1px solid #f1c40f; }
    
    /* أرقام الأسعار */
    .price-label { font-size: 13px; color: #888; margin-bottom: 5px; }
    .price-value { font-size: 24px; font-weight: 900; color: #d4af37; }
    
    /* شريط التقدم للهدف */
    .progress-container { background-color: #333; border-radius: 10px; margin: 10px 0; height: 10px; width: 100%; }
    .progress-bar { background: #d4af37; height: 10px; border-radius: 10px; width: 65%; } /* مثال 65% للهدف */
    </style>
""", unsafe_allow_html=True)

# 3. الشريط الجانبي (لوحة التحكم)
with st.sidebar:
    st.markdown("<h2 style='color:#d4af37; text-align:center;'>⚙️ الإعدادات</h2>", unsafe_allow_html=True)
    st.text_input("🔍 ابحث عن رمز أو سوق:", placeholder="مثلاً: GOLD, NASDAQ...")
    st.divider()
    st.selectbox("الفريم الزمني:", ["5 دقائق", "15 دقيقة", "ساعة", "يومي"])
    st.checkbox("تفعيل التنبيهات الصوتية", value=True)
    st.write("---")
    st.caption("نظام التحديث التلقائي نشط (كل 5 دقائق)")

# 4. هيدر المنصة
col_logo, col_time = st.columns([3, 1])
with col_logo:
    st.markdown("<h1 style='color:#d4af37; margin:0;'>📡 رادار الحبي | <span style='font-size:20px; color:#888;'>Habbi Execution Pro</span></h1>", unsafe_allow_html=True)
with col_time:
    makkah_time = datetime.now(pytz.timezone('Asia/Riyadh')).strftime('%H:%M:%S')
    st.markdown(f"<div style='text-align:left; color:#888;'>توقيت مكة المكرمة<br><b style='color:#fff; font-size:20px;'>{makkah_time}</b></div>", unsafe_allow_html=True)

st.divider()

# 5. عرض الصفقات (نموذج محاكاة للواجهة فقط)
# هنا ستقوم لاحقاً بربط بيانات استراتيجيتك في هذه المربعات
mock_data = [
    {"symbol": "XAUUSD (الذهب)", "status": "جاهز للتنفيذ", "class": "ready", "price": "2,385.40", "entry": "2,382.00", "target": "2,405.00", "stop": "2,375.00", "progress": "75%"},
    {"symbol": "NAS100 (ناسداك)", "status": "قيد المراقبة", "class": "hold", "price": "18,250.10", "entry": "18,180.00", "target": "18,400.00", "stop": "18,100.00", "progress": "30%"}
]

for item in mock_data:
    st.markdown(f"""
        <div class="trade-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <div>
                    <span style="font-size:26px; font-weight:900;">{item['symbol']}</span>
                    <span style="margin-right:15px;" class="status-{item['class']}">{item['status']}</span>
                </div>
                <div style="text-align:left;">
                    <span style="color:#888;">المسافة للهدف:</span> <span style="color:#d4af37; font-weight:bold;">{item['progress']}</span>
                    <div class="progress-container"><div class="progress-bar" style="width:{item['progress']};"></div></div>
                </div>
            </div>
            <div style="display:flex; justify-content:space-around;">
                <div style="text-align:center;"><div class="price-label">السعر اللحظي</div><div class="price-value">{item['price']}</div></div>
                <div style="text-align:center;"><div class="price-label">نقطة الدخول (50%)</div><div class="price-value" style="color:#3498db;">{item['entry']}</div></div>
                <div style="text-align:center;"><div class="price-label">الهدف النهائي (DOL)</div><div class="price-value" style="color:#2ecc71;">{item['target']}</div></div>
                <div style="text-align:center;"><div class="price-label">وقف الخسارة</div><div class="price-value" style="color:#e74c3c;">{item['stop']}</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 6. قسم إدارة الصفقة ورفع الوقف
st.write("##")
with st.expander("🛠️ أدوات إدارة الصفقة النشطة"):
    c1, c2, c3 = st.columns(3)
    c1.button("🚨 إغلاق فوري لجميع المراكز")
    c2.button("🛡️ تأمين (نقل الوقف للدخول)")
    c3.button("📈 جني أرباح جزئي (50%)")

# 7. التحديث الآلي (كل 5 دقائق)
time.sleep(300)
st.rerun()
