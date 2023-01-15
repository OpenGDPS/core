from __main__ import app, cursor, conn, request

@app.route('/database/updateGJDesc20.php', methods=['GET', 'POST'])
async def update_level_desc():
	levelID = request.form['levelID']
	levelDesc = request.form['levelDesc']
	cursor.execute(f"UPDATE levels SET levelDesc = '{levelDesc}' WHERE levelID = {levelID}")
	conn.commit()
	return '1', 200