from __main__ import app, cursor, conn, request

@app.route('/database/blockGJUser20.php', methods=['GET', 'POST'])
async def block_user():
	print(request.form)
	#print(request.form['messageID'])
	accountId = request.form['targetAccountID']
	accountIdMy = request.form['accountID']

	cursor.execute(f'INSERT INTO blocked_users(user1, user2) VALUES ({accountId}, {accountIdMy})')
	return '1', 200