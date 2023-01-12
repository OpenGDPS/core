from __main__ import app, cursor, request

@app.route('/database/getGJUsers20.php', methods=['GET', 'POST'])
async def get_users():
	accountOut = ""
	userToSearch = request.form['str']
	if userToSearch == "@everyone":
		cursor.execute(f"SELECT * FROM accounts")
	else:
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