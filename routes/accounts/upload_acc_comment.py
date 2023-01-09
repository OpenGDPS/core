from __main__ import app, cursor, request, conn
import cryptx

import datetime
import random

@app.route('/database/uploadGJAccComment20.php', methods=['GET', 'POST'])
async def upload_account_comment():
	cursor.execute(f"SELECT * FROM config")
	config = cursor.fetchall()

	if config[0][1] == 0:
		return f'temp_0_{config[0][2]}'


	accountId = request.form['accountID']
	comment = request.form['comment']

	cursor.execute(f"SELECT * FROM comments_ban WHERE accId = '{accountId}'")
	bannedAccounts = cursor.fetchall()

	#duration = bannedAccounts[0][1]
	#reason = bannedAccounts[0][2]

	#except Exception as e: return f'temp_0_{e}'

	date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	commentId = random.randint(0, 2147483647)
	cursor.execute(f"INSERT INTO posts (accId, postText, commentId, likes, isSpam, uploadDate) VALUES ({accountId}, '{comment}', {commentId}, 0, 0, '{date}')")
	conn.commit()
	return "1", 200