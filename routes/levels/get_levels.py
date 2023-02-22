from __main__ import app, request, cursor, random, hashes


@app.route('/database/getGJLevels21.php', methods=['GET', 'POST'])
async def get_levels():
	print(request.form)
	filtersString = ''

	try:
		filterCoins = request.form['coins']
		filterFeatured = request.form['featured']
		filterEpic = request.form['epic']
		filterTwoPlayer = request.form['twoPlayer']
		#filterStr = request.form['str']

		if filterCoins == '1': filtersString += ' AND coins >= 1'
		if filterFeatured == '1': filtersString += ' AND isFeatured = 1'
		if filterEpic == '1': filtersString += ' AND isEpic = 1'
		if filterTwoPlayer == '1': filtersString += ' AND twoPlayer = 1'

		filterSongID = request.form['song']
		filtersString += f' AND songID = {filterSongID}'
	except:
		pass

	#if filterStr != '': filtersString += f' AND levelName = "{filterStr}"  accountID = {filterStr}'

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

	downloads = 1
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
	userStr = f"{userID}:{username}:{userID}|"
	songStr = "1~|~1~|~2~|~StereoMadness~|~3~|~1~~|~4~|~DragonFireCommunity~|~5~|~10~|~6~|~~|~10~|~github.com/matcool/pygdps/routes/levels/get_levels.mp3~|~7~|~~|~8~|~1|"
	totalLvls = len(resultx)
	offset = 0
	hash = hashes.hash_levels(lvlID, starStars)
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