from __main__ import app, cursor, conn, request

import datetime
import random

@app.route('/database/updateGJUserScore22.php', methods=['GET', 'POST'])
async def update_user_score():
	accId = request.form['accountID']
	stars = request.form['stars']
	demons = request.form['demons']
	diamonds = request.form['diamonds']
	coins = request.form['coins']
	userCoins = request.form['userCoins']
	icon_cube = request.form['accIcon']
	icon_ship = request.form['accShip']
	icon_ball = request.form['accBall']
	icon_bird = request.form['accBird']
	icon_dart = request.form['accDart']
	icon_robot = request.form['accRobot']
	icon_glow = request.form['accGlow']
	icon_spider = request.form['accSpider']
	icon_explosion = request.form['accExplosion']
	color_1 = request.form['color1']
	color_2 = request.form['color2']
	icon_type = request.form['iconType']

	# cursor.execute(f"SELECT stars FROM accounts WHERE accId = '{accId}'")
	# starsOld = cursor.fetchone()[0]

	# if stars > 500: return accId, 200

	# count all levels stars
	official_levels = {
		"stars": 190,
		"coins": 63 # not user coins
	}

	all_stars = official_levels['stars']

	cursor.execute(f'SELECT stars FROM levels')
	data = cursor.fetchall()

	for x in data:
		all_stars = all_stars + x[0]
	
	if all_stars < stars:
		cursor.execute(f"UPDATE accounts SET isBanned = 1, modLevel = 0, stars = 0 WHERE accId = {accId}")
		conn.commit()

		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		commentId = random.randint(0, 2147483647)

		cursor.execute(f"INSERT INTO posts (accId, postText, commentId, likes, isSpam, uploadDate) VALUES ({accId}, 'VGhpcyB1c2VyIHdhcyBiYW5uZWQgZnJvbSBPcGVuR0RQUyBpbnN0YW5jZS4gUmVhc29uOiBTdGFycyBvciBjb2lucyBtb3JlIHRoYW4gdGhlIG51bWJlciBvZiBhbGwgc3RhcnMvY29pbnMgZnJvbSB0aGUgc2VydmVyIChpbmNsdWRpbmcgb2ZmaWNpYWwgbGV2ZWxzKQ==', {commentId}, 0, 0, '{date}')")
		conn.commit()
		return accId, 200

	cursor.execute(f"UPDATE accounts SET stars = {stars}, demons = {demons}, diamonds = {diamonds}, coins = {coins}, userCoins = {userCoins}, icon_cube = {icon_cube}, icon_ship = {icon_ship}, icon_ball = {icon_ball}, icon_bird = {icon_bird}, icon_dart = {icon_dart}, icon_robot = {icon_robot}, icon_glow = {icon_glow}, icon_spider = {icon_spider}, icon_explosion = {icon_explosion}, icon_type = {icon_type}, color_1 = {color_1}, color_2 = {color_2} WHERE accId = {accId}")
	conn.commit()

	return accId, 200