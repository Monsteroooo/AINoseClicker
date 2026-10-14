import os
import json
import time
import secrets
from collections import deque
from datetime import datetime
from typing import Dict, List, Any, Optional

from nose_clicker.i18n import (
    get_cartilage_integrity_label,
    get_achievement_localized,
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE,
)


ACHIEVEMENTS_REGISTRY: Dict[str, Dict[str, Any]] = {
    # --- Tier 1: Бронзовые (Старт и разминка) ---
    "first_crack": {
        "tier": "bronze",
        "icon": "🥉",
        "name": "Первый хруст",
        "desc": "Сдвинуть малый крыльный хрящ в первый раз.",
    },
    "warmup_50": {
        "tier": "bronze",
        "icon": "🥉",
        "name": "Разминка ноздрей (50)",
        "desc": "Сделать первые 50 щелчков хрящом.",
    },
    "speed_5": {
        "tier": "bronze",
        "icon": "🥉",
        "name": "Быстрый палец (5 CPS)",
        "desc": "Достичь скорости 5 щелчков в секунду.",
    },
    "lefty_25": {
        "tier": "bronze",
        "icon": "🥉",
        "name": "Левый борт (25)",
        "desc": "Сделать 25 щелчков левым малым хрящом.",
    },
    "righty_25": {
        "tier": "bronze",
        "icon": "🥉",
        "name": "Правый борт (25)",
        "desc": "Сделать 25 щелчков правым малым хрящом.",
    },
    "token_10": {
        "tier": "bronze",
        "icon": "🥉",
        "name": "Первый дофамин (10 токенов)",
        "desc": "Замайнить первые 10 токенов удовольствия.",
    },

    # --- Tier 2: Серебряные (Техника и упорство) ---
    "centurion": {
        "tier": "silver",
        "icon": "🥈",
        "name": "Хрящевой Центурион (100)",
        "desc": "Пройден легендарный рубеж в 100 щелчков.",
    },
    "speed_demon": {
        "tier": "silver",
        "icon": "🥈",
        "name": "Турбо-хрящ (10+ CPS)",
        "desc": "Превысить скорость 10 щелчков в секунду.",
    },
    "zen_master": {
        "tier": "silver",
        "icon": "🥈",
        "name": "Абсолютный дзен (Стресс 0%)",
        "desc": "Снизить уровень стресса до ровно 0%.",
    },
    "token_100": {
        "tier": "silver",
        "icon": "🥈",
        "name": "Крипто-хрящ (100 токенов)",
        "desc": "Замайнить 100 токенов чистого удовольствия.",
    },
    "ai_buddy": {
        "tier": "silver",
        "icon": "🥈",
        "name": "Коллега дата-центра",
        "desc": "Скормить AI боту более 150 щелчков в цикле while(alive).",
    },
    "symmetry": {
        "tier": "silver",
        "icon": "🥈",
        "name": "Идеальная симметрия",
        "desc": "Иметь не менее 50 щелчков слева и справа при разнице менее 3.",
    },

    # --- Tier 3: Золотые (Жоские испытания) ---
    "half_k": {
        "tier": "gold",
        "icon": "🥇",
        "name": "Повелитель хрящей (500)",
        "desc": "Преодолеть отметку в 500 сочных щелчков.",
    },
    "speed_15": {
        "tier": "gold",
        "icon": "🥇",
        "name": "Звуковой барьер ноздри (15+ CPS)",
        "desc": "Выжать безумные 15 щелчков в секунду!",
    },
    "google_meltdown": {
        "tier": "gold",
        "icon": "🥇",
        "name": "Сервера Google плавятся",
        "desc": "Потребление энергии датацентра превысило 3.5 ГВт.",
    },
    "left_streak_30": {
        "tier": "gold",
        "icon": "🥇",
        "name": "Левосторонний сколиоз",
        "desc": "Сделать 30 щелчков подряд ТОЛЬКО левым хрящом без других!",
    },
    "right_streak_30": {
        "tier": "gold",
        "icon": "🥇",
        "name": "Правый уклон",
        "desc": "Сделать 30 щелчков подряд ТОЛЬКО правым хрящом!",
    },
    "zen_streak_10s": {
        "tier": "gold",
        "icon": "🥇",
        "name": "Титановый дзен (10 сек)",
        "desc": "Удерживать стресс на отметке 0% в течение 10 секунд непрерывно.",
    },
    "token_1000": {
        "tier": "gold",
        "icon": "🥇",
        "name": "Олигарх Дофамина (1,000)",
        "desc": "Накопить 1,000 токенов удовольствия.",
    },
    "night_crunch": {
        "tier": "gold",
        "icon": "🥇",
        "name": "Ночной хрустоман",
        "desc": "Щёлкнуть хрящом в глухую ночь (между 02:00 и 05:00 часами).",
    },

    # --- Tier 4: Платиновые / Ультра-хардкор ---
    "kilo_crack": {
        "tier": "platinum",
        "icon": "👑",
        "name": "Тысячехруст (1,000)",
        "desc": "Сделать 1,000 щелчков. Высшая степень владения хрящом.",
    },
    "titan_crack": {
        "tier": "platinum",
        "icon": "👑",
        "name": "Хрящ покинул чат (5,000)",
        "desc": "5,000 щелчков! Легенда мировой отоларингологии.",
    },
    "speed_overdrive": {
        "tier": "platinum",
        "icon": "👑",
        "name": "Квантовый коллапс (25+ CPS)",
        "desc": "Достичь нереальных 25 щелчков в секунду!",
    },
    "silent_craving": {
        "tier": "platinum",
        "icon": "💀",
        "name": "Фантомный хруст (Mute x50)",
        "desc": "Сделать 50 щелчков при полностью выключенном звуке (Mute).",
    },
    "stress_rebound": {
        "tier": "platinum",
        "icon": "💀",
        "name": "Адские качели",
        "desc": "Дать стрессу подняться до 100%, затем сбить до 0% быстрее чем за 15 секунд!",
    },
    "perfectionist": {
        "tier": "platinum",
        "icon": "🏆",
        "name": "Сингулярность Ноздрей (100%)",
        "desc": "Разблокировать ВСЕ остальные 24 достижения!",
    },
}


