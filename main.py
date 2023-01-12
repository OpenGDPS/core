import flask
from flask import Flask, request, send_from_directory
import os
import sqlite3
import random
import datetime
import time

import util
import hashes
import formats
import cryptx
#import requests
from typing import Dict

import asyncio

dragoncoregd_logo = '''
██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗ ██████╗ ██████╗ ██████╗ ███████╗ ██████╗ ██████╗	 ██████╗ ██╗   ██╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝ ██╔══██╗   ██╔══██╗╚██╗ ██╔╝
██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║██║	    ██║   ██║██████╔╝█████╗  ██║  ███╗██║  ██║   ██████╔╝ ╚████╔╝ 
██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║██║	    ██║   ██║██╔══██╗██╔══╝  ██║   ██║██║  ██║   ██╔═══╝   ╚██╔╝  
██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║╚██████╗╚██████╔╝██║  ██║███████╗╚██████╔╝██████╔╝██╗██║	    ██║   
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝╚═╝	    ╚═╝   
'''

print(dragoncoregd_logo)
print()
print("Loading...")

app = Flask(__name__)
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
charInvalid = ['~', '`', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '=', '`', '!', '"', ';', ':', '?', '-', '+']

print('[main] Loading routes please wait...')
import routes.frontend.accManagament
import routes.request_user_access

import routes.scores.get_scores

import routes.accounts.register
import routes.accounts.login
import routes.accounts.backups
import routes.accounts.get_acc_url
import routes.accounts.get_acc_comments
import routes.accounts.upload_acc_comment
import routes.accounts.delete_acc_comment
import routes.accounts.like_acc_comment
import routes.accounts.update_acc_settings
import routes.accounts.upload_acc_comment

import routes.relationships.accept_friend_request
import routes.relationships.get_friend_requests
import routes.relationships.delete_friend_request
import routes.relationships.upload_friend_request
import routes.relationships.read_friend_request
import routes.relationships.remove_friend

import routes.messages.delete_message
import routes.messages.upload_message
import routes.messages.get_messages
import routes.messages.download_message

import routes.users.get_user_list
import routes.users.get_users
import routes.users.get_user_info
import routes.users.update_user_score
import routes.users.block_user
import routes.users.unblock_user
print('[main] Loaded')
SERVER_URL = 'http://127.0.0.1'
SERVER_URL_NO_HTTP = '127.0.0.1'

def gd_dict_str(d: Dict[int, str], separator: str = ":") -> str:
    """Converts the dict `d` into a Geometry Dash-styled HTTP response.
    Args:
        d (dict): A dictionary of keys to convert. Should be in the format
            key int: str`.
        separator (str): The character to separate all elements of the dict.
    Returns:
        Returns a string from the dict in the format `1:aaa:2:b`
    """

    # Combine them all and send off.
    return separator.join([str(arg[i]) for arg in d.items() for i in (0, 1)])

@app.errorhandler(404)
async def err(e):
	#print(f'Unhandled request! {request.path} {json.dumps(request.values.to_dict())}')
	return '1', 404

@app.route('/dl/songs/<path:filename>', methods=['GET', 'POST'])
async def download_songs(filename):
    return send_from_directory(
        os.path.abspath('.\\dl\\songs'),
        filename,
        as_attachment=False,
        mimetype=None
    )

# def convert_bytes(size):
#     """ Convert bytes to KB, or MB or GB"""
#     for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
#         if size < 1024.0:
#             return "%3.1f %s" % (size)
#         size /= 1024.0

# get song info
@app.route('/database/getGJSongInfo.php', methods=['GET', 'POST'])
async def get_song_info():
	songID = request.form['songID']
	# response = requests.post('http://www.boomlings.com/database/getGJSongInfo.php', data={
	# 	'songID': songID,
	# 	'secret': 'Wmfd2893gb7'
	# })
	cursor.execute(f"SELECT * FROM songs WHERE songID = {songID}")
	result = cursor.fetchone()

	try:
		songName = result[1]
		authorID = result[2]
		authorName = result[3]
		downloadURL = f'{SERVER_URL}/dl/songs/{songID}.mp3'
		size = os.path.getsize(f'.\\dl\\songs\\{songID}.mp3')
			
		return f'1~|~{songID}~|~2~|~{songName}~|~3~|~{authorID}~|~4~|~{authorName}~|~5~|~{size}~|~6~|~~|~10~|~{downloadURL}~|~7~|~~|~8~|~0', 200
	except:
		return '-1', 200

