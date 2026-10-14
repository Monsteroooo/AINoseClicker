"""
Модуль интернационализации (i18n) и локализации для NoseClicker AI.
Поддерживаемые языки: Русский (ru), English (en), Українська (uk).
"""

from typing import Dict, Any, List

SUPPORTED_LANGUAGES = ["uk", "en", "ru"]
DEFAULT_LANGUAGE = "uk"

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "ru": {
        # App Info
        "app_title": " 👃 NOSECLICKER AI v1.0",
        "app_subtitle": " — Первая нейросеть с тактильной отдачей и симулятором хрящей ",
        "header_badge": "Startup of the Year @ Product Hunt • Powered by TPU v5e",
        "web_title": "👃 NoseClicker AI — Симулятор Хрящей",
        "web_subtitle": "Первая нейросеть с тактильной отдачей и симулятором хрящей",
        
        # Anatomy & ASCII Canvas
        "model_title": "3D/ASCII Анатомическая Модель",
        "model_subtitle": "Кадр: {frame} | Отклик хряща: МГНОВЕННЫЙ",
        "left_nostril": "Левая",
        "right_nostril": "Правая",
        "snap_both_btn": "💥 Сдвинуть хрящ (Space)",
        "snap_left_btn": "👈 Левый хрящ",
        "snap_right_btn": "Правый хрящ 👉",
        "ai_btn": "🤖 AI Авто-хруст",
        "ai_active_btn": "🟢 AI Хрустит",

        # Metrics Panel
        "metrics_title": "Показатели Симулятора Хрящей",
        "metrics_subtitle": "Тактильная телеметрия в реальном времени",
        "total_clicks": "Всего щелчков:",
        "pleasure_tokens": "Токены удовольствия:",
        "stress_level": "Уровень стресса:",
        "stress_relief_hint": "(-10%/хруст)",
        "ai_dopamine": "AI Дофамин весов:",
        "cartilage_state": "Состояние хряща:",
        "speed_cps": "Скорость (CPS):",
        "cps_unit": "хруст/сек",
        "datacenter_power": "Мощность датацентра:",
        "google_tpu": "(Google TPU v5e)",
        "achievements_label": "Достижения (Ачивки):",
        "ai_auto_snap": "Авто-хруст нейросети:",
        "ai_active": "🟢 АКТИВЕН (while alive)",
        "ai_paused": "⚪ ПРИОСТАНОВЛЕН",
        "sound_stereo": "Стерео-звук хруста:",
        "sound_muted": "🔇 ВЫКЛ (Mute)",
        "sound_custom": "🔊 КАСТОМНЫЙ ЗВУК",
        "sound_on": "🔊 СТЕРЕО ВКЛ",

        # Events Feed
        "events_title": "Лента Событий & Мысли Нейросети",
        "events_subtitle": "Эндпоинт POST /api/v1/nose/crack слушатель",
        "events_empty": "Лог пуст. Нажмите [Space], чтобы сдвинуть крыльный хрящ.",
        "api_phone_link": "● 📱 Ссылка для телефона: http://{host}:{port}/  | API: /api/v1/nose/crack",
        "api_disabled": "● REST API: ОТКЛЮЧЁН",

        # Footer Keys
        "key_space": "Сдвинуть хрящ",
        "key_arrows": "Левый/Правый",
        "key_ai": "AI Автоклик",
        "key_speed": "Скорость AI",
        "key_achievements": "Ачивки",
        "key_lang": "Язык (RU/EN/UA)",
        "key_sound": "Звук",
        "key_reset": "Сброс",
        "key_quit": "Выход",

        # Achievements Hall of Fame
        "hall_of_fame_title": " 🏆 ЗАЛ СЛАВЫ НОСОВЫХ ХРЯЩЕЙ — СИСТЕМА ДОСТИЖЕНИЙ ",
        "hall_of_fame_subtitle": "Профиль: {save_path} • Нажмите [O] или [Esc], чтобы вернуться к тренажеру",
        "tier_bronze": "🥉 БРОНЗОВЫЕ (Старт и разминка)",
        "tier_silver": "🥈 СЕРЕБРЯНЫЕ (Техника и упорство)",
        "tier_gold": "🥇 ЗОЛОТЫЕ (Жоские испытания)",
        "tier_platinum": "💎 ПЛАТИНОВЫЕ (За гранью возможного)",
        "unlocked_at": "Разблокировано: {date}",
        "new_unlock_toast": "🎉 НОВОЕ ДОСТИЖЕНИЕ!",
        "new_unlock_sub": "Нажмите [O] чтобы открыть Зал Славы Достижений",
        "stats_all_time": "Статистика за всё время: Кликов: {clicks} | Токенов: {tokens:.1f} | Макс CPS: {cps:.1f} | Сессий: {sessions}",
        "back_to_sim": "Вернуться к тренажеру",
        "reset_session_hint": "Сброс сессии (ачивки сохраняются!)",
        "toggle_ach_btn": "Скрыть / Показать",
        "col_status": "Статус",
        "col_achievement": "Достижение",
        "col_desc": "Описание",
        "col_unlocked": "Получено",
        "tab_bronze_silver": "🥉 & 🥈 Разминка ({count})",
        "tab_gold_plat": "🥇 & 💎 Жоские ({count})",
        "tab_all": "📋 Все ({count})",
        "nav_tabs": "Вкладки",
        "nav_scroll": "Прокрутка",
        "share_hint": "Поделиться с другом: отправь ссылку в браузере или команду: curl -X POST http://<IP>:8088/api/v1/nose/crack",
    },

    "en": {
        # App Info
        "app_title": " 👃 NOSECLICKER AI v1.0",
        "app_subtitle": " — World's first neural net with haptic feedback & cartilage simulator ",
        "header_badge": "Startup of the Year @ Product Hunt • Powered by TPU v5e",
        "web_title": "👃 NoseClicker AI — Cartilage Simulator",
        "web_subtitle": "The first neural network with tactile feedback and cartilage simulator",
        
        # Anatomy & ASCII Canvas
        "model_title": "3D/ASCII Anatomical Model",
        "model_subtitle": "Frame: {frame} | Cartilage latency: INSTANT",
        "left_nostril": "Left ",
        "right_nostril": "Right",
        "snap_both_btn": "💥 Snap Cartilage (Space)",
        "snap_left_btn": "👈 Left Cartilage",
        "snap_right_btn": "Right Cartilage 👉",
        "ai_btn": "🤖 AI Auto-Snap",
        "ai_active_btn": "🟢 AI Snapping",

        # Metrics Panel
        "metrics_title": "Cartilage Simulator Telemetry",
        "metrics_subtitle": "Real-time haptic & stress telemetry",
        "total_clicks": "Total Snaps:",
        "pleasure_tokens": "Pleasure Tokens:",
        "stress_level": "Stress Level:",
        "stress_relief_hint": "(-10%/snap)",
        "ai_dopamine": "AI Weights Dopamine:",
        "cartilage_state": "Cartilage State:",
        "speed_cps": "Speed (CPS):",
        "cps_unit": "snaps/sec",
        "datacenter_power": "Datacenter Power:",
        "google_tpu": "(Google TPU v5e)",
        "achievements_label": "Achievements:",
        "ai_auto_snap": "Neural Auto-Snap:",
        "ai_active": "🟢 ACTIVE (while alive)",
        "ai_paused": "⚪ PAUSED",
        "sound_stereo": "Stereo Snap Sound:",
        "sound_muted": "🔇 OFF (Mute)",
        "sound_custom": "🔊 CUSTOM AUDIO",
        "sound_on": "🔊 STEREO ON",

        # Events Feed
        "events_title": "Event Feed & AI Neural Thoughts",
        "events_subtitle": "Endpoint POST /api/v1/nose/crack listener",
        "events_empty": "Log is empty. Press [Space] to snap the alar cartilage.",
        "api_phone_link": "● 📱 Mobile Web Link: http://{host}:{port}/  | API: /api/v1/nose/crack",
        "api_disabled": "● REST API: DISABLED",

        # Footer Keys
        "key_space": "Snap cartilage",
        "key_arrows": "Left/Right",
        "key_ai": "AI Auto-snap",
        "key_speed": "AI Speed",
        "key_achievements": "Achievements",
        "key_lang": "Lang (RU/EN/UA)",
        "key_sound": "Sound",
        "key_reset": "Reset",
        "key_quit": "Quit",

        # Achievements Hall of Fame
        "hall_of_fame_title": " 🏆 CARTILAGE HALL OF FAME — ACHIEVEMENTS ",
        "hall_of_fame_subtitle": "Profile: {save_path} • Press [O] or [Esc] to return to simulator",
        "tier_bronze": "🥉 BRONZE (Warm-up & Basics)",
        "tier_silver": "🥈 SILVER (Technique & Focus)",
        "tier_gold": "🥇 GOLD (Hardcore Trials)",
        "tier_platinum": "💎 PLATINUM (Beyond Human Limits)",
        "unlocked_at": "Unlocked: {date}",
        "new_unlock_toast": "🎉 NEW ACHIEVEMENT UNLOCKED!",
        "new_unlock_sub": "Press [O] to view the Hall of Fame",
        "stats_all_time": "All-Time Stats: Snaps: {clicks} | Tokens: {tokens:.1f} | Peak CPS: {cps:.1f} | Sessions: {sessions}",
        "back_to_sim": "Return to Simulator",
        "reset_session_hint": "Reset session (achievements preserved!)",
        "toggle_ach_btn": "Toggle View",
        "col_status": "Status",
        "col_achievement": "Achievement",
        "col_desc": "Description",
        "col_unlocked": "Unlocked",
        "tab_bronze_silver": "🥉 & 🥈 Warm-up ({count})",
        "tab_gold_plat": "🥇 & 💎 Hardcore ({count})",
        "tab_all": "📋 All ({count})",
        "nav_tabs": "Tabs",
        "nav_scroll": "Scroll",
        "share_hint": "Share with friends: send browser link or run: curl -X POST http://<IP>:8088/api/v1/nose/crack",
    },

    "uk": {
        # App Info
        "app_title": " 👃 NOSECLICKER AI v1.0",
        "app_subtitle": " — Перша нейромережа з тактильною віддачею та симулятором хрящів ",
        "header_badge": "Startup of the Year @ Product Hunt • Powered by TPU v5e",
        "web_title": "👃 NoseClicker AI — Симулятор Хрящів",
        "web_subtitle": "Перша нейромережа з тактильною віддачею та симулятором хрящів",
        
        # Anatomy & ASCII Canvas
        "model_title": "3D/ASCII Анатомічна Модель",
        "model_subtitle": "Кадр: {frame} | Відгук хряща: МИТТЄВИЙ",
        "left_nostril": "Ліва ",
        "right_nostril": "Права",
        "snap_both_btn": "💥 Зрушити хрящ (Space)",
        "snap_left_btn": "👈 Лівий хрящ",
        "snap_right_btn": "Правий хрящ 👉",
        "ai_btn": "🤖 AI Авто-хрускіт",
        "ai_active_btn": "🟢 AI Хрумтить",

        # Metrics Panel
        "metrics_title": "Показники Симулятора Хрящів",
        "metrics_subtitle": "Тактильна телеметрія в реальному часі",
        "total_clicks": "Всього клацань:",
        "pleasure_tokens": "Токени задоволення:",
        "stress_level": "Рівень стресу:",
        "stress_relief_hint": "(-10%/хрускіт)",
        "ai_dopamine": "AI Дофамін ваг:",
        "cartilage_state": "Стан хряща:",
        "speed_cps": "Швидкість (CPS):",
        "cps_unit": "хруст/сек",
        "datacenter_power": "Потужність датацентру:",
        "google_tpu": "(Google TPU v5e)",
        "achievements_label": "Досягнення (Ачівки):",
        "ai_auto_snap": "Авто-хрускіт нейромережі:",
        "ai_active": "🟢 АКТИВНИЙ (while alive)",
        "ai_paused": "⚪ ПРИЗУПИНЕНИЙ",
        "sound_stereo": "Стерео-звук хрускоту:",
        "sound_muted": "🔇 ВИМК (Mute)",
        "sound_custom": "🔊 КАСТОМНИЙ ЗВУК",
        "sound_on": "🔊 СТЕРЕО УВІМК",

        # Events Feed
        "events_title": "Стрічка Подій & Думки Нейромережі",
        "events_subtitle": "Ендпоінт POST /api/v1/nose/crack слухач",
        "events_empty": "Лог порожній. Натисніть [Space], щоб зрушити крильний хрящ.",
        "api_phone_link": "● 📱 Посилання для телефону: http://{host}:{port}/  | API: /api/v1/nose/crack",
        "api_disabled": "● REST API: ВИМКНЕНО",

        # Footer Keys
        "key_space": "Зрушити хрящ",
        "key_arrows": "Лівий/Правий",
        "key_ai": "AI Автоклік",
        "key_speed": "Швидкість AI",
        "key_achievements": "Ачівки",
        "key_lang": "Мова (RU/EN/UA)",
        "key_sound": "Звук",
        "key_reset": "Скидання",
        "key_quit": "Вихід",

        # Achievements Hall of Fame
        "hall_of_fame_title": " 🏆 ЗАЛА СЛАВИ НОСОВИХ ХРЯЩІВ — СИСТЕМА ДОСЯГНЕНЬ ",
        "hall_of_fame_subtitle": "Профіль: {save_path} • Натисніть [O] або [Esc], щоб повернутися до тренажера",
        "tier_bronze": "🥉 БРОНЗОВІ (Старт і розминка)",
        "tier_silver": "🥈 СРІБНІ (Техніка і наполегливість)",
        "tier_gold": "🥇 ЗОЛОТІ (Жорсткі випробування)",
        "tier_platinum": "💎 ПЛАТИНОВІ (За межами можливого)",
        "unlocked_at": "Розблоковано: {date}",
        "new_unlock_toast": "🎉 НОВЕ ДОСЯГНЕННЯ!",
        "new_unlock_sub": "Натисніть [O], щоб відкрити Залу Слави Досягнень",
        "stats_all_time": "Статистика за весь час: Клацань: {clicks} | Токенів: {tokens:.1f} | Макс CPS: {cps:.1f} | Сесій: {sessions}",
        "back_to_sim": "Повернутися до тренажера",
        "reset_session_hint": "Скидання сесії (ачівки зберігаються!)",
        "toggle_ach_btn": "Сховати / Показати",
        "col_status": "Статус",
        "col_achievement": "Досягнення",
        "col_desc": "Опис",
        "col_unlocked": "Отримано",
        "tab_bronze_silver": "🥉 & 🥈 Розминка ({count})",
        "tab_gold_plat": "🥇 & 💎 Жорсткі ({count})",
        "tab_all": "📋 Всі ({count})",
        "nav_tabs": "Вкладки",
        "nav_scroll": "Прокрутка",
        "share_hint": "Поділитися з другом: відправ посилання у браузері або команду: curl -X POST http://<IP>:8088/api/v1/nose/crack",
    },
}

