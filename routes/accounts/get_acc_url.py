from __main__ import app, cursor

@app.route('/database/getAccountURL.php', methods=['GET', 'POST'])
async def get_account_url():
	cursor.execute(f"SELECT * FROM config")
	config = cursor.fetchall()
	return f"{config[2][1]}", 200