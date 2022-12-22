from __main__ import app, cursor, conn, request
import datetime
import random

@app.route('/database/uploadGJMessage20.php', methods=['GET', 'POST'])
async def upload_message():
    print(request.form)
    # ('accountID', '469475')('toAccountID', '53118'), ('subject', 'aGV5'), ('body', 'WVtFFVBDURJMXkQL')])
    fromAccId = request.form['accountID']
    toAccID = request.form['toAccountID']
    subject = request.form['subject']
    body = request.form['body']
    uploadDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messageId = random.randint(1, 5000000)
    cursor.execute(f"INSERT INTO messages(fromAccId, toAccId, subject, body, messageId, uploadDate, isNew) VALUES ({fromAccId}, {toAccID}, '{subject}', '{body}', {messageId}, '{uploadDate}', 1)")
    conn.commit()
    return '1', 200