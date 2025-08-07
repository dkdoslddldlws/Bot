#!/usr/bin/env python3
"""
Discord Bot with Gemini AI Integration
Main entry point for the bot application
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from flask import Flask
from threading import Thread

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from bot.discord_bot import GeminiBot
from utils.logger import setup_logging
from config.settings import BotConfig

# Flask web server for keeping the bot alive
app = Flask('')

@app.route('/')
def home():
    return "Hello! I'm alive!"

def run():
    app.run(host='0.0.0.0', port=5000)

def keep_alive():
    t = Thread(target=run)
    t.start()

async def main():
    """Main function to start the Discord bot"""
    
    # Start Flask web server to keep bot alive
    keep_alive()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config = BotConfig()
        
        # Validate required environment variables
        if not config.DISCORD_TOKEN:
            logger.error("DISCORD_TOKEN environment variable is required")
            sys.exit(1)
            
        if not config.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY environment variable is required")
            sys.exit(1)
        
        # Create and start bot
        logger.info("Starting Gemini Discord Bot...")
        bot = GeminiBot()
        
        # Run the bot
        await bot.start(config.DISCORD_TOKEN)
        
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot shutdown complete.")
