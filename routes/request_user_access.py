from __main__ import app, cursor, request

@app.route('/database/requestUserAccess.php', methods=['GET', 'POST'])
async def request_access():
	accId = request.form['accountID']
	cursor.execute(f"SELECT modLevel FROM accounts WHERE accId = {accId}")
	modLevel = cursor.fetchone()[0]
	return f"{modLevel}", 200