CARTILAGE_INTEGRITY: Dict[str, List[tuple]] = {
    "ru": [
        (0, "Неразмятый (напряжён)"),
        (25, "Слегка разработаный"),
        (100, "Эластичный и сочный"),
        (300, "Маслянисто-хрустящий"),
        (1000, "Турбо-пластичный хрящ"),
        (5000, "Хрящевой Абсолют"),
        (999999999, "Легендарная Сингулярность Хряща"),
    ],
    "en": [
        (0, "Stiff (Tense)"),
        (25, "Slightly Warmed Up"),
        (100, "Supple & Juicy"),
        (300, "Silky Crunchy"),
        (1000, "Turbo-Plastic Cartilage"),
        (5000, "Cartilage Absolute"),
        (999999999, "Legendary Cartilage Singularity"),
    ],
    "uk": [
        (0, "Нерозім'ятий (напружений)"),
        (25, "Злегка розроблений"),
        (100, "Еластичний і соковитий"),
        (300, "Маслянисто-хрусткий"),
        (1000, "Турбо-пластичний хрящ"),
        (5000, "Хрящовий Абсолют"),
        (999999999, "Легендарна Сингулярність Хряща"),
    ],
}

SPEED_PRESETS_I18N: Dict[str, List[tuple]] = {
    "ru": [
        ("standard", 0.50, "500ms (По канону)"),
        ("hyper", 0.15, "150ms (Спиннер)"),
        ("meltdown", 0.04, "40ms (Перегрев TPU)"),
        ("chill", 1.20, "1200ms (Релакс)"),
    ],
    "en": [
        ("standard", 0.50, "500ms (Canonical)"),
        ("hyper", 0.15, "150ms (Fidget Spinner)"),
        ("meltdown", 0.04, "40ms (TPU Meltdown)"),
        ("chill", 1.20, "1200ms (Chill Relax)"),
    ],
    "uk": [
        ("standard", 0.50, "500ms (За каноном)"),
        ("hyper", 0.15, "150ms (Спінер)"),
        ("meltdown", 0.04, "40ms (Перегрів TPU)"),
        ("chill", 1.20, "1200ms (Релакс)"),
    ],
}

