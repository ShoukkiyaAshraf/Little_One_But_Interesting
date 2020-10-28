from flask import Flask, render_template, request
from lyrics import scrap_lyric_pages
from markov import MarkovLyrics

app = Flask(__name__)


def generateArtistLyricName(name):
    songs = scrap_lyric_pages(name)
    m = MarkovLyrics()

    for song in songs:
        m.populateMarkovChain(song)
    lyrics = m.generateLyrics()
    return lyrics.split("NEWLINE")


@app.route('/', methods=['GET', 'POST'])
def lyricGenerator():
    lyrics = []
    if request.method == 'POST':
        artist = request.form['search']
        lyrics = generateArtistLyricName(artist)
    return render_template('home.html', lyrics=lyrics)


if __name__ == '__main__':
    app.run(debug=True)
