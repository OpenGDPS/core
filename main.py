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
import timeago

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
	levelID = request.form['levelID']
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
	cursor.execute(f"INSERT INTO levels (gameVersion, binaryVersion, gdw, accountID, gjp, userName, levelID, levelName, levelDesc, levelVersion, levelLength, audioTrack, auto, password, original, twoPlayer, songID, objects, coins, requestedStars, unlisted, wt, wt2, ldm, extraString, seed, seed2, levelString, levelInfo, secret, stars, isFeatured, isEpic) VALUES ({gameVersion}, {binaryVersion}, {gdw}, {accountID}, '{gjp}', '{userName}', {levelID}, '{levelName}', '{levelDesc}', {levelVersion}, {levelLength}, {audioTrack}, {auto}, {password}, {original}, {twoPlayer}, {songID}, {objects}, {coins}, {requestedStars}, {unlisted}, {wt}, {wt2}, {ldm}, '{extraString}', '{seed}', '{seed2}', '{levelString}', '{levelInfo}', '{secret}', 0, 0, 0)")
	conn.commit()
	return levelID, 200

@app.route('/database/getGJDailyLevel.php', methods=['GET', 'POST'])
async def gjfskngfdhgoif():
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
	id = "1"
	stars = "2"
	coins = "3"
	difficulty = 2
	str1 = f"1:1:2:DragoncoreGD v2!:3:5,8,4,3,2:4:{stars}:5:{coins}:6:{difficulty}:7:245, 66, 66:8:255,255,255|"
	return f"{str1}#1:0:10#{hashes.hash_mappack(id, stars, coins)}"

