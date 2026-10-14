"""
HTML5 / CSS / WebAudio веб-клиент для NoseClicker AI с поддержкой локализации (RU, EN, UK).
"""

WEB_UI_HTML = r"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>👃 NoseClicker AI</title>
  <style>
    :root {
      --bg: #0d1117;
      --card-bg: #161b22;
      --border: #30363d;
      --accent: #58a6ff;
      --accent-green: #3fb950;
      --accent-yellow: #d29922;
      --accent-red: #f85149;
      --accent-magenta: #bc8cff;
      --text: #c9d1d9;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; }
    body {
      background: var(--bg);
      color: var(--text);
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
      padding: 1.5rem 1rem;
    }
    header {
      text-align: center;
      margin-bottom: 1.5rem;
      width: 100%;
      max-width: 820px;
    }
    .lang-bar {
      display: flex;
      justify-content: center;
      gap: 0.5rem;
      margin-bottom: 0.9rem;
    }
    .lang-btn {
      flex: none;
      min-width: auto;
      padding: 0.35rem 0.85rem;
      font-size: 0.82rem;
      background: #21262d;
      color: #8b949e;
      border: 1px solid var(--border);
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .lang-btn:hover { background: #30363d; color: var(--text); }
    .lang-btn.active {
      background: var(--accent);
      color: #0d1117;
      font-weight: bold;
      border-color: var(--accent);
    }
    h1 {
      font-size: 1.8rem;
      color: var(--accent);
      margin-bottom: 0.3rem;
    }
    .badge {
      display: inline-block;
      font-size: 0.75rem;
      padding: 0.2rem 0.6rem;
      border-radius: 12px;
      background: rgba(88, 166, 255, 0.15);
      color: var(--accent);
      border: 1px solid var(--accent);
      margin-bottom: 0.5rem;
    }
    .subtitle {
      color: #8b949e;
      font-size: 0.9rem;
    }
    .container {
      width: 100%;
      max-width: 820px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.2rem;
    }
    @media (max-width: 720px) {
      .container { grid-template-columns: 1fr; }
    }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.2rem;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .card-title {
      font-weight: bold;
      font-size: 1rem;
      margin-bottom: 0.8rem;
      align-self: flex-start;
      color: var(--accent-green);
    }
    pre#nose-art {
      font-family: 'Courier New', Courier, monospace;
      font-size: 0.95rem;
      line-height: 1.25;
      color: #79c0ff;
      background: #090d13;
      padding: 1rem;
      border-radius: 6px;
      border: 1px solid #21262d;
      white-space: pre;
      user-select: none;
      transition: transform 0.08s ease, color 0.1s ease;
      text-align: center;
      width: 100%;
    }
    pre#nose-art.snapped {
      transform: scale(1.04);
      color: #ff7b72;
    }
    .btn-group {
      display: flex;
      gap: 0.6rem;
      margin-top: 1rem;
      width: 100%;
      flex-wrap: wrap;
    }
    button.action-btn {
      flex: 1;
      min-width: 120px;
      padding: 0.8rem 1rem;
      border-radius: 6px;
      border: none;
      cursor: pointer;
      font-weight: bold;
      font-size: 0.92rem;
      transition: transform 0.05s ease, opacity 0.15s ease;
      user-select: none;
    }
    button.action-btn:active { transform: scale(0.96); }
    .btn-main { background: var(--accent-green); color: #04260d; }
    .btn-sub { background: #21262d; color: var(--text); border: 1px solid var(--border); }
    .btn-sub:hover { background: #30363d; }
    .btn-ai { background: var(--accent-magenta); color: #1f0b35; }
    .stat-row {
      display: flex;
      justify-content: space-between;
      width: 100%;
      padding: 0.45rem 0;
      border-bottom: 1px solid #21262d;
      font-size: 0.9rem;
    }
    .stat-label { color: #8b949e; }
    .stat-val { font-weight: bold; }
    .progress-bar {
      width: 100%;
      height: 10px;
      background: #21262d;
      border-radius: 5px;
      overflow: hidden;
      margin-top: 4px;
    }
    .progress-fill {
      height: 100%;
      transition: width 0.2s ease;
    }
    .log-box {
      grid-column: 1 / -1;
      background: #090d13;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 0.8rem;
      font-family: monospace;
      font-size: 0.82rem;
      max-height: 160px;
      overflow-y: auto;
      display: flex;
      flex-direction: column-reverse;
      gap: 0.3rem;
    }
    .log-entry { color: #8b949e; }
    .log-token { color: var(--accent-green); }
    .log-thought { color: var(--accent); font-style: italic; }
    .copy-banner {
      margin-top: 1.2rem;
      font-size: 0.85rem;
      color: #8b949e;
      text-align: center;
    }
    code {
      background: #161b22;
      padding: 0.2rem 0.4rem;
      border-radius: 4px;
      border: 1px solid var(--border);
      color: var(--accent-yellow);
    }
    .achievements-card {
      grid-column: 1 / -1;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.2rem;
    }
    .achievements-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 0.75rem;
      margin-top: 0.8rem;
    }
    .ach-item {
      background: #090d13;
      border: 1px solid #21262d;
      border-radius: 6px;
      padding: 0.6rem 0.8rem;
      display: flex;
      flex-direction: column;
      gap: 0.2rem;
      transition: all 0.2s ease;
    }
    .ach-item.unlocked {
      border-color: #2ea043;
      background: rgba(46, 160, 67, 0.08);
    }
    .ach-header {
      display: flex;
      align-items: center;
      gap: 0.4rem;
      font-size: 0.85rem;
      font-weight: bold;
    }
    .ach-desc {
      font-size: 0.75rem;
      color: #8b949e;
      line-height: 1.25;
    }
    .ach-date {
      font-size: 0.7rem;
      color: var(--accent);
      margin-top: 2px;
    }
    .toast-banner {
      position: fixed;
      top: 20px;
      right: 20px;
      background: #238636;
      color: #fff;
      padding: 0.8rem 1.2rem;
      border-radius: 8px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
      font-weight: bold;
      z-index: 9999;
      display: none;
      animation: slideIn 0.3s ease;
    }
    @keyframes slideIn {
      from { transform: translateY(-20px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
  </style>
</head>
<body>

  <div id="toast" class="toast-banner"></div>

  <header>
    <div class="lang-bar">
      <button class="lang-btn active" id="btn-lang-uk" onclick="setLang('uk')">🇺🇦 Українська</button>
      <button class="lang-btn" id="btn-lang-en" onclick="setLang('en')">🇬🇧 English</button>
      <button class="lang-btn" id="btn-lang-ru" onclick="setLang('ru')">🇷🇺 Русский</button>
    </div>
    <div class="badge" id="lbl-badge">🚀 Стартап Року @ Product Hunt</div>
    <h1>👃 NoseClicker AI</h1>
    <div class="subtitle" id="lbl-subtitle">Перша нейромережа з тактильною віддачею та симулятором хрящів</div>
  </header>

  <div class="container">
    <!-- Nose Art Canvas Card -->
    <div class="card">
      <div class="card-title" id="lbl-card-model">Анатомічна Модель Хрящів</div>
      <pre id="nose-art">
       .──────────────────.
      /      ________      \
     │      /        \      │
     │     │  │    │  │     │
     │     │  │    │  │     │
    /      │  │    │  │      \
   │      ┌┴──┴────┴──┴┐      │
   │   (  │   (•)  (•) │  )   │
    \__ \_└───┬────┬───┘_/ __/
       \______/    \______/
          ▲            ▲
     Ліва ніздря  Права ніздря
      </pre>

      <div class="btn-group">
        <button class="action-btn btn-main" id="btn-both" onclick="crack('both')">💥 Зрушити хрящ (Space)</button>
      </div>
      <div class="btn-group">
        <button class="action-btn btn-sub" id="btn-left" onclick="crack('left')">👈 Лівий хрящ</button>
        <button class="action-btn btn-sub" id="btn-right" onclick="crack('right')">Правий хрящ 👉</button>
        <button class="action-btn btn-ai" id="btn-ai" onclick="toggleAI()">🤖 AI Авто-хрускіт</button>
      </div>
    </div>

    <!-- Stats Card -->
    <div class="card">
      <div class="card-title" id="lbl-card-telemetry" style="color: var(--accent-yellow);">Телеметрія & Токеноміка</div>
      
      <div class="stat-row">
        <span class="stat-label" id="lbl-clicks">Всього клацань:</span>
        <span class="stat-val" id="val-clicks" style="color: var(--accent-yellow);">0</span>
      </div>

      <div class="stat-row">
        <span class="stat-label" id="lbl-tokens">Токени задоволення:</span>
        <span class="stat-val" id="val-tokens" style="color: var(--accent-green);">💎 0.0 PLEASURE</span>
      </div>

      <div style="width: 100%; margin: 0.5rem 0;">
        <div style="display:flex; justify-content:space-between; font-size: 0.85rem;">
          <span class="stat-label" id="lbl-stress">Рівень стресу:</span>
          <span class="stat-val" id="val-stress" style="color: var(--accent-red);">85%</span>
        </div>
        <div class="progress-bar">
          <div id="bar-stress" class="progress-fill" style="width: 85%; background: var(--accent-red);"></div>
        </div>
      </div>

      <div style="width: 100%; margin: 0.5rem 0;">
        <div style="display:flex; justify-content:space-between; font-size: 0.85rem;">
          <span class="stat-label" id="lbl-dopamine">AI Дофамін ваг:</span>
          <span class="stat-val" id="val-dopamine" style="color: var(--accent-magenta);">62%</span>
        </div>
        <div class="progress-bar">
          <div id="bar-dopamine" class="progress-fill" style="width: 62%; background: var(--accent-magenta);"></div>
        </div>
      </div>

      <div class="stat-row">
        <span class="stat-label" id="lbl-cartilage">Стан хряща:</span>
        <span class="stat-val" id="val-cartilage">Еластичний</span>
      </div>

      <div class="stat-row">
        <span class="stat-label" id="lbl-cps">Швидкість хрускоту:</span>
        <span class="stat-val" id="val-cps">0.0 CPS</span>
      </div>

      <div class="stat-row">
        <span class="stat-label" id="lbl-power">Навантаження датацентру:</span>
        <span class="stat-val" id="val-power" style="color: var(--accent);">⚡ 1.21 GW</span>
      </div>

      <div class="stat-row">
        <span class="stat-label" id="lbl-ach">Досягнення:</span>
        <span class="stat-val" id="val-ach" style="color: var(--accent-yellow);">🏆 0 / 26 (0%)</span>
      </div>
    </div>

    <!-- Live Event Log -->
    <div class="log-box" id="log-feed">
      <div class="log-entry">[SYSTEM] NoseClicker AI Web Client ready</div>
    </div>

    <!-- Achievements Section -->
    <div class="achievements-card" id="achievements-section">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div class="card-title" id="lbl-card-hall" style="margin-bottom:0; color: var(--accent-yellow);">
          🏆 Зала Слави Досягнень <span id="ach-count-badge" style="font-size: 0.85rem; color: #8b949e;">(0/26)</span>
        </div>
        <button class="action-btn btn-sub" style="flex:none; min-width:auto; padding: 0.35rem 0.8rem; font-size:0.8rem;" onclick="toggleAchVisibility()" id="btn-toggle-ach">Сховати / Показати</button>
      </div>
      <div class="achievements-grid" id="achievements-grid"></div>
    </div>
  </div>

  <div class="copy-banner" id="lbl-copy-banner">
    Поделиться с другом: отправь ссылку в браузере или команду: <code>curl -X POST http://&lt;IP&gt;:8088/api/v1/nose/crack</code>
  </div>

  <script>
    const I18N = {
      ru: {
        badge: "🚀 Startup of the Year @ Product Hunt",
        subtitle: "Первая нейросеть с тактильной отдачей и симулятором хрящей",
        modelTitle: "Анатомическая Модель Хрящей",
        btnBoth: "💥 Сдвинуть хрящ (Space)",
        btnLeft: "👈 Левый хрящ",
        btnRight: "Правый хрящ 👉",
        btnAi: "🤖 AI Авто-хруст",
        btnAiActive: "🟢 AI Хрустит",
        telemetryTitle: "Телеметрия & Токеномика",
        totalClicks: "Всего щелчков:",
        pleasureTokens: "Токены удовольствия:",
        stressLevel: "Уровень стресса:",
        aiDopamine: "AI Дофамин весов:",
        cartilageState: "Состояние хряща:",
        speed: "Скорость хруста:",
        power: "Нагрузка датацентра:",
        achievements: "Достижения:",
        hallOfFame: "🏆 Зал Славы Достижений",
        btnToggleAch: "Скрыть / Показать",
        share: "Поделиться с другом: отправь ссылку в браузере или команду:",
        toastNew: "🎉 Новое достижение разблокировано!",
        unlockedAt: "Разблокировано:",
        leftNostril: "Левая ноздря",
        rightNostril: "Правая ноздря"
      },
      en: {
        badge: "🚀 Startup of the Year @ Product Hunt",
        subtitle: "World's first neural net with haptic feedback & cartilage simulator",
        modelTitle: "Anatomical Cartilage Model",
        btnBoth: "💥 Snap Cartilage (Space)",
        btnLeft: "👈 Left Cartilage",
        btnRight: "Right Cartilage 👉",
        btnAi: "🤖 AI Auto-Snap",
        btnAiActive: "🟢 AI Snapping",
        telemetryTitle: "Telemetry & Tokenomics",
        totalClicks: "Total Snaps:",
        pleasureTokens: "Pleasure Tokens:",
        stressLevel: "Stress Level:",
        aiDopamine: "AI Weights Dopamine:",
        cartilageState: "Cartilage State:",
        speed: "Snap Speed:",
        power: "Datacenter Load:",
        achievements: "Achievements:",
        hallOfFame: "🏆 Cartilage Hall of Fame",
        btnToggleAch: "Toggle View",
        share: "Share with a friend: send browser link or run command:",
        toastNew: "🎉 New achievement unlocked!",
        unlockedAt: "Unlocked:",
        leftNostril: "Left Nostril",
        rightNostril: "Right Nostril"
      },
      uk: {
        badge: "🚀 Стартап Року @ Product Hunt",
        subtitle: "Перша нейромережа з тактильною віддачею та симулятором хрящів",
        modelTitle: "Анатомічна Модель Хрящів",
        btnBoth: "💥 Зрушити хрящ (Space)",
        btnLeft: "👈 Лівий хрящ",
        btnRight: "Правий хрящ 👉",
        btnAi: "🤖 AI Авто-хрускіт",
        btnAiActive: "🟢 AI Хрумтить",
        telemetryTitle: "Телеметрія & Токеноміка",
        totalClicks: "Всього клацань:",
        pleasureTokens: "Токени задоволення:",
        stressLevel: "Рівень стресу:",
        aiDopamine: "AI Дофамін ваг:",
        cartilageState: "Стан хряща:",
        speed: "Швидкість хрускоту:",
        power: "Навантаження датацентру:",
        achievements: "Досягнення:",
        hallOfFame: "🏆 Зала Слави Досягнень",
        btnToggleAch: "Сховати / Показати",
        share: "Поділитися з другом: відправ посилання у браузері або команду:",
        toastNew: "🎉 Нове досягнення розблоковано!",
        unlockedAt: "Розблоковано:",
        leftNostril: "Ліва ніздря",
        rightNostril: "Права ніздря"
      }
    };

    let currentLang = localStorage.getItem('nose_lang') || 'uk';
    if (!['uk', 'en', 'ru'].includes(currentLang)) currentLang = 'uk';

    function setLang(lang) {
      if (!['uk', 'en', 'ru'].includes(lang)) lang = 'uk';
      currentLang = lang;
      localStorage.setItem('nose_lang', lang);

      // Highlight active button
      ['uk', 'en', 'ru'].forEach(l => {
        const btn = document.getElementById(`btn-lang-${l}`);
        if (btn) btn.classList.toggle('active', l === lang);
      });

      // Update static text elements
      const t = I18N[lang];
      document.getElementById('lbl-badge').innerText = t.badge;
      document.getElementById('lbl-subtitle').innerText = t.subtitle;
      document.getElementById('lbl-card-model').innerText = t.modelTitle;
      document.getElementById('btn-both').innerText = t.btnBoth;
      document.getElementById('btn-left').innerText = t.btnLeft;
      document.getElementById('btn-right').innerText = t.btnRight;
      
      const aiBtn = document.getElementById('btn-ai');
      if (aiBtn) {
        aiBtn.innerText = aiBtn.dataset.active === 'true' ? t.btnAiActive : t.btnAi;
      }

      document.getElementById('lbl-card-telemetry').innerText = t.telemetryTitle;
      document.getElementById('lbl-clicks').innerText = t.totalClicks;
      document.getElementById('lbl-tokens').innerText = t.pleasureTokens;
      document.getElementById('lbl-stress').innerText = t.stressLevel;
      document.getElementById('lbl-dopamine').innerText = t.aiDopamine;
      document.getElementById('lbl-cartilage').innerText = t.cartilageState;
      document.getElementById('lbl-cps').innerText = t.speed;
      document.getElementById('lbl-power').innerText = t.power;
      document.getElementById('lbl-ach').innerText = t.achievements;
      document.getElementById('lbl-card-hall').childNodes[0].nodeValue = t.hallOfFame + ' ';
      document.getElementById('btn-toggle-ach').innerText = t.btnToggleAch;
      
      const copyBanner = document.getElementById('lbl-copy-banner');
      copyBanner.innerHTML = `${t.share} <code>curl -X POST http://&lt;IP&gt;:8088/api/v1/nose/crack</code>`;

      // Update nose art labels
      const art = document.getElementById('nose-art');
      if (art) {
        art.innerText = `       .──────────────────.
      /      ________      \\
     │      /        \\      │
     │     │  │    │  │     │
     │     │  │    │  │     │
    /      │  │    │  │      \\
   │      ┌┴──┴────┴──┴┐      │
   │   (  │   (•)  (•) │  )   │
    \\__ \\_└───┬────┬───┘_/ __/
       \\______/    \\______/
          ▲            ▲
     ${t.leftNostril}  ${t.rightNostril}`;
      }

      // Sync backend
      fetch('/api/v1/lang/set', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lang: lang })
      }).catch(() => {});

      // Force refresh data
      pollStatus();
    }

    // Web Audio Synthesizer for instant satisfying tactile cartilage sound in browser
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    function playSnapSound(pan = 0) {
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      const now = audioCtx.currentTime;

      // 1. Low body thump
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      const panner = audioCtx.createStereoPanner ? audioCtx.createStereoPanner() : null;

      osc.type = 'sine';
      osc.frequency.setValueAtTime(155, now);
      osc.frequency.exponentialRampToValueAtTime(70, now + 0.08);

      gain.gain.setValueAtTime(0.5, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);

      if (panner) {
        panner.pan.setValueAtTime(pan, now);
        osc.connect(gain);
        gain.connect(panner);
        panner.connect(audioCtx.destination);
      } else {
        osc.connect(gain);
        gain.connect(audioCtx.destination);
      }

      osc.start(now);
      osc.stop(now + 0.08);

      // 2. Micro snap transient
      const snapOsc = audioCtx.createOscillator();
      const snapGain = audioCtx.createGain();
      snapOsc.type = 'triangle';
      snapOsc.frequency.setValueAtTime(680, now);
      snapOsc.frequency.exponentialRampToValueAtTime(200, now + 0.04);
      snapGain.gain.setValueAtTime(0.4, now);
      snapGain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
      snapOsc.connect(snapGain);
      snapGain.connect(audioCtx.destination);
      snapOsc.start(now);
      snapOsc.stop(now + 0.04);
    }

    const noseArt = document.getElementById('nose-art');

    async function crack(side = 'both') {
      const pan = side === 'left' ? -0.8 : (side === 'right' ? 0.8 : 0);
      playSnapSound(pan);

      noseArt.classList.add('snapped');
      setTimeout(() => noseArt.classList.remove('snapped'), 120);

      try {
        const res = await fetch('/api/v1/nose/crack', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ cartilage: side, caller: 'Web-Client' })
        });
        const data = await res.json();
        addLog(`💥 [${side.toUpperCase()}] ${data.message} • Token: <span class="log-token">${data.pleasure_token}</span>`);
        updateUI(data);
      } catch (err) {
        console.error(err);
      }
    }

    async function toggleAI() {
      try {
        const res = await fetch('/api/v1/ai/toggle', { method: 'POST' });
        const data = await res.json();
        const btn = document.getElementById('btn-ai');
        const t = I18N[currentLang];
        btn.dataset.active = data.ai_worker_enabled ? 'true' : 'false';
        btn.innerText = data.ai_worker_enabled ? t.btnAiActive : t.btnAi;
        addLog(`🤖 AI Loop ${data.message}`);
      } catch (e) {}
    }

    function addLog(html) {
      const box = document.getElementById('log-feed');
      const div = document.createElement('div');
      div.className = 'log-entry';
      const time = new Date().toLocaleTimeString();
      div.innerHTML = `[${time}] ${html}`;
      box.insertBefore(div, box.firstChild);
      if (box.children.length > 25) box.removeChild(box.lastChild);
    }

    let lastUnlockedCount = -1;

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.innerText = msg;
      t.style.display = 'block';
      setTimeout(() => { t.style.display = 'none'; }, 4500);
    }

    function toggleAchVisibility() {
      const g = document.getElementById('achievements-grid');
      g.style.display = (g.style.display === 'none') ? 'grid' : 'none';
    }

    function renderAchievements(achievements, unlockedCount, totalCount) {
      if (unlockedCount !== undefined && totalCount !== undefined) {
        const pct = totalCount ? Math.round((unlockedCount / totalCount) * 100) : 0;
        const valAch = document.getElementById('val-ach');
        if (valAch) valAch.innerText = `🏆 ${unlockedCount} / ${totalCount} (${pct}%)`;
        const badge = document.getElementById('ach-count-badge');
        if (badge) badge.innerText = `(${unlockedCount}/${totalCount} • ${pct}%)`;

        if (lastUnlockedCount !== -1 && unlockedCount > lastUnlockedCount) {
          showToast(`${I18N[currentLang].toastNew} [${unlockedCount}/${totalCount}]`);
        }
        lastUnlockedCount = unlockedCount;
      }

      if (!achievements || achievements.length === 0) return;

      const grid = document.getElementById('achievements-grid');
      grid.dataset.lang = currentLang;
      grid.dataset.unlocked = String(unlockedCount);
      
      const unlText = I18N[currentLang].unlockedAt;
      grid.innerHTML = achievements.map(a => {
        const isUnlocked = a.unlocked;
        const icon = a.icon || "🏆";
        const status = isUnlocked ? "✅" : "🔒";
        const dateStr = a.unlocked_at ? `<div class="ach-date">${unlText} ${a.unlocked_at}</div>` : "";
        return `
          <div class="ach-item ${isUnlocked ? 'unlocked' : ''}">
            <div class="ach-header">
              <span>${status}</span>
              <span>${icon} ${a.name}</span>
            </div>
            <div class="ach-desc">${a.desc}</div>
            ${dateStr}
          </div>
        `;
      }).join('');
    }

    function updateUI(data) {
      if (data.clicks_total !== undefined) document.getElementById('val-clicks').innerText = data.clicks_total.toLocaleString();
      if (data.pleasure_tokens !== undefined) document.getElementById('val-tokens').innerText = `💎 ${data.pleasure_tokens.toFixed(1)} PLEASURE`;
      if (data.stress_level !== undefined) {
        document.getElementById('val-stress').innerText = `${Math.round(data.stress_level)}%`;
        document.getElementById('bar-stress').style.width = `${Math.min(100, Math.max(0, data.stress_level))}%`;
      }
      if (data.ai_dopamine_level !== undefined) {
        document.getElementById('val-dopamine').innerText = `${Math.round(data.ai_dopamine_level)}%`;
        document.getElementById('bar-dopamine').style.width = `${Math.min(100, Math.max(0, data.ai_dopamine_level))}%`;
      }
      if (data.cartilage_integrity) document.getElementById('val-cartilage').innerText = data.cartilage_integrity;
      if (data.cps !== undefined) document.getElementById('val-cps').innerText = `${data.cps.toFixed(1)} CPS`;
      if (data.datacenter_power_gw !== undefined) document.getElementById('val-power').innerText = `⚡ ${data.datacenter_power_gw} GW`;

      if (data.achievements_unlocked !== undefined) {
        renderAchievements(data.achievements, data.achievements_unlocked, data.achievements_total);
      }
    }

    async function pollStatus() {
      try {
        const res = await fetch(`/api/v1/nose/status?lang=${encodeURIComponent(currentLang)}`);
        const data = await res.json();
        updateUI(data);
      } catch (e) {}
    }

    setInterval(pollStatus, 800);

    // Keyboard hotkeys
    window.addEventListener('keydown', (e) => {
      const code = e.code || '';
      const key = (e.key || '').toLowerCase();

      if (code === 'Space' || key === ' ' || code === 'ArrowLeft' || key === 'arrowleft' || code === 'ArrowRight' || key === 'arrowright') {
        e.preventDefault();
      }

      if (code === 'Space' || key === ' ') {
        crack('both');
      } else if (code === 'ArrowLeft' || key === 'arrowleft' || code === 'KeyZ' || key === 'z' || key === 'я') {
        crack('left');
      } else if (code === 'ArrowRight' || key === 'arrowright' || code === 'KeyX' || key === 'x' || key === 'ч') {
        crack('right');
      } else if (code === 'KeyA' || key === 'a' || key === 'ф') {
        toggleAI();
      } else if (code === 'KeyO' || key === 'o' || key === 'щ') {
        const sec = document.getElementById('achievements-section');
        if (sec) sec.scrollIntoView({ behavior: 'smooth' });
      } else if (code === 'KeyL') {
        const order = ['ru', 'en', 'uk'];
        const next = order[(order.indexOf(currentLang) + 1) % order.length];
        setLang(next);
      }
    });

    // Initialize saved language
    setLang(currentLang);
  </script>
</body>
</html>
"""
