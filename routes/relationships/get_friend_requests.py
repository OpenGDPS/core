from __main__ import app, cursor, request
import datetime
import timeago

@app.route('/database/getGJFriendRequests20.php', methods=['GET', 'POST'])
async def get_friend_requests():
    print(request.form)
    now = datetime.datetime.now()
    try:
        if request.form['getSent']:
            str = ""
            accId = request.form['accountID']
            cursor.execute(f'SELECT * FROM friend_requests WHERE fromAccId = {accId}') #  WHERE toAccId = {accId}
            fetched_requests = cursor.fetchall()
            print(fetched_requests)
            for result in fetched_requests:
                userID = result[1]
                cursor.execute(f"SELECT * FROM accounts WHERE accId = '{userID}'")
                account = cursor.fetchone()
                username = account[0]
                color_1 = account[25]
                color_2 = account[26]
                request_id = result[4]
                message = result[2]
                isNew = result[4]
                uploadDate = timeago.format(result[3], now).replace(' ago', '')
                icon_cube = account[15]
                str = str + f"1:{username}:2:{userID}:9:{icon_cube}:10:{color_1}:11:{color_2}:14:0:15:0:16:{userID}:32:{request_id}:35:{message}=:41:{isNew}:37:{uploadDate}|"
            if len(fetched_requests) == 0: return "-2"
            else: return f"{str}#${len(fetched_requests)}$0:10"
    except:
        pass

    str = ""
    accId = request.form['accountID']
    cursor.execute(f'SELECT * FROM friend_requests WHERE toAccId = {accId}') #  WHERE toAccId = {accId}
    fetched_requests = cursor.fetchall()
    for result in fetched_requests:
        userID = result[0]
        cursor.execute(f"SELECT * FROM accounts WHERE accId = '{userID}'")
        account = cursor.fetchone()
        username = account[0]
        color_1 = account[25]
        color_2 = account[26]
        request_id = result[4]
        message = result[2]
        isNew = result[5]
        uploadDate = timeago.format(result[3], now).replace(' ago', '')
        icon_cube = account[15]
        str = str + f"1:{username}:2:{userID}:9:{icon_cube}:10:{color_1}:11:{color_2}:14:0:15:0:16:{userID}:32:{request_id}:35:{message}=:41:{isNew}:37:{uploadDate}|"
    if len(fetched_requests) == 0: return "-2"
    else: return f"{str}#${len(fetched_requests)}$0:10"