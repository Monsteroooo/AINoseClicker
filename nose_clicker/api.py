import threading
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from nose_clicker.engine import NoseEngine
from nose_clicker.sound import SoundManager
from nose_clicker.ai_worker import AIWorker
from nose_clicker.web_ui import WEB_UI_HTML


class CrackRequest(BaseModel):
    cartilage: Optional[str] = Field(default="both", description="Хрящ для сдвига: minor_alar, left, right, both")
    force: Optional[float] = Field(default=1.0, ge=0.1, le=5.0, description="Сила нажатия на хрящ")
    caller: Optional[str] = Field(default="API-Client", description="Идентификатор вызывающей стороны")


def create_api_app(engine: NoseEngine, sound: SoundManager, ai_worker: AIWorker) -> FastAPI:
    app = FastAPI(
        title="NoseClicker AI REST Service",
        description="Первая нейросеть с тактильной отдачей и симулятором хрящей. Эндпоинт для потребления виртуального хряща.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", response_class=HTMLResponse, summary="Интерактивный Web-интерфейс NoseClicker AI")
    async def web_ui():
        return HTMLResponse(content=WEB_UI_HTML)

    @app.post("/api/v1/nose/crack", summary="Сдвинуть малый крыльный хрящ")
    async def crack_nose(req: Optional[CrackRequest] = None):
        cartilage = req.cartilage if req else "both"
        force = req.force if req else 1.0
        caller = req.caller if req else "API-Client"

        # Snap cartilage in engine
        res = engine.crack(side=cartilage, caller=caller, force=force, sound_muted=sound.muted)
        # Play procedural snap sound
        sound.play(res["side"])

        return res

    @app.get("/api/v1/nose/status", summary="Текущий статус носа, стресса и датацентра")
    async def get_status(lang: Optional[str] = None):
        target_lang = (lang or engine.lang).lower()
        return {
            "language": target_lang,
            "engine_language": engine.lang,
            "clicks_total": engine.total_clicks,
            "left_clicks": engine.left_clicks,
            "right_clicks": engine.right_clicks,
            "both_clicks": engine.both_clicks,
            "pleasure_tokens": round(engine.pleasure_tokens, 2),
            "stress_level": round(engine.stress_level, 1),
            "ai_dopamine_level": round(engine.ai_dopamine, 1),
            "cps": round(engine.get_cps(), 2),
            "cartilage_integrity": engine.get_cartilage_integrity(target_lang),
            "datacenter_power_gw": engine.get_datacenter_power(),
            "ai_worker": {
                "enabled": ai_worker.enabled,
                "speed": ai_worker.speed_label,
                "delay_seconds": ai_worker.delay_seconds,
            },
            "sound_muted": sound.muted,
            "achievements_unlocked": engine.get_unlocked_count(),
            "achievements_total": len(engine.achievements),
            "achievements": list(engine.get_localized_achievements(target_lang).values()),
        }

    @app.get("/api/v1/nose/achievements", summary="Список всех достижений и их прогресс")
    async def get_achievements(lang: Optional[str] = None):
        target_lang = (lang or engine.lang).lower()
        return {
            "language": target_lang,
            "unlocked_count": engine.get_unlocked_count(),
            "total_count": len(engine.achievements),
            "achievements": engine.get_localized_achievements(target_lang),
        }

    @app.post("/api/v1/lang/set", summary="Сменить текущий язык симулятора (ru, en, uk)")
    async def set_lang(req: Dict[str, str]):
        new_lang = req.get("lang", "ru").lower()
        engine.set_language(new_lang)
        return {"status": "ok", "language": engine.lang}

    @app.post("/api/v1/ai/toggle", summary="Включить / приостановить фоновый цикл while(alive)")
    async def toggle_ai():
        state = ai_worker.toggle()
        return {
            "ai_worker_enabled": state,
            "speed": ai_worker.speed_label,
            "message": "AI Worker loop " + ("АКТИВИРОВАН" if state else "ПРИОСТАНОВЛЕН"),
        }

    @app.post("/api/v1/ai/speed", summary="Переключить скорость авто-клика AI")
    async def cycle_speed():
        label = ai_worker.cycle_speed()
        return {
            "speed_label": label,
            "delay_seconds": ai_worker.delay_seconds,
        }

    @app.post("/api/v1/nose/reset", summary="Сбросить прогресс и натяжение хрящей")
    async def reset_engine():
        engine.reset()
        return {"status": "ok", "message": "Статистика успешно сброшена"}

    return app


class APIServer:
    def __init__(self, engine: NoseEngine, sound: SoundManager, ai_worker: AIWorker, host: str = "127.0.0.1", port: int = 8088):
        self.engine = engine
        self.sound = sound
        self.ai_worker = ai_worker
        self.host = host
        self.port = port
        self.app = create_api_app(engine, sound, ai_worker)
        self.server: Optional[uvicorn.Server] = None
        self.thread: Optional[threading.Thread] = None

    def start(self):
        config = uvicorn.Config(
            self.app,
            host=self.host,
            port=self.port,
            log_level="error",
            access_log=False,
        )
        self.server = uvicorn.Server(config)
        self.thread = threading.Thread(target=self.server.run, daemon=True)
        self.thread.start()

    def stop(self):
        if self.server:
            self.server.should_exit = True
