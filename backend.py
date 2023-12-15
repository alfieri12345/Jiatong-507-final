from flask import Flask, render_template, request, make_response
import json
from cache_parser import *

app = Flask(__name__)
@app.route("/homepage")
def homepage():
    html = render_template("homepage.html")
    response = make_response(html)
    return response
@app.route("/search")
def search():
    html = render_template("search.html")
    response = make_response(html)
    return response
@app.route("/recommend")
def recommend():
    html = render_template("recommend.html")
    response = make_response(html)
    return response
@app.route("/related")
def related():
    html = render_template("related.html")
    response = make_response(html)
    return response
@app.route("/top")
def top():
    html = render_template("top.html")
    response = make_response(html)
    return response

@app.route("/fetchdata")
def fetch():
    args = dict(request.args)
    infos = []
    if "star" in args.keys():
        star = args["star"]
        if star in star_nodes.keys():
            movies = star_nodes[star]
            for movie in movies.neighbour.values():
                info = movie.get_info()
                [name, year, length, imdb_rating, total_rating_person, genres, intro, neighbour] = info
                new_info = [name, year, length, imdb_rating, total_rating_person, genres, intro]
                infos.append(new_info)
            response = make_response(json.dumps(infos))
            return response
            
    if "name" in args.keys():
        name = args["name"]
        if name in movie_nodes.keys():
            movie = movie_nodes[name]
            info = movie.get_info()
            [name, year, length, imdb_rating, total_rating_person, genres, intro, neighbour] = info
            new_info = [name, year, length, imdb_rating, total_rating_person, genres, intro]
            infos.append(new_info)
            response = make_response(json.dumps(infos))
            return response
        
    if "writer" in args.keys():
        writer = args["writer"]
        if writer in writer_nodes.keys():
            movies = writer_nodes[writer]
            for movie in movies.neighbour.values():
                info = movie.get_info()
                [name, year, length, imdb_rating, total_rating_person, genres, intro, neighbour] = info
                new_info = [name, year, length, imdb_rating, total_rating_person, genres, intro]
                infos.append(new_info)
            response = make_response(json.dumps(infos))
            return response
        
    if "director" in args.keys():
        director = args["director"]
        if director in director_nodes.keys():
            movies = director_nodes[director]
            for movie in movies.neighbour.values():
                info = movie.get_info()
                [name, year, length, imdb_rating, total_rating_person, genres, intro, neighbour] = info
                new_info = [name, year, length, imdb_rating, total_rating_person, genres, intro]
                infos.append(new_info)
            response = make_response(json.dumps(infos))
            return response
    if "genre" in args.keys():
        genre = args["genre"]
        if genre in genre_nodes.keys():
            movies = genre_nodes[genre]
            for movie in movies:
                info = movie.get_info()
                [name, year, length, imdb_rating, total_rating_person, genres, intro, neighbour] = info
                new_info = [name, year, length, imdb_rating, total_rating_person, genres, intro]
                infos.append(new_info)
            response = make_response(json.dumps(infos))
            return response
    return make_response(json.dumps([]))

@app.route("/findrelated")
def findrelated():
    args = dict(request.args)
    common_writers = []
    common_directors = []
    common_stars = []
    if "name" in args.keys():
        name = args["name"]
        if name in movie_nodes.keys():
            movie = movie_nodes[name]
            neighbour = movie.get_info()[-1]
            for oneNeighbor in neighbour.values():
                if oneNeighbor.type == "Director":
                    infos = common_directors
                elif oneNeighbor.type == "Star":
                    infos = common_stars
                else:
                    infos = common_writers
                for onemovie in oneNeighbor.neighbour.values():
                    if onemovie.type == "Movie":
                        if onemovie.name != name:
                            new_info = onemovie.get_info()[:-1]
                            infos.append(new_info)
            all_info = {"stars": common_stars,
                        "directors": common_directors,
                        "writers": common_writers}
            response = make_response(json.dumps(all_info))
            return response
    return make_response(json.dumps([]))

@app.route("/gettop")
def gettop():
    infos = []
    test = [i for i in movie_nodes.values() if i.imdb_rating]
    test.sort(key = lambda x: float(x.imdb_rating), reverse=True)
    for movie in test:
        infos.append(movie.get_info()[:-1])
    response = make_response(json.dumps(infos))
    return response



@app.route("/gettree")
def gettree():
    returnData = {}
    args = dict(request.args)
    answer = args["answer"]
    global now_question_ind
    global curr_data
    if answer == "refresh":
        now_question_ind = 0
    if now_question_ind == 0:
        returnData["prompt"] = "What genre of movie would you like? "
        returnData["data"] = []
        returnData["status"] = 1
        returnData["state"] = 0
        now_question_ind += 1
    elif now_question_ind == 1:
        if answer in genre_nodes.keys():
            curr_data = genre_nodes[answer]
            returnData["prompt"] = "Which release years of movie would you like? (Please connect start and end years with '-')"
            returnData["data"] = []
            returnData["status"] = 1
            returnData["state"] = 0
            now_question_ind += 1
        else:
            returnData["prompt"] = "Which release years of movie would you like? (Please connect start and end years with '-')"
            returnData["data"] = []
            returnData["status"] = 0
            returnData["state"] = 0
            
    elif now_question_ind == 2:
        try:
            start, end = answer.split("-")
            curr_data = [data for data in curr_data if data.year and start <= data.year <= end]
            returnData["prompt"] = "Which star do you like? "
            returnData["data"] = []
            returnData["status"] = 1
            returnData["state"] = 0
            now_question_ind += 1
        except Exception as e:
            returnData["prompt"] = "Which star do you like? "
            returnData["data"] = []
            returnData["status"] = 0
            returnData["state"] = 0
    elif now_question_ind == 3:
        if answer in star_nodes.keys():
            actor_movies = star_nodes[answer].neighbour
            res_data = [data for data in curr_data if data in actor_movies.values()]
            returnData["prompt"] = "Based on your answer, here are the recommended movies, hope you enjoy it! "
            returnData["data"] = [data.get_info()[:-1] for data in curr_data]
            returnData["status"] = 1
            returnData["state"] = 1
            now_question_ind += 0
            curr_data = list(movie_nodes.values())
        else:
            returnData["prompt"] = "Which star do you like? "
            returnData["data"] = []
            returnData["status"] = 0
            returnData["state"] = 0
    response = make_response(json.dumps(returnData))
    return response

if __name__ == "__main__":
    [movie_nodes, star_nodes, writer_nodes, director_nodes, genre_nodes] = cache_parser()
    global now_question_ind
    now_question_ind = 0
    global curr_data
    curr_data = list(movie_nodes.values())
    app.run()

