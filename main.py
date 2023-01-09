import flask
from flask import Flask, request
import sqlite3
import random
import datetime
import time

import util
import hashes
import formats
import cryptx

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

import routes.users.get_user_list
import routes.relationships.remove_friend

import routes.messages.delete_message
import routes.messages.upload_message
import routes.messages.get_messages
import routes.messages.download_message

import routes.users.get_user_info
import routes.users.update_user_score

import routes.users.block_user
import routes.users.unblock_user
print('[main] Loaded')

@app.errorhandler(404)
async def err(e):
	#print(f'Unhandled request! {request.path} {json.dumps(request.values.to_dict())}')
	return '1', 404

# upload level
@app.route('/database/uploadGJLevel21.php', methods=['GET', 'POST'])
async def upload_level():
	#	 "gameVersion"	INTEGER,
	# "binaryVersion"	INTEGER,
	# "gdw"	INTEGER,
	# "accountID"	INTEGER,
	# "gjp"	TEXT,
	# "userName"	TEXT,
	# "levelID"	INTEGER,
	# "levelName"	TEXT,
	# "levelDesc"	TEXT,
	# "levelVersion"	INTEGER,
	# "levelLength"	INTEGER,
	# "audioTrack"	INTEGER,
	# "auto"	INTEGER,
	# "password"	INTEGER,
	# "original"	INTEGER,
	# "twoPlayer"	INTEGER,
	# "songID"	INTEGER,
	# "objects"	INTEGER,
	# "coins"	INTEGER,
	# "uestedStars"	INTEGER,
	# "unlisted"	INTEGER,
	# "wt"	INTEGER,
	# "wt2"	INTEGER,
	# "ldm"	INTEGER,
	# "extraString"	TEXT,
	# "seed"	TEXT,
	# "seed2"	TEXT,
	# "levelString"	TEXT,
	# "levelInfo"	TEXT,
	# "secret"	TEXT
	# add this all to the database
	gameVersion = request.form['gameVersion']
	binaryVersion = request.form['binaryVersion']
	gdw = request.form['gdw']
	accountID = request.form['accountID']
	gjp = request.form['gjp']
	userName = request.form['userName']
	levelID = request.form['levelID']
	levelName = request.form['levelName']
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

@app.route('/database/getGJUsers20.php', methods=['GET', 'POST'])
async def get_users():
	accountOut = ""
	userToSearch = request.form['str']
	cursor.execute(f"SELECT * FROM accounts WHERE userName = '{userToSearch}' OR accId = '{userToSearch}' ORDER BY stars DESC")
	accounts = cursor.fetchall()
	rank = 0
	for account in accounts:
		username = account[0]
		userID = account[4]
		stars = account[5]
		coins = account[6]
		userCoins = account[7]
		diamonds = account[8]
		demons = account[9]
		creator_points = account[10]
		icon_cube = account[15]
		#icon_type = account[24]
		icon_type = 0
		rank = rank + 1
		color_1 = account[25]
		color_2 = account[26]
		if stars < 1: pass
		else:
			accountOut = accountOut + f"1:{username}:2:{userID}:13:{coins}:17:{userCoins}:6:{rank}:9:{icon_cube}:10:{color_1}:11:{color_2}:14:{icon_type}:15:0:16:{userID}:3:{stars}:8:{creator_points}:4:{demons}|"
	return f'{accountOut}#0:0:10', 200

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