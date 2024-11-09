from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('imdb_top_1000.db', check_same_thread=False)
c = conn.cursor()

@app.route('/', methods=['GET'])
def home():
    search_query = request.args.get('search', '')
    category = request.args.get('category', 'Series_Title')
    if search_query:
        query = f"SELECT * FROM imdb WHERE {category} LIKE ?"
        movies = c.execute(query, ('%' + search_query + '%',)).fetchall()
    else:
        movies = c.execute("SELECT * FROM imdb").fetchall()
    return render_template('index.html', movies=movies)


@app.route('/top-rated', methods=['GET'])
def top_rated():
    movies = c.execute("SELECT * FROM imdb ORDER BY IMDB_Rating DESC LIMIT 10").fetchall()
    return render_template('top-rated.html', movies=movies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
