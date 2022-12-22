from __main__ import app, cursor, request, conn
import datetime
import random

@app.route('/database/uploadFriendRequest20.php', methods=['GET', 'POST'])
async def upload_friend_request():
	fromAccId = request.form['accountID']
	toAccId = request.form['toAccountID']
	message = request.form['comment']
	uploadDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	request_id = random.randint(1, 1000000)
	cursor.execute(f"INSERT INTO friend_requests(fromAccId, toAccId, message, uploadDate, request_id, isNew) VALUES ({fromAccId}, {toAccId}, '{message}', '{uploadDate}', {request_id}, 1)")
	conn.commit()
	return "1", 200