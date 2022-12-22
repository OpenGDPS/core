from __main__ import app, request, cursor, conn

@app.route('/database/deleteGJFriendRequests20.php', methods=['GET', 'POST'])
async def delete_friend_requests():
    print(request.form)
    accId = request.form['accountID']
    targetAccountID = request.form['targetAccountID']
    try:
        accsId = request.form['accounts']
    except:
        pass
    cursor.execute(f'DELETE FROM friend_requests WHERE fromAccId = {targetAccountID} AND toAccId = {accId}') #  WHERE toAccId = {accId}
    cursor.execute(f'DELETE FROM friend_requests WHERE fromAccId = {accId} AND toAccId = {targetAccountID}') #  WHERE toAccId = {accId}
    try:
        cursor.execute(f'DELETE FROM friend_requests WHERE fromAccId = {accId} AND toAccId IN ({accsId})') #  WHERE toAccId = {accId}
        cursor.execute(f'DELETE FROM friend_requests WHERE fromAccId IN ({accsId}) AND toAccId = {accId}')
    except:
        pass
    conn.commit()
    return "1", 200