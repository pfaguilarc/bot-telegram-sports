from fastapi import FastAPI, BackgroundTasks
from app.config import settings
from app.bot.telegram_bot import create_bot_application
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Bot Telegram Fútbol", version="1.0.0")

bot_app = None

@app.on_event("startup")
async def startup_event():
    """Iniciar el bot de Telegram al iniciar FastAPI"""
    global bot_app
    logger.info("🚀 Iniciando Bot de Telegram...")
    bot_app = create_bot_application(settings.TELEGRAM_BOT_TOKEN)
    
    # Ejecutar el bot en segundo plano
    asyncio.create_task(run_bot())

async def run_bot():
    """Ejecutar el bot en background"""
    await bot_app.start_polling(allowed_updates=Update.ALL_TYPES)

@app.get("/")
async def root():
    return {"message": "🤖 Bot Telegram Fútbol API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "bot": "running" if bot_app else "stopped"}

@app.get("/api/football/live")
async def get_live_matches():
    """Endpoint para obtener partidos en vivo"""
    from app.api.football_api import football_api
    return football_api.get_live_matches()