@app.route('/database/getGJTopArtists.php', methods=['GET', 'POST'])
async def get_top_artists():
	cursor.execute(f"SELECT * FROM songs")
	result = cursor.fetchall()
	strArtists = ""
	try:
		for music in result:
			songID = music[0]
			songName = music[1]
			authorName = music[3]
			outName = f'{songName} by {authorName} ! {songID}'
			strArtists = strArtists + f'4:{outName}:7:../redirect?q=http%3A%2F%2F{SERVER_URL_NO_HTTP}%2Fdl%2Fsongs%2F{songID}.mp3|'
		print(strArtists)
		return f'{strArtists}#0:0:20', 200
	except:
		return '-1', 200

# upload level
@app.route('/database/uploadGJLevel21.php', methods=['GET', 'POST'])
async def upload_level():
	gameVersion = request.form['gameVersion']
	binaryVersion = request.form['binaryVersion']
	gdw = request.form['gdw']
	accountID = request.form['accountID']
	gjp = request.form['gjp']
	userName = request.form['userName']
	levelID = request.form['levelID']
	for char in charInvalid:
		levelName = request.form['levelName'].replace(char, '')
	if len(levelName) > 20:
		return '-1', 200
	levelDesc = request.form['levelDesc']
	levelVersion = request.form['levelVersion']
	levelLength = request.form['levelLength']
	audioTrack = request.form['audioTrack']
	auto = request.form['auto']
	password = request.form['password']
	original = request.form['original']
	twoPlayer = request.form['twoPlayer']
	songID = request.form['songID']
	objects = request.form['objects']
	coins = request.form['coins']
	requestedStars = request.form['requestedStars']
	unlisted = request.form['unlisted']
	wt = request.form['wt']
	wt2 = request.form['wt2']
	ldm = request.form['ldm']
	extraString = request.form['extraString']
	seed = request.form['seed']
	seed2 = request.form['seed2']
	levelString = request.form['levelString']
	levelInfo = request.form['levelInfo']
	secret = request.form['secret']
	cursor.execute(f"INSERT INTO levels (gameVersion, binaryVersion, gdw, accountID, gjp, userName, levelID, levelName, levelDesc, levelVersion, levelLength, audioTrack, auto, password, original, twoPlayer, songID, objects, coins, requestedStars, unlisted, wt, wt2, ldm, extraString, seed, seed2, levelString, levelInfo, secret) VALUES ({gameVersion}, {binaryVersion}, {gdw}, {accountID}, '{gjp}', '{userName}', {levelID}, '{levelName}', '{levelDesc}', {levelVersion}, {levelLength}, {audioTrack}, {auto}, {password}, {original}, {twoPlayer}, {songID}, {objects}, {coins}, {requestedStars}, {unlisted}, {wt}, {wt2}, {ldm}, '{extraString}', '{seed}', '{seed2}', '{levelString}', '{levelInfo}', '{secret}')")
	conn.commit()
	return levelID, 200

@app.route('/database/updateGJDesc20.php', methods=['GET', 'POST'])
async def update_level_desc():
	levelID = request.form['levelID']
	levelDesc = request.form['levelDesc']
	cursor.execute(f"UPDATE levels SET levelDesc = '{levelDesc}' WHERE levelID = {levelID}")
	conn.commit()
	return '1', 200

@app.route('/database/getGJDailyLevel.php', methods=['GET', 'POST'])
async def gjfskngfdhgoif():
	cursor.execute(f"SELECT setting FROM config WHERE setting = 'dailyLevelId'")
	#dailyLevelId = cursor.fetchone()[0]
	dailyLevelId = 1 + 100001
	timex = 30
	return f'{dailyLevelId}|{timex}', 200

