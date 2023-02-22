from __main__ import app, request, cursor, datetime, random, conn

@app.route('/database/uploadGJComment21.php', methods=['GET', 'POST'])
async def upload_comment_level():
	levelID = request.form['levelID']
	accountID = request.form['accountID']
	userName = request.form['userName']
	comment = request.form['comment']
	date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	commentID = random.randint(1, 2147483647)
	cursor.execute(f'INSERT INTO level_comments VALUES({levelID}, {accountID}, "{userName}", "{comment}", 0, 0, "{date}", {commentID})')
	conn.commit()
	return '1', 200