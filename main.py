# main.py
# This code sets up a Discord bot and a Flask web server for uptime monitoring.

import os
import threading
import discord
from discord.ext import commands
from flask import Flask, request, render_template_string
import random 
import time

# ====================
# HTML for the Dashboard
# ====================

# This is the entire HTML code for the futuristic dashboard.
# We're embedding it directly in the Python file for simplicity.
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dino Bot Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;700&display=swap');
        body {
            font-family: 'Chakra Petch', sans-serif;
            background-color: #0c0a09; /* Deep charcoal background */
            color: #d1d5db; /* Light gray text */
        }
        .glow {
            text-shadow: 0 0 8px #a78bfa, 0 0 16px #a78bfa;
            animation: glow 2s infinite alternate;
        }
        @keyframes glow {
            from {
                text-shadow: 0 0 8px #a78bfa, 0 0 16px #a78bfa, 0 0 24px #a78bfa;
            }
            to {
                text-shadow: 0 0 12px #a78bfa, 0 0 24px #a78bfa, 0 0 36px #a78bfa;
            }
        }
        .glitch-text {
            color: #4ade80; /* Dino green */
            position: relative;
            animation: glitch 1.5s infinite;
        }
        @keyframes glitch {
            0%   { left: 0px; top: 0px; }
            10%  { left: -2px; top: -2px; }
            20%  { left: 2px; top: 2px; }
            30%  { left: -2px; top: -2px; }
            40%  { left: 2px; top: 2px; }
            50%  { left: -2px; top: -2px; }
            60%  { left: 2px; top: 2px; }
            70%  { left: -2px; top: -2px; }
            80%  { left: 2px; top: 2px; }
            90%  { left: -2px; top: -2px; }
            100% { left: 0px; top: 0px; }
        }
        .bg-card {
            background-color: #1a1a1a;
            border: 1px solid #3f3f46;
        }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen p-4">
    <div class="bg-card border-purple-500 rounded-lg shadow-2xl p-8 w-full max-w-2xl text-center">
        <h1 class="text-4xl md:text-5xl font-bold mb-4 glitch-text">Dino Bot Status</h1>
        <p class="text-lg md:text-xl text-gray-400 mb-6">Monitoring the server with style.</p>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div class="bg-gray-800 p-4 rounded-lg border border-green-500">
                <h2 class="text-xl font-bold text-gray-300">Status</h2>
                <p id="status" class="text-green-400 text-3xl font-extrabold mt-2 glow">ONLINE</p>
            </div>
            <div class="bg-gray-800 p-4 rounded-lg border border-yellow-500">
                <h2 class="text-xl font-bold text-gray-300">Ping</h2>
                <p id="ping" class="text-yellow-300 text-3xl font-extrabold mt-2 glow">Fetching...</p>
            </div>
            <div class="bg-gray-800 p-4 rounded-lg border border-purple-500">
                <h2 class="text-xl font-bold text-gray-300">Uptime</h2>
                <p id="uptime" class="text-purple-400 text-3xl font-extrabold mt-2 glow">Fetching...</p>
            </div>
        </div>

        <div class="border-t border-gray-700 pt-6 text-gray-500">
            <p>Last checked: <span id="last-checked">...</span></p>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            function updateDashboard() {
                const now = new Date();
                document.getElementById('last-checked').textContent = now.toLocaleTimeString();

                const uptimeDisplay = document.getElementById('uptime');
                const lastUptime = uptimeDisplay.textContent;
                
                if (lastUptime.startsWith('Fetching')) {
                    uptimeDisplay.textContent = '0h 0m 0s';
                } else {
                    const parts = lastUptime.match(/(\d+)h (\d+)m (\d+)s/);
                    let hours = parseInt(parts[1]);
                    let minutes = parseInt(parts[2]);
                    let seconds = parseInt(parts[3]);
                    
                    seconds++;
                    if (seconds >= 60) {
                        seconds = 0;
                        minutes++;
                    }
                    if (minutes >= 60) {
                        minutes = 0;
                        hours++;
                    }
                    uptimeDisplay.textContent = `${hours}h ${minutes}m ${seconds}s`;
                }
            }
            setInterval(updateDashboard, 1000);
            updateDashboard();
        });
    </script>
</body>
</html>
"""


# ====================
# Web Server for Uptime Monitoring
# ====================

app = Flask(__name__)

@app.route('/')
def home():
    # Now, instead of a simple string, we return the full HTML dashboard.
    return render_template_string(dashboard_html)

def run_server():
    # Run the Flask server.
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# ====================
# Discord Bot Setup
# ====================

# Get the bot token from the environment variables.
# This keeps your token safe and secure.
TOKEN = os.environ.get("DISCORD_BOT_SECRET")

# Define the bot's intents.
# Intents tell Discord what events your bot needs to listen for.
intents = discord.Intents.default()
intents.message_content = True  # Required to read message content.

# Initialize the bot with a command prefix and intents.
# The command prefix is what a user types to tell the bot to listen (e.g., !hello).
bot = commands.Bot(command_prefix='!', intents=intents)

# Store the bot's start time to calculate uptime.
start_time = time.time()

@bot.event
async def on_ready():
    """
    This event runs when the bot successfully connects to Discord.
    """
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('Bot is ready and online!')
    
    # Updated bot status message
    await bot.change_presence(activity=discord.Game(name="Monitoring the server!"))

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
# New Monitor & Monster Commands
# ====================

@bot.command(name='status')
async def bot_status(ctx):
    """
    Reports the bot's uptime.
    """
    current_time = time.time()
    uptime_seconds = int(round(current_time - start_time))
    uptime_minutes = int(uptime_seconds / 60)
    uptime_hours = int(uptime_minutes / 60)

    # Calculate remaining minutes and seconds
    remaining_minutes = uptime_minutes % 60
    remaining_seconds = uptime_seconds % 60

    await ctx.send(f"I've been online for {uptime_hours} hours, {remaining_minutes} minutes, and {remaining_seconds} seconds. Everything is running smoothly! ✅")

@bot.command(name='8ball')
async def eightball(ctx, *, question):
    """
    Asks the magic 8-ball a question.
    """
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes – definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    await ctx.send(f'**Question:** {question}\n**Answer:** {random.choice(responses)}')

@bot.command(name='coinflip')
async def coin_flip(ctx):
    """
    Flips a coin.
    """
    outcomes = ["Heads", "Tails"]
    await ctx.send(f'The coin landed on... **{random.choice(outcomes)}!**')
    
# ====================
# NEW Commands added
# ====================

@bot.command(name='say')
async def say(ctx, *, message):
    """
    Makes the bot say something.
    """
    await ctx.send(message)

@bot.command(name='roll')
async def roll(ctx, dice: int):
    """
    Rolls a dice with the specified number of sides.
    """
    if dice < 1:
        await ctx.send("You must roll a dice with at least 1 side!")
    else:
        roll_result = random.randint(1, dice)
        await ctx.send(f"🎲 You rolled a **{roll_result}**!")

@bot.command(name='info')
async def info(ctx):
    """
    Provides information about the bot.
    """
    embed = discord.Embed(
        title="Bot Information",
        description="I am a custom Discord bot built with the discord.py library.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Author", value=bot.user.name, inline=True)
    embed.add_field(name="Library", value="[discord.py](https://discordpy.readthedocs.io/en/stable/)", inline=True)
    await ctx.send(embed=embed)


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
            print("ERROR: Discord bot token not found in environment variables.")
    except discord.errors.LoginFailure as e:
        print(f"Error logging in: {e}")
        print("Please check your bot token.")
