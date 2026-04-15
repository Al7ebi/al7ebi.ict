import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class HabbiEngine:
    def __init__(self):
        self.freshness_limit_hours = 72 # قاعدة الـ 3 أيام

    def get_market_data(self):
        """
        محاكاة لجلب البيانات. (المبرمج يربطها هنا بـ MetaTrader أو Binance)
        """
        # بيانات تجريبية لمحاكاة استراتيجية Habbi Golden Setup
        data = {
            "symbol": "XAUUSD",
            "current_price": 2355.20,
            "yesterday_high": 2350.00,
            "yesterday_low": 2310.00,
            "h1_high": 2360.00,
            "h1_low": 2345.00,
            "timestamp": datetime.now() - timedelta(hours=2) # مثال لإشارة حديثة
        }
        return data

    def analyze_habbi_golden(self):
        """
        تطبيق استراتيجية Habbi Golden Setup:
        1. سحب سيولة يومية
        2. كسر هيكل (MSS) + IFVG (محاكاة)
        3. دخول عند الـ 50% Equilibrium
        """
        d = self.get_market_data()
        
        # الخطوة 1: كشف سحب السيولة
        sweep_type = None
        if d['current_price'] > d['yesterday_high']:
            sweep_type = "Daily High Swept"
        elif d['current_price'] < d['yesterday_low']:
            sweep_type = "Daily Low Swept"
            
        # الخطوة 2: حساب الـ 50% Equilibrium لموجة الـ H1
        equilibrium_price = (d['h1_high'] + d['h1_low']) / 2
        
        # الخطوة 3: تحديد الهدف (External Liquidity)
        target = d['yesterday_high'] if d['current_price'] < equilibrium_price else d['yesterday_low']

        return {
            "symbol": d['symbol'],
            "status": "Active" if sweep_type else "Scanning",
            "sweep": sweep_type if sweep_type else "Waiting",
            "mss": "Confirmed (H1)",
            "entry": equilibrium_price,
            "target": target,
            "time": d['timestamp']
        }

    def is_fresh(self, signal_time):
        """التحقق من Freshness Rule"""
        return (datetime.now() - signal_time).total_seconds() / 3600 < self.freshness_limit_hours

# استنتاج المحرك للاستخدام المباشر
habbi_brain = HabbiEngine()
