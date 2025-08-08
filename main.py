# Run the bot
if __name__ == "__main__":
    logger.info("Bot startup sequence initiated...")
    
    # Check critical environment variables
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        logger.error("Please add DISCORD_TOKEN to Railway environment variables")
        exit(1)
    
    # Start Flask server in background for Railway
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("Flask web server started for Railway hosting")
    logger.info("Discord token found, proceeding with startup...")
    
    try:
        # Start Flask server in background for Railway
        logger.info("Starting Flask web server for Railway...")
        flask_thread = Thread(target=run_flask, daemon=True)
        flask_thread.start()
        logger.info("Flask web server started successfully")
        
        # Start Discord bot
        logger.info("Starting Discord bot connection...")
        bot.run(DISCORD_TOKEN)
        
    except discord.LoginFailure:
        logger.error("Failed to login to Discord. Check your DISCORD_TOKEN!")
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        logger.error(f"Critical error running bot: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        exit(1)