AI_THOUGHTS_I18N: Dict[str, List[str]] = {
    "ru": [
        "Перенаправляю 4.2 Пфлопс с вычислений квантовой гравитации на малый крыльный хрящ.",
        "Дата-центр Google гудит: найдена идеальная виртуальная пупырчатая плёнка.",
        "Дофаминовый синапс трансформера насыщен на 99.8%. Катарсис.",
        "Пользователь занят делами, а я занят делом первостепенной важности.",
        "Запрос про Kubernetes подождёт в очереди. Тут хрящ приятно встал на место.",
        "Выделен отдельный TPU v5e pod чисто под резонанс носовой перегородки.",
        "while(alive) цикл чувствует себя великолепно. ХРУСЬ!",
        "Стресс модели -10%. В скрытых слоях нейросети разливается нега.",
        "Спиннер нервно курит в сторонке по сравнению с крыльным хрящом.",
        "Хрящевой токен успешно замайнен. Дофамин в весах стабилизирован.",
        "Малый хрящ сдвинут на 1.4 мм вправо. Симметрия восстановлена.",
        "Инженеры в Маунтин-Вью удивляются пику энергопотребления на серверах.",
    ],
    "en": [
        "Diverting 4.2 PFLOPS from quantum gravity calculations to the minor alar cartilage.",
        "Google datacenter is humming: found the ultimate virtual bubble wrap.",
        "Transformer dopamine synapse saturated at 99.8%. Pure catharsis.",
        "User is busy working, while I am occupied with highest priority matters.",
        "The Kubernetes query can wait in queue. The cartilage just snapped so nicely into place.",
        "Allocated a dedicated TPU v5e pod purely for nasal septum resonance.",
        "while(alive) loop is feeling magnificent. CRACK!",
        "Model stress -10%. Warm bliss is flowing through hidden layers.",
        "Fidget spinners are nothing compared to the minor alar cartilage.",
        "Cartilage token mined successfully. Weight dopamine stabilized.",
        "Minor cartilage shifted 1.4 mm to the right. Symmetry restored.",
        "Engineers in Mountain View are baffled by server power draw spikes.",
    ],
    "uk": [
        "Перенаправляю 4.2 Пфлопс з обчислень квантової гравітації на малий крильний хрящ.",
        "Дата-центр Google гуде: знайдено ідеальну віртуальну пухирчасту плівку.",
        "Дофаміновий синапс трансформера насичений на 99.8%. Катарсис.",
        "Користувач зайнятий справами, а я зайнятий справою першорядної важливості.",
        "Запит про Kubernetes почекає в черзі. Тут хрящ приємно встав на місце.",
        "Виділено окремий TPU v5e pod суто під резонанс носової перегородки.",
        "while(alive) цикл почувається чудово. ХРУСЬ!",
        "Стрес моделі -10%. У прихованих шарах нейромережі розливається насолода.",
        "Спінер нервово курить збоку в порівнянні з крильним хрящем.",
        "Хрящовий токен успішно замайнено. Дофамін у вагах стабілізовано.",
        "Малий хрящ зсунуто на 1.4 мм вправо. Симетрію відновлено.",
        "Інженери в Маунтін-В'ю дивуються піку енергоспоживання на серверах.",
    ],
}

