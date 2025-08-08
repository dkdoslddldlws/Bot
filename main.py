# This is a single, self-contained Python script for a Discord bot
# that combines all the functionalities from the previous modular design
# into one file.

import discord
from discord.ext import commands
import os
import asyncio
import threading
from flask import Flask, jsonify
import datetime
import httpx
import json
import random
import base64 # Corrected: Added missing import for base64
import re # Added for music cog stub

# --- BOT CONFIGURATION ---
BOT_TOKEN = "MTQwMzEzNTUxMTgxNTY1MTM4OA.GVHM0A.UkFveFE3KS9dSPjyxHncTRje14BBAgi2LIg-sI"
GEMINI_API_KEY = "" # Leave this empty. Canvas will inject the API key at runtime.
IMAGEN_API_KEY = "" # Leave this empty. Canvas will inject the API key at runtime.

# The port to run the Flask web server on.
FLASK_PORT = 5000

# The prefix for non-slash commands (although we'll focus on slash commands).
COMMAND_PREFIX = '!'

# Define the intents for the bot.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# --- FLASK WEB SERVER SETUP ---
app = Flask(__name__)
uptime_start_time = datetime.datetime.now()

@app.route('/status')
def get_status():
    """
    An API endpoint to get the bot's status in a JSON format.
    """
    current_time = datetime.datetime.now()
    uptime = current_time - uptime_start_time
    return jsonify({
        "status": "operational",
        "uptime": str(uptime),
    })

def run_flask():
    """Starts the Flask web server in a separate thread."""
    app.run(port=FLASK_PORT, debug=False, use_reloader=False)

# --- BOT INITIALIZATION ---
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# ====================================================================
# Cog Definitions (All cogs are now defined as classes in this file)
# ====================================================================

# Cog 1: System Commands
class SystemCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.uptime_start_time = datetime.datetime.now()

    @commands.hybrid_command(
        name="system-status",
        description="Displays the operational status of the Nexus core."
    )
    async def system_status(self, ctx: commands.Context):
        current_time = datetime.datetime.now()
        uptime = current_time - self.uptime_start_time
        uptime_str = str(uptime).split('.')[0]
        embed = discord.Embed(
            title="<:sparkles:1255562095908237372> NEXUS // SYSTEM_STATUS",
            description="__**Real-time operational overview.**__",
            color=discord.Color.from_rgb(0, 255, 192)
        )
        embed.add_field(name="`Status`", value="**_OPERATIONAL_**", inline=False)
        embed.add_field(name="`Uptime`", value=f"⏱️ `{uptime_str}`", inline=True)
        embed.add_field(name="`Active Threads`", value=f"⚙️ `{threading.active_count()}`", inline=True)
        embed.set_footer(text="Nexus Protocol v7.2.2")
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="ping-nexus",
        description="Measures the latency of the Nexus system."
    )
    async def ping_nexus(self, ctx: commands.Context):
        latency = round(self.bot.latency * 1000, 2)
        await ctx.send(f"**NEXUS_CORE** // Latency: `{latency}ms`")

    @commands.hybrid_command(
        name="deploy",
        description="Simulates a rapid deployment of a project.",
    )
    @commands.guild_only()
    async def deploy(self, ctx: commands.Context, module_name: str):
        await ctx.defer()
        message = await ctx.send(f"Initiating deployment of `{module_name}`...\n<a:loading:1255562299839955044> `[                ]` _Initializing..._")
        stages = ["Building...", "Uploading...", "Finalizing...", "Verifying..."]
        for i, stage in enumerate(stages):
            await asyncio.sleep(random.uniform(1.5, 3))
            progress = int((i + 1) / len(stages) * 16)
            progress_bar = f"`[{'█' * progress}{' ' * (16 - progress)}]`"
            await message.edit(content=f"Deploying `{module_name}`...\n<a:loading:1255562299839955044> {progress_bar} _{stage}_")
        await asyncio.sleep(1)
        await message.edit(content=f"Deployment of `{module_name}` complete. Status: **_Success_** 🎉")

    @commands.hybrid_command(
        name="purge-logs",
        description="Clears a specified number of messages from the current channel."
    )
    @commands.has_permissions(manage_messages=True)
    async def purge_logs(self, ctx: commands.Context, count: int):
        if count > 100:
            await ctx.send("Maximum purge limit is 100 messages.", ephemeral=True)
            return
        await ctx.send(f"Executing purge protocol for `{count}` messages...")
        await asyncio.sleep(1)
        deleted = await ctx.channel.purge(limit=count + 2) 
        await ctx.send(f"Purge complete. `{len(deleted)}` records deleted.", ephemeral=True, delete_after=5)

