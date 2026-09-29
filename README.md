Telegram Bot with Groq (and actual memory)

A Telegram bot that talks to you using an LLM instead of canned responses — and unlike a basic wrapper around an API, it actually remembers what you said earlier in the conversation.

What it does

You message the bot on Telegram, it sends your message to Groq's LLM, and replies with a real generated answer. But it doesn't stop there — it keeps a running history of your conversation, per user, so it can actually follow along instead of treating every message like the first one. Ask it something, mention a detail, then refer back to it later — it remembers.

Each user gets their own separate conversation, so if multiple people message the bot, their chats don't get mixed up with each other.

How it works
Bot layer: built with python-telegram-bot, which handles the actual connection to Telegram and listens for incoming messages.
Brain: every message gets sent to Groq's API (currently using openai/gpt-oss-120b), which generates the reply.
Memory: each user's messages (and the bot's replies) get stored in a dictionary, keyed by their Telegram user ID. Every new message gets added to their history, and the whole history gets sent to Groq each time — that's what lets it stay consistent across a conversation instead of forgetting everything between messages.
Memory cap: conversations don't grow forever. Once a user's history passes 20 messages, the oldest ones get dropped so the bot doesn't hit the model's context limit or slow down over a long chat.
Setup
Clone the repo:
   git clone https://github.com/akshajmadan/TelegramBotwithGroq.git
   cd TelegramBotwithGroq
Set up a virtual environment and install dependencies:
   python -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   pip install -r requirements.txt
Create a .env file in the project folder with your own keys:
   GROQ_API_KEY=your_groq_key_here
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
Get a Groq key at console.groq.com
Get a Telegram bot token by messaging @BotFather on Telegram and creating a new bot
Run it:
   python main.py
Open Telegram, find your bot, and start chatting. Try /start first, then just talk normally.
Known limitations (things I know about and haven't fixed yet)
Memory doesn't survive a restart. It's stored in a plain Python dictionary while the script runs, so stopping and starting the bot wipes everyone's conversation history. A future version would save this to a real database instead.
Not deployed anywhere yet. Right now it only runs while I'm actively running the script on my own machine — it's not live 24/7 on a server.
No tool use yet. The bot can only talk — it can't look things up, run calculations, or do anything beyond generating text. That's the next thing I'm building.
Why I built this

This is Project 3 in a self-directed track to learn practical AI engineering skills — after building a CLI summarizer (basic API calls and prompting) and a PDF Q&A tool using RAG (retrieval-augmented generation), this project was about learning how to build something interactive and stateful instead of a one-shot script.
