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

# This is the entire HTML code for the Dyno-inspired dashboard.
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dyno Bot Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0d0f11;
        }
        .sidebar {
            background-color: #1a1b1d;
            border-right: 1px solid #2d2e30;
        }
        .main-content {
            background-color: #121315;
        }
        .active-tab {
            background-color: #c9405d;
            color: white;
            border-radius: 6px;
        }
        .card {
            background-color: #1a1b1d;
        }
    </style>
</head>
<body class="flex min-h-screen text-gray-200">

    <!-- Sidebar -->
    <aside class="sidebar w-64 p-4 flex flex-col hidden md:flex">
        <div class="flex items-center space-x-2 mb-8">
            <svg class="h-8 w-8 text-white" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-4.17 3.06-7.53 7-7.93v15.86zM12 4.07c3.95.49 7 3.85 7 7.93s-3.05 7.44-7 7.93V4.07z"/>
            </svg>
            <span class="text-xl font-bold">DYNABOT</span>
        </div>
        <nav class="space-y-2">
            <a href="#" class="flex items-center p-3 rounded-lg hover:bg-gray-700">
                <svg class="h-5 w-5 mr-3" fill="currentColor" viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
                Dashboard
            </a>
            <a href="#" class="flex items-center p-3 rounded-lg bg-gray-700">
                <svg class="h-5 w-5 mr-3" fill="currentColor" viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 14v-2h8v2H6zm10-3H6V9h10v2zm0-4H6V5h10v2z"/></svg>
                Commands
            </a>
            <a href="#" class="flex items-center p-3 rounded-lg hover:bg-gray-700">
                <svg class="h-5 w-5 mr-3" fill="currentColor" viewBox="0 0 24 24"><path d="M10 2a8 8 0 018 8c0 2.21-.89 4.21-2.34 5.66L20.59 19l-1.42 1.41-3.9-3.9A8 8 0 1110 2zm0 14a6 6 0 100-12 6 6 0 000 12z"/></svg>
                Logs
            </a>
        </nav>
    </aside>

    <!-- Main Content Area -->
    <main class="main-content flex-grow p-6">
        <h1 class="text-3xl font-bold mb-6">Commands</h1>

        <!-- Command Tabs -->
        <div class="flex flex-wrap gap-2 mb-6">
            <span class="p-2 text-sm font-semibold cursor-pointer active-tab">Manager</span>
            <span class="p-2 text-sm font-semibold text-gray-400 rounded-lg hover:bg-gray-700 cursor-pointer">Misc</span>
            <span class="p-2 text-sm font-semibold text-gray-400 rounded-lg hover:bg-gray-700 cursor-pointer">Info</span>
            <span class="p-2 text-sm font-semibold text-gray-400 rounded-lg hover:bg-gray-700 cursor-pointer">Fun</span>
            <span class="p-2 text-sm font-semibold text-gray-400 rounded-lg hover:bg-gray-700 cursor-pointer">Moderator</span>
        </div>

        <!-- Command Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            <!-- Example Card -->
            <div class="card p-4 rounded-lg flex flex-col justify-between">
                <div>
                    <h3 class="text-lg font-semibold flex items-center">
                        Addmod
                        <span class="ml-2 text-sm text-green-400">(Enabled)</span>
                    </h3>
                    <p class="text-sm text-gray-400 mt-1">Add a moderator role.</p>
                </div>
                <div class="mt-4 flex justify-between items-center">
                    <button class="text-sm text-gray-400 hover:text-gray-200">Settings</button>
                    <button class="text-sm text-gray-400 hover:text-gray-200">Help</button>
                </div>
            </div>
            <!-- More example cards would go here -->
             <div class="card p-4 rounded-lg flex flex-col justify-between">
                <div>
                    <h3 class="text-lg font-semibold flex items-center">
                        Addrole
                        <span class="ml-2 text-sm text-green-400">(Enabled)</span>
                    </h3>
                    <p class="text-sm text-gray-400 mt-1">Add a new role with optional color and hoist.</p>
                </div>
                <div class="mt-4 flex justify-between items-center">
                    <button class="text-sm text-gray-400 hover:text-gray-200">Settings</button>
                    <button class="text-sm text-gray-400 hover:text-gray-200">Help</button>
                </div>
            </div>
             <div class="card p-4 rounded-lg flex flex-col justify-between">
                <div>
                    <h3 class="text-lg font-semibold flex items-center">
                        Delmod
                        <span class="ml-2 text-sm text-red-400">(Disabled)</span>
                    </h3>
                    <p class="text-sm text-gray-400 mt-1">Remove a moderator role.</p>
                </div>
                <div class="mt-4 flex justify-between items-center">
                    <button class="text-sm text-gray-400 hover:text-gray-200">Settings</button>
                    <button class="text-sm text-gray-400 hover:text-gray-200">Help</button>
                </div>
            </div>
        </div>
    </main>

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
