import disnake as discord
from disnake.ext import commands

import random
import sqlite3

opengdps_logo = '''
   ____                    _____ _____  _____   _____ 
  / __ \                  / ____|  __ \|  __ \ / ____|
 | |  | |_ __   ___ _ __ | |  __| |  | | |__) | (___  
 | |  | | '_ \ / _ \ '_ \| | |_ | |  | |  ___/ \___ \ 
 | |__| | |_) |  __/ | | | |__| | |__| | |     ____) |
  \____/| .__/ \___|_| |_|\_____|_____/|_|    |_____/ 
        | |                                           
        |_|                                           
'''

print(opengdps_logo)
print()
print("Loading...")

bot = commands.Bot()
token = "MTA2MzQ3NDM3NDEyMTg4NTgxNg.GwFh3E.5vhMuvj0B5hcOW0cYL-vVRMYPVd62Z_AdOXjvA"

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

@bot.event
async def on_ready():
    print('[bot] Bot started')

@bot.slash_command(description = "Developer testing")
async def upload_music(ctx, songname: str, file: discord.Attachment, authorname: str = 'Reupload'):
    await ctx.send('Uploading song please wait...')
    # 1 - Reupload
    if authorname != 'Reupload': authorID = random.randint(2, 999999)
    else: authorID = 1
    musicID = random.randint(1, 999999)

    if file.filename.endswith('.mp3') == False: return await ctx.send('Invalid format: Only mp3 supported')
    print('[upload_music] Saving music file from user...')
    await file.save(f"./dl/songs/{musicID}.mp3")
    print('[upload_music] Saved')
    print('[upload_music] INSERT INTO songs')
    cursor.execute(f'INSERT INTO songs VALUES({musicID}, "{songname}", {authorID}, "{authorname}")')
    conn.commit()
    await ctx.send(f'Song uploaded | ID: {musicID}')

bot.run(token)
