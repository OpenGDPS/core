from __main__ import app, cursor, request, datetime, timeago

@app.route('/database/getGJComments21.php', methods=['GET', 'POST'])
async def get_comments_level():
	#page = int(request.form['page'])
	levelId = request.form['levelID']
	now = datetime.datetime.now()

	cursor.execute(f"SELECT * FROM level_comments WHERE levelID = {levelId}")
	posts = cursor.fetchall()
	if posts is None:
		return '-1'
	else:
		comments = ""
		for post in posts:
			cursor.execute(f"SELECT * FROM level_comments WHERE levelID = {levelId}")
			comments_in_post = cursor.fetchall()
			if comments_in_post is None:
				continue
			else:
				accountId = post[1]
				cursor.execute(f"SELECT icon_cube FROM accounts WHERE accId = '{accountId}'")
				icon_cube = cursor.fetchone()[0]
				#print(f'Comment: {post[1]}, User ID: {post[0]}, Likes: {post[3]}, uploadDate: {post[5]}, Post ID: {post[2]}')
				uploadDate = timeago.format(post[6], now).replace(' ago', '')
				percentCompleted = 1

				cursor.execute(f"SELECT color_1 FROM accounts WHERE accId = '{accountId}'")
				color_1 = cursor.fetchone()[0]

				cursor.execute(f"SELECT color_2 FROM accounts WHERE accId = '{accountId}'")
				color_2 = cursor.fetchone()[0]

				commentsAppend = f"~11~0:1~{post[2]}~7~1~9~{icon_cube}~10~{color_1}~11~{color_2}~14~0~15~0~16~{accountId}"
				comments = f"2~{post[3]}~3~{accountId}~4~{post[4]}~5~0~7~{post[5]}~9~{uploadDate}~6~{post[7]}~10~{percentCompleted}{commentsAppend}|" + comments
		#print(comments)
		print(comments)
		return comments + f"#0:0:10", 200
	#return f'2~SGVsbG8hIE5ldyBsZXZlbCBzeXN0ZW0gb21n~3~1~4~200~5~0~7~0~9~15.01.2023~6~1~10~53~11~2:1~DragonFire~7~1~9~1~10~3~11~4~14~0~15~0~16~1|#$1:$1:$1'