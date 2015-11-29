from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3 as lite
app = Flask(__name__)

app.secret_key = '/x9c/x11/xf2/xe0/xc6/xdb/x0f/x10/xf4/x89/xca/x02/x9eS/x83/x1c/x95/x12/xb1/x9a[`/x93/xb0'

@app.route('/')
def redirLogin():
    return redirect(url_for('loadWelcome'))

@app.route('/welcome')
def loadWelcome():
    return render_template('welcome.html')

@app.route('/chat', methods=['POST', 'GET'])
def loadChat():

  session['name'] = request.args.get('user_id', '')

  if request.method == 'GET':
    user_id = request.args.get('user_id', '')
    con = lite.connect('messages.db')

    c = con.cursor()

    c.execute("SELECT * FROM messages")
    Messages = [dict(user_id=row[0], message_text=row[1]) for row in
    c.fetchall()]

    con.close()

    return render_template('chat.html', Messages = Messages)
  else:
    user_id = request.args.get('user_id', '')
    message = request.form['message']
    con = lite.connect('messages.db')

    c = con.cursor()

    c.execute("INSERT INTO messages VALUES (?, ?)", (user_id, message))
    con.commit()

    c.execute("SELECT * FROM messages")

    Messages = [dict(user_id=row[0], message_text=row[1]) for row in
    c.fetchall()]
    con.close()

    return render_template('chat.html', Messages = Messages)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