# Cog 2: AI Tools
class AITools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = GEMINI_API_KEY

    async def call_gemini_api(self, prompt):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={self.api_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, data=json.dumps(payload), timeout=30)
                response.raise_for_status()
                data = response.json()
                if data and data.get('candidates') and data['candidates'][0].get('content'):
                    return data['candidates'][0]['content']['parts'][0]['text']
                else:
                    return "ERROR: AI system received an invalid response."
            except httpx.HTTPStatusError as e:
                return f"API Error: HTTP status code {e.response.status_code}. Please check the API key and try again."
            except Exception as e:
                return f"ERROR: AI system offline. Details: {e}"

    @commands.hybrid_command(
        name="generate-code",
        description="Generate Python code for a given task."
    )
    async def generate_code(self, ctx: commands.Context, prompt: str):
        await ctx.defer()
        ai_prompt = f"You are an expert Python programmer. Write a complete, well-commented Python script for the following task:\n\nTask: {prompt}\n\nMake sure the code is syntactically correct and includes a main function."
        generated_code = await self.call_gemini_api(ai_prompt)
        embed = discord.Embed(
            title="<:code:1255562404060868668> NEXUS // CODE_GENERATOR",
            description=f"**Task:** _{prompt}_",
            color=discord.Color.from_rgb(0, 255, 192)
        )
        embed.add_field(name="Generated Code", value=f"```python\n{generated_code}\n```", inline=False)
        embed.set_footer(text="Powered by Nexus AI Assistant.")
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="ai-explain",
        description="Explain a given piece of Python code."
    )
    async def ai_explain(self, ctx: commands.Context, code: str):
        await ctx.defer()
        ai_prompt = f"You are an expert code explainer. Break down the following Python code in a clear, easy-to-understand way. Explain what the code does, its main purpose, and how each part of the code contributes to the overall function.\n\nCode:\n{code}"
        explanation = await self.call_gemini_api(ai_prompt)
        embed = discord.Embed(
            title="<:document:1255562441999912066> NEXUS // CODE_ANALYSIS",
            description="**Explanation:**",
            color=discord.Color.from_rgb(0, 255, 192)
        )
        embed.add_field(name="Code", value=f"```python\n{code}\n```", inline=False)
        embed.add_field(name="Explanation", value=explanation, inline=False)
        embed.set_footer(text="Powered by Nexus AI Assistant.")
        await ctx.send(embed=embed)

