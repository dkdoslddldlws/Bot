# Emergency Simple Discord Bot for Railway
# Copy this ENTIRE file as main.py in Railway

import os
import asyncio

try:
    import discord
except ImportError:
    print("Installing discord.py...")
    os.system("pip install discord.py")
    import discord

try:
    from flask import Flask
except ImportError:
    print("Installing flask...")
    os.system("pip install flask")
    from flask import Flask

# Configuration
TOKEN = os.getenv("DISCORD_TOKEN")
print(f"Token found: {'Yes' if TOKEN else 'No'}")

# Create simple bot
class SimpleBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f'SUCCESS: Bot online as {self.user}')
        print(f'Connected to {len(self.guilds)} servers')

bot = SimpleBot()

# Simple web server for Railway
app = Flask(__name__)

@app.route('/')
def health():
    status = "Online" if bot.is_ready() else "Starting"
    return f"Discord Bot Status: {status}"

# Start web server in background
import threading
def start_web():
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting web server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

web_thread = threading.Thread(target=start_web, daemon=True)
web_thread.start()

# Start bot
if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found!")
        print("Add DISCORD_TOKEN in Railway environment variables")
        exit(1)
    
    print("Starting Discord bot...")
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Bot failed to start: {e}")
        import time
        time.sleep(30)  # Keep container alive for debugging
