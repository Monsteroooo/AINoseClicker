import threading
import time
import random
from typing import Optional, List
from nose_clicker.engine import NoseEngine
from nose_clicker.sound import SoundManager
from nose_clicker.i18n import AI_THOUGHTS_I18N, SPEED_PRESETS_I18N


class AIWorker:
    """
    Автономный фоновый бот, наяривающий хрящом в бесконечном цикле while(alive).
    Поддерживает мультиязычные мысли и скорости (RU, EN, UK).
    """

    def __init__(self, engine: NoseEngine, sound: SoundManager, enabled_initially: bool = False):
        self.engine = engine
        self.sound = sound
        self.enabled = enabled_initially
        self.alive = True
        self.speed_index = 0  # defaults to standard (500ms)
        self.thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._thought_counter = 0

    @property
    def current_preset_name(self) -> str:
        presets = SPEED_PRESETS_I18N.get(self.engine.lang, SPEED_PRESETS_I18N["ru"])
        return presets[self.speed_index][0]

    @property
    def delay_seconds(self) -> float:
        presets = SPEED_PRESETS_I18N.get(self.engine.lang, SPEED_PRESETS_I18N["ru"])
        return presets[self.speed_index][1]

    @property
    def speed_label(self) -> str:
        presets = SPEED_PRESETS_I18N.get(self.engine.lang, SPEED_PRESETS_I18N["ru"])
        return presets[self.speed_index][2]

    def start(self):
        self.alive = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.alive = False
        self.enabled = False

    def toggle(self) -> bool:
        with self._lock:
            self.enabled = not self.enabled
            lang = self.engine.lang
            if lang == "en":
                state_str = "ACTIVATED" if self.enabled else "PAUSED"
                msg = f"Background while(alive) loop {state_str}. Speed: {self.speed_label}"
            elif lang == "uk":
                state_str = "АКТИВОВАНО" if self.enabled else "ПРИЗУПИНЕНО"
                msg = f"Фоновий цикл while(alive) {state_str}. Швидкість: {self.speed_label}"
            else:
                state_str = "АКТИВИРОВАН" if self.enabled else "ПРИОСТАНОВЛЕН"
                msg = f"Фоновый цикл while(alive) {state_str}. Скорость: {self.speed_label}"

            self.engine._add_event("AI-WORKER", msg)
            return self.enabled

    def cycle_speed(self) -> str:
        with self._lock:
            presets = SPEED_PRESETS_I18N.get(self.engine.lang, SPEED_PRESETS_I18N["uk"])
            self.speed_index = (self.speed_index + 1) % len(presets)
            label = self.speed_label
            lang = self.engine.lang
            if lang == "en":
                msg = f"AI speed changed to: {label}"
            elif lang == "uk":
                msg = f"Швидкість AI змінена на: {label}"
            else:
                msg = f"Скорость AI изменена на: {label}"

            self.engine._add_event("AI-SPEED", msg)
            return label

    def _run_loop(self):
        while self.alive:
            if not self.enabled:
                time.sleep(0.1)
                continue

            # Weighted choice: both, left, or right
            side = random.choices(["both", "left", "right"], weights=[0.45, 0.275, 0.275])[0]

            # Crack!
            res = self.engine.crack(side=side, caller="AI-Worker", force=1.0, sound_muted=self.sound.muted)
            self.sound.play(side)

            self._thought_counter += 1
            if self._thought_counter >= (8 if self.current_preset_name != "meltdown" else 25):
                self._thought_counter = 0
                thoughts = AI_THOUGHTS_I18N.get(self.engine.lang, AI_THOUGHTS_I18N["ru"])
                thought = random.choice(thoughts)
                self.engine._add_event("AI-THOUGHT", f'"{thought}"')

            time.sleep(self.delay_seconds)
