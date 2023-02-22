# Discord Bot to log sourcebans database in discord by Бизак🧃#3385
# My Discord Server https://discord.gg/BvJaXXDbat
# Visit my website https://astralcm.com/
# Astral Community™ Paypal if you wanna donate:
# https://www.paypal.com/paypalme/ByZakUnknow

import discord
import pymysql.cursors
import asyncio

# Define your database connection information
HOST = 'localhost'
USER = 'user'
PASSWORD = 'password'
DATABASE = 'sb'

# Define your Discord bot token
TOKEN = 'Token'

# Define your Discord channel ID
CHANNEL_ID = Channel ID

# Define your query to retrieve the latest ban information
query = """
SELECT `name`, `authid`, `reason`, `country`, `length`
FROM `sb_bans`
ORDER BY `created` DESC
LIMIT 1
"""

# Create a connection to your SourceBans database
connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DATABASE)

# Create a Discord client object with the required intents
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Keep track of the latest ban that was sent
latest_ban = None

# Define an event to run when the bot is ready
@client.event
async def on_ready():
    global latest_ban
    
    print(f'{client.user} is working')

    # Retrieve the latest ban information from your SourceBans database
    with connection.cursor() as cursor:
        cursor.execute(query)
        ban_info = cursor.fetchone()

    # If the latest ban is different from the previous latest ban, send a new message
    if ban_info != latest_ban:
        # Format the latest ban information as a Discord message
        embed = await format_ban_message(ban_info)

        # Send the ban message to your Discord channel
        channel = client.get_channel(CHANNEL_ID)
        await channel.send(embed=embed)

        # Update the latest ban
        latest_ban = ban_info

    # Wait for 10 seconds and check for new bans again
    await asyncio.sleep(10)
    await on_ready()

# Define a function to format the ban information as a Discord message
async def format_ban_message(ban_info):
    embed = discord.Embed(title="Latest Ban", color=0x1e1f22)
    embed.add_field(name="Name", value=ban_info[0], inline=False)
    embed.add_field(name="SteamID", value=ban_info[1], inline=False)
    embed.add_field(name="Reason", value=ban_info[2], inline=False)
    embed.add_field(name="From", value=ban_info[3], inline=False)
    embed.add_field(name="Expires on", value=ban_info[4], inline=False)

    return embed

# Start the Discord bot
client.run(TOKEN)
