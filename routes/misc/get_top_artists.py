from __main__ import app, cursor, SERVER_URL_NO_HTTP

@app.route('/database/getGJTopArtists.php', methods=['GET', 'POST'])
async def get_top_artists():
	cursor.execute(f"SELECT * FROM songs")
	result = cursor.fetchall()
	strArtists = ""
	try:
		for music in result:
			songID = music[0]
			songName = music[1]
			authorName = music[3]
			outName = f'{songName} by {authorName} ! {songID}'
			strArtists = strArtists + f'4:{outName}:7:../redirect?q=http%3A%2F%2F{SERVER_URL_NO_HTTP}%2Fdl%2Fsongs%2F{songID}.mp3|'
		print(strArtists)
		return f'{strArtists}#0:0:20', 200
	except:
		return '-1', 200