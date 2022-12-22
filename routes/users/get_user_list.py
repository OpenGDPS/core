from __main__ import app, cursor, request
import datetime

@app.route('/database/getGJUserList20.php', methods=['GET', 'POST'])
async def get_friends():
    print(request.form)
    type = request.form['type']
    if type == "0":
        str = ""
        accId = request.form['accountID']
        cursor.execute(f'SELECT * FROM friends WHERE user2 = {accId}') #  WHERE toAccId = {accId}
        fetched_requests = cursor.fetchall()
        print(fetched_requests)
        for result in fetched_requests:
            userID = result[0]
            cursor.execute(f"SELECT * FROM accounts WHERE accId = '{userID}'")
            account = cursor.fetchone()
            username = account[0]
            icon_cube = account[15]
            color_1 = account[25]
            color_2 = account[26]
            str = str + f"1:{username}:2:{userID}:9:{icon_cube}:10:{color_1}:11:{color_2}:14:0:15:0:16:{userID}:18:0:41:{userID}|"
        if str == "": return "-2"
        else: return f"{str}"
        #return "1:dragonfirexx:2:1:9:1:10:5:11:6:14:1:15:1:16:1:18:0:41:16|"
    if type == "1":
        str = ""
        accId = request.form['accountID']
        cursor.execute(f'SELECT * FROM blocked_users WHERE user2 = {accId}') #  WHERE toAccId = {accId}
        fetched_requests = cursor.fetchall()
        print(fetched_requests)
        for result in fetched_requests:
            userID = result[0]
            cursor.execute(f"SELECT * FROM accounts WHERE accId = '{userID}'")
            account = cursor.fetchone()
            username = account[0]
            icon_cube = account[15]
            color_1 = account[25]
            color_2 = account[26]
            str = str + f"1:{username}:2:{userID}:9:{icon_cube}:10:{color_1}:11:{color_2}:14:0:15:0:16:{userID}:18:0:41:{userID}|"
        if str == "": return "-2"
        else: return f"{str}"
    else:
        return f"-1"