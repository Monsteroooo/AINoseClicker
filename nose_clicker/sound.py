import sys
import os
import wave
import math
import struct
import random
import shutil
import subprocess
import threading
import hashlib
import time
from typing import Optional, Dict


class SoundManager:
    """
    Процедурный генератор и проигрыватель приятных ASMR стерео-звуков хруста хрящей.
    Также поддерживает пользовательские аудиофайлы (.wav, .mp3, .ogg, .flac, .m4a)
    из папки custom_sounds/ или через параметр --sound.
    """

    SOUND_VERSION = "v2"

    def __init__(
        self,
        sounds_dir: Optional[str] = None,
        custom_sound: Optional[str] = None,
        muted: bool = False,
    ):
        self.muted = muted
        if sounds_dir is None:
            self.sounds_dir = os.path.expanduser(f"~/.cache/ainoseclicker_sounds_{self.SOUND_VERSION}")
        else:
            self.sounds_dir = sounds_dir

        os.makedirs(self.sounds_dir, exist_ok=True)
        self.player_cmd = self._detect_player()
        self.custom_map: Dict[str, str] = self._resolve_custom_sounds(custom_sound)
        self._ensure_sounds()
        self._last_play_time = 0.0
        self._min_interval = 0.030  # Max ~33 sounds/sec

    @property
    def has_custom_sound(self) -> bool:
        return bool(self.custom_map)

    def _detect_player(self) -> Optional[str]:
        if sys.platform == "win32":
            try:
                import winsound
                return "winsound"
            except ImportError:
                pass

        if sys.platform == "darwin":
            if shutil.which("afplay"):
                return "afplay"

        for candidate in ["pw-play", "paplay", "aplay", "ffplay"]:
            path = shutil.which(candidate)
            if path:
                return candidate
        return None

    def _ensure_playable_wav(self, src_path: str) -> str:
        """
        Если файл в формате mp3/ogg/flac/m4a, конвертирует его в чистый WAV через ffmpeg
        в кеш-директорию, чтобы плееры (в т.ч. aplay/paplay) воспроизводили его мгновенно.
        """
        src_path = os.path.abspath(os.path.expanduser(src_path))
        if not os.path.exists(src_path):
            return src_path

        if src_path.lower().endswith(".wav"):
            return src_path

        # Need conversion to WAV
        src_hash = hashlib.md5(f"{src_path}_{os.path.getmtime(src_path)}".encode()).hexdigest()[:10]
        dst_wav = os.path.join(self.sounds_dir, f"custom_{src_hash}.wav")

        if not os.path.exists(dst_wav) or os.path.getsize(dst_wav) < 100:
            if shutil.which("ffmpeg"):
                try:
                    subprocess.run(
                        ["ffmpeg", "-y", "-i", src_path, "-ar", "44100", "-ac", "2", dst_wav],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=5.0,
                    )
                except Exception:
                    return src_path
            else:
                return src_path

        return dst_wav if os.path.exists(dst_wav) else src_path

    def _resolve_custom_sounds(self, custom_path: Optional[str]) -> Dict[str, str]:
        valid_exts = (".wav", ".mp3", ".ogg", ".flac", ".m4a", ".aac", ".opus", ".webm")
        mapping: Dict[str, str] = {}

        candidate_dir = None
        if custom_path:
            p = os.path.expanduser(custom_path)
            if os.path.isfile(p):
                wav_path = self._ensure_playable_wav(p)
                return {"center": wav_path, "left": wav_path, "right": wav_path, "mega": wav_path}
            elif os.path.isdir(p):
                candidate_dir = p

        if not candidate_dir and os.path.isdir("custom_sounds"):
            candidate_dir = "custom_sounds"

        if candidate_dir and os.path.isdir(candidate_dir):
            try:
                files = [
                    os.path.join(candidate_dir, f)
                    for f in sorted(os.listdir(candidate_dir))
                    if f.lower().endswith(valid_exts)
                ]
                if files:
                    # 1. Exact base matches take top priority
                    for f in files:
                        base = os.path.splitext(os.path.basename(f))[0].lower()
                        conv = self._ensure_playable_wav(f)
                        if base in ("left", "snap_left"):
                            mapping["left"] = conv
                        elif base in ("right", "snap_right"):
                            mapping["right"] = conv
                        elif base in ("center", "both", "snap_center"):
                            mapping["center"] = conv
                        elif base in ("mega", "snap_mega"):
                            mapping["mega"] = conv

                    # 2. Substring matches for any unassigned
                    for f in files:
                        base = os.path.splitext(os.path.basename(f))[0].lower()
                        conv = self._ensure_playable_wav(f)
                        if "left" in base and "left" not in mapping:
                            mapping["left"] = conv
                        elif "right" in base and "right" not in mapping:
                            mapping["right"] = conv
                        elif "mega" in base and "mega" not in mapping:
                            mapping["mega"] = conv
                        elif any(k in base for k in ["center", "both", "snap", "crack", "nose", "pop", "click"]) and "center" not in mapping:
                            mapping["center"] = conv

                    # 3. Fallback to first file for any still unassigned
                    first_file = mapping.get("center") or self._ensure_playable_wav(files[0])
                    for k in ["center", "left", "right", "mega"]:
                        mapping.setdefault(k, first_file)
            except Exception:
                pass

        return mapping

    def _ensure_sounds(self):
        sides = ["center", "left", "right", "mega"]
        for side in sides:
            for var in range(3):
                filename = f"snap_{side}_{var}.wav"
                path = os.path.join(self.sounds_dir, filename)
                if not os.path.exists(path) or os.path.getsize(path) < 100:
                    self._generate_pleasant_sound(path, side, var)

    def _generate_pleasant_sound(self, path: str, side: str, var: int = 0, sample_rate: int = 44100):
        duration = 0.092 if side != "mega" else 0.130
        num_samples = int(sample_rate * duration)
        frames = bytearray()

        # Stereo spatialization
        if side == "left":
            pan_l, pan_r = 1.0, 0.32
        elif side == "right":
            pan_l, pan_r = 0.32, 1.0
        else:
            pan_l, pan_r = 0.96, 0.96

        rnd = random.Random(hash(f"{side}_{var}_{self.SOUND_VERSION}") & 0xFFFFFFFF)
        pitch_jitter = 1.0 + (rnd.random() - 0.5) * 0.10

        for i in range(num_samples):
            t = i / sample_rate

            # 1. Warm low body 'thump' (155Hz -> 72Hz gentle resonant decay)
            thump_env = math.exp(-t * (52.0 if side != "mega" else 40.0))
            thump_freq = (155.0 * math.exp(-t * 38.0) + 72.0) * pitch_jitter
            thump = math.sin(2.0 * math.pi * thump_freq * t) * thump_env * 0.48

            # 2. Organic cartilage snap transient (smooth pitch glide 680Hz -> 210Hz)
            snap_env = math.exp(-t * (92.0 if side != "mega" else 68.0))
            snap_freq = (680.0 * math.exp(-t * 65.0) + 210.0) * pitch_jitter
            phase = 2.0 * math.pi * snap_freq * t
            snap = (math.sin(phase) * 0.46 + math.sin(phase * 2.0) * 0.20 + math.sin(phase * 3.0) * 0.08) * snap_env

            # 3. Micro cavitation pops (soft ASMR air/cartilage bubbles)
            micro = 0.0
            t1 = 0.011 + rnd.uniform(-0.002, 0.002)
            if abs(t - t1) < 0.006:
                micro += (math.sin(2.0 * math.pi * 950.0 * t)) * math.exp(-((t - t1) ** 2) / 0.00004) * 0.30

            t2 = 0.024 + rnd.uniform(-0.003, 0.003)
            if abs(t - t2) < 0.008:
                micro += (math.sin(2.0 * math.pi * 620.0 * t)) * math.exp(-((t - t2) ** 2) / 0.00006) * 0.25

            if side == "mega":
                t3 = 0.042
                if abs(t - t3) < 0.010:
                    micro += (math.sin(2.0 * math.pi * 480.0 * t)) * math.exp(-((t - t3) ** 2) / 0.00008) * 0.35

            # 4. Soft initial pressure-release tick (first 1.2ms)
            tick = 0.0
            if i < 22:
                tick = ((1.0 - i / 22.0) ** 2.0) * 0.38

            sig = thump + snap + micro + tick
            # Analog tape saturation: warm tanh rounding, no harsh clipping
            sig = math.tanh(sig * 1.30)

            # 16-bit stereo PCM
            sample_l = int(max(-32767, min(32767, sig * pan_l * 28500)))
            sample_r = int(max(-32767, min(32767, sig * pan_r * 28500)))
            frames.extend(struct.pack("<hh", sample_l, sample_r))

        with wave.open(path, "wb") as f:
            f.setnchannels(2)
            f.setsampwidth(2)
            f.setframerate(sample_rate)
            f.writeframes(frames)

    def play(self, sound_type: str = "center"):
        if self.muted or not self.player_cmd:
            return

        now = time.time()
        if now - self._last_play_time < self._min_interval:
            return
        self._last_play_time = now

        if sound_type not in ["left", "right", "center", "mega"]:
            sound_type = "center"

        # Check if user provided custom sound
        if self.custom_map and sound_type in self.custom_map:
            filepath = self.custom_map[sound_type]
            if os.path.exists(filepath):
                threading.Thread(target=self._play_subprocess, args=(filepath,), daemon=True).start()
                return

        # Fallback to procedural variations
        var = random.randint(0, 2)
        filename = f"snap_{sound_type}_{var}.wav"
        filepath = os.path.join(self.sounds_dir, filename)

        if not os.path.exists(filepath):
            filepath = os.path.join(self.sounds_dir, f"snap_{sound_type}_0.wav")
            if not os.path.exists(filepath):
                return

        # Fire and forget playback thread
        threading.Thread(target=self._play_subprocess, args=(filepath,), daemon=True).start()

    def _play_subprocess(self, filepath: str):
        try:
            if self.player_cmd == "winsound":
                import winsound
                winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
            elif self.player_cmd == "afplay":
                subprocess.run(["afplay", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1.0)
            elif self.player_cmd == "ffplay":
                cmd = ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", filepath]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1.0)
            elif self.player_cmd:
                cmd = [self.player_cmd, filepath]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1.0)
        except Exception:
            pass

    def toggle_mute(self) -> bool:
        self.muted = not self.muted
        return self.muted
