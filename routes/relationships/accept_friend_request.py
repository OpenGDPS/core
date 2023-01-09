from __main__ import app, request, cursor, conn

@app.route('/database/acceptGJFriendRequest20.php', methods=['GET', 'POST'])
async def accept_friend_request():
    print(request.form)
    accId = request.form['accountID']
    targetAccountID = request.form['targetAccountID']
    cursor.execute(f'DELETE FROM friend_requests WHERE fromAccId = {targetAccountID} AND toAccId = {accId}') #  WHERE toAccId = {accId}
    cursor.execute(f'DELETE FROM friend_requests WHERE fromAccId = {accId} AND toAccId = {targetAccountID}') #  WHERE toAccId = {accId}
    cursor.execute(f'INSERT INTO friends(user1, user2, isNew) VALUES ({accId}, {targetAccountID}, 1)')
    cursor.execute(f'INSERT INTO friends(user1, user2, isNew) VALUES ({targetAccountID}, {accId}, 1)')
    conn.commit()
    #fetched_requests = cursor.fetchall()
    return "1", 200