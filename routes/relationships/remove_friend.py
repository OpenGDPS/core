from __main__ import app, request, cursor, conn

@app.route('/database/removeGJFriend20.php', methods=['GET', 'POST'])
async def remove_friend():
    print(request.form)
    accId = request.form['accountID']
    targetAccountID = request.form['targetAccountID']
    cursor.execute(f'DELETE FROM friends WHERE user1 = {targetAccountID} AND user2 = {accId}') #  WHERE toAccId = {accId}
    cursor.execute(f'DELETE FROM friends WHERE user1 = {accId} AND user2 = {targetAccountID}') #  WHERE toAccId = {accId}
    conn.commit()
    return "1", 200