<!doctype html>
<html lang="ar" dir="rtl">
 <head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>منصة الحبي للتداول</title>
  <script src="https://cdn.tailwindcss.com/3.4.17"></script>
  <script src="https://cdn.jsdelivr.net/npm/lucide@0.263.0/dist/umd/lucide.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
  <style>
    html, body {
      width: 100%;
      height: 100%;
      margin: 0;
      padding: 0;
      overflow: hidden;
    }
    
    * { font-family: 'Noto Kufi Arabic', sans-serif; }
    
    .glow-green { box-shadow: 0 0 12px rgba(34, 197, 94, 0.3); }
    .glow-red { box-shadow: 0 0 12px rgba(239, 68, 68, 0.3); }
    
    @keyframes fadeIn { 
      from { opacity: 0; transform: translateY(8px); } 
      to { opacity: 1; transform: translateY(0); } 
    }
    .fade-in { animation: fadeIn 0.4s ease forwards; }
    
    @keyframes pulse-dot { 
      0%, 100% { opacity: 1; } 
      50% { opacity: 0.4; } 
    }
    .pulse-dot { animation: pulse-dot 1.5s infinite; }
    
    @keyframes slideDown { 
      from { opacity: 0; max-height: 0; } 
      to { opacity: 1; max-height: 500px; } 
    }
    .slide-down { animation: slideDown 0.3s ease forwards; }
    
    .progress-fill { transition: width 0.8s ease; }
    
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #1a1f2e; }
    ::-webkit-scrollbar-thumb { background: #374151; border-radius: 3px; }
    
    .card-hover { transition: all 0.2s ease; }
    .card-hover:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3); }
    
    .tab-active { border-bottom: 3px solid #3b82f6; color: #3b82f6; }
    
    #app-container {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
    }
  </style>
  <style>body { box-sizing: border-box; }</style>
  <script src="/_sdk/data_sdk.js" type="text/javascript"></script>
  <script src="/_sdk/element_sdk.js" type="text/javascript"></script>
 </head>
 <body class="bg-[#0d1117] text-gray-200">
  <div id="app-container" class="w-full h-full flex flex-col">
   <div id="app" class="w-full h-full flex flex-col" style="min-height:100%">
    <!-- Header -->
    <header class="bg-[#161b26] border-b border-gray-800 px-4 py-3 flex items-center justify-between flex-shrink-0">
     <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-white font-bold text-lg">
       ح
      </div>
      <div>
       <h1 id="platformName" class="text-lg font-bold text-white">منصة الحبي للتداول</h1>
       <p class="text-xs text-gray-500">تداول ذكي • تحليل متقدم</p>
      </div>
     </div>
     <div class="flex items-center gap-4">
      <div id="clockDisplay" class="text-sm font-mono text-gray-400"></div><button id="alertToggle" onclick="toggleAlerts()" class="relative p-2 rounded-lg bg-[#1e2536] hover:bg-[#2a3348] transition"> <i data-lucide="bell" style="width:20px;height:20px" class="text-gray-400"></i> <span id="alertBadge" class="hidden absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full text-[10px] text-white flex items-center justify-center">0</span> </button> <button onclick="toggleSound()" id="soundBtn" class="p-2 rounded-lg bg-[#1e2536] hover:bg-[#2a3348] transition"> <i data-lucide="volume-2" style="width:20px;height:20px" class="text-gray-400"></i> </button>
     </div>
    </header><!-- Market Tabs -->
    <div class="bg-[#161b26] border-b border-gray-800 px-4 flex gap-0 flex-shrink-0">
     <button onclick="switchMarket('saudi')" id="tabSaudi" class="px-5 py-3 text-sm font-semibold tab-active transition">🇸🇦 السوق السعودي</button> <button onclick="switchMarket('us')" id="tabUS" class="px-5 py-3 text-sm font-semibold text-gray-500 hover:text-gray-300 transition">🇺🇸 السوق الأمريكي</button>
    </div><!-- Market Status Bar -->
    <div id="marketStatusBar" class="flex-shrink-0 px-4 py-2 bg-[#0f1520] border-b border-gray-800 flex items-center justify-between">
     <div class="flex items-center gap-3">
      <span id="statusDot" class="w-3 h-3 rounded-full bg-green-500 pulse-dot inline-block"></span> <span id="statusText" class="text-sm font-semibold text-green-400">السوق مفتوح</span> <span id="marketTime" class="text-xs text-gray-500 mr-2"></span>
     </div>
     <div class="flex items-center gap-4 text-xs text-gray-500">
      <span>آخر تحديث: <span id="lastUpdate">--:--</span></span> <span>التحديث كل 5 دقائق</span>
      <div id="updateTimer" class="w-16 h-1.5 bg-gray-800 rounded-full overflow-hidden">
       <div id="timerBar" class="h-full bg-blue-500 rounded-full transition-all" style="width:100%"></div>
      </div>
     </div>
    </div><!-- Main Content -->
    <div class="flex-1 overflow-auto p-4">
     <!-- Search & Filter Bar -->
     <div class="flex flex-wrap gap-3 mb-4 fade-in">
      <div class="relative flex-1 min-w-[200px]">
       <i data-lucide="search" style="width:16px;height:16px" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500"></i> <input id="searchInput" oninput="filterTrades()" type="text" placeholder="بحث بالرمز أو الاسم..." class="w-full bg-[#1e2536] border border-gray-700 rounded-lg pr-10 pl-4 py-2.5 text-sm text-gray-200 placeholder-gray-600 focus:border-blue-500 focus:outline-none transition">
      </div><select id="filterStatus" onchange="filterTrades()" class="bg-[#1e2536] border border-gray-700 rounded-lg px-4 py-2.5 text-sm text-gray-300 focus:border-blue-500 focus:outline-none"> <option value="all">جميع الحالات</option> <option value="active">صفقات نشطة</option> <option value="waiting">صفقات منتظرة</option> <option value="closed">صفقات مغلقة</option> </select> <select id="filterStrength" onchange="filterTrades()" class="bg-[#1e2536] border border-gray-700 rounded-lg px-4 py-2.5 text-sm text-gray-300 focus:border-blue-500 focus:outline-none"> <option value="all">جميع القوة</option> <option value="3">قوة 3 ⭐⭐⭐</option> <option value="2">قوة 2 ⭐⭐</option> <option value="1">قوة 1 ⭐</option> </select> <select id="sortBy" onchange="filterTrades()" class="bg-[#1e2536] border border-gray-700 rounded-lg px-4 py-2.5 text-sm text-gray-300 focus:border-blue-500 focus:outline-none"> <option value="strength">ترتيب بالقوة</option> <option value="progress">ترتيب بالتقدم</option> <option value="name">ترتيب أبجدي</option> </select>
     </div><!-- Summary Cards -->
     <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
      <div class="bg-[#161b26] rounded-xl p-4 border border-gray-800 card-hover">
       <p class="text-xs text-gray-500 mb-1">إجمالي الصفقات</p>
       <p id="totalTrades" class="text-2xl font-bold text-white">0</p>
      </div>
      <div class="bg-[#161b26] rounded-xl p-4 border border-gray-800 card-hover">
       <p class="text-xs text-gray-500 mb-1">صفقات نشطة</p>
       <p id="activeTrades" class="text-2xl font-bold text-green-400">0</p>
      </div>
      <div class="bg-[#161b26] rounded-xl p-4 border border-gray-800 card-hover">
       <p class="text-xs text-gray-500 mb-1">صفقات منتظرة</p>
       <p id="waitingTrades" class="text-2xl font-bold text-yellow-400">0</p>
      </div>
      <div class="bg-[#161b26] rounded-xl p-4 border border-gray-800 card-hover">
       <p class="text-xs text-gray-500 mb-1">صفقات مغلقة</p>
       <p id="closedTrades" class="text-2xl font-bold text-gray-500">0</p>
      </div>
     </div><!-- Trades Grid -->
     <div id="tradesGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
     </div><!-- Empty State -->
     <div id="emptyState" class="hidden text-center py-16">
      <i data-lucide="inbox" style="width:48px;height:48px" class="text-gray-700 mx-auto mb-3"></i>
      <p class="text-gray-600 text-sm">لا توجد صفقات مطابقة للبحث</p>
     </div>
    </div><!-- Alerts Panel (hidden by default) -->
    <div id="alertsPanel" class="hidden fixed top-0 left-0 w-80 h-full bg-[#161b26] border-l border-gray-800 z-50 overflow-auto slide-down" style="box-shadow:-4px 0 20px rgba(0,0,0,0.4)">
     <div class="p-4 border-b border-gray-800 flex items-center justify-between">
      <h3 class="font-bold text-white">التنبيهات</h3><button onclick="toggleAlerts()" class="p-1 hover:bg-gray-800 rounded"><i data-lucide="x" style="width:18px;height:18px" class="text-gray-400"></i></button>
     </div>
     <div id="alertsList" class="p-3 space-y-2">
      <p class="text-gray-600 text-xs text-center py-8">لا توجد تنبيهات حالياً</p>
     </div>
    </div><!-- Footer -->
    <footer class="flex-shrink-0 bg-[#161b26] border-t border-gray-800 px-4 py-3 text-center">
     <p id="footerText" class="text-[11px] text-gray-600 leading-relaxed">جميع الحقوق محفوظة © 2025 منصة الحبي للتداول. هذه المنصة لأغراض تعليمية فقط ولا تتحمل أي التزامات مالية. جميع البيانات المعروضة تجريبية.</p>
    </footer>
   </div>
   <script>
// ===== CONFIG & SDK =====
const defaultConfig = {
  platform_name: 'منصة الحبي للتداول',
  footer_text: 'جميع الحقوق محفوظة © 2025 منصة الحبي للتداول. هذه المنصة لأغراض تعليمية فقط ولا تتحمل أي التزامات مالية.',
  background_color: '#0d1117',
  surface_color: '#161b26',
  text_color: '#e5e7eb',
  primary_color: '#3b82f6',
  accent_color: '#22d3ee',
  font_family: 'Noto Kufi Arabic',
  font_size: 14
};

function applyConfig(config) {
  const c = {...defaultConfig, ...config};
  document.getElementById('platformName').textContent = c.platform_name;
  document.getElementById('footerText').textContent = c.footer_text;
  
  document.body.style.backgroundColor = c.background_color;
  document.querySelectorAll('.bg-\\[\\#161b26\\]').forEach(el => el.style.backgroundColor = c.surface_color);
  
  const font = c.font_family + ', sans-serif';
  document.body.style.fontFamily = font;
  
  const base = c.font_size;
  document.getElementById('platformName').style.fontSize = (base * 1.3) + 'px';
}

if (window.elementSdk) {
  window.elementSdk.init({
    defaultConfig,
    onConfigChange: async (config) => applyConfig(config),
    mapToCapabilities: (config) => ({
      recolorables: [
        { get: () => config.background_color || defaultConfig.background_color, set: v => { config.background_color = v; window.elementSdk.setConfig({background_color:v}); }},
        { get: () => config.surface_color || defaultConfig.surface_color, set: v => { config.surface_color = v; window.elementSdk.setConfig({surface_color:v}); }},
        { get: () => config.text_color || defaultConfig.text_color, set: v => { config.text_color = v; window.elementSdk.setConfig({text_color:v}); }},
        { get: () => config.primary_color || defaultConfig.primary_color, set: v => { config.primary_color = v; window.elementSdk.setConfig({primary_color:v}); }},
        { get: () => config.accent_color || defaultConfig.accent_color, set: v => { config.accent_color = v; window.elementSdk.setConfig({accent_color:v}); }}
      ],
      borderables: [],
      fontEditable: {
        get: () => config.font_family || defaultConfig.font_family,
        set: v => { config.font_family = v; window.elementSdk.setConfig({font_family:v}); }
      },
      fontSizeable: {
        get: () => config.font_size || defaultConfig.font_size,
        set: v => { config.font_size = v; window.elementSdk.setConfig({font_size:v}); }
      }
    }),
    mapToEditPanelValues: (config) => new Map([
      ['platform_name', config.platform_name || defaultConfig.platform_name],
      ['footer_text', config.footer_text || defaultConfig.footer_text]
    ])
  });
}

// ===== MARKET DATA =====
let currentMarket = 'saudi';
let soundEnabled = true;
let alertsVisible = false;
let alerts = [];
let updateCountdown = 300; // 5 min in seconds

const saudiMarketHours = { open: 10, close: 15, tz: 'Asia/Riyadh' };
const usMarketHours = { open: 9.5, close: 16, tz: 'America/New_York' }; // 9:30 AM

const saudiTrades = [
  { symbol: '2222', name: 'أرامكو', status: 'active', strength: 3, entry: 28.50, stopLoss: 27.80, target1: 29.50, target2: 30.20, target3: 31.00, current: 29.10, sector: 'طاقة' },
  { symbol: '1120', name: 'الراجحي', status: 'active', strength: 3, entry: 95.00, stopLoss: 93.50, target1: 97.00, target2: 99.00, target3: 102.00, current: 96.20, sector: 'بنوك' },
  { symbol: '2010', name: 'سابك', status: 'waiting', strength: 2, entry: 78.00, stopLoss: 76.50, target1: 80.00, target2: 82.00, target3: 85.00, current: 77.40, waitReason: 'بانتظار كسر المقاومة عند 78.00' },
  { symbol: '7010', name: 'STC', status: 'active', strength: 2, entry: 42.00, stopLoss: 41.00, target1: 43.50, target2: 45.00, target3: 47.00, current: 43.10, sector: 'اتصالات' },
  { symbol: '4200', name: 'الدواء', status: 'waiting', strength: 1, entry: 55.00, stopLoss: 53.80, target1: 57.00, target2: 59.00, target3: 62.00, current: 54.20, waitReason: 'بانتظار ارتداد من الدعم 54.00' },
  { symbol: '1180', name: 'الأهلي', status: 'closed', strength: 2, entry: 38.00, stopLoss: 37.00, target1: 39.50, target2: 41.00, target3: 43.00, current: 39.50, sector: 'بنوك' },
];

const usTrades = [
  { symbol: 'AAPL', name: 'آبل', status: 'active', strength: 3, entry: 192.00, stopLoss: 188.00, target1: 198.00, target2: 205.00, target3: 212.00, current: 196.50, sector: 'تكنولوجيا' },
  { symbol: 'MSFT', name: 'مايكروسوفت', status: 'active', strength: 3, entry: 415.00, stopLoss: 408.00, target1: 425.00, target2: 435.00, target3: 450.00, current: 422.00, sector: 'تكنولوجيا' },
  { symbol: 'TSLA', name: 'تسلا', status: 'waiting', strength: 2, entry: 250.00, stopLoss: 242.00, target1: 260.00, target2: 275.00, target3: 290.00, current: 247.00, waitReason: 'بانتظار تأكيد الاتجاه الصاعد' },
  { symbol: 'NVDA', name: 'إنفيديا', status: 'active', strength: 3, entry: 880.00, stopLoss: 860.00, target1: 920.00, target2: 960.00, target3: 1000.00, current: 910.00, sector: 'تكنولوجيا' },
  { symbol: 'AMZN', name: 'أمازون', status: 'closed', strength: 2, entry: 178.00, stopLoss: 174.00, target1: 185.00, target2: 192.00, target3: 200.00, current: 185.00, sector: 'تجارة' },
];

function getTrades() { return currentMarket === 'saudi' ? saudiTrades : usTrades; }

function getMarketStatus() {
  const mkt = currentMarket === 'saudi' ? saudiMarketHours : usMarketHours;
  const now = new Date();
  const options = { timeZone: mkt.tz, hour: 'numeric', minute: 'numeric', hour12: false };
  const timeStr = now.toLocaleTimeString('en-US', options);
  const [h, m] = timeStr.split(':').map(Number);
  const hourDecimal = h + m / 60;
  
  const hoursToClose = mkt.close - hourDecimal;
  
  if (hourDecimal >= mkt.open && hourDecimal < mkt.close) {
    if (hoursToClose <= 1) return { status: 'closing', text: 'يغلق قريباً', color: 'orange', dotClass: 'bg-orange-500', textClass: 'text-orange-400' };
    return { status: 'open', text: 'السوق مفتوح', color: 'green', dotClass: 'bg-green-500', textClass: 'text-green-400' };
  }
  return { status: 'closed', text: 'السوق مغلق', color: 'red', dotClass: 'bg-red-500', textClass: 'text-red-400' };
}

function updateMarketStatus() {
  const ms = getMarketStatus();
  const dot = document.getElementById('statusDot');
  const txt = document.getElementById('statusText');
  dot.className = `w-3 h-3 rounded-full ${ms.dotClass} pulse-dot inline-block`;
  txt.className = `text-sm font-semibold ${ms.textClass}`;
  txt.textContent = ms.text;
  
  const mkt = currentMarket === 'saudi' ? saudiMarketHours : usMarketHours;
  const now = new Date();
  const timeStr = now.toLocaleTimeString('ar-SA', { timeZone: mkt.tz, hour: '2-digit', minute: '2-digit', second: '2-digit' });
  document.getElementById('marketTime').textContent = timeStr;
}

function updateClock() {
  const now = new Date();
  document.getElementById('clockDisplay').textContent = now.toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

// ===== AUDIO =====
let audioCtx;
function playAlert() {
  if (!soundEnabled) return;
  if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.frequency.value = 800;
  osc.type = 'sine';
  gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
  osc.start();
  osc.stop(audioCtx.currentTime + 0.5);
}

function toggleSound() {
  soundEnabled = !soundEnabled;
  const btn = document.getElementById('soundBtn');
  btn.innerHTML = soundEnabled
    ? '<i data-lucide="volume-2" style="width:20px;height:20px" class="text-gray-400"></i>'
    : '<i data-lucide="volume-x" style="width:20px;height:20px" class="text-red-400"></i>';
  lucide.createIcons();
}

function toggleAlerts() {
  alertsVisible = !alertsVisible;
  document.getElementById('alertsPanel').classList.toggle('hidden', !alertsVisible);
}

function addAlert(msg) {
  const time = new Date().toLocaleTimeString('ar-SA', {hour:'2-digit',minute:'2-digit'});
  alerts.unshift({ msg, time });
  if (alerts.length > 20) alerts.pop();
  const badge = document.getElementById('alertBadge');
  badge.classList.remove('hidden');
  badge.textContent = alerts.length;
  renderAlerts();
  playAlert();
}

function renderAlerts() {
  const list = document.getElementById('alertsList');
  if (alerts.length === 0) {
    list.innerHTML = '<p class="text-gray-600 text-xs text-center py-8">لا توجد تنبيهات حالياً</p>';
    return;
  }
  list.innerHTML = alerts.map(a => `
    <div class="bg-[#1e2536] rounded-lg p-3 border border-gray-800">
      <p class="text-xs text-gray-300">${a.msg}</p>
      <p class="text-[10px] text-gray-600 mt-1">${a.time}</p>
    </div>
  `).join('');
}

// ===== TRADES RENDERING =====
function getProgress(trade) {
  if (trade.status === 'waiting') return 0;
  const range = trade.target1 - trade.entry;
  if (range === 0) return 0;
  const prog = ((trade.current - trade.entry) / range) * 100;
  return Math.max(0, Math.min(100, prog));
}

function getStrengthStars(s) {
  return '⭐'.repeat(s) + '<span class="text-gray-700">' + '☆'.repeat(3-s) + '</span>';
}

function getPnL(trade) {
  const diff = trade.current - trade.entry;
  const pct = ((diff / trade.entry) * 100).toFixed(2);
  return { diff: diff.toFixed(2), pct, isPositive: diff >= 0 };
}

function renderTradeCard(trade) {
  const progress = getProgress(trade);
  const pnl = getPnL(trade);
  const statusColors = {
    active: { bg: 'border-green-900/40', badge: 'bg-green-900/60 text-green-300', label: 'نشط' },
    waiting: { bg: 'border-yellow-900/40', badge: 'bg-yellow-900/60 text-yellow-300', label: 'منتظر' },
    closed: { bg: 'border-gray-800', badge: 'bg-gray-800 text-gray-400', label: 'مغلق' }
  };
  const sc = statusColors[trade.status];

  return `
    <div class="bg-[#161b26] rounded-xl border ${sc.bg} card-hover fade-in overflow-hidden" data-symbol="${trade.symbol}">
      <div class="p-4">
        <!-- Header -->
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-2">
            <span class="text-base font-bold text-white">${trade.symbol}</span>
            <span class="text-xs text-gray-500">${trade.name}</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-[10px] px-2 py-0.5 rounded-full ${sc.badge}">${sc.label}</span>
            <span class="text-xs">${getStrengthStars(trade.strength)}</span>
          </div>
        </div>
        
        ${trade.status === 'active' ? `
        <!-- Progress to Target 1 -->
        <div class="mb-3">
          <div class="flex justify-between text-[10px] text-gray-500 mb-1">
            <span>التقدم نحو الهدف 1</span>
            <span class="font-bold ${progress >= 80 ? 'text-green-400' : 'text-blue-400'}">${progress.toFixed(0)}%</span>
          </div>
          <div class="w-full h-2 bg-gray-800 rounded-full overflow-hidden">
            <div class="h-full rounded-full progress-fill ${progress >= 80 ? 'bg-green-500' : progress >= 50 ? 'bg-blue-500' : 'bg-cyan-500'}" style="width:${progress}%"></div>
          </div>
        </div>
        <!-- PnL -->
        <div class="flex items-center gap-2 mb-3 p-2 rounded-lg ${pnl.isPositive ? 'bg-green-900/20' : 'bg-red-900/20'}">
          <i data-lucide="${pnl.isPositive ? 'trending-up' : 'trending-down'}" style="width:14px;height:14px" class="${pnl.isPositive ? 'text-green-400' : 'text-red-400'}"></i>
          <span class="text-sm font-bold ${pnl.isPositive ? 'text-green-400' : 'text-red-400'}">${pnl.isPositive ? '+' : ''}${pnl.pct}%</span>
          <span class="text-[10px] text-gray-500">السعر الحالي: ${trade.current}</span>
        </div>
        ` : ''}

        ${trade.status === 'waiting' ? `
        <div class="mb-3 p-2 rounded-lg bg-yellow-900/20 border border-yellow-900/30">
          <div class="flex items-center gap-1 mb-1">
            <i data-lucide="clock" style="width:12px;height:12px" class="text-yellow-400"></i>
            <span class="text-[10px] text-yellow-400 font-semibold">سبب الانتظار</span>
          </div>
          <p class="text-xs text-yellow-300/80">${trade.waitReason}</p>
        </div>
        ` : ''}

        <!-- Levels Grid -->
        <div class="grid grid-cols-2 gap-2 text-[11px]">
          <div class="bg-[#0d1117] rounded-lg p-2">
            <span class="text-gray-600 block">نقطة الدخول</span>
            <span class="text-white font-bold">${trade.entry}</span>
          </div>
          <div class="bg-[#0d1117] rounded-lg p-2">
            <span class="text-gray-600 block">وقف الخسارة</span>
            <span class="text-red-400 font-bold">${trade.stopLoss}</span>
          </div>
          <div class="bg-[#0d1117] rounded-lg p-2">
            <span class="text-gray-600 block">هدف 1</span>
            <span class="text-green-400 font-bold">${trade.target1}</span>
          </div>
          <div class="bg-[#0d1117] rounded-lg p-2">
            <span class="text-gray-600 block">هدف 2</span>
            <span class="text-green-400 font-bold">${trade.target2}</span>
          </div>
          <div class="bg-[#0d1117] rounded-lg p-2 col-span-2">
            <span class="text-gray-600 block">هدف 3</span>
            <span class="text-cyan-400 font-bold">${trade.target3}</span>
          </div>
        </div>
      </div>
    </div>
  `;
}

function renderTrades(trades) {
  const grid = document.getElementById('tradesGrid');
  const empty = document.getElementById('emptyState');
  
  if (trades.length === 0) {
    grid.innerHTML = '';
    empty.classList.remove('hidden');
    return;
  }
  empty.classList.add('hidden');
  grid.innerHTML = trades.map(renderTradeCard).join('');
  lucide.createIcons();
  
  // Update summary
  const all = getTrades();
  document.getElementById('totalTrades').textContent = all.length;
  document.getElementById('activeTrades').textContent = all.filter(t => t.status === 'active').length;
  document.getElementById('waitingTrades').textContent = all.filter(t => t.status === 'waiting').length;
  document.getElementById('closedTrades').textContent = all.filter(t => t.status === 'closed').length;
}

function filterTrades() {
  let trades = [...getTrades()];
  const search = document.getElementById('searchInput').value.toLowerCase();
  const status = document.getElementById('filterStatus').value;
  const strength = document.getElementById('filterStrength').value;
  const sort = document.getElementById('sortBy').value;

  if (search) trades = trades.filter(t => t.symbol.toLowerCase().includes(search) || t.name.includes(search));
  if (status !== 'all') trades = trades.filter(t => t.status === status);
  if (strength !== 'all') trades = trades.filter(t => t.strength === parseInt(strength));

  if (sort === 'strength') trades.sort((a, b) => b.strength - a.strength);
  else if (sort === 'progress') trades.sort((a, b) => getProgress(b) - getProgress(a));
  else if (sort === 'name') trades.sort((a, b) => a.name.localeCompare(b.name, 'ar'));

  renderTrades(trades);
}

function switchMarket(market) {
  currentMarket = market;
  document.getElementById('tabSaudi').className = market === 'saudi'
    ? 'px-5 py-3 text-sm font-semibold tab-active transition'
    : 'px-5 py-3 text-sm font-semibold text-gray-500 hover:text-gray-300 transition';
  document.getElementById('tabUS').className = market === 'us'
    ? 'px-5 py-3 text-sm font-semibold tab-active transition'
    : 'px-5 py-3 text-sm font-semibold text-gray-500 hover:text-gray-300 transition';
  
  document.getElementById('searchInput').value = '';
  document.getElementById('filterStatus').value = 'all';
  document.getElementById('filterStrength').value = 'all';
  updateMarketStatus();
  filterTrades();
}

// ===== SIMULATE PRICE UPDATES =====
function simulatePriceUpdate() {
  const trades = getTrades();
  trades.forEach(t => {
    if (t.status === 'closed') return;
    const volatility = t.current * 0.003;
    const change = (Math.random() - 0.45) * volatility; // slight upward bias
    t.current = parseFloat((t.current + change).toFixed(2));
    
    // Check if target1 hit
    if (t.status === 'active' && t.current >= t.target1) {
      addAlert(`🎯 ${t.symbol} ${t.name} وصل للهدف الأول!`);
    }
    // Check stop loss
    if (t.status === 'active' && t.current <= t.stopLoss) {
      addAlert(`🔴 ${t.symbol} ${t.name} وصل لوقف الخسارة!`);
    }
  });
  
  document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString('ar-SA', {hour:'2-digit',minute:'2-digit'});
  filterTrades();
}

// ===== TIMER =====
function updateTimer() {
  updateCountdown--;
  if (updateCountdown <= 0) {
    updateCountdown = 300;
    simulatePriceUpdate();
  }
  const pct = (updateCountdown / 300) * 100;
  document.getElementById('timerBar').style.width = pct + '%';
}

// ===== INIT =====
updateClock();
updateMarketStatus();
filterTrades();
lucide.createIcons();

setInterval(updateClock, 1000);
setInterval(updateMarketStatus, 5000);
setInterval(updateTimer, 1000);

// Initial price update after 10s for demo
setTimeout(simulatePriceUpdate, 10000);
</script>
  </div>
 <script>(function(){function c(){var b=a.contentDocument||a.contentWindow.document;if(b){var d=b.createElement('script');d.innerHTML="window.__CF$cv$params={r:'9ece9b13b40bb538',t:'MTc3NjI5NDQzOS4wMDAwMDA='};var a=document.createElement('script');a.nonce='';a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";b.getElementsByTagName('head')[0].appendChild(d)}}if(document.body){var a=document.createElement('iframe');a.height=1;a.width=1;a.style.position='absolute';a.style.top=0;a.style.left=0;a.style.border='none';a.style.visibility='hidden';document.body.appendChild(a);if('loading'!==document.readyState)c();else if(window.addEventListener)document.addEventListener('DOMContentLoaded',c);else{var e=document.onreadystatechange||function(){};document.onreadystatechange=function(b){e(b);'loading'!==document.readyState&&(document.onreadystatechange=e,c())}}}})();</script></body>
</html>
