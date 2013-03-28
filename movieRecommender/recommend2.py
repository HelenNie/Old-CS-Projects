import json
import urllib
import sys
from urllib2 import Request, urlopen
global info
import string
API_KEY = "450062599145d021e7243a767de7c7d0"
    
def get_similar_movies(movie_id):
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/movie/" + str(movie_id) + "/similar_movies" + "?api_key=" + API_KEY, headers=headers)
    response_body = urlopen(request).read()
    res = json.loads(response_body)
    result = []
    for thing in res['results']:
        result.append({'title': thing['title'], 'id': thing['id'], 'date': thing['release_date']})
    return result

def get_movie_using_id(movie_id):
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=" + API_KEY, headers=headers)
    response_body = urlopen(request).read()
    result = json.loads(response_body)
    return result    

def get_info(movie_id):
    global info
    global temp
    info = {}
    temp = get_movie_using_id(movie_id)
    info['summary'] = temp['overview']
    if len(temp['genres']) > 0:
        info['genre'] = temp['genres'][0]['name']
    else:
        info['genre'] = "unavailable"
    info['cast'] = movie_cast(movie_id)
    info['id'] = movie_id
    info['title'] = temp['title']
    info['date'] = temp['release_date']
    info['popularity'] = temp['vote_average']
    info['review'] = getReviews(info['title'], info['date'])
    info['similar movies'] = get_similar_movies(info['id'])
    if get_trailer_youtube(movie_id):
        info['trailer_id'] = get_trailer_youtube(movie_id)
    return info

def get_movie(movie_name):
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/search/movie?api_key=" + API_KEY + "&query=" + movie_name, headers=headers)
    response_body = urlopen(request).read()
    result = json.loads(response_body)
    return result

def movie_info(movie_name):
    global temp
    temp = get_movie(movie_name)
    global result
    global info
    counter = 0
    info = {}
    info['ids'] = []
    info['titles'] = []
    info['dates'] = []
    for thing in temp['results']:
        info['ids'].append(thing['id'])
        info['titles'].append(thing['title'])
        info['dates'].append(thing['release_date'])
    return info

def get_trailer_youtube(movie_id):
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/movie/" + str(movie_id) + "/trailers?api_key=" + API_KEY, headers=headers)
    response_body = urlopen(request).read()
    result = json.loads(response_body)
    if len(result['youtube']) > 0:
        return result['youtube'][0]['source']
    else:
        return "IJNR2EpS0jw"
    
def get_person_id(name):
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/search/person?api_key=" + API_KEY + "&query=" + name, headers=headers)
    response_body = urlopen(request).read()
    res = json.loads(response_body)
    result = []
    for thing in res['results']:
        result.append({'name': thing['name'], 'id': thing['id']})
    return result

def get_actor_movies(actorid):
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/person/"+ str(actorid) +"/credits?api_key=" + API_KEY , headers=headers)
    response_body = urlopen(request).read()
    res = json.loads(response_body)
    print res
    result = []
    for thing in res['cast']:
        result.append({'title':thing['title'], 'id': thing['id'], 'date': thing['release_date']})
    return result
    
def call(q):
    urlstring = '%s/%s'%('http://api.nytimes.com/svc/movies/v2/reviews',q)
    print urlstring
    request = urllib.urlopen(urlstring)
    try:
        result = json.loads(request.read())
    except ValueError:
        return {'results': []}
    return result

def getReviews(movie, date):
    #cleaning title for things like dash and colon, will probably have to add
    if string.find(movie, ':') > 0:
        movie = string.split(movie, ':')[1];
    if string.find(movie, ' - ') > 0:
        movie = string.split(movie, ' - ')[0];
    title = movie.replace(' ', '+')
    #requests data
    qstring = 'search.json?query=' + title + '&api-key=d392ca168b1be29a3360f09ecdf195c6:0:66271972'
    result = call(qstring)
    for r in result['results']:
        if movie == r['display_title'] and date[0:4] == r['opening_date'][0:4]:
            link =  r['link']['url']
            return link 
    return "no review available"
        
