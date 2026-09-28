from dotenv import load_dotenv
load_dotenv()
import os

import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")

conversation_history = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text_message = update.message.text
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    conversation_history[user_id].append({"role": "user", "content": text_message})
    chat_completion = client.chat.completions.create(
    messages=conversation_history[user_id],
    model="openai/gpt-oss-120b",
)
    reply = chat_completion.choices[0].message.content
    conversation_history[user_id].append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply)

def main() -> None:
    
    application = Application.builder().token(telegram_token).build()

   
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))


    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

   
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()  