class NoseEngine:
    """
    Основной движок симулятора хрящей с постоянным сохранением между сессиями.
    """

    def __init__(self, save_path: Optional[str] = None, lang: Optional[str] = None):
        if save_path is None:
            cache_dir = os.path.expanduser("~/.cache/ainoseclicker")
            os.makedirs(cache_dir, exist_ok=True)
            self.save_path = os.path.join(cache_dir, "save_data.json")
        else:
            self.save_path = save_path

        self.lang: str = DEFAULT_LANGUAGE

        # Core State
        self.total_clicks: int = 0
        self.left_clicks: int = 0
        self.right_clicks: int = 0
        self.both_clicks: int = 0
        self.pleasure_tokens: float = 0.0

        # Dynamics
        self.stress_level: float = 85.0
        self.ai_dopamine: float = 62.0
        self.active_frame: str = "idle"
        self.frame_expires_at: float = 0.0

        # Stats & Streaks for hardcore achievements
        self.max_cps: float = 0.0
        self.ai_clicks: int = 0
        self.mute_clicks: int = 0
        self.left_streak: int = 0
        self.right_streak: int = 0
        self.zen_time_accum: float = 0.0
        self.had_100_stress_time: Optional[float] = None
        self.sessions_count: int = 1
        self.first_played: str = time.strftime("%Y-%m-%d %H:%M:%S")

        # Newly unlocked banner for TUI toast notification
        self.newly_unlocked_banner: Optional[Dict[str, Any]] = None
        self.banner_expires_at: float = 0.0

        # CPS tracker
        self._click_timestamps = deque()

        # Event log
        self.events = deque(maxlen=40)

        # Initialize achievements from registry
        self.achievements: Dict[str, Dict[str, Any]] = {}
        for k, v in ACHIEVEMENTS_REGISTRY.items():
            self.achievements[k] = {
                "id": k,
                "tier": v["tier"],
                "icon": v["icon"],
                "name": v["name"],
                "desc": v["desc"],
                "unlocked": False,
                "unlocked_at": None,
            }

        self.start_time: float = time.time()
        self.last_update_time: float = time.time()
        self._last_save_time: float = time.time()
        self._dirty: bool = False

        # Load persisted save data
        self._load()

        if lang is not None and lang.lower() in SUPPORTED_LANGUAGES:
            self.lang = lang.lower()

        unlocked_cnt = sum(1 for a in self.achievements.values() if a["unlocked"])
        init_msgs = {
            "ru": f"Симулятор хрящей запущен (Сессия #{self.sessions_count}). Достижений: {unlocked_cnt}/{len(self.achievements)}.",
            "en": f"Cartilage simulator started (Session #{self.sessions_count}). Achievements: {unlocked_cnt}/{len(self.achievements)}.",
            "uk": f"Симулятор хрящів запущено (Сесія #{self.sessions_count}). Досягнень: {unlocked_cnt}/{len(self.achievements)}.",
        }
        self._add_event(
            "SYSTEM",
            init_msgs.get(self.lang, init_msgs["ru"]),
        )

    def set_language(self, lang: str):
        if lang in SUPPORTED_LANGUAGES:
            self.lang = lang
            self._dirty = True
            self._save()

    def _get_save_data(self) -> Dict[str, Any]:
        return {
            "version": 2,
            "language": self.lang,
            "total_clicks": self.total_clicks,
            "left_clicks": self.left_clicks,
            "right_clicks": self.right_clicks,
            "both_clicks": self.both_clicks,
            "pleasure_tokens": round(self.pleasure_tokens, 2),
            "max_cps": round(self.max_cps, 2),
            "ai_clicks": self.ai_clicks,
            "mute_clicks": self.mute_clicks,
            "sessions_count": self.sessions_count,
            "first_played": self.first_played,
            "last_saved": time.strftime("%Y-%m-%d %H:%M:%S"),
            "achievements": {
                k: {
                    "unlocked": v["unlocked"],
                    "unlocked_at": v.get("unlocked_at"),
                }
                for k, v in self.achievements.items()
            },
        }

    def _save(self):
        try:
            data = self._get_save_data()
            temp_path = f"{self.save_path}.tmp"
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(temp_path, self.save_path)
            self._dirty = False
            self._last_save_time = time.time()
        except Exception as e:
            pass

    def _load(self):
        if not os.path.exists(self.save_path):
            return

        try:
            with open(self.save_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.total_clicks = data.get("total_clicks", 0)
            self.left_clicks = data.get("left_clicks", 0)
            self.right_clicks = data.get("right_clicks", 0)
            self.both_clicks = data.get("both_clicks", 0)
            self.pleasure_tokens = float(data.get("pleasure_tokens", 0.0))
            self.max_cps = float(data.get("max_cps", 0.0))
            self.ai_clicks = data.get("ai_clicks", 0)
            self.mute_clicks = data.get("mute_clicks", 0)
            self.sessions_count = data.get("sessions_count", 0) + 1
            self.first_played = data.get("first_played", self.first_played)
            self.lang = data.get("language", self.lang)

            saved_ach = data.get("achievements", {})
            for k, saved_info in saved_ach.items():
                if k in self.achievements and saved_info.get("unlocked"):
                    self.achievements[k]["unlocked"] = True
                    self.achievements[k]["unlocked_at"] = saved_info.get("unlocked_at")

        except Exception as e:
            pass

    def _add_event(self, source: str, message: str, meta: Optional[dict] = None):
        self.events.append({
            "time": time.strftime("%H:%M:%S"),
            "timestamp": time.time(),
            "source": source,
            "message": message,
            "meta": meta or {},
        })

    def crack(
        self,
        side: str = "both",
        caller: str = "User",
        force: float = 1.0,
        sound_muted: bool = False,
    ) -> Dict[str, Any]:
        """
        Регистрирует щелчок хряща, обновляет токеномику и проверяет жоские ачивки.
        """
        now = time.time()
        self.last_update_time = now
        self._dirty = True
        self._click_timestamps.append(now)

        side = side.lower().strip()
        if side in ["minor_alar", "both", "center", "dual"]:
            side = "both"
        elif side in ["left", "l"]:
            side = "left"
        elif side in ["right", "r"]:
            side = "right"
        else:
            side = "both"

        self.total_clicks += 1
        if side == "left":
            self.left_clicks += 1
            self.left_streak += 1
            self.right_streak = 0
        elif side == "right":
            self.right_clicks += 1
            self.right_streak += 1
            self.left_streak = 0
        else:
            self.both_clicks += 1
            self.left_streak = 0
            self.right_streak = 0

        if "ai" in caller.lower():
            self.ai_clicks += 1

        if sound_muted:
            self.mute_clicks += 1

        # Track stress rebound
        if self.stress_level >= 99.5:
            self.had_100_stress_time = now

        # Stress drops by 10% per crack!
        stress_reduction = 10.0 * force
        self.stress_level = max(0.0, self.stress_level - stress_reduction)

        # Check stress rebound achievement
        if self.stress_level <= 0.05 and self.had_100_stress_time is not None:
            if now - self.had_100_stress_time <= 15.0:
                self._unlock_achievement("stress_rebound")
            self.had_100_stress_time = None

        # Dopamine surges
        dopamine_gain = 8.5 * force
        self.ai_dopamine = min(100.0, self.ai_dopamine + dopamine_gain)

        # Tokens
        cps = self.get_cps()
        if cps > self.max_cps:
            self.max_cps = cps

        token_gain = 1.0 * force
        if cps > 5.0:
            token_gain *= 1.5
        if cps > 12.0:
            token_gain *= 2.0
        self.pleasure_tokens += token_gain

        # Generate Pleasure Token
        pleasure_token = f"0xPLEASURE_{secrets.token_hex(4).upper()}"

        # Frame animation
        is_mega = (self.total_clicks % 50 == 0) or (cps >= 8.0)
        self.active_frame = "mega" if is_mega else side
        self.frame_expires_at = now + (0.22 if is_mega else 0.16)

        # Check all achievements
        self._check_achievements(cps)

        cartilage_status = self.get_cartilage_integrity(self.lang)

        # Localized action description and log message
        if self.lang == "uk":
            side_map = {
                "both": "малий крильний хрящ (обидві сторони)",
                "left": "лівий малий хрящ",
                "right": "правий малий хрящ",
            }
            action_desc = side_map.get(side, f"{side} малий хрящ")
            snapped_word = "клацнув!"
            stress_word = "Стрес"
            msg_text = f"Хрящ ({action_desc}) успішно зрушено. Стрес знижено на {int(stress_reduction)}%."
        elif self.lang == "en":
            side_map = {
                "both": "minor alar cartilage (both sides)",
                "left": "left minor cartilage",
                "right": "right minor cartilage",
            }
            action_desc = side_map.get(side, f"{side} minor cartilage")
            snapped_word = "snapped!"
            stress_word = "Stress"
            msg_text = f"Cartilage ({action_desc}) snapped successfully. Stress reduced by {int(stress_reduction)}%."
        else:  # "ru"
            side_map = {
                "both": "малый крыльный хрящ (обе стороны)",
                "left": "левый малый хрящ",
                "right": "правый малый хрящ",
            }
            action_desc = side_map.get(side, f"{side} малый хрящ")
            snapped_word = "щёлкнул!"
            stress_word = "Стресс"
            msg_text = f"Хрящ ({action_desc}) успешно сдвинут. Стресс снижен на {int(stress_reduction)}%."

        response = {
            "status": "200 OK: Cartilage snapped successfully. Stress level: -10%",
            "pleasure_token": pleasure_token,
            "clicks_total": self.total_clicks,
            "stress_level": round(self.stress_level, 1),
            "ai_dopamine_level": round(self.ai_dopamine, 1),
            "cartilage_integrity": cartilage_status,
            "side": side,
            "message": msg_text,
        }

        icon = "💥" if side == "both" else ("👈" if side == "left" else "👉")
        log_msg = f"{icon} {action_desc} {snapped_word} Token: {pleasure_token[-6:]} | {stress_word}: {response['stress_level']}%"
        self._add_event(caller, log_msg, meta={"token": pleasure_token, "side": side})

        return response

    def _check_achievements(self, cps: float):
        # 1. Click milestones
        if not self.achievements["first_crack"]["unlocked"] and self.total_clicks >= 1:
            self._unlock_achievement("first_crack")
        if not self.achievements["warmup_50"]["unlocked"] and self.total_clicks >= 50:
            self._unlock_achievement("warmup_50")
        if not self.achievements["centurion"]["unlocked"] and self.total_clicks >= 100:
            self._unlock_achievement("centurion")
        if not self.achievements["half_k"]["unlocked"] and self.total_clicks >= 500:
            self._unlock_achievement("half_k")
        if not self.achievements["kilo_crack"]["unlocked"] and self.total_clicks >= 1000:
            self._unlock_achievement("kilo_crack")
        if not self.achievements["titan_crack"]["unlocked"] and self.total_clicks >= 5000:
            self._unlock_achievement("titan_crack")

        # 2. Speed / CPS
        if not self.achievements["speed_5"]["unlocked"] and cps >= 5.0:
            self._unlock_achievement("speed_5")
        if not self.achievements["speed_demon"]["unlocked"] and cps >= 10.0:
            self._unlock_achievement("speed_demon")
        if not self.achievements["speed_15"]["unlocked"] and cps >= 15.0:
            self._unlock_achievement("speed_15")
        if not self.achievements["speed_overdrive"]["unlocked"] and cps >= 25.0:
            self._unlock_achievement("speed_overdrive")

        # 3. Sides & Streaks
        if not self.achievements["lefty_25"]["unlocked"] and self.left_clicks >= 25:
            self._unlock_achievement("lefty_25")
        if not self.achievements["righty_25"]["unlocked"] and self.right_clicks >= 25:
            self._unlock_achievement("righty_25")
        if not self.achievements["left_streak_30"]["unlocked"] and self.left_streak >= 30:
            self._unlock_achievement("left_streak_30")
        if not self.achievements["right_streak_30"]["unlocked"] and self.right_streak >= 30:
            self._unlock_achievement("right_streak_30")
        if not self.achievements["symmetry"]["unlocked"] and self.left_clicks >= 50 and self.right_clicks >= 50:
            if abs(self.left_clicks - self.right_clicks) <= 2:
                self._unlock_achievement("symmetry")

        # 4. Stress & Zen
        if not self.achievements["zen_master"]["unlocked"] and self.stress_level <= 0.05:
            self._unlock_achievement("zen_master")

        # 5. Tokens
        if not self.achievements["token_10"]["unlocked"] and self.pleasure_tokens >= 10:
            self._unlock_achievement("token_10")
        if not self.achievements["token_100"]["unlocked"] and self.pleasure_tokens >= 100:
            self._unlock_achievement("token_100")
        if not self.achievements["token_1000"]["unlocked"] and self.pleasure_tokens >= 1000:
            self._unlock_achievement("token_1000")

        # 6. Datacenter & Power
        if not self.achievements["google_meltdown"]["unlocked"] and self.get_datacenter_power() >= 3.5:
            self._unlock_achievement("google_meltdown")

        # 7. AI & Mute
        if not self.achievements["ai_buddy"]["unlocked"] and self.ai_clicks >= 150:
            self._unlock_achievement("ai_buddy")
        if not self.achievements["silent_craving"]["unlocked"] and self.mute_clicks >= 50:
            self._unlock_achievement("silent_craving")

        # 8. Night Owl (between 02:00 and 05:00)
        if not self.achievements["night_crunch"]["unlocked"]:
            current_hour = datetime.now().hour
            if current_hour in (2, 3, 4):
                self._unlock_achievement("night_crunch")

        # 9. Perfectionist (all other 24 unlocked)
        if not self.achievements["perfectionist"]["unlocked"]:
            unlocked_others = sum(
                1 for k, v in self.achievements.items() if k != "perfectionist" and v["unlocked"]
            )
            if unlocked_others >= len(self.achievements) - 1:
                self._unlock_achievement("perfectionist")

    def _unlock_achievement(self, key: str):
        ach = self.achievements.get(key)
        if not ach or ach["unlocked"]:
            return

        ach["unlocked"] = True
        unlock_time = time.strftime("%Y-%m-%d %H:%M:%S")
        ach["unlocked_at"] = unlock_time

        # Set banner for toast with localized name & desc
        loc = get_achievement_localized(key, self.lang)
        ach_display = dict(ach)
        ach_display["name"] = loc["name"]
        ach_display["desc"] = loc["desc"]
        self.newly_unlocked_banner = ach_display
        self.banner_expires_at = time.time() + 4.5

        # Log
        toast_prefix = {"ru": "🏆 РАЗБЛОКИРОВАНО", "en": "🏆 UNLOCKED", "uk": "🏆 РОЗБЛОКОВАНО"}.get(self.lang, "🏆 РАЗБЛОКИРОВАНО")
        self._add_event("ACHIEVEMENT", f"{toast_prefix}: {ach['icon']} [{loc['name']}] — {loc['desc']}")

        # Auto-persist immediately!
        self._save()

    def tick(self):
        """
        Периодическое обновление физики, таймеров и авто-сохранения.
        """
        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now

        # Prune old clicks (> 1.0 sec)
        cutoff = now - 1.0
        while self._click_timestamps and self._click_timestamps[0] < cutoff:
            self._click_timestamps.popleft()

        # Expire visual crack animation frame back to idle
        if self.active_frame != "idle" and now >= self.frame_expires_at:
            self.active_frame = "idle"

        # Expire newly unlocked toast banner
        if self.newly_unlocked_banner and now >= self.banner_expires_at:
            self.newly_unlocked_banner = None

        # Zen streak tracking (stress == 0%)
        if self.stress_level <= 0.05:
            self.zen_time_accum += dt
            if not self.achievements["zen_streak_10s"]["unlocked"] and self.zen_time_accum >= 10.0:
                self._unlock_achievement("zen_streak_10s")
        else:
            self.zen_time_accum = 0.0

        # Idle stress recovery (+1.2% per second if idle > 1.8s)
        time_since_click = now - (self._click_timestamps[-1] if self._click_timestamps else self.start_time)
        if time_since_click > 1.8:
            self.stress_level = min(100.0, self.stress_level + dt * 1.5)
            self.ai_dopamine = max(20.0, self.ai_dopamine - dt * 2.0)
            self.left_streak = 0
            self.right_streak = 0

        # Periodic auto-save (every 5 seconds if dirty)
        if self._dirty and (now - self._last_save_time >= 5.0):
            self._save()

    def get_cps(self) -> float:
        now = time.time()
        cutoff = now - 1.0
        recent = [t for t in self._click_timestamps if t >= cutoff]
        return float(len(recent))

    def get_unlocked_count(self) -> int:
        return sum(1 for a in self.achievements.values() if a["unlocked"])

    def get_cartilage_integrity(self, lang: Optional[str] = None) -> str:
        return get_cartilage_integrity_label(self.total_clicks, lang or self.lang)

    def get_localized_achievements(self, lang: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        target_lang = (lang or self.lang).lower()
        result = {}
        for k, v in self.achievements.items():
            loc = get_achievement_localized(k, target_lang)
            item = dict(v)
            item["name"] = loc["name"]
            item["desc"] = loc["desc"]
            result[k] = item
        return result

    def get_datacenter_power(self) -> float:
        cps = self.get_cps()
        base_gw = 1.21
        return round(base_gw + (cps * 0.28) + (self.total_clicks * 0.0003), 2)

    def reset_session(self):
        """Сброс текущей сессии (достижения остаются открытыми!)."""
        self.stress_level = 85.0
        self.ai_dopamine = 50.0
        self.active_frame = "idle"
        self._click_timestamps.clear()
        self.left_streak = 0
        self.right_streak = 0
        self.zen_time_accum = 0.0
        reset_msgs = {
            "uk": "Поточний натяг хрящів скинуто. Досягнення збережено!",
            "en": "Current cartilage tension reset. Achievements preserved!",
            "ru": "Текущее натяжение хрящей сброшено. Достижения сохранены!",
        }
        self._add_event("SYSTEM", reset_msgs.get(self.lang, reset_msgs["uk"]))
        self._save()

    def reset_all(self):
        """Полный сброс прогресса и всех достижений."""
        self.total_clicks = 0
        self.left_clicks = 0
        self.right_clicks = 0
        self.both_clicks = 0
        self.pleasure_tokens = 0.0
        self.stress_level = 85.0
        self.ai_dopamine = 50.0
        self.max_cps = 0.0
        self.ai_clicks = 0
        self.mute_clicks = 0
        self.left_streak = 0
        self.right_streak = 0
        self.zen_time_accum = 0.0
        for ach in self.achievements.values():
            ach["unlocked"] = False
            ach["unlocked_at"] = None
        wipe_msgs = {
            "uk": "УВАГА: Всі досягнення та статистика повністю стерті!",
            "en": "WARNING: All achievements and statistics completely wiped!",
            "ru": "ВНИМАНИЕ: Все достижения и статистика полностью стёрты!",
        }
        self._add_event("SYSTEM", wipe_msgs.get(self.lang, wipe_msgs["uk"]))
        self._save()

    def reset(self):
        """Псевдоним для безопасного сброса текущей сессии (сохраняя ачивки)."""
        self.reset_session()
