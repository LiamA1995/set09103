from flask import Flask, redirect, url_for, request, render_template
import sqlite3 as lite
app = Flask(__name__)

#If user loads '/' then redirect to '/home'
@app.route("/")
def redirHome():
  return redirect(url_for('loadHome'))

#Load the home page
@app.route("/home")
def loadHome():
  #return the template for the home page
  return render_template('home.html', search_page=url_for('loadResults'))

#load search results page
@app.route("/results")
def loadResults():
  #name and search method pulled from the URL
  name = request.args.get('query', '')
  search_method = request.args.get('searchby', '')

  #connect to the database
  con = lite.connect('music.db')

  cur = con.cursor()

  #if the user chooses to search by artist, query database for artist matches
  if search_method == 'artist':
     cur.execute("SELECT * FROM Song WHERE artist_name LIKE :name", {"name":
     '%'+name+'%'})

     #Pull results into a python dictionary - used to loop with templates to
     #display multiple results
     Song=[dict(name=row[1], artist_name=row[2], length=row[3]) for row in
     cur.fetchall()]

     return render_template('results.html', Song = Song)

  else:
     #else, user chooses to search by song name so query databse for song
     #matches instead
     cur.execute("SELECT * FROM Song WHERE name LIKE :name",
     {"name":'%'+name+'%'})

     #Again with artist search method, pull results into a python dictionary
     #to display multiple results
     Song=[dict(name=row[1], artist_name=row[2], length=row[3]) for row in
     cur.fetchall()]
     return render_template('results.html', Song = Song)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
