from __main__ import app, cursor, conn, request

@app.route('/database/accounts/loginGJAccount.php', methods=['GET', 'POST'])
async def account_login():
	inputForm = request.form
	#print(inputForm)
	userName = inputForm['userName']
	password = inputForm['password']

	cursor.execute(f"SELECT * FROM accounts WHERE userName = '{userName}' AND password = '{password}'")
	account = cursor.fetchone()
	# get account id
	if account is None:
		print(f"[Login] Account not found! {userName}")
		return '-11'
	else:
		print(f"[Login] Account found! {userName}")
		# example response (type tuple): ('DragonFire', '00000p', 'dragonfirecommunity@gmail.com', 'Wmfv3899gc9', 1)
		accId = account[4]
		return f'{accId},{accId}'