@app.route('/database/getGJLevels21.php', methods=['GET', 'POST'])
async def get_levels():
	print(request.form)
	filtersString = ''

	filterCoins = request.form['coins']
	filterFeatured = request.form['featured']
	filterEpic = request.form['epic']
	filterTwoPlayer = request.form['twoPlayer']

	try:
		filterSongID = request.form['song']
		filtersString += f' AND songID = {filterSongID}'
	except:
		pass

	if filterCoins == '1': filtersString += ' AND coins >= 1'
	if filterFeatured == '1': filtersString += ' AND isFeatured = 1'
	if filterEpic == '1': filtersString += ' AND isEpic = 1'
	if filterTwoPlayer == '1': filtersString += ' AND twoPlayer = 1'

	cursor.execute('SELECT * FROM levels WHERE unlisted = 0' + filtersString)
	resultx = cursor.fetchall()
	try:
		result = random.choice(resultx)
	except:
		return '-1', 200
	#print(result)
	levelStr = ""
	lvlID = result[6]
	lvlName = result[7]
	lvlVersion = result[9]
	userID = result[3]
	# 8:10:9
	# starDifficulty - Difficulty
	# starStars - Stars
	if result[30] == 1:
		starAuto = 1
	else:
		starAuto = result[12]
	starDifficulty = result[30] * 5

	downloads = 1
	audioTrack = result[11]
	likes = 1
	starDemon = 0
	starDemonDiff = 0
	starStars = result[30]
	starFeatured = result[31]
	starEpic = result[32]
	objects = result[17]
	levelDesc = result[8]
	levelLength = result[10]
	original = result[14]
	twoPlayer = result[15]
	coins = result[18]
	starCoins = 0
	requestedStars = result[19]
	isLDM = result[23]
	songId = result[16]
	levelStr = levelStr + f"1:{lvlID}:2:{lvlName}:5:{lvlVersion}:6:{userID}:8:10:9:{starDifficulty}:10:{downloads}:12:{audioTrack}:13:21:14:{likes}:17:{starDemon}:43:{starDemonDiff}:25:{starAuto}:18:{starStars}:19:{starFeatured}:42:{starEpic}:45:{objects}:3:{levelDesc}:15:{levelLength}:30:{original}:31:{twoPlayer}:37:{coins}:38:{starCoins}:39:{requestedStars}:46:1:47:2:40:{isLDM}:35:{songId}|"
	userStr = "1:DragonFire:1|"
	songStr = "1~|~1~|~2~|~StereoMadness~|~3~|~1~~|~4~|~DragonFireCommunity~|~5~|~10~|~6~|~~|~10~|~github.com/matcool/pygdps/routes/levels/get_levels.mp3~|~7~|~~|~8~|~1|"
	totalLvls = len(resultx)
	offset = 0
	hash = hashes.hash_levels(lvlID, starStars)
	# levelStr = ""
	# lvlID = 1
	# lvlName = "Hello"
	# lvlVersion = 1
	# userID = 1
	# # 8:10:9
	# # starDifficulty - Difficulty
	# # starStars - Stars
	# starDifficulty = 5
	# downloads = 301
	# audioTrack = 1
	# likes = 1
	# starDemon = 0
	# starDemonDiff = 0
	# starAuto = 0
	# starStars = 2
	# starFeatured = 1
	# starEpic = 1
	# objects = 30
	# levelDesc = "VGhpcyBsZXZlbCB3YXMgdXNpbmcgZm9yIGNvcmUgdGVzdGluZy4gUmVwb3J0IGFueSBidWdzIGluIERyYWdvbkZpcmUncyBkbQ=="
	# levelLength = 30
	# original = 0
	# twoPlayer = 0
	# coins = 0
	# starCoins = 0
	# requestedStars = 5
	# isLDM = 0
	# songId = 533164
	# levelStr = levelStr + f"1:{lvlID}:2:{lvlName}:5:{lvlVersion}:6:{userID}:8:10:9:{starDifficulty}:10:{downloads}:12:{audioTrack}:13:21:14:{likes}:17:{starDemon}:43:{starDemonDiff}:25:{starAuto}:18:{starStars}:19:{starFeatured}:42:{starEpic}:45:{objects}:3:{levelDesc}:15:{levelLength}:30:{original}:31:{twoPlayer}:37:{coins}:38:{starCoins}:39:{requestedStars}:46:1:47:2:40:{isLDM}:35:{songId}|"
	# userStr = "1:DragonFire:1|"
	# songStr = "1~|~1~|~2~|~StereoMadness~|~3~|~1~~|~4~|~DragonFireCommunity~|~5~|~10~|~6~|~~|~10~|~github.com/matcool/pygdps/routes/levels/get_levels.mp3~|~7~|~~|~8~|~1|"
	# totalLvls = 1
	# offset = 0
	# hash = hashes.hash_levels(lvlID, starStars)
	return f'{levelStr}#{userStr}#{songStr}#{totalLvls}:{offset}#{hash}', 200

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
# async def download_level():
# 	levelID = 1
# 	#levelID = request.form['levelID'].replace('-', '')
# 	#print(levelID)
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

@app.route('/database/downloadGJLevel.php', methods=['GET', 'POST'])
@app.route('/database/downloadGJLevel19.php', methods=['GET', 'POST'])
@app.route('/database/downloadGJLevel20.php', methods=['GET', 'POST'])
@app.route('/database/downloadGJLevel21.php', methods=['GET', 'POST'])
@app.route('/database/downloadGJLevel22.php', methods=['GET', 'POST'])
async def download_level():
	print('DOWNLOAD LEVEL: Experimental feature')
	uploadDate = "09.01.2023"
	settingsString = "1"
	userString = "1,2,0,1,10,1,0,0"
	extraString = "0_75_0_0_0_0_0_0_0_0_0_0_57_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0"
	levelString = "H4sIAAAAAAAAC6WT3W3DMAyEF2ID_kmy0afMkAE4QFbo8LXEPNRAeTGQF9HSZ57uCPv5sI0knENDtIWFthYiWTRLHnp8SfQQZo4REtLmsgXHFvIjsSRYr0nI5xL7vxLznWy4JKIx-ysvl2UalLk82F7I0PMuRjxLy9KzOB1rPo88eZVtlofta6drTYEF7r7WpMJZhPhbSEhJ9kZGo5Eee2YnOxRu7UQdUuEKb4ykFy2lF62lGbpetHNBFdpinInhQDpuXnivfHWYqcNMHdqy97S816Bng67swiwP6dOpKjJ7_EOIbu9pZTZpNYak1RiSlkHV0aeegetmhTcrdK0osTGyZQPaSlzZSlrZsg4v7vDXT2nsukzsOJPDTA4z-fuLS9OCqLdxm1x1lhMZWpFXz6ha_oBf3dmmzhcIAAA="
	lvlStr = f"1:1:2:Hello:3:omg:4:{levelString}:5:1:6:1:8:10:9:2:10:150:11:1:12:0:13:21:14:10:17:10:43:2:25:0:18:8:19:1:42:1:45:30:15:10:30:0:31:0:28:{uploadDate}:29:{uploadDate}:35:533164:36:{extraString}:37:0:38:0:39:5:46:120:47:0:48:{settingsString}:40:0:27:0"
	responseOutput = f"{lvlStr}#{hashes.hash_levels(1, 2)}#{hashes.hash_solo2(lvlStr)}#{hashes.hash_level(userString)}"
	print(responseOutput)
	return responseOutput, 200

