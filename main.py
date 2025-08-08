#!/usr/bin/env python3
"""
ULTRA-SIMPLE Railway Discord Bot - Copy this as main.py
This version eliminates all permission and complexity issues
"""

import os
import discord
from discord.ext import commands
from discord import app_commands

# Simple setup
TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Basic bot with minimal permissions
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot online: {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'✅ Synced {len(synced)} commands')
    except Exception as e:
        print(f'❌ Sync failed: {e}')

@bot.tree.command(name="ping", description="Test if bot is working")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong! Bot is working!")

@bot.tree.command(name="hello", description="Say hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"👋 Hello {interaction.user.mention}!")

@bot.tree.command(name="chat", description="Basic AI chat")
async def chat(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"🤖 You said: {message}\n\n*AI features coming soon!*")

# Simple Flask for Railway
try:
    from flask import Flask
    from threading import Thread
    
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "🤖 Discord Bot Online!"
    
    def run_flask():
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    
    # Start Flask in background
    Thread(target=run_flask, daemon=True).start()
    
except ImportError:
    print("Flask not available, skipping web server")

# Run bot
if __name__ == "__main__":
    if TOKEN:
        print("🚀 Starting bot...")
        bot.run(TOKEN)
    else:
        print("❌ DISCORD_TOKEN missing!")
        print("Add DISCORD_TOKEN to Railway environment variables")
