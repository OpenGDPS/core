from __main__ import app, request, cursor, SERVER_URL, os

@app.route('/database/getGJSongInfo.php', methods=['GET', 'POST'])
async def get_song_info():
	songID = request.form['songID']
	# response = requests.post('http://www.boomlings.com/database/getGJSongInfo.php', data={
	# 	'songID': songID,
	# 	'secret': 'Wmfd2893gb7'
	# })
	cursor.execute(f"SELECT * FROM songs WHERE songID = {songID}")
	result = cursor.fetchone()

	try:
		songName = result[1]
		authorID = result[2]
		authorName = result[3]
		downloadURL = f'{SERVER_URL}/dl/songs/{songID}.mp3'
		size = os.path.getsize(f'.\\dl\\songs\\{songID}.mp3')
			
		return f'1~|~{songID}~|~2~|~{songName}~|~3~|~{authorID}~|~4~|~{authorName}~|~5~|~{size}~|~6~|~~|~10~|~{downloadURL}~|~7~|~~|~8~|~0', 200
	except:
		return '-1', 200