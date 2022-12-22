from __main__ import app, cursor, conn, request

@app.route('/database/deleteGJAccComment20.php', methods=['GET', 'POST'])
async def delete_comment():
	cursor.execute(f"DELETE FROM posts WHERE commentId = {request.form['commentID']}")
	conn.commit()
	#print(request.form)
	return "1", 200