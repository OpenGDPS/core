from __main__ import app
from flask import render_template

@app.route('/database/accounts/accountManagement.php', methods=['GET', 'POST'])
async def acc_managament():
    return render_template('account_management.html')