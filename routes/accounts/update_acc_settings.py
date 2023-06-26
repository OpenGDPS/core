from __main__ import app, cursor, conn, request

@app.route('/database/updateGJAccSettings20.php', methods=['GET', 'POST'])
async def update_acc_settings():
	#print(request.form)
	#print(request.form)

	accountID = request.form['accountID']
	youtube_url = request.form['yt']
	twitter_url = request.form['twitter']
	twitch_url = request.form['twitch']
	
	can_message = request.form['mS']
	can_friend = request.form['frS']
	show_comment_history = request.form['cS']

	cursor.execute(f'UPDATE accounts SET youtube_url = "{youtube_url}", twitch_url = "{twitch_url}", twitter_url = "{twitter_url}", canMessage = {can_message}, canFriend = {can_friend}, showCommentHistory = {show_comment_history} WHERE accId = {accountID}')
	conn.commit()
	return "1", 200