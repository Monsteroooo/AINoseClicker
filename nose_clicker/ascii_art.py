from rich.text import Text


def render_bar(val: float, max_val: float = 100.0, width: int = 20, fill_color: str = "green", empty_color: str = "grey30") -> str:
    val = max(0.0, min(max_val, val))
    filled_len = int(round((val / max_val) * width))
    empty_len = width - filled_len
    return f"[{fill_color}]{'█' * filled_len}[/{fill_color}][{empty_color}]{'░' * empty_len}[/{empty_color}]"


def render_nose_art(
    frame: str = "idle",
    stress: float = 80.0,
    dopamine: float = 50.0,
    cps: float = 0.0,
    lang: str = "uk",
    show_labels: bool = False,
) -> Text:
    """
    Генерирует идеально отцентрированную цветную анатомическую 3D/ASCII модель носа
    с визуальной тактильной отдачей и локализацией (uk/en/ru).
    """
    t = Text()

    # Dynamic color palette
    main_color = "bright_cyan" if dopamine < 80 else "bright_green"
    accent = "bright_yellow" if cps > 3.0 else "cyan"

    # I18N Labels & Text
    lang = lang.lower() if lang in ["ru", "en", "uk"] else "uk"
    if lang == "en":
        dorsum_label = "◄ Bridge"
        lateral_label = "◄ Lateral"
        alar_label = "◄ Alar"
        nostrils_line = "     Left Nostril Right Nostril"
        haptic_active = "   ««« TACTILE CARTILAGE SNAP »»»"
        haptic_idle = "   «« Ready to snap: [Space] »»"
    elif lang == "ru":
        dorsum_label = "◄ Спинка"
        lateral_label = "◄ Боковые"
        alar_label = "◄ Крыльный"
        nostrils_line = "     Левая ноздря Правая ноздря"
        haptic_active = "   ««« ТАКТИЛЬНЫЙ ХРУСТ В ХРЯЩЕ »»»"
        haptic_idle = "   «« Готов к хрусту: [Space] »»"
    else:  # "uk" (default)
        dorsum_label = "◄ Спинка"
        lateral_label = "◄ Бічні"
        alar_label = "◄ Крильний"
        nostrils_line = "     Ліва ніздря  Права ніздря"
        haptic_active = "   ««« ТАКТИЛЬНИЙ ХРУСКІТ »»»"
        haptic_idle = "   «« Готовий: тисни [Space] »»"

    # 1. Nasal Bridge Top
    t.append(r"       .──────────────────." + "\n", "bright_blue")
    t.append(r"      /      ________      \ " + "\n", main_color)
    t.append(r"     │      /        \      │" + "\n", main_color)

    # 2. Dorsum (Septum)
    t.append(r"     │     │  │    │  │     │", main_color)
    if show_labels:
        t.append(f"  {dorsum_label}", "dim cyan")
    t.append("\n")

    t.append(r"     │     │  │    │  │     │" + "\n", main_color)
    t.append(r"    /      │  │    │  │      \ " + "\n", main_color)

    # 3. Lateral Cartilages
    t.append(r"   │      ┌┴──┴────┴──┴┐      │", main_color)
    if show_labels:
        t.append(f"  {lateral_label}", "dim cyan")
    t.append("\n")

    # 4. Minor Alar Cartilage & Pupils (Snap reactions)
    if frame == "left":
        t.append(r"💥 ((( │  │   (•)  (•) │  )   │" + "\n", "bold bright_yellow")
        t.append(r"    \____ └───┬────┬───┘_/ __/" + "\n", "bold bright_yellow")
    elif frame == "right":
        t.append(r"   │   (  │   (•)  (•) │  │ ))) 💥" + "\n", "bold bright_yellow")
        t.append(r"    \__ \_└───┬────┬───┘ ____/" + "\n", "bold bright_yellow")
    elif frame == "both":
        t.append(r"💥 ((( │  │  (💥)  (💥) │  │ ))) 💥" + "\n", "bold bright_magenta")
        t.append(r"    \____ └───┬────┬───┘ ____/" + "\n", "bold bright_yellow")
    elif frame == "mega":
        t.append(r"🔥 (((││││ (♨)  (♨) ││││))) 🔥" + "\n", "bold bright_white on red blink")
        t.append(r"    \~~~~ └───┴────┴───┘ ~~~~/" + "\n", "bold bright_red")
    else:
        pupil = "(•)" if stress > 30 else "(◠)"
        t.append(r"   │   (  │   " + pupil + "  " + pupil + r" │  )   │", main_color)
        if show_labels:
            t.append(f"  {alar_label}", "bold bright_yellow" if cps > 3.0 else "dim cyan")
        t.append("\n")
        t.append(r"    \__ \_└───┬────┬───┘_/ __/" + "\n", main_color)

    # 5. Nostrils
    t.append(r"       \______/    \______/" + "\n", "bold bright_blue")
    t.append(r"          ▲            ▲" + "\n", "yellow")
    t.append(nostrils_line + "\n", "bold white")

    # 6. Tactile vibration hint
    if frame in ["left", "right", "both", "mega"]:
        t.append(haptic_active + "\n", "bold bright_green")
    else:
        t.append(haptic_idle + "\n", "dim white")

    return t
