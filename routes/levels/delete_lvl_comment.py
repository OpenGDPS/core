from __main__ import app, request, cursor, conn

@app.route('/database/deleteGJComment20.php', methods=['GET', 'POST'])
async def delete_comment_level():
	levelID = request.form['levelID']
	commentID = request.form['commentID']
	cursor.execute(f'DELETE FROM level_comments WHERE levelID = {levelID} AND commentID = {commentID}')
	conn.commit()
	return '-1', 200