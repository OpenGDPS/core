from __main__ import app, cursor, request

@app.route('/database/getGJUserInfo.php', methods=['GET', 'POST'])
@app.route('/database/getGJUserInfo20.php', methods=['GET', 'POST'])
async def get_user_info():
	print(request.form)
	accountId = request.form['targetAccountID']
	accountIdMy = request.form['accountID']

	cursor.execute(f"SELECT * FROM accounts WHERE accId = '{accountId}'")
	account = cursor.fetchone()
	if account is None:
		return '-1'
	else:
		# Stats
		cursor.execute(f"SELECT stars FROM accounts WHERE accId = '{accountId}'")
		stars = cursor.fetchone()[0]

		cursor.execute(f"SELECT coins FROM accounts WHERE accId = '{accountId}'")
		coins = cursor.fetchone()[0]

		cursor.execute(f"SELECT userCoins FROM accounts WHERE accId = '{accountId}'")
		userCoins = cursor.fetchone()[0]

		cursor.execute(f"SELECT diamonds FROM accounts WHERE accId = '{accountId}'")
		diamonds = cursor.fetchone()[0]

		cursor.execute(f"SELECT demons FROM accounts WHERE accId = '{accountId}'")
		demons = cursor.fetchone()[0]

		cursor.execute(f"SELECT creator_points FROM accounts WHERE accId = '{accountId}'")
		creator_points = cursor.fetchone()[0]

		cursor.execute(f"SELECT modLevel FROM accounts WHERE accId = '{accountId}'")
		modBadge = cursor.fetchone()[0]

		# Social networks
		cursor.execute(f"SELECT youtube_url FROM accounts WHERE accId = '{accountId}'")
		youtube_url = cursor.fetchone()[0]

		cursor.execute(f"SELECT twitch_url FROM accounts WHERE accId = '{accountId}'")
		twitch_url = cursor.fetchone()[0]

		cursor.execute(f"SELECT twitter_url FROM accounts WHERE accId = '{accountId}'")
		twitter_url = cursor.fetchone()[0]

		# Icons
		cursor.execute(f"SELECT icon_cube FROM accounts WHERE accId = '{accountId}'")
		icon_cube = cursor.fetchone()[0]

		cursor.execute(f"SELECT icon_ship FROM accounts WHERE accId = '{accountId}'")
		icon_ship = cursor.fetchone()[0]

		cursor.execute(f"SELECT icon_ball FROM accounts WHERE accId = '{accountId}'")
		icon_ball = cursor.fetchone()[0]

		cursor.execute(f"SELECT icon_bird FROM accounts WHERE accId = '{accountId}'")
		icon_bird = cursor.fetchone()[0]

		cursor.execute(f"SELECT icon_dart FROM accounts WHERE accId = '{accountId}'")
		icon_dart = cursor.fetchone()[0]

		cursor.execute(f"SELECT icon_robot FROM accounts WHERE accId = '{accountId}'")
		icon_robot = cursor.fetchone()[0]

		cursor.execute(f"SELECT icon_glow FROM accounts WHERE accId = '{accountId}'")
		icon_glow = cursor.fetchone()[0]

		cursor.execute(f"SELECT icon_spider FROM accounts WHERE accId = '{accountId}'")
		icon_spider = cursor.fetchone()[0]

		cursor.execute(f"SELECT icon_explosion FROM accounts WHERE accId = '{accountId}'")
		icon_explosion = cursor.fetchone()[0]
		
		# Colors
		cursor.execute(f"SELECT color_1 FROM accounts WHERE accId = '{accountId}'")
		color_1 = cursor.fetchone()[0]

		cursor.execute(f"SELECT color_2 FROM accounts WHERE accId = '{accountId}'")
		color_2 = cursor.fetchone()[0]

		# Some States
		cursor.execute(f"SELECT * FROM blocked_users WHERE user1 = {accountIdMy} AND user2 = {accountId}")
		block_state = len(cursor.fetchall())

		print(block_state)
		if block_state != 0:
			can_message = 2
			can_friend = 1
			show_comment_history = 2
		else:
			cursor.execute(f"SELECT canMessage FROM accounts WHERE accId = '{accountId}'")
			can_message = cursor.fetchone()[0]

			cursor.execute(f"SELECT canFriend FROM accounts WHERE accId = '{accountId}'")
			can_friend = cursor.fetchone()[0]

			cursor.execute(f"SELECT showCommentHistory FROM accounts WHERE accId = '{accountId}'")
			show_comment_history = cursor.fetchone()[0]

		#rank = 1
		rank = accountId

		cursor.execute(f"SELECT * FROM friends WHERE user1 = '{accountId}'")
		friends_list = len(cursor.fetchall())
		cursor.execute(f"SELECT * FROM friend_requests WHERE toAccId = '{accountId}' AND isNew = 1")
		new_friend_requests = len(cursor.fetchall())
		cursor.execute(f"SELECT * FROM messages WHERE toAccId = '{accountId}' AND isNew = 1")
		messages = len(cursor.fetchall())

		cursor.execute(f"SELECT * FROM friend_requests WHERE fromAccId = '{accountId}'")
		friendStateCheckOUTCOMING = cursor.fetchall()
		cursor.execute(f"SELECT * FROM friend_requests WHERE toAccId = '{accountId}'")
		friendStateCheckINCOMING = cursor.fetchall()
		cursor.execute(f"SELECT * FROM friends WHERE user1 = '{accountId}' OR user2 = '{accountId}'")
		friendStateCheckIN_FRIENDS = cursor.fetchall()
		if len(friendStateCheckINCOMING) != 0: friendState = 3
		if len(friendStateCheckOUTCOMING) != 0: friendState = 4
		if len(friendStateCheckIN_FRIENDS) != 0: friendState = 1
		else: friendState = 0

		return f"1:{account[0]}:2:{accountId}:13:{coins}:17:{userCoins}:10:{color_1}:11:{color_2}:3:{stars}:46:{diamonds}:4:{demons}:8:{creator_points}:18:{can_message}:19:{can_friend}:50:{show_comment_history}:20:{youtube_url}:21:{icon_cube}:22:{icon_ship}:23:{icon_ball}:24:{icon_bird}:25:{icon_dart}:26:{icon_robot}:28:{icon_glow}:43:{icon_spider}:47:{icon_explosion}:30:{rank}:16:{accountId}:31:{friendState}:44:{twitter_url}:45:{twitch_url}:29:1:49:{modBadge}:32:1:35:1:37:1:38:{messages}:39:{new_friend_requests}:40:{friends_list}", 200
