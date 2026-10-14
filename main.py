#!/usr/bin/env python3
"""
NoseClicker AI — Главная точка входа.
"""

import sys
import os
import argparse
import time
import signal

# Auto-install dependencies if missing
try:
    import rich
    import fastapi
    import uvicorn
except ImportError:
    print("[*] Установка необходимых библиотек (rich, fastapi, uvicorn)...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rich>=13.0.0", "fastapi>=0.100.0", "uvicorn>=0.20.0"])
        print("[*] Библиотеки успешно установлены!\n")
    except Exception as e:
        print(f"[!] Не удалось автоматически установить библиотеки: {e}")
        print("Попробуйте выполнить вручную: pip install -r requirements.txt\n")

from nose_clicker.engine import NoseEngine
from nose_clicker.sound import SoundManager
from nose_clicker.ai_worker import AIWorker
from nose_clicker.api import APIServer
from nose_clicker.app import NoseClickerApp


def main():
    parser = argparse.ArgumentParser(
        description="NoseClicker AI — Первая нейросеть с тактильной отдачей и симулятором хрящей."
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Хост для REST API сервера (по умолчанию: 0.0.0.0 — доступен с телефона по Wi-Fi)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8088,
        help="Порт для REST API сервера (по умолчанию: 8088)",
    )
    parser.add_argument(
        "--no-api",
        action="store_true",
        help="Отключить REST API сервер и запустить только локальный TUI",
    )
    parser.add_argument(
        "--no-sound",
        "--muted",
        action="store_true",
        help="Отключить звуковые эффекты хруста хрящей (Mute)",
    )
    parser.add_argument(
        "--ai",
        action="store_true",
        help="Сразу активировать фоновый цикл AI while(alive) при старте",
    )
    parser.add_argument(
        "--headless",
        "--api-only",
        action="store_true",
        help="Запустить только REST микросервис без интерактивного TUI интерфейса",
    )
    parser.add_argument(
        "--sound",
        "-s",
        type=str,
        default=None,
        help="Путь к вашему аудиофайлу (.wav, .mp3, .ogg) или папке с кастомными звуками",
    )
    parser.add_argument(
        "--lang",
        "-l",
        type=str,
        default=None,
        choices=["uk", "en", "ru"],
        help="Мова інтерфейсу / Language / Язык интерфейса (uk, en, ru; за замовчуванням: uk)",
    )

    args = parser.parse_args()

    # Initialize Engine & Sound
    engine = NoseEngine(lang=args.lang)
    sound = SoundManager(custom_sound=args.sound, muted=args.no_sound)

    # Initialize AI Worker
    ai_worker = AIWorker(engine, sound, enabled_initially=args.ai)
    ai_worker.start()

    # Initialize & Start API Server
    api_server = None
    if not args.no_api:
        api_server = APIServer(
            engine=engine,
            sound=sound,
            ai_worker=ai_worker,
            host=args.host,
            port=args.port,
        )
        try:
            api_server.start()
        except Exception as e:
            engine._add_event("SYSTEM", f"Предупреждение: Не удалось запустить API: {e}")

    # Headless mode
    if args.headless:
        print(f"👃 NoseClicker AI запущен в режиме REST API микросервиса.")
        print(f"📡 Слушатель эндпоинта: http://{args.host}:{args.port}/api/v1/nose/crack")
        print(f"📖 Swagger документация: http://{args.host}:{args.port}/docs")
        print("Нажмите Ctrl+C для остановки сервера...")

        def sig_handler(sig, frame):
            print("\nОстановка микросервиса...")
            ai_worker.stop()
            if api_server:
                api_server.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)

        while True:
            time.sleep(1)

    # TUI Interactive Mode
    app = NoseClickerApp(
        engine=engine,
        sound=sound,
        ai_worker=ai_worker,
        api_host=args.host,
        api_port=args.port,
        api_enabled=not args.no_api,
    )

    try:
        app.run()
    finally:
        ai_worker.stop()
        if api_server:
            api_server.stop()


if __name__ == "__main__":
    main()
