from __main__ import app, cursor, conn, request
import datetime
import timeago

@app.route('/database/getGJMessages20.php', methods=['GET', 'POST'])
async def get_messages():
    str = ""
    accId = request.form['accountID']
    now = datetime.datetime.now()
    try:
        if request.form['getSent'] == '1': cursor.execute(f'SELECT * FROM messages WHERE fromAccId = {accId}')
    except:
        cursor.execute(f'SELECT * FROM messages WHERE toAccId = {accId}') #  WHERE toAccId = {accId}
    fetched_requests = cursor.fetchall()
    for result in fetched_requests:
        userID = result[0]
        cursor.execute(f"SELECT * FROM accounts WHERE accId = '{userID}'")
        account = cursor.fetchone()
        username = account[0]
        subject = result[2]
        messageId = result[4]
        uploadDate = timeago.format(result[5], now).replace(' ago', '')
        isNew = 1
        str = str + f"6:{username}:3:{userID}:2:{userID}:1:{messageId}:4:{subject}:8:{isNew}:9:{uploadDate}:7:{uploadDate}|"
    if len(fetched_requests) == 0: return "-2"
    else: return f"{str}#${len(fetched_requests)}$0:10"