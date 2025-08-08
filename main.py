# main.py
# This code sets up a Discord bot and a Flask web server for uptime monitoring.

import os
import threading
import discord
from discord.ext import commands
from flask import Flask, request

# ====================
# Web Server for Uptime Monitoring
# ====================

app = Flask(__name__)

@app.route('/')
def home():
    # This is a simple web page that lets you know the bot is online.
    return "The bot is awake!"

def run_server():
    # Run the Flask server.
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# ====================
# Discord Bot Setup
# ====================

# Get the bot token from the environment variables.
# Note: Hard-coding your token like this is not recommended for security.
TOKEN = "MTQwMzEzNTUxMTgxNTY1MTM4OA.GtGhf_.V73KmWYTisS91e-HsiKHy0J02nvlr7o6g06AU"

# Define the bot's intents.
# Intents tell Discord what events your bot needs to listen for.
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content.

# Initialize the bot with a command prefix and intents.
# The command prefix is what a user types to tell the bot to listen (e.g., !hello).
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """
    This event runs when the bot successfully connects to Discord.
    """
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('Bot is ready and online!')
    # You can add a status message here if you like.
    # await bot.change_presence(activity=discord.Game(name="Hello World!"))

@bot.command()
async def hello(ctx):
    """
    A simple command that responds with 'Hello!'.
    """
    await ctx.send(f'Hello {ctx.author.name}!')

@bot.command()
async def ping(ctx):
    """
    Responds with the bot's latency (ping).
    """
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

# ====================
# Main Execution
# ====================

if __name__ == "__main__":
    # Start the web server in a separate thread.
    # This allows the bot and the web server to run at the same time.
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True # This ensures the thread closes when the main program exits.
    server_thread.start()

    # Start the Discord bot.
    try:
        if TOKEN:
            bot.run(TOKEN)
        else:
            print("ERROR: Discord bot token not found.")
    except discord.errors.LoginFailure as e:
        print(f"Error logging in: {e}")
        print("Please check your bot token.")
