from __main__ import app, cursor, conn, request

@app.route('/database/downloadGJMessage20.php', methods=['GET', 'POST'])
async def download_message():
    str = ""
    accId = request.form['accountID']
    msgId = request.form['messageID']
    cursor.execute(f'SELECT * FROM messages WHERE messageId = {msgId}') #  WHERE toAccId = {accId}
    fetched_requests = cursor.fetchall()
    for result in fetched_requests:
        userID = result[0]
        cursor.execute(f"SELECT * FROM accounts WHERE accId = '{userID}'")
        account = cursor.fetchone()
        username = account[0]
        subject = result[2]
        messageId = result[4]
        uploadDate = result[5]
        text = result[3]
        isNew = 1
        str = str + f"6:{username}:3:{userID}:2:{userID}:1:{messageId}:4:{subject}:8:{isNew}:9:{userID}:5:{text}:7:{uploadDate}|"
    cursor.execute(f"UPDATE messages SET isNew = 0 WHERE toAccId = '{accId}' AND messageId = {msgId}")
    conn.commit()
    return f"{str}#${len(fetched_requests)}$0:10"