from __main__ import app, cursor, conn, request
import random

# Register account
@app.route('/database/accounts/registerGJAccount.php', methods=['GET', 'POST'])
async def account_register():
	# check if account exists
	cursor.execute(f"SELECT * FROM accounts WHERE userName = '{request.form['userName']}'")
	checkUsername = cursor.fetchone()

	cursor.execute(f"SELECT * FROM accounts WHERE email = '{request.form['email']}'")
	checkEmail = cursor.fetchone()

	cursor.execute(f"SELECT * FROM accounts WHERE password = '{request.form['password']}'")
	checkPassword = cursor.fetchone()

	if checkUsername is not None:
		return '-2'
	if checkEmail is not None:
		return '-3'
	if '@' not in request.form['email']:
		return '-6'
	#if '.ru' not in request.form['email']:
	#	return '-6'
	#if '.com' not in request.form['email']:
	#	return '-6'
	if checkPassword is not None:
		return '-5'
	else:
		inputForm = request.form
		#print(inputForm)
		userName = inputForm['userName']
		password = inputForm['password']
		email = inputForm['email']
		secret = inputForm['secret']
		accId = random.randint(5, 1000000)
		cursor.execute(f"INSERT INTO accounts (userName, password, email, secret, accId, stars, coins, userCoins, diamonds, demons, creator_points, modLevel, canMessage, canFriend, showCommentHistory, isBanned) VALUES ('{userName}', '{password}', '{email}', '{secret}', {accId}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
		conn.commit()
		return '1'