@app.route('/database/uploadGJComment21.php', methods=['GET', 'POST'])
async def upload_comment_level():
	levelID = request.form['levelID']
	accountID = request.form['accountID']
	userName = request.form['userName']
	comment = request.form['comment']
	date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	commentID = random.randint(1, 2147483647)
	cursor.execute(f'INSERT INTO level_comments VALUES({levelID}, {accountID}, "{userName}", "{comment}", 0, 0, "{date}", {commentID})')
	conn.commit()
	return '1', 200

@app.route('/database/deleteGJComment20.php', methods=['GET', 'POST'])
async def delete_comment_level():
	levelID = request.form['levelID']
	commentID = request.form['commentID']
	cursor.execute(f'DELETE FROM level_comments WHERE levelID = {levelID} AND commentID = {commentID}')
	conn.commit()
	return '-1', 200

@app.route('/database/getGJComments21.php', methods=['GET', 'POST'])
async def get_comments_level():
	#page = int(request.form['page'])
	levelId = request.form['levelID']
	now = datetime.datetime.now()

	cursor.execute(f"SELECT * FROM level_comments WHERE levelID = {levelId}")
	posts = cursor.fetchall()
	if posts is None:
		return '-1'
	else:
		comments = ""
		for post in posts:
			cursor.execute(f"SELECT * FROM level_comments WHERE levelID = {levelId}")
			comments_in_post = cursor.fetchall()
			if comments_in_post is None:
				continue
			else:
				accountId = post[1]
				cursor.execute(f"SELECT icon_cube FROM accounts WHERE accId = '{accountId}'")
				icon_cube = cursor.fetchone()[0]
				#print(f'Comment: {post[1]}, User ID: {post[0]}, Likes: {post[3]}, uploadDate: {post[5]}, Post ID: {post[2]}')
				uploadDate = timeago.format(post[6], now).replace(' ago', '')
				percentCompleted = 1

				cursor.execute(f"SELECT color_1 FROM accounts WHERE accId = '{accountId}'")
				color_1 = cursor.fetchone()[0]

				cursor.execute(f"SELECT color_2 FROM accounts WHERE accId = '{accountId}'")
				color_2 = cursor.fetchone()[0]

				commentsAppend = f"~11~0:1~{post[2]}~7~1~9~{icon_cube}~10~{color_1}~11~{color_2}~14~0~15~0~16~{accountId}"
				comments = f"2~{post[3]}~3~{accountId}~4~{post[4]}~5~0~7~{post[5]}~9~{uploadDate}~6~{post[7]}~10~{percentCompleted}{commentsAppend}|" + comments
		#print(comments)
		print(comments)
		return comments + f"#0:0:10", 200
	#return f'2~SGVsbG8hIE5ldyBsZXZlbCBzeXN0ZW0gb21n~3~1~4~200~5~0~7~0~9~15.01.2023~6~1~10~53~11~2:1~DragonFire~7~1~9~1~10~3~11~4~14~0~15~0~16~1|#$1:$1:$1'

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