from __main__ import app, cursor, conn, request
import datetime
import random

@app.route('/database/deleteGJMessages20.php', methods=['GET', 'POST'])
async def delete_message():
    print(request.form)
    #print(request.form['messageID'])
    try:
        msgID = request.form['messageID']
        cursor.execute(f'DELETE FROM messages WHERE messageID = {msgID}')
    except:
        msgID = request.form['messages']
        cursor.execute(f'DELETE FROM messages WHERE messageID IN ({msgID})')
    conn.commit()
    return '1', 200