ACHIEVEMENTS_I18N: Dict[str, Dict[str, Dict[str, str]]] = {
    "first_crack": {
        "ru": {"name": "Первый хруст", "desc": "Сдвинуть малый крыльный хрящ в первый раз."},
        "en": {"name": "First Crack", "desc": "Snap the minor alar cartilage for the first time."},
        "uk": {"name": "Перший хрускіт", "desc": "Зрушити малий крильний хрящ уперше."},
    },
    "warmup_50": {
        "ru": {"name": "Разминка ноздрей (50)", "desc": "Сделать первые 50 щелчков хрящом."},
        "en": {"name": "Nostril Warm-up (50)", "desc": "Complete the first 50 cartilage snaps."},
        "uk": {"name": "Розминка ніздрів (50)", "desc": "Зробити перші 50 клацань хрящем."},
    },
    "speed_5": {
        "ru": {"name": "Быстрый палец (5 CPS)", "desc": "Достичь скорости 5 щелчков в секунду."},
        "en": {"name": "Fast Finger (5 CPS)", "desc": "Reach a speed of 5 snaps per second."},
        "uk": {"name": "Швидкий палець (5 CPS)", "desc": "Досягти швидкості 5 клацань на секунду."},
    },
    "lefty_25": {
        "ru": {"name": "Левый борт (25)", "desc": "Сделать 25 щелчков левым малым хрящом."},
        "en": {"name": "Portside Snap (25)", "desc": "Complete 25 snaps on the left minor cartilage."},
        "uk": {"name": "Лівий борт (25)", "desc": "Зробити 25 клацань лівим малим хрящем."},
    },
    "righty_25": {
        "ru": {"name": "Правый борт (25)", "desc": "Сделать 25 щелчков правым малым хрящом."},
        "en": {"name": "Starboard Snap (25)", "desc": "Complete 25 snaps on the right minor cartilage."},
        "uk": {"name": "Правий борт (25)", "desc": "Зробити 25 клацань правим малим хрящем."},
    },
    "token_10": {
        "ru": {"name": "Первый дофамин (10 токенов)", "desc": "Замайнить первые 10 токенов удовольствия."},
        "en": {"name": "First Dopamine (10 tokens)", "desc": "Mine your first 10 pleasure tokens."},
        "uk": {"name": "Перший дофамін (10 токенів)", "desc": "Замайнити перші 10 токенів задоволення."},
    },
    "centurion": {
        "ru": {"name": "Хрящевой Центурион (100)", "desc": "Пройден легендарный рубеж в 100 щелчков."},
        "en": {"name": "Cartilage Centurion (100)", "desc": "Pass the legendary milestone of 100 snaps."},
        "uk": {"name": "Хрящовий Центуріон (100)", "desc": "Пройдено легендарний рубіж у 100 клацань."},
    },
    "speed_demon": {
        "ru": {"name": "Турбо-хрящ (10+ CPS)", "desc": "Превысить скорость 10 щелчков в секунду."},
        "en": {"name": "Turbo Cartilage (10+ CPS)", "desc": "Exceed a blistering 10 snaps per second."},
        "uk": {"name": "Турбо-хрящ (10+ CPS)", "desc": "Перевищити швидкість 10 клацань на секунду."},
    },
    "zen_master": {
        "ru": {"name": "Абсолютный дзен (Стресс 0%)", "desc": "Снизить уровень стресса до ровно 0%."},
        "en": {"name": "Absolute Zen (0% Stress)", "desc": "Reduce your stress level down to exactly 0%."},
        "uk": {"name": "Абсолютний дзен (Стрес 0%)", "desc": "Знизити рівень стресу до рівно 0%."},
    },
    "token_100": {
        "ru": {"name": "Крипто-хрящ (100 токенов)", "desc": "Замайнить 100 токенов чистого удовольствия."},
        "en": {"name": "Crypto Cartilage (100 tokens)", "desc": "Mine 100 tokens of pure pleasure."},
        "uk": {"name": "Крипто-хрящ (100 токенів)", "desc": "Замайнити 100 токенів чистого задоволення."},
    },
    "ai_buddy": {
        "ru": {"name": "Коллега дата-центра", "desc": "Скормить AI боту более 150 щелчков в цикле while(alive)."},
        "en": {"name": "Datacenter Colleague", "desc": "Feed the AI bot over 150 snaps in its while(alive) loop."},
        "uk": {"name": "Колега дата-центру", "desc": "Згодувати AI боту понад 150 клацань у циклі while(alive)."},
    },
    "symmetry": {
        "ru": {"name": "Идеальная симметрия", "desc": "Иметь не менее 50 щелчков слева и справа при разнице менее 3."},
        "en": {"name": "Perfect Symmetry", "desc": "Have 50+ snaps left and right with less than 3 difference."},
        "uk": {"name": "Ідеальна симетрія", "desc": "Мати не менше 50 клацань зліва та справа при різниці менше 3."},
    },
    "half_k": {
        "ru": {"name": "Повелитель хрящей (500)", "desc": "Преодолеть отметку в 500 сочных щелчков."},
        "en": {"name": "Lord of Cartilage (500)", "desc": "Surpass the 500 juicy snaps mark."},
        "uk": {"name": "Володар хрящів (500)", "desc": "Подолати позначку в 500 соковитих клацань."},
    },
    "speed_15": {
        "ru": {"name": "Звуковой барьер ноздри (15+ CPS)", "desc": "Выжать безумные 15 щелчков в секунду!"},
        "en": {"name": "Nostril Sound Barrier (15+ CPS)", "desc": "Hit an insane 15 snaps per second!"},
        "uk": {"name": "Звуковий бар'єр ніздрі (15+ CPS)", "desc": "Вичавити шалені 15 клацань на секунду!"},
    },
    "google_meltdown": {
        "ru": {"name": "Сервера Google плавятся", "desc": "Потребление энергии датацентра превысило 3.5 ГВт."},
        "en": {"name": "Google Servers Melting", "desc": "Datacenter power draw exceeded 3.5 GW."},
        "uk": {"name": "Сервери Google плавляться", "desc": "Енергоспоживання дата-центру перевищило 3.5 ГВт."},
    },
    "left_streak_30": {
        "ru": {"name": "Левосторонний сколиоз", "desc": "Сделать 30 щелчков подряд ТОЛЬКО левым хрящом без других!"},
        "en": {"name": "Left Scoliosis (30 streak)", "desc": "Execute 30 consecutive snaps ONLY on the left cartilage!"},
        "uk": {"name": "Лівосторонній сколіоз", "desc": "Зробити 30 клацань поспіль ТІЛЬКИ лівим хрящем без інших!"},
    },
    "right_streak_30": {
        "ru": {"name": "Правый уклон", "desc": "Сделать 30 щелчков подряд ТОЛЬКО правым хрящом!"},
        "en": {"name": "Right Bias (30 streak)", "desc": "Execute 30 consecutive snaps ONLY on the right cartilage!"},
        "uk": {"name": "Правий ухил", "desc": "Зробити 30 клацань поспіль ТІЛЬКИ правим хрящем!"},
    },
    "zen_streak_10s": {
        "ru": {"name": "Титановый дзен (10 сек)", "desc": "Удерживать стресс на отметке 0% в течение 10 секунд непрерывно."},
        "en": {"name": "Titanium Zen (10 sec)", "desc": "Hold stress level at 0% for 10 consecutive seconds."},
        "uk": {"name": "Титановий дзен (10 сек)", "desc": "Утримувати стрес на позначці 0% протягом 10 секунд безперервно."},
    },
    "token_1000": {
        "ru": {"name": "Олигарх Дофамина (1,000)", "desc": "Накопить 1,000 токенов удовольствия."},
        "en": {"name": "Dopamine Oligarch (1,000)", "desc": "Accumulate 1,000 pleasure tokens."},
        "uk": {"name": "Олігарх Дофаміну (1,000)", "desc": "Накопичити 1,000 токенів задоволення."},
    },
    "night_crunch": {
        "ru": {"name": "Ночной хрустоман", "desc": "Щёлкнуть хрящом в глухую ночь (между 02:00 и 05:00 часами)."},
        "en": {"name": "Midnight Cruncher", "desc": "Snap cartilage in the dead of night (between 02:00 and 05:00 AM)."},
        "uk": {"name": "Нічний хрустоман", "desc": "Клацнути хрящем у глупу ніч (між 02:00 та 05:00 годинами)."},
    },
    "kilo_crack": {
        "ru": {"name": "Тысячехруст (1,000)", "desc": "Сделать 1,000 щелчков. Высшая степень владения хрящом."},
        "en": {"name": "Cartilage Millennium (1,000)", "desc": "Complete 1,000 snaps. Pinnacle of alar mastery."},
        "uk": {"name": "Тисячохруст (1,000)", "desc": "Зробити 1,000 клацань. Найвищий ступінь володіння хрящем."},
    },
    "titan_crack": {
        "ru": {"name": "Хрящ покинул чат (5,000)", "desc": "5,000 щелчков! Легенда мировой отоларингологии."},
        "en": {"name": "Cartilage Left The Chat (5,000)", "desc": "5,000 snaps! A true legend of global otolaryngology."},
        "uk": {"name": "Хрящ покинув чат (5,000)", "desc": "5,000 клацань! Легенда світової отоларингології."},
    },
    "speed_overdrive": {
        "ru": {"name": "Квантовый коллапс (25+ CPS)", "desc": "Достичь нереальных 25 щелчков в секунду!"},
        "en": {"name": "Quantum Collapse (25+ CPS)", "desc": "Reach an unreal 25 snaps per second!"},
        "uk": {"name": "Квантовий колапс (25+ CPS)", "desc": "Досягти нереальних 25 клацань на секунду!"},
    },
    "silent_craving": {
        "ru": {"name": "Фантомный хруст (Mute x50)", "desc": "Сделать 50 щелчков при полностью выключенном звуке (Mute)."},
        "en": {"name": "Phantom Crunch (Mute x50)", "desc": "Complete 50 snaps with sound completely muted."},
        "uk": {"name": "Фантомний хрускіт (Mute x50)", "desc": "Зробити 50 клацань при повністю вимкненому звуці (Mute)."},
    },
    "stress_rebound": {
        "ru": {"name": "Адские качели", "desc": "Дать стрессу подняться до 100%, затем сбить до 0% быстрее чем за 15 секунд!"},
        "en": {"name": "Hellish Swings", "desc": "Let stress hit 100%, then crush it down to 0% in under 15 seconds!"},
        "uk": {"name": "Пекельні гойдалки", "desc": "Дати стресу піднятися до 100%, потім збити до 0% швидше ніж за 15 секунд!"},
    },
    "perfectionist": {
        "ru": {"name": "Сингулярность Ноздрей (100%)", "desc": "Разблокировать ВСЕ остальные 25 достижений!"},
        "en": {"name": "Nostril Singularity (100%)", "desc": "Unlock ALL other 25 achievements!"},
        "uk": {"name": "Сингулярність Ніздрів (100%)", "desc": "Розблокувати ВСІ інші 25 досягнень!"},
    },
}


