from __main__ import app, cursor, request

@app.route('/database/getGJScores20.php', methods=['GET', 'POST'])
async def get_scores():
	cursor.execute(f"SELECT * FROM config")
	config = cursor.fetchall()
	if config[1][1] == 0:
		return f"1:Disabled by server administrator:2:1:13:0:17:0:6:1:9:0:10:0:11:0:14:0:15:0:16:1:3:0:8:0:4:0:7:1:46:0|"

	# leaderboard
	#print(request.form)
	accID = request.form['accountID']
	accountOut = ""
	if request.form['type'] == "relative":
		cursor.execute(f"SELECT * FROM accounts")
		accounts = cursor.fetchall()
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
			color_1 = account[25]
			color_2 = account[26]
			accountOut = accountOut + f"1:{username}:2:{userID}:13:{coins}:17:{userCoins}:6:{userID}:9:{icon_cube}:10:{color_1}:11:{color_2}:14:{icon_type}:15:0:16:{userID}:3:{stars}:8:{creator_points}:4:{demons}:7:{userID}:46:{diamonds}|"
		
		return accountOut, 200
	
	if request.form['type'] == "creators":
		cursor.execute(f"SELECT * FROM accounts")
		accounts = cursor.fetchall()
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
			color_1 = account[25]
			color_2 = account[26]
			#print(f"Creator points: {creator_points}")
			if creator_points == 0: pass
			else:
				accountOut = accountOut + f"1:{username}:2:{userID}:13:{coins}:17:{userCoins}:6:{userID}:9:{icon_cube}:10:{color_1}:11:{color_2}:14:{icon_type}:15:0:16:{userID}:3:{stars}:8:{creator_points}:4:{demons}:7:{userID}:46:{diamonds}|"
		
		return accountOut, 200
	
	if request.form['type'] == "top":
		cursor.execute(f"SELECT * FROM accounts LIMIT 100")
		accounts = cursor.fetchall()
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
			color_1 = account[25]
			color_2 = account[26]
			accountOut = accountOut + f"1:{username}:2:{userID}:13:{coins}:17:{userCoins}:6:{userID}:9:{icon_cube}:10:{color_1}:11:{color_2}:14:{icon_type}:15:0:16:{userID}:3:{stars}:8:{creator_points}:4:{demons}:7:{userID}:46:{diamonds}|"
		
		return accountOut, 200

	if request.form['type'] == "friends":
		cursor.execute(f"SELECT * FROM friends WHERE user1 = {accID}")
		friends = cursor.fetchall()
		for friend in friends:
			#print(friend[1])
			friendAccID = friend[1]
			cursor.execute(f'SELECT * FROM accounts WHERE accId = {friendAccID}')
			acc = cursor.fetchall()
			for account in acc:
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
				color_1 = account[25]
				color_2 = account[26]
				accountOut = accountOut + f"1:{username}:2:{userID}:13:{coins}:17:{userCoins}:6:{userID}:9:{icon_cube}:10:{color_1}:11:{color_2}:14:{icon_type}:15:0:16:{userID}:3:{stars}:8:{creator_points}:4:{demons}:7:{userID}:46:{diamonds}|"
		#print(accountOut)
		return accountOut, 200
	else:
		# not implemented
		return f"1:Not implemented:2:1:13:0:17:0:6:1:9:0:10:1:11:1:14:0:15:0:16:1:3:0:8:0:4:0:7:1:46:0|", 200