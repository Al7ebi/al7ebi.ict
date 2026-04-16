import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="منصة الحبي للتداول", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
html, body, [class*="css"] { direction: rtl; text-align: right; font-family: 'Noto Kufi Arabic', 'Segoe UI', sans-serif; }
html { font-size: 19px; }
.stApp { background: #0d1117; color: #e5e7eb; }
.block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 100% !important; }
.shell { background:#161b26; border:1px solid #263244; border-radius:18px; box-shadow:0 8px 24px rgba(0,0,0,0.18); }
.top-shell { padding: 1rem 1.1rem; margin-bottom: 0.9rem; }
.iconbtn { width: 46px; height: 46px; border-radius: 14px; background: #1e2536; display: flex; align-items: center; justify-content: center; color: #aab3c5; font-size: 1.1rem; border: 1px solid #2b3550; }
.brand-badge { width: 56px; height: 56px; border-radius: 16px; background: linear-gradient(135deg,#2f80ed,#29b6f6); display:flex; align-items:center; justify-content:center; color:white; font-size:1.8rem; font-weight:800; box-shadow:0 10px 28px rgba(41,182,246,0.28); }
.brand-title { font-size:1.8rem; line-height:1.2; font-weight:900; color:#fff; margin:0; }
.brand-sub { color:#7a8497; font-size:0.93rem; margin-top:0.15rem; }
.clock-box { color:#aab3c5; font-size:1.05rem; font-weight:700; letter-spacing:0.5px; }
.tabs-shell { margin-bottom:0.65rem; border-bottom:1px solid #232c3b; padding:0 0.5rem; }
.market-tab { display:inline-flex; align-items:center; gap:0.45rem; color:#7b8498; font-size:1.05rem; font-weight:800; padding:0.95rem 0.3rem 0.8rem 0.3rem; margin-left:1.25rem; border-bottom:3px solid transparent; }
.market-tab.active { color:#3b82f6; border-bottom-color:#3b82f6; }
.status-shell { background:#0f1520; border:1px solid #243041; border-radius:16px; padding:0.95rem 1rem; margin-bottom:1rem; }
.status-dot { width:13px; height:13px; border-radius:999px; background:#ef4444; display:inline-block; margin-lef
