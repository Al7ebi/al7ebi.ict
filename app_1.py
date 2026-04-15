from flask import Flask, render_template, jsonify
import datetime
import random

app = Flask(__name__)

# المحرك التحليلي - طريقة الحبي
class HabbiLogic:
    @staticmethod
    def check_daily_sweep(price_data):
        # محاكاة فحص سحب السيولة (ضرب قمة أو قاع اليوم السابق)
        return random.choice([True, False])

    @staticmethod
    def confirm_mss_ifvg(price_data):
        # محاكاة تأكيد كسر هيكل السوق وتكون الفجوة العكسية
        return random.choice([True, False])

    @staticmethod
    def calculate_equilibrium(wave_high, wave_low):
        # تحديد منطقة الخصم 50%
        return (wave_high + wave_low) / 2

    @staticmethod
    def get_score(signal_data):
        # نظام التقييم من 13
        score = 0
        if signal_data['sweep']: score += 4
        if signal_data['mss']: score += 3
        if signal_data['ifvg']: score += 3
        if signal_data['equilibrium']: score += 3
        return score

# بيانات تجريبية
signals_db = [
    {
        "symbol": "BTC/USD",
        "sweep": True,
        "mss": True,
        "ifvg": True,
        "equilibrium": True,
        "price": 65000,
        "high": 66000,
        "low": 64000,
        "timestamp": datetime.datetime.now() - datetime.timedelta(hours=2),
        "type": "شراء (Long)"
    },
    {
        "symbol": "GOLD",
        "sweep": True,
        "mss": False,
        "ifvg": True,
        "equilibrium": True,
        "price": 2350,
        "high": 2360,
        "low": 2340,
        "timestamp": datetime.datetime.now() - datetime.timedelta(hours=75), # منتهية الصلاحية
        "type": "بيع (Short)"
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/market_data')
def market_data():
    now = datetime.datetime.now()
    # محاكاة حالة السوق (مفتوح من 9 ص إلى 5 م)
    is_open = 9 <= now.hour < 17
    
    indicators = [
        {"name": "مؤشر السيولة", "price": "1.2B", "change": 2.5},
        {"name": "تاسي (TASI)", "price": "12,450", "change": -0.4},
        {"name": "الذهب", "price": "2,385", "change": 1.2},
        {"name": "النفط", "price": "85.4", "change": 0.8},
        {"name": "البيتكوين", "price": "67,200", "change": 4.1},
        {"name": "الدولار/ريال", "price": "3.75", "change": 0.0}
    ]
    
    return jsonify({
        "market_open": is_open,
        "countdown": "يغلق بعد: 04:20:15" if is_open else "يفتح بعد: 08:00:00",
        "indicators": indicators
    })

@app.route('/api/signals')
def get_signals():
    fresh_signals = []
    for s in signals_db:
        age = (datetime.datetime.now() - s['timestamp']).total_seconds() / 3600
        
        # قانون الـ 3 أيام (72 ساعة)
        if age > 72:
            status = "منتهية"
            continue # استبعاد التلقائي
        else:
            status = "طازجة"
            
        score = HabbiLogic.get_score(s)
        entry = HabbiLogic.calculate_equilibrium(s['high'], s['low'])
        
        fresh_signals.append({
            "symbol": s['symbol'],
            "score": score,
            "type": s['type'],
            "reason": "سحب سيولة + MSS + IFVG" if score > 10 else "تجميع وقود",
            "entry": f"{entry:.2f}",
            "tp": f"{s['high'] if s['type'] == 'شراء (Long)' else s['low']}",
            "age": int(age)
        })
    
    return jsonify(fresh_signals)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
