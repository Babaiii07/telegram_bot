import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import google.generativeai as genai

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        "Hi ! My name is Parthib_Bot built by Parthib. I can have any conversation with you. Please say something!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("I can help you with anything!")

async def bot_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate a response using Google Generative AI model with a 30-word limit."""
    API_KEY = "your api key"
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    user_message = update.message.text + " in 20 words please"
    print(user_message)
    response = model.generate_content(user_message)
    print(response.text)

    response_words = response.text.split()
    limited_response = ' '.join(response_words[:30]) 
    await update.message.reply_text(limited_response)

def main() -> None:
    """Start the bot."""
    bot_api = "your telegram bot api key"
    application = Application.builder().token(bot_api).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot_reply))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
