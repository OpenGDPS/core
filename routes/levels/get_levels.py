from __main__ import app, request, cursor, requests, mainlib

@app.route('/database/getGJLevels21.php', methods=['GET', 'POST'])
async def get_levels():
	# gd & gdps bridge
	# print(levelID)
	# print('DOWNLOAD LEVEL: Experimental feature')

	# with this code we are getting the level Test by DevExit
	# levelID: 62687277
	data = {
		"secret": "Wmfd2893gb7",  # common secret
		"type": request.form['type'],
		"str": request.form['str'],
		"len": request.form['len'],
		"page": request.form['page'],
		"total": request.form['total'],
		"uncompleted": request.form['uncompleted'],
		"onlyCompleted": request.form['onlyCompleted'],
		"featured": request.form['featured'],
		"original": request.form['original'],
		"twoPlayer": request.form['twoPlayer'],
		"coins": request.form['coins'],
		"epic": request.form['epic'],
		"secret": request.form['secret'],
	}

	response = requests.post(
		"http://www.boomlings.com/database/getGJLevels21.php",
		data=data,
		headers={
			"User-Agent": "",
			#"Content-Type": "application/x-www-form-urlencoded"
		}
	)

	resp = response.text
	print(resp)

	return resp, 200

	return '', 200
	filtersString = ''

	try:
		filterCoins = request.form['coins']
		filterFeatured = request.form['featured']
		filterEpic = request.form['epic']
		filterTwoPlayer = request.form['twoPlayer']
		filterLen = request.form['len']
		#filterStr = request.form['str']

		if filterCoins == '1': filtersString += ' AND coins >= 1'
		if filterFeatured == '1': filtersString += ' AND isFeatured = 1'
		if filterEpic == '1': filtersString += ' AND isEpic = 1'
		if filterTwoPlayer == '1': filtersString += ' AND twoPlayer = 1'
		if filterLen != '-': filtersString += f' AND levelLength = {filterLen}'

		filterSongID = request.form['song']
		filtersString += f' AND songID = {filterSongID}'
	except:
		pass

	try:
		filterType = request.form['type']
		if filterType == "1": filtersString += " ORDER BY downloads DESC"
		if filterType == "2": filtersString += " ORDER BY likes DESC"
		if filterType == "4": filtersString += " ORDER BY uploadDate DESC"
	except:
		pass

	#if filterStr != '': filtersString += f' AND levelName = "{filterStr}"  accountID = {filterStr}'

	print(filtersString)

	cursor.execute('SELECT * FROM levels WHERE unlisted = 0' + filtersString + ' LIMIT 1')
	resultx = cursor.fetchall()

	totalLvls = len(resultx)
	offset = 0

	tempLvlsList = []

	levelStr = ""
	userStr = ""
	songStr = ""

	for result in resultx:
		#print(result)
		levelStr = ""
		lvlID = result[6]
		lvlName = result[7]
		lvlVersion = result[9]
		userID = result[3]
		cursor.execute(f'SELECT userName FROM accounts WHERE accId = {userID}')
		try:
			username = cursor.fetchone()[0]
		except:
			userID = 2
			username = "Invalid User"
		# 8:10:9
		# starDifficulty - Difficulty
		# starStars - Stars
		if result[30] == 1:
			starAuto = 1
		else:
			starAuto = result[12]
		starDifficulty = result[30] * 5

		downloads = result[34]
		audioTrack = result[11]
		likes = result[33]
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
		userStr = userStr + f"{userID}:{username}:{userID}|"
		songStr = songStr + "1~|~1~|~2~|~StereoMadness~|~3~|~1~~|~4~|~DragonFireCommunity~|~5~|~10~|~6~|~~|~10~|~github.com/matcool/pygdps/routes/levels/get_levels.mp3~|~7~|~~|~8~|~1|"
		tempLvlsList.append({'levelid': lvlID, 'starstars': starStars, 'starcoins': coins})
	hash = mainlib.GenMulti(tempLvlsList)
	#hash = hashes.hash_levels2(result)
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