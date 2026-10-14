import sys
import os
import time
import atexit
from typing import Optional

if sys.platform == "win32":
    import msvcrt
    termios = None
    tty = None
    select = None
else:
    import termios
    import tty
    import select
    msvcrt = None

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live

from nose_clicker.engine import NoseEngine
from nose_clicker.sound import SoundManager
from nose_clicker.ai_worker import AIWorker
from nose_clicker.ascii_art import render_nose_art, render_bar
from nose_clicker.i18n import t, cycle_language


class NoseClickerApp:
    def __init__(
        self,
        engine: NoseEngine,
        sound: SoundManager,
        ai_worker: AIWorker,
        api_host: str = "127.0.0.1",
        api_port: int = 8088,
        api_enabled: bool = True,
    ):
        self.engine = engine
        self.sound = sound
        self.ai_worker = ai_worker
        self.api_host = api_host
        self.api_port = api_port
        self.api_enabled = api_enabled

        self.console = Console()
        self.running = False
        self.show_achievements = False
        self.ach_tab = 0
        self.ach_scroll = 0
        self._orig_termios = None
        self._is_tty = sys.stdin.isatty()
        self._fd = sys.stdin.fileno() if (self._is_tty and sys.platform != "win32") else None

    def _setup_terminal(self):
        if sys.platform == "win32":
            # Enable ANSI escape code processing on Windows 10/11 CMD and PowerShell
            os.system("")
        elif self._is_tty and self._fd is not None and termios and tty:
            self._orig_termios = termios.tcgetattr(self._fd)
            tty.setcbreak(self._fd)
            atexit.register(self._restore_terminal)

    def _restore_terminal(self):
        if sys.platform != "win32" and self._orig_termios and self._is_tty and self._fd is not None and termios:
            try:
                termios.tcsetattr(self._fd, termios.TCSADRAIN, self._orig_termios)
            except Exception:
                pass

    def _read_key(self) -> Optional[str]:
        if not self._is_tty:
            return None

        # --- Windows implementation using msvcrt ---
        if sys.platform == "win32" and msvcrt:
            if not msvcrt.kbhit():
                return None
            try:
                ch = msvcrt.getwch()
            except Exception:
                return None

            # Case 1: Standard MSVCRT extended key prefix (\x00 or \xe0)
            if ch in ("\x00", "\xe0"):
                try:
                    ch2 = msvcrt.getwch()
                except Exception:
                    return None
                if ch2 in ("K", "k", "s", "4"):  # K = Left, s = Ctrl+Left
                    return "LEFT"
                elif ch2 in ("M", "m", "t", "6"): # M = Right, t = Ctrl+Right
                    return "RIGHT"
                elif ch2 in ("H", "h", "w", "8"): # H = Up
                    return "UP"
                elif ch2 in ("P", "p", "z", "2"): # P = Down
                    return "DOWN"
                elif ch2 in ("I", "i"):
                    return "PGUP"
                elif ch2 in ("Q", "q"):
                    return "PGDN"
                return None

            # Case 2: Windows Terminal ANSI escape sequences (\x1b[D, \x1b[C, etc.)
            if ch == "\x1b":
                seq = ""
                time.sleep(0.003)
                while msvcrt.kbhit():
                    try:
                        seq += msvcrt.getwch()
                    except Exception:
                        break
                if seq:
                    if seq in ("[D", "OD", "[1;5D", "[1;2D") or seq.endswith("D"):
                        return "LEFT"
                    elif seq in ("[C", "OC", "[1;5C", "[1;2C") or seq.endswith("C"):
                        return "RIGHT"
                    elif seq in ("[A", "OA", "[1;5A", "[1;2A") or seq.endswith("A"):
                        return "UP"
                    elif seq in ("[B", "OB", "[1;5B", "[1;2B") or seq.endswith("B"):
                        return "DOWN"
                    elif seq in ("[5~", "[5^"):
                        return "PGUP"
                    elif seq in ("[6~", "[6^"):
                        return "PGDN"
                    return None
                return "ESC"

            return ch

        # --- POSIX implementation (Linux, macOS) using direct fd select & read ---
        if self._fd is None:
            return None

        r, _, _ = select.select([self._fd], [], [], 0)
        if not r:
            return None

        try:
            raw = os.read(self._fd, 32)
        except Exception:
            return None

        if not raw:
            return None

        if raw.startswith(b"\x1b"):
            if raw == b"\x1b":
                r2, _, _ = select.select([self._fd], [], [], 0.035)
                if r2:
                    try:
                        raw += os.read(self._fd, 31)
                    except Exception:
                        pass

            # Arrow keys standard (\x1b[D / \x1b[C) and application mode (\x1bOD / \x1bOC)
            if raw in (b"\x1b[D", b"\x1bOD") or raw.endswith(b"D"):
                return "LEFT"
            elif raw in (b"\x1b[C", b"\x1bOC") or raw.endswith(b"C"):
                return "RIGHT"
            elif raw in (b"\x1b[A", b"\x1bOA") or raw.endswith(b"A"):
                return "UP"
            elif raw in (b"\x1b[B", b"\x1bOB") or raw.endswith(b"B"):
                return "DOWN"
            elif raw in (b"\x1b[5~", b"\x1b[[5~"):
                return "PGUP"
            elif raw in (b"\x1b[6~", b"\x1b[[6~"):
                return "PGDN"
            elif raw == b"\x1b":
                return "ESC"
            return None

        try:
            return raw.decode("utf-8", errors="ignore")
        except Exception:
            return None

    def _build_achievements_layout(self) -> Layout:
        lang = self.engine.lang
        w = self.console.width
        h = self.console.height

        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=3),
        )

        unlocked_cnt = self.engine.get_unlocked_count()
        total_cnt = len(self.engine.achievements)
        pct = int((unlocked_cnt / total_cnt) * 100) if total_cnt else 0

        # 1. Header
        header_text = Text()
        header_text.append(t("hall_of_fame_title", lang), style="bold bright_yellow")
        header_text.append(f"[{unlocked_cnt}/{total_cnt} | {pct}%]", style="bold bright_green")
        header_panel = Panel(
            header_text,
            style="bold yellow",
            subtitle=t("hall_of_fame_subtitle", lang, save_path=self.engine.save_path),
        )
        layout["header"].update(header_panel)

        # 2. Tabs & Achievements Filtering
        all_achs = list(self.engine.get_localized_achievements(lang).values())
        tab_filters = [
            [a for a in all_achs if a["tier"] in ["bronze", "silver"]],
            [a for a in all_achs if a["tier"] in ["gold", "platinum"]],
            all_achs,
        ]

        if not (0 <= self.ach_tab < len(tab_filters)):
            self.ach_tab = 0

        current_achs = tab_filters[self.ach_tab]

        tab_labels = [
            f"[1] {t('tab_bronze_silver', lang, count=len(tab_filters[0]))}",
            f"[2] {t('tab_gold_plat', lang, count=len(tab_filters[1]))}",
            f"[3] {t('tab_all', lang, count=len(tab_filters[2]))}",
        ]

        tabs_text = Text()
        for idx, label in enumerate(tab_labels):
            if idx == self.ach_tab:
                tabs_text.append(f" {label} ", style="bold black on bright_yellow")
            else:
                tabs_text.append(f" {label} ", style="bold dim white on #222222")
            tabs_text.append("  ")

        # 3. Dynamic row calculation & Table
        # console height - header(3) - footer(3) - panel borders(2) - table header & divider(2)
        avail_rows = max(5, h - 10)
        total_items = len(current_achs)
        max_scroll = max(0, total_items - avail_rows)
        self.ach_scroll = max(0, min(self.ach_scroll, max_scroll))
        visible_achs = current_achs[self.ach_scroll : self.ach_scroll + avail_rows]

        table = Table.grid(padding=(0, 1), expand=True)
        table.add_column("icon", width=3, justify="center")
        name_w = 26 if w >= 100 else 23
        table.add_column("name", width=name_w, no_wrap=True)
        table.add_column("desc", ratio=1)
        date_w = 16 if w >= 105 else 11
        table.add_column("date", width=date_w, justify="right")

        # Table Header Row
        col_icon = "✔"
        col_ach = t("col_achievement", lang)
        col_dsc = t("col_desc", lang)
        col_unl = t("col_unlocked", lang)
        table.add_row(
            f"[bold bright_cyan]{col_icon}[/]",
            f"[bold bright_cyan]{col_ach}[/]",
            f"[bold bright_cyan]{col_dsc}[/]",
            f"[bold bright_cyan]{col_unl}[/]",
        )
        # Divider Row
        table.add_row(
            "[dim white]──[/]",
            f"[dim white]{'─' * name_w}[/]",
            "[dim white]──────────────────────────────────────[/]",
            f"[dim white]{'─' * date_w}[/]",
        )

        for a in visible_achs:
            icon = "✅" if a["unlocked"] else "🔒"
            name_style = "bold bright_green" if a["unlocked"] else "dim white"
            name_cell = f"[{name_style}]{a['icon']} {a['name']}[/]"

            desc_style = "white" if a["unlocked"] else "dim"
            desc_cell = f"[{desc_style}]{a['desc']}[/]"

            if a["unlocked"] and a.get("unlocked_at"):
                raw_dt = a["unlocked_at"].strip()
                parts = raw_dt.split()
                if len(parts) >= 2:
                    ymd, hms = parts[0], parts[1]
                    y, m, d = ymd.split("-")
                    hm = ":".join(hms.split(":")[:2])
                    date_cell = f"{ymd} {hm}" if w >= 105 else f"{d}.{m} {hm}"
                else:
                    date_cell = raw_dt
                date_cell = f"[bright_cyan]{date_cell}[/]"
            else:
                date_cell = "[dim]—[/]"

            table.add_row(icon, name_cell, desc_cell, date_cell)

        # Subtitle with scroll info
        if total_items > avail_rows:
            scroll_info = f"▲ [↑/w] | ▼ [↓/s] ({self.ach_scroll + 1}-{min(self.ach_scroll + avail_rows, total_items)} / {total_items})"
        else:
            scroll_info = f"({total_items} / {total_items})"

        body_panel = Panel(
            table,
            title=tabs_text,
            subtitle=f"[dim bright_yellow]{scroll_info}[/]",
            style="yellow",
            padding=0,
        )
        layout["body"].update(body_panel)

        # 4. Footer
        flag_map = {"uk": "🇺🇦 UA", "en": "🇬🇧 EN", "ru": "🇷🇺 RU"}
        footer_text = Text()
        footer_text.append(" [Tab / 1-3] ", style="bold black on bright_yellow")
        footer_text.append(f" {t('nav_tabs', lang)}    ", style="bold white")
        footer_text.append(" [↑ / ↓] ", style="bold black on bright_cyan")
        footer_text.append(f" {t('nav_scroll', lang)}    ", style="bold white")
        footer_text.append(" [O / Esc / Space] ", style="bold black on bright_green")
        footer_text.append(f" {t('back_to_sim', lang)}    ", style="bold white")
        footer_text.append(" [L] ", style="bold black on bright_magenta")
        footer_text.append(f" {flag_map.get(lang, lang.upper())}    ", style="bold white")
        footer_text.append(" [R] ", style="bold black on bright_cyan")
        footer_text.append(f" {t('reset_session_hint', lang)}    ", style="bold white")
        footer_text.append(" [Q] ", style="bold black on white")
        footer_text.append(f" {t('key_quit', lang)}\n", style="bold white")
        footer_text.append(
            f"  ● {t('stats_all_time', lang, clicks=f'{self.engine.total_clicks:,}', tokens=self.engine.pleasure_tokens, cps=self.engine.max_cps, sessions=self.engine.sessions_count)}",
            style="dim bright_cyan",
        )
        layout["footer"].update(Panel(footer_text, style="dim white"))

        return layout

    def _build_layout(self) -> Layout:
        if self.show_achievements:
            return self._build_achievements_layout()

        lang = self.engine.lang
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=3),
            Layout(name="events", ratio=1, minimum_size=4),
            Layout(name="footer", size=3),
        )
        layout["body"].split_row(
            Layout(name="nose", ratio=50),
            Layout(name="metrics", ratio=50),
        )

        # 1. Header (Normal or Achievement Toast Banner)
        if self.engine.newly_unlocked_banner:
            banner = self.engine.newly_unlocked_banner
            header_text = Text()
            header_text.append(f" {t('new_unlock_toast', lang)} ", style="bold bright_white on dark_green")
            header_text.append(f" {banner['icon']} {banner['name']}: {banner['desc']}", style="bold bright_yellow")
            header_panel = Panel(
                header_text,
                style="bold bright_green",
                subtitle=f"[bold bright_yellow]{t('new_unlock_sub', lang)}[/]",
            )
        else:
            header_text = Text()
            header_text.append(t("app_title", lang), style="bold bright_cyan")
            header_text.append(t("app_subtitle", lang), style="bold white")
            header_panel = Panel(
                header_text,
                style="bold cyan",
                subtitle=f"[dim]{t('header_badge', lang)}[/]",
            )
        layout["header"].update(header_panel)

        # 2. Nose Art Canvas
        cps = self.engine.get_cps()
        show_labels = self.console.width >= 90
        nose_art = render_nose_art(
            frame=self.engine.active_frame,
            stress=self.engine.stress_level,
            dopamine=self.engine.ai_dopamine,
            cps=cps,
            lang=lang,
            show_labels=show_labels,
        )
        nose_panel = Panel(
            nose_art,
            title=f"[bold bright_yellow]{t('model_title', lang)}[/]",
            subtitle=f"[dim]{t('model_subtitle', lang, frame=self.engine.active_frame.upper())}[/]",
            style="cyan",
        )
        layout["body"]["nose"].update(nose_panel)

        # 3. Metrics Panel
        stress_color = "bright_green" if self.engine.stress_level < 35 else ("bright_yellow" if self.engine.stress_level < 70 else "bright_red")
        stress_bar = render_bar(self.engine.stress_level, 100.0, 16, fill_color=stress_color)
        dopamine_bar = render_bar(self.engine.ai_dopamine, 100.0, 16, fill_color="bright_magenta")

        metrics_table = Table.grid(padding=(0, 1))
        metrics_table.add_column(style="bold white", width=24)
        metrics_table.add_column(style="bright_cyan")

        unlocked_cnt = self.engine.get_unlocked_count()
        total_cnt = len(self.engine.achievements)
        pct = int((unlocked_cnt / total_cnt) * 100) if total_cnt else 0

        l_label = {"ru": "Л", "en": "L", "uk": "Л"}.get(lang, "L")
        r_label = {"ru": "П", "en": "R", "uk": "П"}.get(lang, "R")
        metrics_table.add_row(t("total_clicks", lang), f"[bold bright_yellow]{self.engine.total_clicks:,}[/] [dim]({l_label}: {self.engine.left_clicks} | {r_label}: {self.engine.right_clicks})[/]")
        metrics_table.add_row(t("pleasure_tokens", lang), f"[bold bright_green]💎 {self.engine.pleasure_tokens:.1f} PLEASURE[/]")
        metrics_table.add_row(t("stress_level", lang), f"{stress_bar} [bold {stress_color}]{self.engine.stress_level:.0f}%[/] [dim]{t('stress_relief_hint', lang)}[/]")
        metrics_table.add_row(t("ai_dopamine", lang), f"{dopamine_bar} [bold bright_magenta]{self.engine.ai_dopamine:.0f}%[/]")
        metrics_table.add_row(t("cartilage_state", lang), f"[bold white]{self.engine.get_cartilage_integrity(lang)}[/]")
        metrics_table.add_row(t("speed_cps", lang), f"[bold bright_cyan]{cps:.1f}[/] [dim]{t('cps_unit', lang)}[/]")
        metrics_table.add_row(t("datacenter_power", lang), f"[bold yellow]⚡ {self.engine.get_datacenter_power()} GW[/] [dim]{t('google_tpu', lang)}[/]")
        metrics_table.add_row(t("achievements_label", lang), f"[bold bright_yellow]🏆 {unlocked_cnt}/{total_cnt}[/] [dim]({pct}% • [O])[/]")

        # AI Worker Status Badge
        ai_badge = f"[bold bright_green]{t('ai_active', lang)}[/]" if self.ai_worker.enabled else f"[dim white]{t('ai_paused', lang)}[/]"
        metrics_table.add_row(t("ai_auto_snap", lang), f"{ai_badge} [dim]({self.ai_worker.speed_label})[/]")
        
        # Sound status
        if self.sound.muted:
            snd_badge = f"[bold bright_red]{t('sound_muted', lang)}[/]"
        elif self.sound.has_custom_sound:
            snd_badge = f"[bold bright_green]{t('sound_custom', lang)}[/]"
        else:
            snd_badge = f"[bold bright_green]{t('sound_on', lang)}[/]"
        metrics_table.add_row(t("sound_stereo", lang), snd_badge)

        metrics_panel = Panel(
            metrics_table,
            title=f"[bold bright_green]{t('metrics_title', lang)}[/]",
            subtitle=f"[dim]{t('metrics_subtitle', lang)}[/]",
            style="green",
        )
        layout["body"]["metrics"].update(metrics_panel)

        # 4. Live Log Feed
        events_text = Text()
        recent_events = list(self.engine.events)[-5:]
        if not recent_events:
            events_text.append(t("events_empty", lang), style="dim")
        else:
            for ev in recent_events:
                src = ev["source"]
                if src in ["AI-Worker", "AI-SPEED"]:
                    src_style = "bold bright_magenta"
                elif src == "AI-THOUGHT":
                    src_style = "italic bright_cyan"
                elif src == "User":
                    src_style = "bold bright_yellow"
                elif src == "ACHIEVEMENT":
                    src_style = "bold bright_white on blue"
                elif "API" in src:
                    src_style = "bold bright_green"
                else:
                    src_style = "dim cyan"

                events_text.append(f"[{ev['time']}] ", style="dim")
                events_text.append(f"[{src}] ", style=src_style)
                events_text.append(f"{ev['message']}\n", style="white")

        events_panel = Panel(
            events_text,
            title=f"[bold bright_cyan]{t('events_title', lang)}[/]",
            subtitle=f"[dim]{t('events_subtitle', lang)}[/]",
            style="blue",
        )
        layout["events"].update(events_panel)

        # 5. Footer Controls
        if self.api_enabled:
            display_host = self.api_host
            if display_host in ("0.0.0.0", "", "::"):
                try:
                    import socket
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect(("8.8.8.8", 80))
                    display_host = s.getsockname()[0]
                    s.close()
                except Exception:
                    display_host = "127.0.0.1"
            api_status = t("api_phone_link", lang, host=display_host, port=self.api_port)
        else:
            api_status = t("api_disabled", lang)

        flag_map = {"uk": "🇺🇦 UA", "en": "🇬🇧 EN", "ru": "🇷🇺 RU"}
        footer_text = Text()
        footer_text.append(" [Space] ", style="bold black on bright_yellow")
        footer_text.append(f" {t('key_space', lang)}  ", style="bold white")
        footer_text.append(" [← / →] ", style="bold black on bright_yellow")
        footer_text.append(f" {t('key_arrows', lang)}  ", style="bold white")
        footer_text.append(" [A] ", style="bold black on bright_cyan")
        footer_text.append(f" {t('key_ai', lang)}  ", style="bold white")
        footer_text.append(" [S] ", style="bold black on bright_cyan")
        footer_text.append(f" {t('key_speed', lang)}  ", style="bold white")
        footer_text.append(" [O] ", style="bold black on bright_yellow")
        footer_text.append(f" {t('key_achievements', lang)}  ", style="bold white")
        footer_text.append(" [L] ", style="bold black on bright_magenta")
        footer_text.append(f" {flag_map.get(lang, lang.upper())}  ", style="bold white")
        footer_text.append(" [M] ", style="bold black on bright_green")
        footer_text.append(f" {t('key_sound', lang)}  ", style="bold white")
        footer_text.append(" [R] ", style="bold black on bright_red")
        footer_text.append(f" {t('key_reset', lang)}  ", style="bold white")
        footer_text.append(" [Q / Esc] ", style="bold black on white")
        footer_text.append(f" {t('key_quit', lang)}\n", style="bold white")
        footer_text.append(f"  {api_status}", style="bold bright_cyan")

        footer_panel = Panel(footer_text, style="dim white")
        layout["footer"].update(footer_panel)

        return layout

    def run(self):
        self._setup_terminal()
        self.running = True

        try:
            with Live(
                self._build_layout(),
                console=self.console,
                screen=True,
                auto_refresh=False,
                vertical_overflow="crop",
            ) as live:
                while self.running:
                    # Update physics & engine timers
                    self.engine.tick()

                    # Handle key presses
                    key = self._read_key()
                    if key:
                        self._handle_key(key)

                    # Update UI atomically in main thread (eliminates Windows flickering)
                    live.update(self._build_layout(), refresh=True)
                    time.sleep(0.035)
        except (KeyboardInterrupt, SystemExit):
            pass
        except Exception as e:
            self.console.print(f"[bold red]Ошибка выполнения:[/] {e}")
            import traceback
            traceback.print_exc()
        finally:
            self._restore_terminal()

    def _handle_key(self, key: str):
        if self.show_achievements:
            if key in ["o", "O", "щ", "Щ", "ESC"]:
                self.show_achievements = False
            elif key in ["\t"]:
                self.ach_tab = (self.ach_tab + 1) % 3
                self.ach_scroll = 0
            elif key == "1":
                self.ach_tab = 0
                self.ach_scroll = 0
            elif key == "2":
                self.ach_tab = 1
                self.ach_scroll = 0
            elif key == "3":
                self.ach_tab = 2
                self.ach_scroll = 0
            elif key in ["LEFT"]:
                self.ach_tab = (self.ach_tab - 1) % 3
                self.ach_scroll = 0
            elif key in ["RIGHT"]:
                self.ach_tab = (self.ach_tab + 1) % 3
                self.ach_scroll = 0
            elif key in ["UP", "w", "W", "ц", "Ц", "k", "K"]:
                self.ach_scroll = max(0, self.ach_scroll - 1)
            elif key in ["DOWN", "s", "S", "ы", "Ы", "і", "І", "j", "J"]:
                self.ach_scroll += 1
            elif key == "PGUP":
                self.ach_scroll = max(0, self.ach_scroll - 5)
            elif key == "PGDN":
                self.ach_scroll += 5
            elif key in [" ", "\r", "\n"]:
                self.show_achievements = False
            elif key in ["l", "L", "д", "Д"]:
                new_lang = cycle_language(self.engine.lang)
                self.engine.set_language(new_lang)
            elif key in ["q", "Q", "й", "Й", "\x03"]:
                self.running = False
            elif key in ["r", "R", "к", "К"]:
                self.engine.reset_session()
            return

        if key in ["q", "Q", "й", "Й", "\x03"]:  # Ctrl+C or Q
            self.running = False
        elif key == "ESC":
            self.running = False
        elif key in ["o", "O", "щ", "Щ"]:
            self.show_achievements = True
        elif key in ["l", "L"]:
            # Cycle language
            new_lang = cycle_language(self.engine.lang)
            self.engine.set_language(new_lang)
            flag_map = {"uk": "Українська 🇺🇦", "en": "English 🇬🇧", "ru": "Русский 🇷🇺"}
            prefix = {"uk": "Мова", "en": "Language", "ru": "Язык"}.get(new_lang, "Мова")
            self.engine._add_event("SYSTEM", f"{prefix}: {flag_map.get(new_lang, new_lang.upper())}")
        elif key in ["LEFT", "h", "H", "z", "Z", "я", "Я", "р", "Р", ",", "б", "Б", "<", "4"]:
            # Left alar cartilage snap
            res = self.engine.crack(side="left", caller="User", force=1.0, sound_muted=self.sound.muted)
            self.sound.play("left")
        elif key in ["RIGHT", "x", "X", "ч", "Ч", "д", "Д", ".", "ю", "Ю", ">", "6"]:
            # Right alar cartilage snap
            res = self.engine.crack(side="right", caller="User", force=1.0, sound_muted=self.sound.muted)
            self.sound.play("right")
        elif key in [" ", "\r", "\n", "UP", "DOWN", "5", "c", "C", "с", "С"]:
            # Space or Enter: Snap both / center
            res = self.engine.crack(side="both", caller="User", force=1.0, sound_muted=self.sound.muted)
            self.sound.play("center")
        elif key in ["a", "A", "ф", "Ф", "\t"]:
            # Toggle AI worker loop
            self.ai_worker.toggle()
        elif key in ["s", "S", "ы", "Ы"]:
            # Cycle AI speed
            self.ai_worker.cycle_speed()
        elif key in ["m", "M", "ь", "Ь"]:
            # Toggle sound
            muted = self.sound.toggle_mute()
            state_msg = {
                "uk": "вимкнено (Mute)" if muted else "увімкнено",
                "en": "turned OFF (Mute)" if muted else "turned ON",
                "ru": "выключен (Mute)" if muted else "включен",
            }.get(self.engine.lang, "вимкнено" if muted else "увімкнено")
            sound_word = {"uk": "Звук", "en": "Sound", "ru": "Звук"}.get(self.engine.lang, "Звук")
            self.engine._add_event("SYSTEM", f"{sound_word} {state_msg}.")
        elif key in ["r", "R", "к", "К"]:
            # Reset session (preserving achievements)
            self.engine.reset_session()