@app.route('/database/getGJGauntlets21.php', methods=['GET', 'POST'])
async def get_gauntlets():
	gauntletstring = ""
	gauntletid = 1
	lvls = "5,8,4,3,2"
	gauntletstring = gauntletstring + f"1:{gauntletid}:3:{lvls}|"
	str2 = f"{gauntletid}{lvls}"
	return f"{gauntletstring}#{hashes.hash_solo2(str2)}"

@app.route('/database/getGJMapPacks21.php', methods=['GET', 'POST'])
async def get_mappacks():
	id = "1"
	stars = "2"
	coins = "3"
	difficulty = 2
	str1 = f"1:1:2:DragoncoreGD v2!:3:5,8,4,3,2:4:{stars}:5:{coins}:6:{difficulty}:7:245, 66, 66:8:255,255,255|"
	return f"{str1}#1:0:10#{hashes.hash_mappack(id, stars, coins)}"

@app.route('/database/getGJLevels21.php', methods=['GET', 'POST'])
async def get_levels():
	print(request.form)
	levelStr = ""
	lvlID = 1
	lvlName = "Hello"
	lvlVersion = 1
	userID = 1
	# 8:10:9
	starDifficulty = 5
	downloads = 300
	audioTrack = 1
	likes = 1
	starDemon = 1
	starDemonDiff = 3
	starAuto = 0
	starStars = 5
	starFeatured = 1
	starEpic = 1
	objects = 30
	levelDesc = "dGVzdCB5ZXM="
	levelLength = 30
	original = 2147
	twoPlayer = 0
	coins = 3
	starCoins = 3
	requestedStars = 5
	isLDM = 1
	songId = 533164
	levelStr = levelStr + f"1:{lvlID}:2:{lvlName}:5:{lvlVersion}:6:{userID}:8:10:9:{starDifficulty}:10:{downloads}:12:{audioTrack}:13:21:14:{likes}:17:{starDemon}:43:{starDemonDiff}:25:{starAuto}:18:{starStars}:19:{starFeatured}:42:{starEpic}:45:{objects}:3:{levelDesc}:15:{levelLength}:30:{original}:31:{twoPlayer}:37:{coins}:38:{starCoins}:39:{requestedStars}:46:1:47:2:40:{isLDM}:35:{songId}|"
	userStr = "1:DragonFire:1|"
	songStr = "1~|~1~|~2~|~StereoMadness~|~3~|~1~~|~4~|~DragonFireCommunity~|~5~|~10~|~6~|~~|~10~|~github.com/matcool/pygdps/routes/levels/get_levels.mp3~|~7~|~~|~8~|~1|"
	totalLvls = 1
	offset = 0
	hash = hashes.hash_levels(lvlID, starStars)
	return f'{levelStr}#{userStr}#{songStr}#{totalLvls}:{offset}#{hash}', 200

@app.route('/database/downloadGJLevel.php', methods=['GET', 'POST'])
@app.route('/database/downloadGJLevel19.php', methods=['GET', 'POST'])
@app.route('/database/downloadGJLevel20.php', methods=['GET', 'POST'])
@app.route('/database/downloadGJLevel21.php', methods=['GET', 'POST'])
@app.route('/database/downloadGJLevel22.php', methods=['GET', 'POST'])
async def download_level():
	levelID = request.form['levelID']
	cursor.execute(f'SELECT * FROM levels WHERE levelID = {levelID}')
	result = cursor.fetchone()

	# rewrite code:
	#  - https://github.com/RealistikDash/GDPyS/blob/v3/handlers/levels.py#L260
	main_resp = gd_dict_str(
		{
			1: levelID,
			2: result[7],
			3: result[8],
			4: result[27],
			5: result[9],
			6: result[3],
			8: 10 if result[19] else 0,
			9: result[19],
			10: 300,
			12: 1,
			13: result[0],
			14: 100,
			15: result[10],
			17: 1 if 0 == 10 else 0,
			18: 0,
			19: 0,
			25: 1 if 0 == 1 else 0,
			26: 0,
			27: result[13],
			28: '12.01.2023',
			29: 0, # update_ts
			30: 0, # original
			31: 1 if 0 else 0,
			35: 0 if 1 else 0, # level.song.id, level.song
			36: result[24],
			37: result[18],
			38: 1, # TODO: if level.coins_verified else 0
			39: result[19],
			40: 1 if result[23] else 0,
			41: 0, # TODO: DAILY NUMBER.
			42: 0, # TODO: epic. 1 if level.epic else 0
			43: level.demon_diff,
			45: level.objects,
			46: level.working_time,
			47: level.working_time,
        },
    )