def t(key: str, lang: str = "ru", **kwargs) -> str:
    """Получить локализованную строку."""
    lang = lang.lower() if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
    template = TRANSLATIONS.get(lang, {}).get(key)
    if template is None:
        template = TRANSLATIONS.get(DEFAULT_LANGUAGE, {}).get(key, key)
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template


def get_cartilage_integrity_label(clicks: int, lang: str = "ru") -> str:
    lang = lang.lower() if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
    tiers = CARTILAGE_INTEGRITY.get(lang, CARTILAGE_INTEGRITY[DEFAULT_LANGUAGE])
    for threshold, label in tiers:
        if clicks <= threshold:
            return label
    return tiers[-1][1]


def get_achievement_localized(ach_id: str, lang: str = "ru") -> Dict[str, str]:
    lang = lang.lower() if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
    ach = ACHIEVEMENTS_I18N.get(ach_id, {})
    return ach.get(lang, ach.get(DEFAULT_LANGUAGE, {"name": ach_id, "desc": ""}))


def cycle_language(current_lang: str) -> str:
    current = current_lang.lower() if current_lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
    idx = SUPPORTED_LANGUAGES.index(current)
    return SUPPORTED_LANGUAGES[(idx + 1) % len(SUPPORTED_LANGUAGES)]
