from __main__ import app, request, cursor, conn

@app.route('/database/likeGJItem211.php', methods=['GET', 'POST'])
async def like_item():
	#print(request.form)
	itemID = request.form['itemID']
	like = request.form['like']
	if like == "1":
		cursor.execute(f"UPDATE posts SET likes = likes + 1 WHERE commentId = {itemID}")
		cursor.execute(f"UPDATE level_comments SET likes = likes + 1 WHERE commentID = {itemID}")
		cursor.execute(f"UPDATE levels SET likes = likes + 1 WHERE levelID = {itemID}")
	if like == "0":
		cursor.execute(f"UPDATE posts SET likes = likes - 1 WHERE commentId = {itemID}")
		cursor.execute(f"UPDATE level_comments SET likes = likes - 1 WHERE commentID = {itemID}")
		cursor.execute(f"UPDATE levels SET likes = likes - 1 WHERE levelID = {itemID}")
	conn.commit()
	return "1", 200