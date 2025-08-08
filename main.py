import os
import discord

# Get token
TOKEN = os.getenv("DISCORD_TOKEN")

# Create bot
bot = discord.Client(intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f'Bot connected: {bot.user}')

# Start Flask web server for Railway
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# Start web server
Thread(target=run_web, daemon=True).start()

# Run bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("No DISCORD_TOKEN found")