# Cog 3: Moderation Commands
class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="kick",
        description="Removes a member from the server."
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        if member.top_role >= ctx.author.top_role and ctx.author.id != ctx.guild.owner.id:
            await ctx.send("ERROR: Cannot execute. Target user has an equal or higher role.", ephemeral=True)
            return

        try:
            await member.kick(reason=reason)
            embed = discord.Embed(title="NEXUS // KICK_PROTOCOL", description=f"Kicked `{member.display_name}`. Reason: `{reason}`", color=discord.Color.red())
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("ERROR: Insufficient permissions to kick this user.", ephemeral=True)
        except Exception as e:
            await ctx.send(f"ERROR: An unexpected error occurred: `{e}`", ephemeral=True)

    @commands.hybrid_command(
        name="ban",
        description="Bans a member from the server."
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        if member.top_role >= ctx.author.top_role and ctx.author.id != ctx.guild.owner.id:
            await ctx.send("ERROR: Cannot execute. Target user has an equal or higher role.", ephemeral=True)
            return
            
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(title="NEXUS // BAN_PROTOCOL", description=f"Banned `{member.display_name}`. Reason: `{reason}`", color=discord.Color.red())
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("ERROR: Insufficient permissions to ban this user.", ephemeral=True)
        except Exception as e:
            await ctx.send(f"ERROR: An unexpected error occurred: `{e}`", ephemeral=True)

# Cog 4: Fun Commands
class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="8ball",
        description="Ask the Nexus 8-Ball a question."
    )
    async def eight_ball(self, ctx: commands.Context, *, question: str):
        responses = [
            "__Query Acknowledged__... **Answer:** `It is certain.`",
            "__Query Acknowledged__... **Answer:** `It is decidedly so.`",
            "__Query Acknowledged__... **Answer:** `Without a doubt.`",
            "__Query Acknowledged__... **Answer:** `Yes - definitely.`",
            "__Query Acknowledged__... **Answer:** `You may rely on it.`",
            "__Query Acknowledged__... **Answer:** `As I see it, yes.`",
            "__Query Acknowledged__... **Answer:** `Most likely.`",
            "__Query Acknowledged__... **Answer:** `Outlook good.`",
            "__Query Acknowledged__... **Answer:** `Yes.`",
            "__Query Acknowledged__... **Answer:** `Signs point to yes.`",
            "__Query Acknowledged__... **Answer:** `Reply hazy, try again.`",
            "__Query Acknowledged__... **Answer:** `Ask again later.`",
            "__Query Acknowledged__... **Answer:** `Better not tell you now.`",
            "__Query Acknowledged__... **Answer:** `Cannot predict now.`",
            "__Query Acknowledged__... **Answer:** `Concentrate and ask again.`",
            "__Query Acknowledged__... **Answer:** `Don't count on it.`",
            "__Query Acknowledged__... **Answer:** `My reply is no.`",
            "__Query Acknowledged__... **Answer:** `My sources say no.`",
            "__Query Acknowledged__... **Answer:** `Outlook not so good.`",
            "__Query Acknowledged__... **Answer:** `Very doubtful.`"
        ]
        await ctx.send(f"**Question:** `{question}`\n{random.choice(responses)}")

    @commands.hybrid_command(
        name="coin-flip",
        description="Flips a coin to determine the outcome."
    )
    async def coin_flip(self, ctx: commands.Context):
        result = random.choice(["Heads", "Tails"])
        await ctx.send(f"The coin lands on: **__{result}__**.")

    @commands.hybrid_command(
        name="roll",
        description="Rolls a die with a specified number of sides."
    )
    async def roll(self, ctx: commands.Context, sides: int = 6):
        if sides < 2:
            await ctx.send("ERROR: The die must have at least 2 sides.", ephemeral=True)
            return
        result = random.randint(1, sides)
        await ctx.send(f"Rolling a `{sides}`-sided die... Result: **__{result}__**")

# Cog 5: Utility Commands
class UtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="user-info",
        description="Displays information about a user."
    )
    async def user_info(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        
        embed = discord.Embed(
            title=f"User Info: {member.name}",
            color=member.color if member.color != discord.Color.default() else discord.Color.from_rgb(0, 255, 192),
            timestamp=datetime.datetime.now()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="ID", value=f"`{member.id}`", inline=False)
        embed.add_field(name="Created At", value=f"`{member.created_at.strftime('%Y-%m-%d %H:%M:%S')}`", inline=True)
        embed.add_field(name="Joined Server", value=f"`{member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}`", inline=True)
        embed.add_field(name="Roles", value=', '.join([role.mention for role in member.roles[1:]]) or 'No roles', inline=False)
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="server-info",
        description="Displays information about the current server."
    )
    @commands.guild_only()
    async def server_info(self, ctx: commands.Context):
        guild = ctx.guild
        embed = discord.Embed(
            title=f"Server Info: {guild.name}",
            color=discord.Color.from_rgb(0, 255, 192),
            timestamp=datetime.datetime.now()
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="Owner", value=f"`{guild.owner.name}`", inline=True)
        embed.add_field(name="Created At", value=f"`{guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}`", inline=True)
        embed.add_field(name="Members", value=f"`{guild.member_count}`", inline=True)
        embed.add_field(name="Channels", value=f"`{len(guild.channels)}`", inline=True)
        embed.add_field(name="Roles", value=f"`{len(guild.roles)}`", inline=True)
        embed.add_field(name="Emojis", value=f"`{len(guild.emojis)}`", inline=True)
        await ctx.send(embed=embed)

