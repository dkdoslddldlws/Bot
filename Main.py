    await interaction.response.send_message(embed=embed)
# Flask web server for Railway hosting
from flask import Flask
from threading import Thread
# Create Flask app for Railway health checks
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