def movie_cast(movie_id):
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/movie/" + str(movie_id) + "/casts?api_key=" + API_KEY, headers=headers)
    response_body = urlopen(request).read()
    res = json.loads(response_body)
    result = []
    for thing in res['cast']:
        result.append(" " + thing['name'])
    return result

def movie_image(movie_id):
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/movie/" + str(movie_id) + "/images?api_key=" + API_KEY, headers=headers)
    response_body = urlopen(request).read()
    result = json.loads(response_body)
    return result

def upcoming_movies():
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/movie/upcoming?api_key=" + API_KEY, headers=headers)
    response_body = urlopen(request).read()
    result = json.loads(response_body)
    return result

def latest_movies():
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/movie/latest?api_key=" + API_KEY, headers=headers)
    response_body = urlopen(request).read()
    result = json.loads(response_body)
    return result

def latest_info():
    global temp
    global info
    temp = latest_movies()
    info = {}
    info['ids'] = temp['id']
    info['titles'] = temp['title']
    info['dates'] = temp['release_date']
    info['ratings'] = "Not available yet"
    info['trailer_ids'] = get_trailer_youtube(temp['id'])
    #info['cast']
    info['summary'] = temp['overview']
    return info

def now_playing_movies():
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/movie/now_playing?api_key=" + API_KEY, headers=headers)
    response_body = urlopen(request).read()
    result = json.loads(response_body)
    return result


def popular_movies():
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/movie/popular?api_key=" + API_KEY, headers=headers)
    response_body = urlopen(request).read()
    result = json.loads(response_body)
    return result

def popular_info():
    global temp
    temp = top_rated_movies()
    global result
    global info
    info = {}
    info['ids'] = []
    info['titles'] = []
    info['dates'] = []
    info['ratings'] = []
    for thing in temp['results']:
        info['ids'].append(thing['id'])
        info['titles'].append(thing['title'])
        info['dates'].append(thing['release_date'])
    return info


def top_rated_movies():
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/movie/top_rated?api_key=" + API_KEY, headers=headers)
    response_body = urlopen(request).read()
    result = json.loads(response_body)
    return result


def get_genres():
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/genre/list?api_key=" + API_KEY, headers=headers)
    response_body = urlopen(request).read()
    result = json.loads(response_body)
    return result


def get_movies_by_genre(genre_id):
    global API_KEY
    headers = {"Accept": "application/json"}
    request = Request("http://api.themoviedb.org/3/genre/" + str(genre_id) + "/movies?api_key=" + API_KEY, headers=headers)
    response_body = urlopen(request).read()
    result = json.loads(response_body)
    return result

def now_playing_info():
    global temp
    temp = now_playing_movies()
    global result
    global info
    counter = 0
    info = {}
    info['ids'] = []
    info['titles'] = []
    info['dates'] = []
    for thing in temp['results']:
        info['ids'].append(thing['id'])
        info['titles'].append(thing['title'])
        info['dates'].append(thing['release_date'])
    return info



def upcoming_info():
    global temp
    temp = upcoming_movies()
    global result
    global info
    counter = 0
    info = {}
    info['ids'] = []
    info['titles'] = []
    info['dates'] = []
    for thing in temp['results']:
        info['ids'].append(thing['id'])
        info['titles'].append(thing['title'])
        info['dates'].append(thing['release_date'])
    return info

def genre_info(genre_name):
    global info
    global genre
    info = {}
    for genre in get_genres()['genres']:
        if genre['name'] == genre_name:
            temp = get_movies_by_genre(genre['id'])
            break
    global result
    counter = 0
    info['ids'] = []
    info['titles'] = []
    info['dates'] = []
    for thing in temp['results']:
        info['ids'].append(thing['id'])
        info['titles'].append(thing['title'])
        info['dates'].append(thing['release_date'])
    return info

if __name__ == "__main__":
    pass
