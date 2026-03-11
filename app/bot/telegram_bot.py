import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from app.api.football_api import football_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    keyboard = [
        [InlineKeyboardButton("⚽ Partidos en Vivo", callback_data="live")],
        [InlineKeyboardButton("🏆 Ligas", callback_data="leagues")],
        [InlineKeyboardButton("📊 Mi Perfil", callback_data="profile")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 ¡Bienvenido al Bot de Fútbol!\n\n"
        "Selecciona una opción:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejar clicks en botones"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "live":
        data = football_api.get_live_matches()
        if "error" in data:
            await query.edit_message_text("❌ Error al obtener partidos")
            return
        
        matches = data.get("response", [])
        if not matches:
            await query.edit_message_text("📭 No hay partidos en vivo ahora")
            return
        
        message = "🔴 **PARTIDOS EN VIVO**\n\n"
        for match in matches[:5]:  # Mostrar solo 5
            teams = match.get("teams", {})
            goals = match.get("goals", {})
            message += f"{teams.get('home', {}).get('name')} {goals.get('home')} - {goals.get('away')} {teams.get('away', {}).get('name')}\n"
        
        await query.edit_message_text(message, parse_mode="Markdown")
    
    elif query.data == "leagues":
        keyboard = [
            [InlineKeyboardButton("🇪🇸 España", callback_data="league_es")],
            [InlineKeyboardButton("🇬🇧 Inglaterra", callback_data="league_en")],
            [InlineKeyboardButton("🇮🇹 Italia", callback_data="league_it")],
            [InlineKeyboardButton("🔙 Volver", callback_data="back")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🏆 Selecciona una liga:", reply_markup=reply_markup)
    
    elif query.data == "back":
        await start(update, context)
    
    elif query.data == "profile":
        await query.edit_message_text("📊 **Tu Perfil**\n\nUsuario: " + str(update.effective_user.id))

def create_bot_application(token):
    """Crear la aplicación del bot"""
    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    return application