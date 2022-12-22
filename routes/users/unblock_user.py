from __main__ import app, cursor, conn, request

@app.route('/database/unblockGJUser20.php', methods=['GET', 'POST'])
async def unblock_user():
	print(request.form)
	#print(request.form['messageID'])
	accountId = request.form['targetAccountID']
	accountIdMy = request.form['accountID']

	cursor.execute(f'DELETE FROM blocked_users WHERE user1 = {accountId} AND user2 = {accountIdMy}')
	conn.commit()
	return '1', 200