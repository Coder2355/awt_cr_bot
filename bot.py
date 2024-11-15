from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import asyncio
from config import config  # Import the configuration file

app = Client("anime_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

# Start message
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "👋 Hello! I am your Anime Downloader Bot.\n\n"
        "Send /search <anime name> to look up an anime.\n"
        "I'll guide you through selecting episodes and quality options to download your favorite anime!",
    )

# Step 1: Search for Anime with status message
@app.on_message(filters.command("search"))
async def search_anime(client, message):
    query = message.text.split("/search ", 1)[-1]
    if not query:
        await message.reply("Please provide an anime name to search.")
        return
    
    status_msg = await message.reply("🔍 Searching for anime...")
    anime_results = search_gogoanime(query)
    
    if anime_results:
        buttons = [[InlineKeyboardButton(anime["title"], callback_data=f"anime_{anime['id']}")]
                   for anime in anime_results]
        await status_msg.edit("Select an anime:", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await status_msg.edit("No anime found with that name.")

# Step 2: Fetch Episodes on Anime Selection with status message
@app.on_callback_query(filters.regex("^anime_"))
async def show_episodes(client, callback_query):
    anime_id = callback_query.data.split("_")[1]
    status_msg = await callback_query.message.reply("📂 Fetching episodes...")
    episodes = fetch_episodes(anime_id)
    
    if episodes:
        buttons = [[InlineKeyboardButton(f"Episode {ep['number']}", callback_data=f"episode_{ep['id']}")]
                   for ep in episodes]
        await status_msg.edit("Select an episode:", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await status_msg.edit("No episodes found.")

# Step 3: Show Quality Options on Episode Selection with status message
@app.on_callback_query(filters.regex("^episode_"))
async def show_quality_options(client, callback_query):
    episode_id = callback_query.data.split("_")[1]
    buttons = [
        [InlineKeyboardButton("360p", callback_data=f"download_{episode_id}_360")],
        [InlineKeyboardButton("480p", callback_data=f"download_{episode_id}_480")],
        [InlineKeyboardButton("720p", callback_data=f"download_{episode_id}_720")],
        [InlineKeyboardButton("1080p", callback_data=f"download_{episode_id}_1080")]
    ]
    await callback_query.message.reply("Select quality:", reply_markup=InlineKeyboardMarkup(buttons))

# Step 4: Download and Send the Episode with status messages
@app.on_callback_query(filters.regex("^download_"))
async def download_and_send(client, callback_query):
    _, episode_id, quality = callback_query.data.split("_")
    
    status_msg = await callback_query.message.reply("📥 Starting download...")
    video_url = get_video_url(episode_id, quality)
    
    if not video_url:
        await status_msg.edit("Failed to retrieve the video URL.")
        return

    file_path = await download_video(video_url, status_msg)  # Pass status message to show download progress
    await callback_query.message.reply_document(file_path)
    await status_msg.edit("✅ Download complete and sent to you!")

# Helper functions
def search_gogoanime(query):
    response = requests.get(f"{config.GOGOANIME_API_URL}/search?keyword={query}")
    return response.json().get("results", [])

def fetch_episodes(anime_id):
    response = requests.get(f"{config.GOGOANIME_API_URL}/anime/{anime_id}/episodes")
    return response.json().get("episodes", [])

async def download_video(url, status_msg):
    # Placeholder for actual download code
    # Show ongoing status, e.g., "Downloading: 25%"
    await asyncio.sleep(5)  # Simulate download
    return "/path/to/downloaded/video.mp4"
    
def get_video_url(episode_id, quality):
    # Simulate getting the video URL
    return f"https://example.com/video/{episode_id}_{quality}.mp4"

app.run()