# Cog 6: Music Commands (Stub)
class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.is_playing = False

    @commands.hybrid_command(
        name="play",
        description="Simulates playing a song (not a real music bot)."
    )
    async def play(self, ctx: commands.Context, song: str):
        if not self.is_playing:
            self.queue.append(song)
            self.is_playing = True
            await ctx.send(f"Now playing: **__{song}__** 🎶")
        else:
            self.queue.append(song)
            await ctx.send(f"**__{song}__** has been added to the queue.")

    @commands.hybrid_command(
        name="skip",
        description="Simulates skipping the current song."
    )
    async def skip(self, ctx: commands.Context):
        if self.is_playing and len(self.queue) > 0:
            skipped_song = self.queue.pop(0)
            if self.queue:
                next_song = self.queue[0]
                await ctx.send(f"Skipped **__{skipped_song}__**. Now playing: **__{next_song}__**.")
            else:
                self.is_playing = False
                await ctx.send(f"Skipped **__{skipped_song}__**. Queue is now empty.")
        else:
            await ctx.send("The queue is empty. Nothing to skip.")
            
    @commands.hybrid_command(
        name="stop",
        description="Simulates stopping music playback."
    )
    async def stop(self, ctx: commands.Context):
        if self.is_playing:
            self.is_playing = False
            self.queue.clear()
            await ctx.send("Music playback has been stopped and the queue has been cleared.")
        else:
            await ctx.send("Music is not currently playing.")

# Cog 7: Image Tools
class ImageTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = IMAGEN_API_KEY
    
    async def generate_image(self, prompt):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={self.api_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "instances": {
                "prompt": prompt
            },
            "parameters": {
                "sampleCount": 1
            }
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, data=json.dumps(payload), timeout=60)
                response.raise_for_status()
                data = response.json()
                if data and data['predictions'] and data['predictions'][0].get('bytesBase64Encoded'):
                    base64_data = data['predictions'][0]['bytesBase64Encoded']
                    return discord.File(
                        await asyncio.to_thread(
                            lambda: base64.b64decode(base64_data)),
                        filename='generated_image.png'
                    )
                else:
                    return None
            except httpx.HTTPStatusError as e:
                return f"API Error: HTTP status code {e.response.status_code}. Please check the API key and try again."
            except Exception as e:
                return f"ERROR: Image generation system offline. Details: {e}"

    @commands.hybrid_command(
        name="generate-image",
        description="Generates an image from a text prompt."
    )
    async def generate_image_command(self, ctx: commands.Context, prompt: str):
        await ctx.defer()
        
        if not prompt:
            await ctx.send("ERROR: Please provide a descriptive prompt for the image.", ephemeral=True)
            return

        await ctx.send(f"**Image generation initiated.** Please wait while the AI crafts your image of: `{prompt}`")
        
        image_file = await self.generate_image(prompt)
        
        if isinstance(image_file, str):
            await ctx.edit_original_response(content=image_file)
        elif image_file:
            await ctx.send(file=image_file, content=f"**Image successfully generated.**")
        else:
            await ctx.edit_original_response(content="ERROR: Failed to generate the image. Please try again with a different prompt.")


@bot.event
async def on_ready():
    """
    This function is called when the bot is ready to operate.
    """
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('-------------------------------------------')

    # Load all cogs.
    try:
        await bot.add_cog(SystemCommands(bot))
        print('Loaded cog: SystemCommands')
        await bot.add_cog(AITools(bot))
        print('Loaded cog: AITools')
        await bot.add_cog(ModerationCommands(bot))
        print('Loaded cog: ModerationCommands')
        await bot.add_cog(FunCommands(bot))
        print('Loaded cog: FunCommands')
        await bot.add_cog(UtilityCommands(bot))
        print('Loaded cog: UtilityCommands')
        await bot.add_cog(MusicCommands(bot))
        print('Loaded cog: MusicCommands')
        await bot.add_cog(ImageTools(bot))
        print('Loaded cog: ImageTools')
    except Exception as e:
        print(f'Failed to load cogs: {e}')

    # Sync all slash commands with Discord.
    await bot.tree.sync()
    print('Slash commands synced successfully.')
    print('Nexus is online and ready for commands.')

# --- MAIN ENTRY POINT ---
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    try:
        bot.run(BOT_TOKEN)
    except discord.LoginFailure as e:
        print(f"Error: Invalid token provided. Please check your BOT_TOKEN. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while running the bot: {e}")
