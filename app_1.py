// This Pine Script™ source code is subject to the terms of the Mozilla Public License 2.0
// © الحبي - Al-Habibi ICT Analyzer
// Version: 2.0.0 - Full ICT Suite

//@version=5
indicator("الحبي - Al-Habibi ICT v2", overlay=true, max_boxes_count=500, max_lines_count=500, max_labels_count=500, max_bars_back=5000)

// ══════════════════════════════════════════════════════════════════════════════
// ██  إعدادات اللغة / Language Settings
// ══════════════════════════════════════════════════════════════════════════════
string langChoice = input.string("عربي", title="اللغة / Language", options=["عربي", "English"], group="⚙️ عام / General")
bool isArabic = langChoice == "عربي"

// ══════════════════════════════════════════════════════════════════════════════
// ██  إعدادات عامة / General Settings
// ══════════════════════════════════════════════════════════════════════════════
int swingLen       = input.int(3, title="طول السوينج / Swing Length", minval=1, maxval=10, group="⚙️ عام / General")
int maxPat         = input.int(50, title="أقصى عدد نماذج / Max Patterns", minval=10, maxval=200, group="⚙️ عام / General")
float dispThresh   = input.float(1.5, title="عتبة الاندفاع / Displacement Threshold", minval=1.0, maxval=5.0, step=0.1, group="⚙️ عام / General")
int pdLookback     = input.int(50, title="فترة Premium/Discount", minval=20, maxval=200, group="⚙️ عام / General")

// ══════════════════════════════════════════════════════════════════════════════
// ██  إعدادات العرض / Display Toggles
// ══════════════════════════════════════════════════════════════════════════════
bool showFVG       = input.bool(true, title="FVG", group="📊 نماذج / Patterns")
bool showInvFVG    = input.bool(true, title="Inversion FVG", group="📊 نماذج / Patterns")
bool showOB        = input.bool(true, title="Order Blocks", group="📊 نماذج / Patterns")
bool showMSS       = input.bool(true, title="MSS", group="📊 نماذج / Patterns")
bool showBOS       = input.bool(true, title="BOS", group="📊 نماذج / Patterns")
bool showBPR       = input.bool(true, title="BPR", group="📊 نماذج / Patterns")
bool showRejBlock  = input.bool(true, title="Rejection Block", group="📊 نماذج / Patterns")
bool showVoids     = input.bool(true, title="Liquidity Voids", group="📊 نماذج / Patterns")
bool showBreakers  = input.bool(true, title="Breakers", group="📊 نماذج / Patterns")
bool showMitBlock  = input.bool(true, title="Mitigation Block", group="📊 نماذج / Patterns")
bool showDisp      = input.bool(true, title="Displacement", group="📊 نماذج / Patterns")
bool showCISD      = input.bool(true, title="CISD", group="📊 نماذج / Patterns")
bool showMeasGap   = input.bool(true, title="Measuring Gap", group="📊 نماذج / Patterns")
bool showLiq       = input.bool(true, title="السيولة / Liquidity", group="💧 سيولة / Liquidity")
bool showKZ        = input.bool(true, title="Kill Zones", group="⏰ وقت / Time")
bool showMacro     = input.bool(true, title="Macro Windows", group="⏰ وقت / Time")
bool showNWOG      = input.bool(true, title="NWOG / NDOG", group="⏰ وقت / Time")
bool showPD        = input.bool(true, title="Premium/Discount", group="📈 تحليل / Analysis")
bool showFib       = input.bool(true, title="فيبوناتشي / Fibonacci", group="📈 تحليل / Analysis")
bool showProtected = input.bool(true, title="Protected High/Low", group="📈 تحليل / Analysis")
bool showDash      = input.bool(true, title="الجدول / Dashboard", group="📋 جدول / Dashboard")
string dashPos     = input.string("top_right", title="موقع الجدول / Position", options=["top_right", "top_left", "bottom_right", "bottom_left"], group="📋 جدول / Dashboard")
bool fridayFilter  = input.bool(true, title="فلتر الجمعة / Friday Filter", group="🔍 فلاتر / Filters")

