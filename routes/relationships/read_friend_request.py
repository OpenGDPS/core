from __main__ import app, request, cursor, conn

@app.route('/database/readGJFriendRequest20.php', methods=['GET', 'POST'])
async def read_friend_request():
    request_id = request.form['requestID']
    cursor.execute(f'UPDATE friend_requests SET isNew = 0 WHERE request_id = {request_id}')
    conn.commit()
    return "1"