# 1.7 feature, yes
# from https://github.com/Cvolton/GMDprivateServer/pull/945
# @app.route('/database/submitGJUserInfo.php', methods=['GET', 'POST'])
# async def sumbit_info():
#     return 'not implemented', 501

# @app.route('/database/restoreGJItems.php', methods=['GET', 'POST'])
# async def restore_items():
#     return 'not implemented', 501

# @app.route('/database/downloadGJLevel.php', methods=['GET', 'POST'])
# @app.route('/database/downloadGJLevel19.php', methods=['GET', 'POST'])
# @app.route('/database/downloadGJLevel20.php', methods=['GET', 'POST'])
# @app.route('/database/downloadGJLevel21.php', methods=['GET', 'POST'])
# @app.route('/database/downloadGJLevel22.php', methods=['GET', 'POST'])
# async def download_level():
# 	print('DOWNLOAD LEVEL: Experimental feature')
# 	uploadDate = "09.01.2023"
# 	settingsString = "1"
# 	userString = "1,8,4,1,10,1,0,100001"
# 	extraString = "0_75_0_0_0_0_0_0_0_0_0_0_57_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0"
# 	levelString = "H4sIAAAAAAAAC6WT3W3DMAyEF2ID_kmy0afMkAE4QFbo8LXEPNRAeTGQF9HSZ57uCPv5sI0knENDtIWFthYiWTRLHnp8SfQQZo4REtLmsgXHFvIjsSRYr0nI5xL7vxLznWy4JKIx-ysvl2UalLk82F7I0PMuRjxLy9KzOB1rPo88eZVtlofta6drTYEF7r7WpMJZhPhbSEhJ9kZGo5Eee2YnOxRu7UQdUuEKb4ykFy2lF62lGbpetHNBFdpinInhQDpuXnivfHWYqcNMHdqy97S816Bng67swiwP6dOpKjJ7_EOIbu9pZTZpNYak1RiSlkHV0aeegetmhTcrdK0osTGyZQPaSlzZSlrZsg4v7vDXT2nsukzsOJPDTA4z-fuLS9OCqLdxm1x1lhMZWpFXz6ha_oBf3dmmzhcIAAA="
# 	lvlStr = f"1:1:2:xd lol:3:{levelString}:5:1:6:469475:8:10:9:2:10:150:11:1:12:0:13:21:14:10:17:10:43:2:25:0:18:8:19:1:42:1:45:40:15:10:30:1:31:0:28:{uploadDate}:29:{uploadDate}:35:1:36:{extraString}:37:0:38:0:39:8:46:120:47:0:48:{settingsString}:40:0:27:0"
# 	responseOutput = f"{lvlStr}#{hashes.hash_levels('1', '8')}#{hashes.hash_solo2(lvlStr)}#{userString}"
# 	return responseOutput, 200

#@app.route('/database/getGJCommentHistory.php', methods=['GET', 'POST'])
#async def comment_history():
#    # #1:0:1
#    a = "~1~2147~2~SGVsbG8hIFRoaXMgaXMgbmV3IGNvbW1lbnQgdGVzdGluZyE=~3~469475~4~2000~5~0~7~0~9~TESTCOMMENT~6~1~10~100"
#    return a + "~11~2$252,119,3:1~dragonfire~7~1~9~3~10~3~11~4~14~0~15~No~16~1#1:0:1"

# @app.route('/database/getGJRewards.php', methods=['GET', 'POST'])
# async def get_rewards():
# 	chk = request.form['chk']
# 	udid = request.form['udid']
# 	a = cryptx.base64_encode(f"1:1:{chk}:{udid}:1:10:10:20:10:10:15:1").replace('/','_').replace('+','-')
# 	hash = hashes.hash_rewards(a)
# 	return f"SaKuJ{a}|{hash}"

app.run(
	host = "0.0.0.0",
	port = 80,
	debug = True
)