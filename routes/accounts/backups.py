from __main__ import app, request, cursor, conn

# Backups
@app.route('/database/accounts/backupGJAccountNew.php', methods=['GET', 'POST'])
async def backup_account():
	inputForm = request.form
	userName = inputForm['userName']
	password = inputForm['password']

	cursor.execute(f"SELECT accId FROM accounts WHERE userName = '{userName}' AND password = '{password}'")
	account = cursor.fetchone()
	# get account id
	if account is None:
		return '-2'
	else:
		saveData = inputForm['saveData']
		cursor.execute(f"INSERT INTO backup (accId, saveData) VALUES ({account[0]}, '{saveData}')")
		conn.commit()
		return "1"

@app.route('/database/accounts/syncGJAccount.php', methods=['GET', 'POST'])
@app.route('/database/accounts/syncGJAccount20.php', methods=['GET', 'POST'])
@app.route('/database/accounts/syncGJAccountNew.php', methods=['GET', 'POST'])
async def sync_account():
	inputForm = request.form
	userName = inputForm['userName']
	password = inputForm['password']

	cursor.execute(f"SELECT accId FROM accounts WHERE userName = '{userName}' AND password = '{password}'")
	account = cursor.fetchone()
	# get account id
	if account is None:
		return '-2'
	else:
		cursor.execute(f"SELECT saveData FROM backup WHERE accId = {account[0]}")
		saveData = cursor.fetchone()
		return f"{saveData[0]};21;30;a;a"