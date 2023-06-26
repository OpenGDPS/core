from flask import Flask, request, send_from_directory
import os
import sqlite3
import random
import datetime
import requests
from typing import Dict
import base64
import timeago

import hashes
import cryptx
import mainlib

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

app = Flask(__name__)
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
charInvalid = ['~', '`', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '=', '`', '!', '"', ';', ':', '?', '-', '+']
SERVER_URL = 'http://127.0.0.1'
SERVER_URL_NO_HTTP = '127.0.0.1'
SECURITY_APPEND = "xI25fpAapCQg"

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
import routes.like_acc_or_lvl_comment
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

import routes.misc.get_song_info
import routes.misc.get_top_artists

import routes.levels.update_desc

import routes.levels.get_levels
import routes.levels.get_lvl_comments
import routes.levels.upload_lvl_comment
import routes.levels.delete_lvl_comment

import routes.dl

print('[main] Loaded')

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

@app.before_request
async def before_req():
	print(request.form)

# def convert_bytes(size):
#     """ Convert bytes to KB, or MB or GB"""
#     for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
#         if size < 1024.0:
#             return "%3.1f %s" % (size)
#         size /= 1024.0

# upload level
@app.route('/database/uploadGJLevel21.php', methods=['GET', 'POST'])
async def upload_level():
	gameVersion = request.form['gameVersion']
	binaryVersion = request.form['binaryVersion']
	gdw = request.form['gdw']
	accountID = request.form['accountID']
	gjp = request.form['gjp']
	userName = request.form['userName']
	levelID = random.randint(1, 2147483647)
	#levelID = request.form['levelID']
	for char in charInvalid:
		levelName = request.form['levelName'].replace(char, '')
	if len(levelName) > 20:
		return '-1', 200
	levelDesc = request.form['levelDesc']
	levelVersion = request.form['levelVersion']
	levelLength = request.form['levelLength']
	audioTrack = request.form['audioTrack']
	auto = 0
	#auto = request.form['auto']
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
	uploadDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	cursor.execute("INSERT INTO levels (gameVersion, binaryVersion, gdw, accountID, gjp, userName, levelID, levelName, levelDesc, levelVersion, levelLength, audioTrack, auto, password, original, twoPlayer, songID, objects, coins, requestedStars, unlisted, wt, wt2, ldm, extraString, seed, seed2, levelString, levelInfo, secret, stars, isFeatured, isEpic, likes, uploadDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (gameVersion, binaryVersion, gdw, accountID, gjp, userName, levelID, levelName, levelDesc, levelVersion, levelLength, audioTrack, auto, password, original, twoPlayer, songID, objects, coins, requestedStars, unlisted, wt, wt2, ldm, extraString, seed, seed2, levelString, levelInfo, secret, 0, 0, 0, 0, f'{uploadDate}'))
	conn.commit()
	return str(levelID), 200

@app.route('/database/getGJDailyLevel.php', methods=['GET', 'POST'])
async def get_daily_level():
	cursor.execute(f"SELECT setting FROM config WHERE setting = 'dailyLevelId'")
	dailyLevelId = cursor.fetchone()[0]
	#dailyLevelId = 1
	#dailyLevelId = 1 + 100001
	timex = 30
	return f'{dailyLevelId}|{timex}', 200

@app.route('/database/getGJGauntlets21.php', methods=['GET', 'POST'])
async def get_gauntlets():
	gauntletstring = ""
	gauntletid = "1"
	lvls = "5,8,4,3,2"
	gauntletstring = gauntletstring + f"1:{gauntletid}:3:{lvls}|"
	str2 = f"{gauntletid}{lvls}"
	return f"{gauntletstring}#{hashes.hash_solo2(str2)}"

@app.route('/database/getGJMapPacks21.php', methods=['GET', 'POST'])
async def get_mappacks():
	strout = ""
	hashesx = ""
	#for x in range(1):
	id = "1"
	stars = "2"
	coins = "3"
	difficulty = 2
	levels = "5,8,4,3,2"
	rgb = "245, 66, 66"
	rgb2 = "255,255,255"
	strout += f"1:1:2:DragoncoreGD v1:3:{levels}:4:{stars}:5:{coins}:6:{difficulty}:7:{rgb}:8:{rgb2}|"
	hashesx += hashes.hash_mappack(id, stars, coins)
	#hashesx = hashes.hash_solo2(hashesx)
	return f"{strout}#1:0:10#{hashesx}"

@app.route('/database/suggestGJStars20.php', methods=['GET', 'POST'])
async def suggest_stars():
	stars = request.form['stars']
	feature = request.form['feature']
	levelID = request.form['levelID']
	print(stars)
	cursor.execute(f'UPDATE levels SET stars = {stars}, isFeatured = {feature} WHERE levelID = {levelID}')
	conn.commit()
	return '1', 200

# @app.route('/database/downloadGJLevel.php', methods=['GET', 'POST'])
# @app.route('/database/downloadGJLevel19.php', methods=['GET', 'POST'])
# @app.route('/database/downloadGJLevel20.php', methods=['GET', 'POST'])
# @app.route('/database/downloadGJLevel21.php', methods=['GET', 'POST'])
# @app.route('/database/downloadGJLevel22.php', methods=['GET', 'POST'])
# async def download_levelx():
# 	levelID = request.form['levelID'].replace('-', '')
# 	print(levelID)
# 	#return '-1', 501

# 	cursor.execute(f'SELECT * FROM levels WHERE levelID = {levelID}')
# 	result = cursor.fetchone()
# 	#print(result)
# 	#names = result.keys()
# 	#print(names)

# 	# rewrite code:
# 	#  - https://github.com/RealistikDash/GDPyS/blob/v3/handlers/levels.py#L260
# 	main_resp = gd_dict_str(
# 		{
# 			1: levelID,
# 			2: result[7],
# 			3: result[8],
# 			4: result[27],
# 			5: result[9],
# 			6: result[3],
# 			8: 10 if result[19] else 0,
# 			9: result[19],
# 			10: 300,
# 			12: 1,
# 			13: result[0],
# 			14: 100,
# 			15: result[10],
# 			17: 1 if 0 == 10 else 0,
# 			18: 0,
# 			19: 0,
# 			25: 1 if 0 == 1 else 0,
# 			26: 0,
# 			27: result[13],
# 			28: '12.01.2023',
# 			29: 0, # TODO: update_ts
# 			30: 0, # TODO: original
# 			31: 1 if 0 else 0,
# 			35: 0 if 1 else 0, # TODO: level.song.id, level.song
# 			36: result[24],
# 			37: result[18],
# 			38: 1, # TODO: if level.coins_verified else 0
# 			39: result[19],
# 			40: 1 if result[23] else 0,
# 			41: 0, # TODO: DAILY NUMBER.
# 			42: 0, # TODO: epic. 1 if level.epic else 0
# 			43: 0, # TODO: demon_diff
# 			45: result[17],
# 			46: 1, # TODO: working_time
# 			47: 1, # TODO: working_time
#         },
#     )
# 	security_str = ""
# 	s_len = len(main_resp) // 40
# 	for i in range(40):
# 		security_str += main_resp[i * s_len]
# 		security_str = cryptx.sha1_hash(security_str + SECURITY_APPEND)

# 	lvldemon = 0
# 	security_str2 = ",".join(
# 		(
# 			str(result[3]),
# 			str(result[19]),
# 			"1" if lvldemon else "0", # TODO: Level demon
# 			str(levelID),
# 			"1" if 1 else "0",  # TODO: if level.coins_verified else 0
# 			str(0), # TODO: level.feature_id
# 			str(result[13]),
# 			"0",
# 		),
# 	)
# 	security_str2_h = cryptx.sha1_hash(security_str2 + SECURITY_APPEND)

# 	final_resp = "#".join((main_resp, security_str, security_str2_h, security_str2))
# 	print(final_resp)
# 	return final_resp, 200

# 1.7 feature, yes
# from https://github.com/Cvolton/GMDprivateServer/pull/945
# @app.route('/database/submitGJUserInfo.php', methods=['GET', 'POST'])
# async def sumbit_info():
#     return 'not implemented', 501

# @app.route('/database/restoreGJItems.php', methods=['GET', 'POST'])
# async def restore_items():
#     return 'not implemented', 501

def json_to_robtop(dictionary: dict):
    result = ""
    for key, value in dictionary.items():
        result += f"{key}:{value}:"
    return result[:-1]

@app.route('/database/downloadGJLevel.php', methods=['GET', 'POST'])
@app.route('/database/downloadGJLevel19.php', methods=['GET', 'POST'])
@app.route('/database/downloadGJLevel20.php', methods=['GET', 'POST'])
@app.route('/database/downloadGJLevel21.php', methods=['GET', 'POST'])
@app.route('/database/downloadGJLevel22.php', methods=['GET', 'POST'])
async def download_level():
	# gd & gdps bridge
	levelID = request.form['levelID'].replace('-', '')
	extras = request.form['extras']
	# print(levelID)
	# print('DOWNLOAD LEVEL: Experimental feature')

	# with this code we are getting the level Test by DevExit
	# levelID: 62687277
	data = {
		"levelID": levelID,      # level ID
		"secret": "Wmfd2893gb7",  # common secret
		"gameVersion": request.form['gameVersion'],
		"binaryVersion": request.form['binaryVersion'],
		"gdw": request.form['gdw'],
		"extras": request.form['extras'],
		"rs": request.form['rs'],
		"chk": request.form['chk'],
		"udid": request.form['udid'],
		"uuid": request.form['uuid'],
		"gjp": request.form['gjp']
	}

	response = requests.post(
		"http://www.boomlings.com/database/downloadGJLevel22.php",
		data=data,
		headers={
			"User-Agent": "",
			#"Content-Type": "application/x-www-form-urlencoded"
		}
	)

	resp = response.text
	print(resp)

	return resp, 200

	cursor.execute(f'SELECT * FROM levels WHERE levelID = {levelID}')
	result = cursor.fetchone()

	# for testing
	# print(json_to_robtop(
	# 	{
	# 		1: "gdg",
	# 		2: 3
	# 	}
	# ))

	levelName = result[7]
	levelDescription = result[8]
	levelVersion = result[9]
	audioTrack = result[11]
	userID = result[3]
	password = result[13]
	#password = mainlib.CharXor(cryptx.base64_encode(str(result[13])), "26364")
	if result[30] == 1:
		starAuto = 1
	else:
		starAuto = result[12]
	starDifficulty = result[30] * 5
	likes = result[33]
	gameVersion = result[0]
	downloads = 1
	songID = result[16]
	coins = result[18]
	starCoins = 0
	requestedStars = result[19]
	isLDM = result[23]
	starStars = result[30]
	wt = result[21]
	wt2 = result[22]
	twoPlayer = result[15]
	original = result[14]
	levelLength = result[10]
	objects = result[17]
	starFeatured = result[31]
	starEpic = result[32]
	levelInfo = result[28]
	starDemon = 0
	starDemonDiff = 0

	cursor.execute(f'SELECT userName FROM accounts WHERE accId = {userID}')
	try:
		username = cursor.fetchone()[0]
	except:
		userID = 2
		username = "Invalid User"

	uploadDate = "09-01-2023"
	settingsString = "1"
	userString = f"{userID}:{username}:{userID}"
	#userString = f"{userID},10,0,{levelID},{starCoins},{starFeatured},0,0"
	extraString = result[24]
	levelString = result[27]

	lvlStr = json_to_robtop({
        1: levelID,
        2: levelName,
        3: levelDescription,
        4: levelString,
        5: levelVersion,
        6: userID,
        8: 10,
        9: starDifficulty,
        10: downloads,
        11: 1,
        12: audioTrack,
        13: 21,
        14: likes,
        15: levelLength,
		16: likes,
        17: starDemon,
        18: starStars,
        19: starFeatured,
        25: starAuto,
        27: password,
        28: uploadDate,
        29: uploadDate, # updateDate,
        30: original,
        31: twoPlayer,
        35: songID,
        36: extraString,
        37: coins,
        38: starCoins,
        39: requestedStars,
        40: isLDM,
		41: 0,
        42: starEpic,
        43: starDemonDiff,
		44: 0,
        45: objects,
        46: 1,
        47: 2,
        48: 1,
    })
	if extras == '1':
		lvlStr = lvlStr + f":26:{levelInfo}"
	
	someString = f"{userID},{starStars},{starDemon},{levelID},{starCoins},{starFeatured},{password},{0}"
	responseOutput = f"{lvlStr}#{mainlib.GenSolo(lvlStr)}#{mainlib.GenSolo2(someString)}#{someString}"
	# if (request.form['binaryVersion'] == 30):
	# 	responseOutput += f"#{someString}"
	print(responseOutput)
	return responseOutput, 200

@app.route('/database/getGJCommentHistory.php', methods=['GET', 'POST'])
async def comment_history():
	#page = int(request.form['page'])
	now = datetime.datetime.now()

	userID = request.form['userID']
	cursor.execute(f"SELECT * FROM level_comments WHERE authorID = {userID}")
	posts = cursor.fetchall()
	if posts is None:
		return '-1'
	else:
		comments = ""
		for post in posts:
			userID = request.form['userID']
			cursor.execute(f"SELECT * FROM level_comments WHERE authorID = {userID}")
			comments_in_post = cursor.fetchall()
			if comments_in_post is None:
				continue
			else:
				accountId = post[1]
				cursor.execute(f"SELECT icon_cube FROM accounts WHERE accId = '{accountId}'")
				icon_cube = cursor.fetchone()[0]
				#print(f'Comment: {post[1]}, User ID: {post[0]}, Likes: {post[3]}, uploadDate: {post[5]}, Post ID: {post[2]}')
				uploadDate = timeago.format(post[6], now).replace(' ago', '')

				cursor.execute(f"SELECT color_1 FROM accounts WHERE accId = '{accountId}'")
				color_1 = cursor.fetchone()[0]

				cursor.execute(f"SELECT color_2 FROM accounts WHERE accId = '{accountId}'")
				color_2 = cursor.fetchone()[0]

				commentsAppend = f"~11~0:1~{post[2]}~7~1~9~{icon_cube}~10~{color_1}~11~{color_2}~14~0~15~0~16~{accountId}"
				comments = f"1~{post[0]}~2~{post[3]}~3~{accountId}~4~{post[4]}~5~0~7~{post[5]}~9~{uploadDate}~6~{post[7]}~10~{post[8]}{commentsAppend}|" + comments
		#print(comments)
		print(comments)
		return comments + f"#0:0:10", 200


from itertools import cycle

DEFAULT_ENCODING = "utf-8"
DEFAULT_ERRORS = "strict"

def cyclic_xor(data: bytes, key: bytes) -> bytes:
    return bytes(byte ^ key_byte for byte, key_byte in zip(data, cycle(key)))

def cyclic_xor_string(
    string: str, key: str, encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS
) -> str:
    result = cyclic_xor(string.encode(encoding, errors), key.encode(encoding, errors))

    return result.decode(encoding, errors)

# @app.route('/database/getGJRewards.php', methods=['GET', 'POST'])
# async def get_rewards():
# 	chk = request.form['chk']
# 	udid = request.form['udid']
# 	accountID = request.form['accountID']

# 	chk = cyclic_xor_string(cryptx.base64_encode(chk), '59182')

# 	chestOrbs = random.randint(1, 2000)
# 	chestDiamonds = random.randint(1, 2000)
# 	chestShards = random.randint(1, 2000)
# 	chestKeys = random.randint(1, 3)

# 	chestContent = f"{chestOrbs},{chestDiamonds},{chestShards},{chestKeys}"

# 	chest1Content = chestContent
# 	chest2Content = chestContent

# 	rewardType = 1
# 	rewards = cryptx.base64_encode(f"1:{accountID}:{chk}:{udid}:{accountID}:0:{chest1Content}:50:0:{chest2Content}:50:{rewardType}").replace('/','_').replace('+','-')
# 	hash = hashes.hash_rewards(rewards)
# 	return f"SaKuJ{rewards}|{hash}"

app.run(
	host = "0.0.0.0",
	# port = 80,
	debug = True
)
