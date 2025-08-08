"""
Railway Discord Bot - COPY THIS ENTIRE FILE AS "main.py"
"""

import os
import logging
import asyncio
import aiohttp
import aiosqlite
import discord
from discord.ext import commands
from discord import app_commands
from google import genai
from google.genai import types
import json
from typing import Optional, Dict, Any
from datetime import datetime
import traceback
from flask import Flask
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
UPTIMEROBOT_API_KEY = os.getenv("UPTIMEROBOT_API_KEY")

# Initialize Gemini client
if GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
else:
    gemini_client = None
    logger.warning("GEMINI_API_KEY not found. AI features will be disabled.")

class SimplifiedBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
    
    async def setup_hook(self):
        """Initialize bot"""
        try:
            # Sync slash commands
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"Error in setup_hook: {e}")
    
    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f"Bot is ready! Logged in as {self.user} (ID: {self.user.id})")
        logger.info(f"Connected to {len(self.guilds)} guilds")
        
        # Set bot activity
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name="your commands | /help"
        )
        await self.change_presence(activity=activity, status=discord.Status.online)

# Create bot instance
bot = SimplifiedBot()

# AI Chat Command
@bot.tree.command(name="chat", description="Chat with Gemini AI")
@app_commands.describe(message="Your message to the AI")
async def chat_command(interaction: discord.Interaction, message: str):
    """Chat with Gemini AI"""
    await interaction.response.defer()
    
    try:
        if not gemini_client:
            embed = discord.Embed(
                title="❌ AI Unavailable",
                description="Gemini AI is not configured. Please add GEMINI_API_KEY.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Generate response
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message
        )
        
        ai_response = response.text if response.text else "Sorry, I couldn't generate a response."
        
        # Create embed
        embed = discord.Embed(
            title="🤖 Nexus AI Response",
            description=ai_response[:2000],  # Discord limit
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Requested by {interaction.user}")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        logger.error(f"Error in chat command: {e}")
        embed = discord.Embed(
            title="❌ Error",
            description="Sorry, I encountered an error processing your request.",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed)

# Image Analysis Command
@bot.tree.command(name="analyze_image", description="Analyze an image with AI")
@app_commands.describe(image="Upload an image to analyze")
async def analyze_image(interaction: discord.Interaction, image: discord.Attachment):
    """Analyze an image with Gemini AI"""
    await interaction.response.defer()
    
    try:
        if not gemini_client:
            embed = discord.Embed(
                title="❌ AI Unavailable",
                description="Gemini AI is not configured.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Check if it's an image
        if not image.content_type or not image.content_type.startswith('image/'):
            embed = discord.Embed(
                title="❌ Invalid File",
                description="Please upload a valid image file (PNG, JPG, GIF).",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Download and analyze image
        image_data = await image.read()
        
        response = gemini_client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                types.Part.from_bytes(
                    data=image_data,
                    mime_type=image.content_type,
                ),
                "Analyze this image in detail and describe its key elements, context, and any notable aspects."
            ],
        )
        
        analysis = response.text if response.text else "I couldn't analyze this image."
        
        embed = discord.Embed(
            title="🖼️ Image Analysis",
            description=analysis[:2000],
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Analyzed by {interaction.user}")
        embed.set_image(url=image.url)
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        logger.error(f"Error in image analysis: {e}")
        embed = discord.Embed(
            title="❌ Error",
            description="Failed to analyze the image.",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed)

# Help Command
@bot.tree.command(name="help", description="Show available commands")
async def help_command(interaction: discord.Interaction):
    """Show help information"""
    embed = discord.Embed(
        title="🤖 Nexus AI Bot Commands",
        description="Your intelligent Discord companion powered by Gemini AI",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="💬 Chat Commands",
        value="`/chat` - Chat with Gemini AI\n`/analyze_image` - Analyze images with AI",
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ Information",
        value="`/help` - Show this help message\n`/about` - About this bot",
        inline=False
    )
    
    embed.set_footer(text="Made with ❤️ using Gemini AI")
    
    await interaction.response.send_message(embed=embed)

# About Command
@bot.tree.command(name="about", description="About this bot")
async def about_command(interaction: discord.Interaction):
    """About this bot"""
    embed = discord.Embed(
        title="🤖 About Nexus AI",
        description="A comprehensive Discord bot powered by Google's Gemini AI",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🚀 Features",
        value="• Smart AI conversations\n• Image analysis\n• Always learning\n• Free hosting ready",
        inline=True
    )
    
    embed.add_field(
        name="⚡ Powered By",
        value="• Google Gemini AI\n• Discord.py\n• Python 3.11\n• Free hosting platforms",
        inline=True
    )
    
    embed.add_field(
        name="📊 Stats",
        value=f"• Guilds: {len(bot.guilds)}\n• Latency: {round(bot.latency * 1000)}ms\n• Commands: {len(bot.tree.get_commands())}",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

# Flask web server for Railway hosting
app = Flask(__name__)

@app.route('/')
def home():
    return f"🤖 Nexus AI Bot is running! Connected to {len(bot.guilds)} guilds."

@app.route('/health')
def health():
    return {"status": "healthy", "guilds": len(bot.guilds), "latency": f"{round(bot.latency * 1000)}ms"}

def run_flask():
    """Run Flask server on Railway's required port"""
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

# Run the bot
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        exit(1)
    
    # Start Flask server in background for Railway
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("Flask web server started for Railway hosting")
    
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Error running bot: {e}")
