import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Fetch Token from Environment Variables (Render will supply this)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --- Command: /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("⚽ Latest Football News", callback_data="news")],
        [InlineKeyboardButton("🏆 Live Scores / Matches", callback_data="scores")],
        [InlineKeyboardButton("📊 Transfer Rumors", callback_data="transfers")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcom_msg = (
        f"Hello {user.first_name}! ⚽\n\n"
        "Welcome to your ultimate Football News Bot. "
        "Choose an option below to get started:"
    )
    
    if update.message:
        await update.message.reply_text(welcom_msg, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcom_msg, reply_markup=reply_markup)

# --- Button Click Handler ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Back button to return to home menu
    back_keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]]
    back_markup = InlineKeyboardMarkup(back_keyboard)

    if query.data == "news":
        # You can integrate a real news API here (e.g., NewsAPI or football-data.org)
        news_text = (
            "📰 **Latest Football Headlines:**\n\n"
            "1. *Champions League:* Thrilling quarter-final draws announced!\n"
            "2. *Premier League:* Title race heats up as leaders draw.\n"
            "3. *La Liga:* Star striker secures a dramatic last-minute win."
        )
        await query.message.edit_text(news_text, reply_markup=back_markup, parse_mode="Markdown")

    elif query.data == "scores":
        scores_text = (
            "⚽ **Recent Match Results:**\n\n"
            "• Real Madrid 2 - 1 Barcelona\n"
            "• Arsenal 3 - 0 Chelsea\n"
            "• Bayern Munich 2 - 2 Dortmund"
        )
        await query.message.edit_text(scores_text, reply_markup=back_markup, parse_mode="Markdown")

    elif query.data == "transfers":
        transfer_text = (
            "🔄 **Top Transfer Rumors:**\n\n"
            "• Midfield prodigy linked with a £80m summer switch.\n"
            "• Winger confirms open talks with European giants."
        )
        await query.message.edit_text(transfer_text, reply_markup=back_markup, parse_mode="Markdown")

    elif query.data == "main_menu":
        await start(update, context)

def main() -> None:
    if not TOKEN:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment variables!")
        return

    # Build the application
    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Start the Bot using Polling (Render Background Worker friendly)
    logger.info("Starting bot polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
