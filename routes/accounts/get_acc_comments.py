from __main__ import app, cursor, request
import datetime
import timeago

@app.route('/database/getGJAccountComments20.php', methods=['GET', 'POST'])
async def get_account_comments():
	accountId = request.form['accountID']
	now = datetime.datetime.now()

	cursor.execute(f"SELECT * FROM posts WHERE accId = {accountId}")
	posts = cursor.fetchall()
	if posts is None:
		return '-1'
	else:
		comments = ""
		for post in posts:
			cursor.execute(f"SELECT * FROM posts WHERE accId = {accountId}")
			comments_in_post = cursor.fetchall()
			if comments_in_post is None:
				continue
			else:
				
				#print(f'Comment: {post[1]}, User ID: {post[0]}, Likes: {post[3]}, uploadDate: {post[5]}, Post ID: {post[2]}')
				uploadDate = timeago.format(post[5], now).replace(' ago', '')
				comments = f"2~{post[1]}~3~{post[0]}~4~{post[3]}~5~0~7~0~9~{uploadDate}~6~{post[2]}|" + comments
		#print(comments)
		return comments + "#0:0:10", 200