// ══════════════════════════════════════════════════════════════════════════════
// ██  الألوان / Colors
// ══════════════════════════════════════════════════════════════════════════════
color cBullFVG   = input.color(color.new(#00E676, 80), title="FVG صاعد", group="🎨 ألوان / Colors")
color cBearFVG   = input.color(color.new(#FF5252, 80), title="FVG هابط", group="🎨 ألوان / Colors")
color cBullOB    = input.color(color.new(#2196F3, 80), title="OB صاعد", group="🎨 ألوان / Colors")
color cBearOB    = input.color(color.new(#FF9800, 80), title="OB هابط", group="🎨 ألوان / Colors")
color cMSS       = input.color(color.new(#E040FB, 0), title="MSS", group="🎨 ألوان / Colors")
color cBOS       = input.color(color.new(#00BCD4, 0), title="BOS", group="🎨 ألوان / Colors")
color cBPR       = input.color(color.new(#9C27B0, 80), title="BPR", group="🎨 ألوان / Colors")
color cVoid      = input.color(color.new(#FF6D00, 80), title="Void", group="🎨 ألوان / Colors")
color cBreaker   = input.color(color.new(#F50057, 80), title="Breaker", group="🎨 ألوان / Colors")
color cKZAsia    = input.color(color.new(#FFD600, 92), title="آسيا", group="🎨 ألوان / Colors")
color cKZLondon  = input.color(color.new(#2979FF, 92), title="لندن", group="🎨 ألوان / Colors")
color cKZNY      = input.color(color.new(#00E676, 92), title="نيويورك", group="🎨 ألوان / Colors")
color cKZLC      = input.color(color.new(#FF6D00, 92), title="لندن إغلاق", group="🎨 ألوان / Colors")

// ══════════════════════════════════════════════════════════════════════════════
// ██  دوال مساعدة / Helpers
// ══════════════════════════════════════════════════════════════════════════════
f_t(string ar, string en) => isArabic ? ar : en

float atrVal = ta.atr(14)

nyH(int t) => hour(t, "America/New_York")
nyM(int t) => minute(t, "America/New_York")
nyD(int t) => dayofweek(t, "America/New_York")

// ══════════════════════════════════════════════════════════════════════════════
// ██  1. Swing Detection
// ══════════════════════════════════════════════════════════════════════════════
float pivH = ta.pivothigh(high, swingLen, swingLen)
float pivL = ta.pivotlow(low, swingLen, swingLen)
bool isSH = not na(pivH)
bool isSL = not na(pivL)

var float lastSH = na
var float lastSL = na
var int lastSHBar = na
var int lastSLBar = na

if isSH
    lastSH := pivH
    lastSHBar := bar_index - swingLen
if isSL
    lastSL := pivL
    lastSLBar := bar_index - swingLen

// ══════════════════════════════════════════════════════════════════════════════
// ██  2. Trend Detection
// ══════════════════════════════════════════════════════════════════════════════
var int trend = 0
var float tSH = na
var float tSL = na

if isSH
    if not na(tSH) and pivH > tSH
        trend := 1
    tSH := pivH
if isSL
    if not na(tSL) and pivL < tSL
        trend := -1
    tSL := pivL

// ══════════════════════════════════════════════════════════════════════════════
// ██  3. Displacement Detection
// ══════════════════════════════════════════════════════════════════════════════
float bodySize = math.abs(close - open)
float upWick = high - math.max(close, open)
float dnWick = math.min(close, open) - low
bool isDisp = bodySize > (atrVal * dispThresh)
bool dispCandle = isDisp and bodySize > upWick * 2 and bodySize > dnWick * 2
string dispDir = close > open ? "bull" : "bear"

if dispCandle and showDisp
    color dc = dispDir == "bull" ? color.new(#00E676, 0) : color.new(#FF5252, 0)
    label.new(bar_index, dispDir == "bull" ? low : high, "⚡", color=color.new(color.white, 100), textcolor=dc, style=dispDir == "bull" ? label.style_label_up : label.style_label_down, size=size.tiny)

// ══════════════════════════════════════════════════════════════════════════════
// ██  4. MSS & BOS Detection
// ══════════════════════════════════════════════════════════════════════════════
var bool mssNow = false
var bool bosNow = false
var float mssLvl = na
var float bosLvl = na
var int mssBI = na
var int bosBI = na
var string mssD = na
var string bosD = na

bool bullBrk = not na(lastSH) and close > lastSH and close[1] <= lastSH
bool bearBrk = not na(lastSL) and close < lastSL and close[1] >= lastSL

mssNow := false
bosNow := false

if bullBrk
    if trend == -1 and isDisp
        mssNow := true
        mssLvl := lastSH
        mssBI := bar_index
        mssD := "bull"
        trend := 1
    else if trend == 1
        bosNow := true
        bosLvl := lastSH
        bosBI := bar_index
        bosD := "bull"

if bearBrk
    if trend == 1 and isDisp
        mssNow := true
        mssLvl := lastSL
        mssBI := bar_index
        mssD := "bear"
        trend := -1
    else if trend == -1
        bosNow := true
        bosLvl := lastSL
        bosBI := bar_index
        bosD := "bear"

if mssNow and showMSS
    line.new(mssBI - 10, mssLvl, mssBI, mssLvl, color=cMSS, width=3)
    label.new(mssBI, mssLvl, f_t("⚡ تحول", "⚡ MSS"), color=cMSS, textcolor=color.white, style=mssD == "bull" ? label.style_label_up : label.style_label_down, size=size.small)

if bosNow and showBOS
    line.new(bosBI - 10, bosLvl, bosBI, bosLvl, color=cBOS, width=2, style=line.style_dashed)
    label.new(bosBI, bosLvl, f_t("كسر", "BOS"), color=cBOS, textcolor=color.white, style=bosD == "bull" ? label.style_label_up : label.style_label_down, size=size.tiny)

// ══════════════════════════════════════════════════════════════════════════════
// ██  5. FVG Detection (BISI / SIBI)
// ══════════════════════════════════════════════════════════════════════════════
bool bullFVG = low > high[2] and close[1] > open[1]
bool bearFVG = high < low[2] and close[1] < open[1]

var float fvgBT = na
var float fvgBB = na
var float fvgST = na
var float fvgSB = na
var bool fvgBA = false
var bool fvgSA = false
var int fvgCnt = 0

if bullFVG and showFVG and fvgCnt < maxPat
    fvgBA := true
    fvgBT := low
    fvgBB := high[2]
    fvgCnt += 1
    box.new(bar_index - 2, low, bar_index + 10, high[2], bgcolor=cBullFVG, border_color=color.new(#00E676, 50))
    // CE line (50%)
    float ce = (low + high[2]) / 2
    line.new(bar_index - 2, ce, bar_index + 10, ce, color=color.new(#00E676, 60), style=line.style_dotted, width=1)
    label.new(bar_index - 1, ce, f_t("BISI", "BISI"), color=color.new(color.green, 90), textcolor=color.green, style=label.style_label_center, size=size.tiny)

if bearFVG and showFVG and fvgCnt < maxPat
    fvgSA := true
    fvgST := low[2]
    fvgSB := high
    fvgCnt += 1
    box.new(bar_index - 2, low[2], bar_index + 10, high, bgcolor=cBearFVG, border_color=color.new(#FF5252, 50))
    float ce = (low[2] + high) / 2
    line.new(bar_index - 2, ce, bar_index + 10, ce, color=color.new(#FF5252, 60), style=line.style_dotted, width=1)
    label.new(bar_index - 1, ce, f_t("SIBI", "SIBI"), color=color.new(color.red, 90), textcolor=color.red, style=label.style_label_center, size=size.tiny)

// ══════════════════════════════════════════════════════════════════════════════
// ██  6. Inversion FVG
// ══════════════════════════════════════════════════════════════════════════════
// عندما يتم كسر FVG كانت تدعم الشراء وتتحول لمقاومة (أو العكس)
bool invFVGBull = false
bool invFVGBear = false

if fvgBA and close < fvgBB and bodySize > atrVal * 0.5
    invFVGBear := true
    fvgBA := false
    if showInvFVG
        label.new(bar_index, high, f_t("انقلاب ↓", "Inv FVG ↓"), color=color.new(#FF1744, 0), textcolor=color.white, style=label.style_label_down, size=size.tiny)

if fvgSA and close > fvgST and bodySize > atrVal * 0.5
    invFVGBull := true
    fvgSA := false
    if showInvFVG
        label.new(bar_index, low, f_t("انقلاب ↑", "Inv FVG ↑"), color=color.new(#00E676, 0), textcolor=color.white, style=label.style_label_up, size=size.tiny)

// ══════════════════════════════════════════════════════════════════════════════
// ██  7. Order Blocks
// ══════════════════════════════════════════════════════════════════════════════
bool bullOB = close[1] < open[1] and close > open and close > high[1] and isDisp
bool bearOB = close[1] > open[1] and close < open and close < low[1] and isDisp
var int obCnt = 0

if bullOB and showOB and obCnt < maxPat
    obCnt += 1
    box.new(bar_index - 1, high[1], bar_index + 15, low[1], bgcolor=cBullOB, border_color=color.new(#2196F3, 50))
    // Mean Threshold (50%)
    float mt = (high[1] + low[1]) / 2
    line.new(bar_index - 1, mt, bar_index + 15, mt, color=color.new(#2196F3, 60), style=line.style_dotted)
    label.new(bar_index - 1, low[1], f_t("OB ↑", "OB ↑"), color=color.new(color.blue, 80), textcolor=color.blue, style=label.style_label_up, size=size.tiny)

if bearOB and showOB and obCnt < maxPat
    obCnt += 1
    box.new(bar_index - 1, high[1], bar_index + 15, low[1], bgcolor=cBearOB, border_color=color.new(#FF9800, 50))
    float mt = (high[1] + low[1]) / 2
    line.new(bar_index - 1, mt, bar_index + 15, mt, color=color.new(#FF9800, 60), style=line.style_dotted)
    label.new(bar_index - 1, high[1], f_t("OB ↓", "OB ↓"), color=color.new(color.orange, 80), textcolor=color.orange, style=label.style_label_down, size=size.tiny)

// ══════════════════════════════════════════════════════════════════════════════
// ██  8. Rejection Block
// ══════════════════════════════════════════════════════════════════════════════
bool bullRej = dnWick > bodySize * 2 and isSL and showRejBlock
bool bearRej = upWick > bodySize * 2 and isSH and showRejBlock
var int rejCnt = 0

if bullRej and rejCnt < maxPat
    rejCnt += 1
    box.new(bar_index, math.min(close, open), bar_index + 8, low, bgcolor=color.new(#00BFA5, 85), border_color=color.new(#00BFA5, 50))
    label.new(bar_index, low, f_t("رفض ↑", "Rej ↑"), color=color.new(#00BFA5, 80), textcolor=#00BFA5, style=label.style_label_up, size=size.tiny)

if bearRej and rejCnt < maxPat
    rejCnt += 1
    box.new(bar_index, high, bar_index + 8, math.max(close, open), bgcolor=color.new(#D50000, 85), border_color=color.new(#D50000, 50))
    label.new(bar_index, high, f_t("رفض ↓", "Rej ↓"), color=color.new(#D50000, 80), textcolor=#D50000, style=label.style_label_down, size=size.tiny)

// ══════════════════════════════════════════════════════════════════════════════
// ██  9. BPR (Balanced Price Range)
// ══════════════════════════════════════════════════════════════════════════════
bool bprNow = false
float bprT = na
float bprB = na

if bullFVG and bearFVG[1] and showBPR
    float oT = math.min(low, low[3])
    float oB = math.max(high[2], high[1])
    if oT > oB
        bprNow := true
        bprT := oT
        bprB := oB
        box.new(bar_index - 2, oT, bar_index + 10, oB, bgcolor=cBPR, border_color=color.new(#9C27B0, 50), border_width=2)
        label.new(bar_index - 1, (oT + oB) / 2, "BPR", color=color.new(#9C27B0, 80), textcolor=#9C27B0, style=label.style_label_center, size=size.small)

// ══════════════════════════════════════════════════════════════════════════════
// ██  10. Liquidity Voids
// ══════════════════════════════════════════════════════════════════════════════
bool bullVoid = low > high[1] and (low - high[1]) > atrVal * 2
bool bearVoid = high < low[1] and (low[1] - high) > atrVal * 2
var int vdCnt = 0

if bullVoid and showVoids and vdCnt < maxPat
    vdCnt += 1
    box.new(bar_index - 1, low, bar_index + 10, high[1], bgcolor=cVoid, border_color=color.new(#FF6D00, 50), border_style=line.style_dotted)
    label.new(bar_index, (low + high[1]) / 2, f_t("فراغ", "Void"), color=color.new(#FF6D00, 80), textcolor=#FF6D00, style=label.style_label_center, size=size.tiny)

if bearVoid and showVoids and vdCnt < maxPat
    vdCnt += 1
    box.new(bar_index - 1, low[1], bar_index + 10, high, bgcolor=cVoid, border_color=color.new(#FF6D00, 50), border_style=line.style_dotted)
    label.new(bar_index, (low[1] + high) / 2, f_t("فراغ", "Void"), color=color.new(#FF6D00, 80), textcolor=#FF6D00, style=label.style_label_center, size=size.tiny)

// ══════════════════════════════════════════════════════════════════════════════
// ██  11. Breakers
// ══════════════════════════════════════════════════════════════════════════════
bool bullBrker = bullOB[1] and close < low[2] and isDisp
bool bearBrker = bearOB[1] and close > high[2] and isDisp
var int brkCnt = 0

if bullBrker and showBreakers and brkCnt < maxPat
    brkCnt += 1
    box.new(bar_index - 2, high[2], bar_index + 10, low[2], bgcolor=cBreaker, border_color=color.new(#F50057, 50))
    label.new(bar_index - 1, (high[2] + low[2]) / 2, f_t("كسارة ↓", "Brk ↓"), color=color.new(#F50057, 80), textcolor=#F50057, style=label.style_label_center, size=size.tiny)

if bearBrker and showBreakers and brkCnt < maxPat
    brkCnt += 1
    box.new(bar_index - 2, high[2], bar_index + 10, low[2], bgcolor=cBreaker, border_color=color.new(#F50057, 50))
    label.new(bar_index - 1, (high[2] + low[2]) / 2, f_t("كسارة ↑", "Brk ↑"), color=color.new(#F50057, 80), textcolor=#F50057, style=label.style_label_center, size=size.tiny)

// ══════════════════════════════════════════════════════════════════════════════
// ██  12. Mitigation Block
// ══════════════════════════════════════════════════════════════════════════════
// OB تم لمسه جزئياً ثم ارتد السعر منه
bool mitBull = bullOB[2] and low[1] <= (high[3] + low[3]) / 2 and close > close[1] and close > open
bool mitBear = bearOB[2] and high[1] >= (high[3] + low[3]) / 2 and close < close[1] and close < open

if mitBull and showMitBlock
    label.new(bar_index, low, f_t("تخفيف ↑", "Mit ↑"), color=color.new(#7C4DFF, 0), textcolor=color.white, style=label.style_label_up, size=size.tiny)

if mitBear and showMitBlock
    label.new(bar_index, high, f_t("تخفيف ↓", "Mit ↓"), color=color.new(#7C4DFF, 0), textcolor=color.white, style=label.style_label_down, size=size.tiny)

// ══════════════════════════════════════════════════════════════════════════════
// ██  13. CISD (Change in State of Delivery)
// ══════════════════════════════════════════════════════════════════════════════
var bool cisdNow = false
cisdNow := false

if trend == 1 and fvgBA and close < fvgBB and bodySize > atrVal * 0.5
    cisdNow := true
    if showCISD
        label.new(bar_index, high, f_t("⚠ CISD", "⚠ CISD"), color=color.new(#FFD600, 0), textcolor=color.black, style=label.style_label_down, size=size.small)

if trend == -1 and fvgSA and close > fvgST and bodySize > atrVal * 0.5
    cisdNow := true
    if showCISD
        label.new(bar_index, low, f_t("⚠ CISD", "⚠ CISD"), color=color.new(#FFD600, 0), textcolor=color.black, style=label.style_label_up, size=size.small)

// ══════════════════════════════════════════════════════════════════════════════
// ██  14. Measuring Gap (فجوة القياس)
// ══════════════════════════════════════════════════════════════════════════════
// فجوة لا يتم لمسها وتدل على قوة الاتجاه
bool measGapBull = bullFVG and bosNow and bosD == "bull"
bool measGapBear = bearFVG and bosNow and bosD == "bear"

if measGapBull and showMeasGap
    label.new(bar_index - 1, (low + high[2]) / 2, f_t("قياس", "Meas"), color=color.new(#00E5FF, 0), textcolor=color.white, style=label.style_label_center, size=size.tiny)

if measGapBear and showMeasGap
    label.new(bar_index - 1, (low[2] + high) / 2, f_t("قياس", "Meas"), color=color.new(#00E5FF, 0), textcolor=color.white, style=label.style_label_center, size=size.tiny)

// ══════════════════════════════════════════════════════════════════════════════
// ██  15. Liquidity Models
// ══════════════════════════════════════════════════════════════════════════════

// ── Equal Highs / Equal Lows ──
float eqTh = atrVal * 0.1
bool eqH = math.abs(high - high[1]) < eqTh and math.abs(high - high[2]) < eqTh
bool eqL = math.abs(low - low[1]) < eqTh and math.abs(low - low[2]) < eqTh

if eqH and showLiq
    line.new(bar_index - 2, high, bar_index + 5, high, color=color.new(#FF5252, 30), width=2, style=line.style_dotted)
    label.new(bar_index, high, f_t("EQH 🎯", "EQH 🎯"), color=color.new(color.red, 90), textcolor=color.red, style=label.style_label_down, size=size.tiny)

if eqL and showLiq
    line.new(bar_index - 2, low, bar_index + 5, low, color=color.new(#00E676, 30), width=2, style=line.style_dotted)
    label.new(bar_index, low, f_t("EQL 🎯", "EQL 🎯"), color=color.new(color.green, 90), textcolor=color.green, style=label.style_label_up, size=size.tiny)

// ── BSL / SSL ──
bool bslSw = not na(lastSH) and high > lastSH and close < lastSH
bool sslSw = not na(lastSL) and low < lastSL and close > lastSL

if bslSw and showLiq
    label.new(bar_index, high, f_t("BSL ✗", "BSL ✗"), color=color.new(color.red, 0), textcolor=color.white, style=label.style_label_down, size=size.small)

if sslSw and showLiq
    label.new(bar_index, low, f_t("SSL ✗", "SSL ✗"), color=color.new(color.green, 0), textcolor=color.white, style=label.style_label_up, size=size.small)

// ── Stop Run ──
bool srH = high > ta.highest(high, 20)[1] and close < open and close < high[1]
bool srL = low < ta.lowest(low, 20)[1] and close > open and close > low[1]

if srH and showLiq
    label.new(bar_index, high, f_t("🛑 ستوب", "🛑 Stop"), color=color.new(#D50000, 0), textcolor=color.white, style=label.style_label_down, size=size.small)

if srL and showLiq
    label.new(bar_index, low, f_t("🛑 ستوب", "🛑 Stop"), color=color.new(#00C853, 0), textcolor=color.white, style=label.style_label_up, size=size.small)

// ── Inducement ──
bool idmH = not na(pivH) and high[1] > pivH and close[1] < pivH and close < close[1]
bool idmL = not na(pivL) and low[1] < pivL and close[1] > pivL and close > close[1]

if idmH and showLiq
    label.new(bar_index - 1, high[1], "IDM", color=color.new(#FF6D00, 0), textcolor=color.white, style=label.style_label_down, size=size.tiny)

if idmL and showLiq
    label.new(bar_index - 1, low[1], "IDM", color=color.new(#FF6D00, 0), textcolor=color.white, style=label.style_label_up, size=size.tiny)

// ── Judas Swing ──
int curH = nyH(time)
int curM = nyM(time)
bool isLO = curH >= 2 and curH < 5
bool judasBull = isLO and low < ta.lowest(low, 10)[1] and close > open and isDisp
bool judasBear = isLO and high > ta.highest(high, 10)[1] and close < open and isDisp

if judasBull and showLiq
    label.new(bar_index, low, f_t("يهوذا ↑", "Judas ↑"), color=color.new(#00E676, 0), textcolor=color.white, style=label.style_label_up, size=size.small)

if judasBear and showLiq
    label.new(bar_index, high, f_t("يهوذا ↓", "Judas ↓"), color=color.new(#FF5252, 0), textcolor=color.white, style=label.style_label_down, size=size.small)

// ── Liquidity Sweep ──
bool swpH = high > high[1] and high > high[2] and close < high[1] and close < open
bool swpL = low < low[1] and low < low[2] and close > low[1] and close > open

if swpH and showLiq
    label.new(bar_index, high, f_t("سحب ↓", "Sweep ↓"), color=color.new(#FF1744, 80), textcolor=#FF1744, style=label.style_label_down, size=size.tiny)

if swpL and showLiq
    label.new(bar_index, low, f_t("سحب ↑", "Sweep ↑"), color=color.new(#00E676, 80), textcolor=#00E676, style=label.style_label_up, size=size.tiny)

// ══════════════════════════════════════════════════════════════════════════════
// ██  16. Kill Zones & Macro Windows
// ══════════════════════════════════════════════════════════════════════════════
bool inAsia   = curH >= 20 or curH < 0
bool inLondon = curH >= 2 and curH < 5
bool inNY     = (curH == 9 and curM >= 30) or (curH >= 10 and curH < 12)
bool inLC     = curH >= 15 and curH < 17

// Macro Windows
bool mac1 = (curH == 9 and curM >= 50) or (curH == 10 and curM <= 10)
bool mac2 = (curH == 11 and curM >= 50) or (curH == 12 and curM <= 10)
bool mac3 = (curH == 13 and curM >= 50) or (curH == 14 and curM <= 10)

bgcolor(showKZ and inAsia ? cKZAsia : na, title="Asia KZ")
bgcolor(showKZ and inLondon ? cKZLondon : na, title="London KZ")
bgcolor(showKZ and inNY ? cKZNY : na, title="NY KZ")
bgcolor(showKZ and inLC ? cKZLC : na, title="LC KZ")
bgcolor(showMacro and mac1 ? color.new(#E040FB, 93) : na, title="Macro 1")
bgcolor(showMacro and mac2 ? color.new(#E040FB, 93) : na, title="Macro 2")
bgcolor(showMacro and mac3 ? color.new(#E040FB, 93) : na, title="Macro 3")

// ══════════════════════════════════════════════════════════════════════════════
// ██  17. NWOG / NDOG (New Week/Day Opening Gap)
// ══════════════════════════════════════════════════════════════════════════════
var float ndogHigh = na
var float ndogLow = na
var float nwogHigh = na
var float nwogLow = na
var int prevDayBar = na

bool newDay = ta.change(time("D")) != 0
bool newWeek = ta.change(time("W")) != 0

if newDay and showNWOG
    ndogHigh := open
    ndogLow := close[1]
    if ndogHigh < ndogLow
        float tmp = ndogHigh
        ndogHigh := ndogLow
        ndogLow := tmp
    line.new(bar_index, ndogHigh, bar_index + 20, ndogHigh, color=color.new(#00BCD4, 50), style=line.style_dotted, width=1)
    line.new(bar_index, ndogLow, bar_index + 20, ndogLow, color=color.new(#00BCD4, 50), style=line.style_dotted, width=1)
    label.new(bar_index, (ndogHigh + ndogLow) / 2, "NDOG", color=color.new(#00BCD4, 80), textcolor=#00BCD4, style=label.style_label_center, size=size.tiny)

if newWeek and showNWOG
    nwogHigh := open
    nwogLow := close[1]
    if nwogHigh < nwogLow
        float tmp2 = nwogHigh
        nwogHigh := nwogLow
        nwogLow := tmp2
    line.new(bar_index, nwogHigh, bar_index + 50, nwogHigh, color=color.new(#FFD600, 40), style=line.style_dashed, width=2)
    line.new(bar_index, nwogLow, bar_index + 50, nwogLow, color=color.new(#FFD600, 40), style=line.style_dashed, width=2)
    label.new(bar_index, (nwogHigh + nwogLow) / 2, "NWOG", color=color.new(#FFD600, 80), textcolor=#FFD600, style=label.style_label_center, size=size.small)

// ══════════════════════════════════════════════════════════════════════════════
// ██  18. Premium / Discount
// ══════════════════════════════════════════════════════════════════════════════
float rH = ta.highest(high, pdLookback)
float rL = ta.lowest(low, pdLookback)
float rEQ = (rH + rL) / 2
bool inPrem = close > rEQ
bool inDisc = close < rEQ

plot(showPD ? rEQ : na, title="Equilibrium", color=color.new(#FFD600, 50), linewidth=1, style=plot.style_stepline)

// ══════════════════════════════════════════════════════════════════════════════
// ██  19. Protected High / Low
// ══════════════════════════════════════════════════════════════════════════════
var float protH = na
var float protL = na

if trend == 1 and not na(lastSL)
    protL := lastSL
if trend == -1 and not na(lastSH)
    protH := lastSH

plot(showProtected and trend == 1 and not na(protL) ? protL : na, title="Protected Low", color=color.new(#00E676, 40), linewidth=2, style=plot.style_linebr)
plot(showProtected and trend == -1 and not na(protH) ? protH : na, title="Protected High", color=color.new(#FF5252, 40), linewidth=2, style=plot.style_linebr)

// ══════════════════════════════════════════════════════════════════════════════
// ██  20. Fibonacci Standard Deviations
// ══════════════════════════════════════════════════════════════════════════════
float fibR = rH - rL
float fib2   = trend == 1 ? rH + fibR * 2.0 : rL - fibR * 2.0
float fib2_5 = trend == 1 ? rH + fibR * 2.5 : rL - fibR * 2.5
float fib4   = trend == 1 ? rH + fibR * 4.0 : rL - fibR * 4.0

plot(showFib ? fib2 : na, title="Fib -2.0", color=color.new(#00BCD4, 60), linewidth=1, style=plot.style_cross)
plot(showFib ? fib2_5 : na, title="Fib -2.5", color=color.new(#7C4DFF, 60), linewidth=1, style=plot.style_cross)
plot(showFib ? fib4 : na, title="Fib -4.0", color=color.new(#FF5252, 60), linewidth=1, style=plot.style_cross)

// ══════════════════════════════════════════════════════════════════════════════
// ██  21. HRLR / LRLR
// ══════════════════════════════════════════════════════════════════════════════
int swCnt = 0
for i = 1 to 20
    if not na(ta.pivothigh(high, 2, 2)[i]) or not na(ta.pivotlow(low, 2, 2)[i])
        swCnt += 1

bool isHRLR = swCnt > 10
bool isLRLR = swCnt < 5

// ══════════════════════════════════════════════════════════════════════════════
// ██  22. Day Type & Filters
// ══════════════════════════════════════════════════════════════════════════════
int dow = nyD(time)
bool isFri = dow == dayofweek.friday
bool friAfternoon = isFri and curH >= 12
bool noTrade = fridayFilter and friAfternoon

var string dayType = na
bool lonLow = inLondon and low == ta.lowest(low, 20)
bool nyUp   = inNY and close > open and close > close[1]
bool revD   = (bslSw or sslSw) and mssNow
bool consD  = not mssNow and not bosNow and not bslSw and not sslSw

if lonLow and nyUp
    dayType := f_t("يوم شراء كلاسيكي", "Classic Buy Day")
else if revD
    dayType := f_t("يوم انعكاس", "Reversal Day")
else if consD
    dayType := f_t("يوم تذبذب", "Consolidation")
else
    dayType := f_t("يوم اتجاه", "Trend Day")

// Draw on Liquidity
var string dolTxt = na
if trend == 1
    dolTxt := eqH ? f_t("قمم متساوية (EQH)", "Equal Highs (EQH)") : f_t("قمة أسبوعية سابقة", "Prev Weekly High")
else if trend == -1
    dolTxt := eqL ? f_t("قيعان متساوية (EQL)", "Equal Lows (EQL)") : f_t("قاع أسبوعي سابق", "Prev Weekly Low")

// ══════════════════════════════════════════════════════════════════════════════
// ██  23. Dashboard Table (الجدول التفاعلي)
// ══════════════════════════════════════════════════════════════════════════════
var table dash = na

if showDash and barstate.islast
    string tPos = switch dashPos
        "top_right" => position.top_right
        "top_left" => position.top_left
        "bottom_right" => position.bottom_right
        "bottom_left" => position.bottom_left
        => position.top_right

    dash := table.new(tPos, 4, 32, bgcolor=color.new(#0D0D1A, 5), border_color=color.new(#333366, 0), border_width=1, frame_color=color.new(#1A1A2E, 0), frame_width=2)

    // Header
    table.cell(dash, 0, 0, f_t("الحبي - محلل ICT v2", "Al-Habibi ICT v2"), text_color=#00E5FF, text_size=size.normal, bgcolor=color.new(#0D0D1A, 0), text_halign=text.align_center)
    table.merge_cells(dash, 0, 0, 3, 0)

    // Column headers
    color hdrBg = color.new(#16213E, 0)
    table.cell(dash, 0, 1, f_t("النموذج", "Pattern"), text_color=color.white, text_size=size.small, bgcolor=hdrBg)
    table.cell(dash, 1, 1, f_t("الحالة", "Status"), text_color=color.white, text_size=size.small, bgcolor=hdrBg)
    table.cell(dash, 2, 1, f_t("الاتجاه", "Dir"), text_color=color.white, text_size=size.small, bgcolor=hdrBg)
    table.cell(dash, 3, 1, f_t("القيمة", "Value"), text_color=color.white, text_size=size.small, bgcolor=hdrBg)

    // Helper colors
    color bg1 = color.new(#0D0D1A, 0)
    color bg2 = color.new(#16213E, 0)

    // ── Row 2: Trend ──
    string trTxt = trend == 1 ? f_t("صاعد ↑", "Bullish ↑") : trend == -1 ? f_t("هابط ↓", "Bearish ↓") : f_t("محايد", "Neutral")
    color trC = trend == 1 ? color.green : trend == -1 ? color.red : color.gray
    table.cell(dash, 0, 2, f_t("الاتجاه المؤسساتي", "Inst. Trend"), text_color=color.white, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 1, 2, "✓", text_color=trC, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 2, 2, trTxt, text_color=trC, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 3, 2, str.tostring(close, "#.####"), text_color=color.white, text_size=size.small, bgcolor=bg1)

    // ── Row 3: Premium/Discount ──
    string pdT = inPrem ? f_t("علاوة (بيع)", "Premium") : f_t("خصم (شراء)", "Discount")
    color pdC = inPrem ? color.red : color.green
    table.cell(dash, 0, 3, f_t("المنطقة", "Zone"), text_color=color.white, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 1, 3, "✓", text_color=pdC, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 2, 3, pdT, text_color=pdC, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 3, 3, str.tostring(rEQ, "#.####"), text_color=color.white, text_size=size.small, bgcolor=bg2)

    // ── Row 4: Day Type ──
    table.cell(dash, 0, 4, f_t("نوع اليوم", "Day Type"), text_color=color.white, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 1, 4, "✓", text_color=#FFD600, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 2, 4, dayType, text_color=#FFD600, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 3, 4, "", text_color=color.white, text_size=size.small, bgcolor=bg1)

    // ── Separator: Structure ──
    table.cell(dash, 0, 5, f_t("══ النماذج الهيكلية ══", "══ Structure ══"), text_color=#00E5FF, text_size=size.small, bgcolor=color.new(#1A1A2E, 0))
    table.merge_cells(dash, 0, 5, 3, 5)

    // Row 6: MSS
    table.cell(dash, 0, 6, "MSS", text_color=color.white, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 1, 6, mssNow ? "✓" : "✗", text_color=mssNow ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 2, 6, mssNow ? (mssD == "bull" ? "↑" : "↓") : "-", text_color=mssNow ? (mssD == "bull" ? color.green : color.red) : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 3, 6, mssNow ? str.tostring(mssLvl, "#.####") : "-", text_color=color.white, text_size=size.small, bgcolor=bg2)

    // Row 7: BOS
    table.cell(dash, 0, 7, "BOS", text_color=color.white, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 1, 7, bosNow ? "✓" : "✗", text_color=bosNow ? color.green : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 2, 7, bosNow ? (bosD == "bull" ? "↑" : "↓") : "-", text_color=bosNow ? (bosD == "bull" ? color.green : color.red) : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 3, 7, bosNow ? str.tostring(bosLvl, "#.####") : "-", text_color=color.white, text_size=size.small, bgcolor=bg1)

    // Row 8: FVG BISI
    table.cell(dash, 0, 8, "FVG (BISI)", text_color=color.white, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 1, 8, bullFVG ? "✓" : "✗", text_color=bullFVG ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 2, 8, bullFVG ? "↑" : "-", text_color=bullFVG ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 3, 8, bullFVG ? str.tostring(fvgBT, "#.####") : "-", text_color=color.white, text_size=size.small, bgcolor=bg2)

    // Row 9: FVG SIBI
    table.cell(dash, 0, 9, "FVG (SIBI)", text_color=color.white, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 1, 9, bearFVG ? "✓" : "✗", text_color=bearFVG ? color.green : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 2, 9, bearFVG ? "↓" : "-", text_color=bearFVG ? color.red : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 3, 9, bearFVG ? str.tostring(fvgSB, "#.####") : "-", text_color=color.white, text_size=size.small, bgcolor=bg1)

    // Row 10: Inversion FVG
    table.cell(dash, 0, 10, f_t("انقلاب FVG", "Inv FVG"), text_color=color.white, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 1, 10, invFVGBull or invFVGBear ? "✓" : "✗", text_color=invFVGBull or invFVGBear ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 2, 10, invFVGBull ? "↑" : invFVGBear ? "↓" : "-", text_color=invFVGBull ? color.green : invFVGBear ? color.red : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 3, 10, "-", text_color=color.white, text_size=size.small, bgcolor=bg2)

    // Row 11: OB
    table.cell(dash, 0, 11, "Order Block", text_color=color.white, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 1, 11, bullOB or bearOB ? "✓" : "✗", text_color=bullOB or bearOB ? color.green : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 2, 11, bullOB ? "↑" : bearOB ? "↓" : "-", text_color=bullOB ? color.green : bearOB ? color.red : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 3, 11, "-", text_color=color.white, text_size=size.small, bgcolor=bg1)

    // Row 12: BPR
    table.cell(dash, 0, 12, "BPR", text_color=color.white, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 1, 12, bprNow ? "✓" : "✗", text_color=bprNow ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 2, 12, bprNow ? "⬛" : "-", text_color=color.purple, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 3, 12, bprNow ? str.tostring(bprT, "#.####") : "-", text_color=color.white, text_size=size.small, bgcolor=bg2)

    // Row 13: Rejection Block
    table.cell(dash, 0, 13, f_t("كتلة الرفض", "Rej Block"), text_color=color.white, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 1, 13, bullRej or bearRej ? "✓" : "✗", text_color=bullRej or bearRej ? color.green : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 2, 13, bullRej ? "↑" : bearRej ? "↓" : "-", text_color=bullRej ? color.green : bearRej ? color.red : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 3, 13, "-", text_color=color.white, text_size=size.small, bgcolor=bg1)

    // Row 14: Mitigation Block
    table.cell(dash, 0, 14, f_t("تخفيف", "Mitigation"), text_color=color.white, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 1, 14, mitBull or mitBear ? "✓" : "✗", text_color=mitBull or mitBear ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 2, 14, mitBull ? "↑" : mitBear ? "↓" : "-", text_color=mitBull ? color.green : mitBear ? color.red : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 3, 14, "-", text_color=color.white, text_size=size.small, bgcolor=bg2)

    // ── Separator: Liquidity ──
    table.cell(dash, 0, 15, f_t("══ نماذج السيولة ══", "══ Liquidity ══"), text_color=#FF5252, text_size=size.small, bgcolor=color.new(#1A1A2E, 0))
    table.merge_cells(dash, 0, 15, 3, 15)

    // Row 16: Void
    table.cell(dash, 0, 16, f_t("فراغ سعري", "Void"), text_color=color.white, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 1, 16, bullVoid or bearVoid ? "✓" : "✗", text_color=bullVoid or bearVoid ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 2, 16, bullVoid ? "↑" : bearVoid ? "↓" : "-", text_color=bullVoid ? color.green : bearVoid ? color.red : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 3, 16, "-", text_color=color.white, text_size=size.small, bgcolor=bg2)

    // Row 17: Breaker
    table.cell(dash, 0, 17, f_t("كسارة", "Breaker"), text_color=color.white, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 1, 17, bullBrker or bearBrker ? "✓" : "✗", text_color=bullBrker or bearBrker ? color.green : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 2, 17, bullBrker ? "↓" : bearBrker ? "↑" : "-", text_color=bullBrker ? color.red : bearBrker ? color.green : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 3, 17, "-", text_color=color.white, text_size=size.small, bgcolor=bg1)

    // Row 18: Displacement
    table.cell(dash, 0, 18, f_t("اندفاع", "Displacement"), text_color=color.white, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 1, 18, dispCandle ? "✓" : "✗", text_color=dispCandle ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 2, 18, dispCandle ? (dispDir == "bull" ? "↑" : "↓") : "-", text_color=dispCandle ? (dispDir == "bull" ? color.green : color.red) : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 3, 18, dispCandle ? str.tostring(bodySize, "#.####") : "-", text_color=color.white, text_size=size.small, bgcolor=bg2)

    // Row 19: CISD
    table.cell(dash, 0, 19, "CISD", text_color=color.white, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 1, 19, cisdNow ? "✓" : "✗", text_color=cisdNow ? #FFD600 : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 2, 19, cisdNow ? "⚠" : "-", text_color=#FFD600, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 3, 19, "-", text_color=color.white, text_size=size.small, bgcolor=bg1)

    // Row 20: Measuring Gap
    table.cell(dash, 0, 20, f_t("فجوة قياس", "Meas Gap"), text_color=color.white, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 1, 20, measGapBull or measGapBear ? "✓" : "✗", text_color=measGapBull or measGapBear ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 2, 20, measGapBull ? "↑" : measGapBear ? "↓" : "-", text_color=measGapBull ? color.green : measGapBear ? color.red : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 3, 20, "-", text_color=color.white, text_size=size.small, bgcolor=bg2)

    // Row 21: EQH
    table.cell(dash, 0, 21, "EQH", text_color=color.white, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 1, 21, eqH ? "✓" : "✗", text_color=eqH ? color.green : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 2, 21, eqH ? "🎯" : "-", text_color=color.red, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 3, 21, eqH ? str.tostring(high, "#.####") : "-", text_color=color.white, text_size=size.small, bgcolor=bg1)

    // Row 22: EQL
    table.cell(dash, 0, 22, "EQL", text_color=color.white, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 1, 22, eqL ? "✓" : "✗", text_color=eqL ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 2, 22, eqL ? "🎯" : "-", text_color=color.green, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 3, 22, eqL ? str.tostring(low, "#.####") : "-", text_color=color.white, text_size=size.small, bgcolor=bg2)

    // Row 23: BSL/SSL
    table.cell(dash, 0, 23, "BSL/SSL", text_color=color.white, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 1, 23, bslSw or sslSw ? "✓" : "✗", text_color=bslSw or sslSw ? color.green : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 2, 23, bslSw ? "BSL" : sslSw ? "SSL" : "-", text_color=bslSw ? color.red : sslSw ? color.green : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 3, 23, "-", text_color=color.white, text_size=size.small, bgcolor=bg1)

    // Row 24: Stop Run
    table.cell(dash, 0, 24, f_t("ضرب ستوب", "Stop Run"), text_color=color.white, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 1, 24, srH or srL ? "✓" : "✗", text_color=srH or srL ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 2, 24, srH ? "↓" : srL ? "↑" : "-", text_color=srH ? color.red : srL ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 3, 24, "-", text_color=color.white, text_size=size.small, bgcolor=bg2)

    // Row 25: Judas
    table.cell(dash, 0, 25, f_t("مصيدة يهوذا", "Judas Swing"), text_color=color.white, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 1, 25, judasBull or judasBear ? "✓" : "✗", text_color=judasBull or judasBear ? color.green : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 2, 25, judasBull ? "↑" : judasBear ? "↓" : "-", text_color=judasBull ? color.green : judasBear ? color.red : color.gray, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 3, 25, "-", text_color=color.white, text_size=size.small, bgcolor=bg1)

    // Row 26: Inducement
    table.cell(dash, 0, 26, f_t("استدراج", "Inducement"), text_color=color.white, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 1, 26, idmH or idmL ? "✓" : "✗", text_color=idmH or idmL ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 2, 26, idmH ? "↓" : idmL ? "↑" : "-", text_color=idmH ? color.red : idmL ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 3, 26, "-", text_color=color.white, text_size=size.small, bgcolor=bg2)

    // ── Separator: Filters ──
    table.cell(dash, 0, 27, f_t("══ الفلاتر والمخاطر ══", "══ Filters & Risk ══"), text_color=#FFD600, text_size=size.small, bgcolor=color.new(#1A1A2E, 0))
    table.merge_cells(dash, 0, 27, 3, 27)

    // Row 28: HRLR/LRLR
    string lrT = isHRLR ? f_t("مقاومة عالية ⛔", "High Resist ⛔") : isLRLR ? f_t("مقاومة منخفضة ✅", "Low Resist ✅") : f_t("متوسط", "Medium")
    color lrC = isHRLR ? color.red : isLRLR ? color.green : color.gray
    table.cell(dash, 0, 28, "HRLR/LRLR", text_color=color.white, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 1, 28, "✓", text_color=lrC, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 2, 28, lrT, text_color=lrC, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 3, 28, str.tostring(swCnt), text_color=color.white, text_size=size.small, bgcolor=bg2)

    // Row 29: Friday
    table.cell(dash, 0, 29, f_t("فلتر الجمعة", "Friday"), text_color=color.white, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 1, 29, noTrade ? "⛔" : "✅", text_color=noTrade ? color.red : color.green, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 2, 29, noTrade ? f_t("لا تداول", "No Trade") : f_t("مسموح", "OK"), text_color=noTrade ? color.red : color.green, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 3, 29, "-", text_color=color.white, text_size=size.small, bgcolor=bg1)

    // Row 30: Protected Level
    string prTxt = trend == 1 ? f_t("قاع محمي", "Prot Low") : f_t("قمة محمية", "Prot High")
    float prVal = trend == 1 ? protL : protH
    table.cell(dash, 0, 30, prTxt, text_color=color.white, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 1, 30, not na(prVal) ? "✓" : "✗", text_color=not na(prVal) ? color.green : color.gray, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 2, 30, trend == 1 ? "SL ↓" : "SL ↑", text_color=trend == 1 ? color.green : color.red, text_size=size.small, bgcolor=bg2)
    table.cell(dash, 3, 30, not na(prVal) ? str.tostring(prVal, "#.####") : "-", text_color=color.white, text_size=size.small, bgcolor=bg2)

    // Row 31: Draw on Liquidity
    table.cell(dash, 0, 31, f_t("هدف السيولة", "Draw on Liq"), text_color=color.white, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 1, 31, "🎯", text_color=#00E5FF, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 2, 31, na(dolTxt) ? "-" : dolTxt, text_color=#00E5FF, text_size=size.small, bgcolor=bg1)
    table.cell(dash, 3, 31, "-", text_color=color.white, text_size=size.small, bgcolor=bg1)

// ══════════════════════════════════════════════════════════════════════════════
// ██  24. Alerts (تنبيهات)
// ══════════════════════════════════════════════════════════════════════════════
alertcondition(mssNow, title="MSS", message="⚡ الحبي: تحول هيكل السوق (MSS)")
alertcondition(bosNow, title="BOS", message="📊 الحبي: كسر هيكل (BOS)")
alertcondition(bullFVG or bearFVG, title="FVG", message="📐 الحبي: فجوة سعرية (FVG)")
alertcondition(invFVGBull or invFVGBear, title="Inversion FVG", message="🔄 الحبي: انقلاب FVG")
alertcondition(bullOB or bearOB, title="Order Block", message="🏛 الحبي: كتلة أوامر (OB)")
alertcondition(bprNow, title="BPR", message="⬛ الحبي: توازن سعري (BPR)")
alertcondition(bslSw or sslSw, title="BSL/SSL", message="💧 الحبي: سحب سيولة")
alertcondition(judasBull or judasBear, title="Judas Swing", message="🎭 الحبي: مصيدة يهوذا")
alertcondition(srH or srL, title="Stop Run", message="🛑 الحبي: ضرب ستوبات")
alertcondition(cisdNow, title="CISD", message="⚠ الحبي: تغير حالة التسليم (CISD)")
alertcondition(dispCandle, title="Displacement", message="⚡ الحبي: شمعة اندفاعية")
alertcondition(noTrade, title="No Trade Zone", message="⛔ الحبي: منطقة لا تداول")
alertcondition(bullBrker or bearBrker, title="Breaker", message="💥 الحبي: كسارة")
alertcondition(mitBull or mitBear, title="Mitigation", message="🔧 الحبي: تخفيف")
alertcondition(eqH, title="Equal Highs", message="🎯 الحبي: قمم متساوية")
alertcondition(eqL, title="Equal Lows", message="🎯 الحبي: قيعان متساوية")
