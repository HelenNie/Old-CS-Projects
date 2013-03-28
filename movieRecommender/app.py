from flask import request,Flask,render_template, url_for,redirect,request
import urllib2,json
import recommend2

app = Flask(__name__) 

global result, genre, search, playing, upcoming, popular, wordSelected, booleanGenre, booleanSearch, booleanLatest, booleanPlaying, booleanUpcoming, booleanPopular, genreSelected, booleanActor, actorSelected
result = {}
genre = []
search= []
playing = []
upcoming = []
popular = []
actor = []
actorSelected = ""
wordSelected = ""
genreSelected = ""

booleanGenre = False
booleanPlaying = False
booleanSearch = False
booleanUpcoming = False
booleanPopular = False
booleanActor = False

@app.route("/", methods=["GET", "POST"])
def home():
    global result
    if request.method=="GET":
        return render_template("moviechooser.html", genres = recommend2.get_genres())
    else:
        button = request.form["button"]
        if button == "Search Movie": #WORKS
            search.append(request.form["searchdata"].replace(" ", "_"))
            return redirect(url_for('searchResults'))
        if button == "Genre Selection": #WORKS
            res = request.form["genre_selection"]
            genre.append(res)
            return redirect(url_for('searchResults'))
        if button == "Now Playing Selection": #I THINK IT WORKS
            playing.append("now playing")
            return redirect(url_for('searchResults'))
        if button == "Upcoming Selection": #I THINK IT WORKS
            upcoming.append("upcoming movies")
            return redirect(url_for('searchResults'))
        if button == "Popular Selection": #WORKS
            popular.append("popular movies")
            return redirect(url_for('searchResults'))
        if button == "Search Actor":
            actor.append(request.form['searchperson'].replace(" ", "_"))
            return redirect(url_for('searchResults'))

@app.route("/searchResults/", methods=["GET", "POST"])
def searchResults():
    global result, wordSelected, genreSelected, booleanGenre, booleanSearch, booleanPlaying, booleanUpcoming, booleanPopular, actorSelected
    if request.method=="GET":
        if len(actor)>0:
            actorSelected = actor.pop(0)
            return render_template("actorresult.html", headerThing = "These are the results for your search for " + actorSelected)
        if len(search)>0:
            wordSelected = search.pop(0)
            booleanSearch = True
            return render_template("searchresults.html", headerThing= "These are the results for your search for the word " + wordSelected)
        if len(genre)>0:
            genreSelected = genre.pop(0)
            booleanGenre = True
            return render_template("searchresults.html", headerThing= "These are the results for your search for the genre " + genreSelected)
        if len(playing)>0:
            global f
            f = playing.pop(0)
            booleanPlaying = True
            return render_template("searchresults.html", headerThing= "These are the results for your search for movies playing in theaters")
        if len(upcoming)>0:
            global g
            g = upcoming.pop(0)
            booleanUpcoming = True
            return render_template("searchresults.html", headerThing= "These are the results for your search of upcoming movies")
        if len(popular)>0:
            global h
            h = popular.pop(0)
            booleanPopular = True
            return render_template("searchresults.html", headerThing= "These are the results of your search of popular movies")
    else:
        button = request.form["button"]
        if button == "back":
            return redirect(url_for('home'))
        #if button == "See these movies' information":
            #return redirect(url_for('home'))
        else:
            pass
          
@app.route("/get_info")
def get_info():
    movie_id=request.args.get('movie_id','') 
    return json.dumps(recommend2.get_info(movie_id))

@app.route("/get_dropdown")
def get_dropdown():
    global booleanGenre, booleanSearch, booleanPlaying, booleanUpcoming, booleanActor, booleanPopular, result
    if booleanGenre:
        result = recommend2.genre_info(genreSelected)
        booleanGenre = False
    elif booleanSearch:
        result = recommend2.movie_info(wordSelected)
        booleanSearch = False
    elif booleanPlaying:
        print booleanPlaying
        result = recommend2.now_playing_info()
        booleanPlaying = False
    elif booleanUpcoming:
        result = recommend2.upcoming_info()
        booleanUpcoming = False
    elif booleanPopular:
        result = recommend2.popular_info()
        booleanPopular = False
    return json.dumps(result)

@app.route("/get_similar")
def get_similar():
    booleanSearch = True
    movie_id=request.args.get('movie_id','')
    wordSelected = recommend2.get_info(movie_id)['title']
    return json.dumps(recommend2.movie_info(wordSelected))

@app.route("/get_dropdown_actor")
def get_dropdown_actor():
    global result, actorSelected
    print actorSelected
    result = recommend2.get_person_id(actorSelected)
    return json.dumps(result)

@app.route("/get_movies_actor")
def get_stuff():
    global result
    actorid = request.args.get('actorid','')
    result = recommend2.get_actor_movies(actorid)
    return json.dumps(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=6202)
