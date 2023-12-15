from json_parser import *
def cache_parser():
    datas = read_data()
    movie_nodes = {}
    star_nodes = {}
    writer_nodes = {}
    director_nodes = {}
    genre_nodes = {}
    for one_data in datas:
        title = one_data["title"]
        year = one_data["year"]
        length = one_data["length"]
        imdb_rating = one_data["imdb_rating"]
        total_rating_person = one_data["total_rating_person"]
        genres = one_data["genres"]
        intro = one_data["intro"]
        directors = one_data["directors"]
        writers = one_data["writers"]
        stars = one_data["stars"]
        movie_node = Node(nodeType="Movie", name = title, year = year, length=length,imdb_rating=imdb_rating, total_rating_person=total_rating_person, 
                                    genres=genres, intro=intro)
        if title not in movie_nodes.keys():
            movie_nodes[title] = movie_node
        if directors:
            for director in directors:
                if not director in director_nodes.keys():
                    dire_node = Node(nodeType="Director", name = director)
                    director_nodes[director] = dire_node
                else:
                    dire_node = director_nodes[director]
                dire_node.connect(movie_node)
        if writers:
            for writer in writers:
                if not writer in writer_nodes.keys():
                    writer_node = Node(nodeType="Writer", name = writer)
                    writer_nodes[writer] = writer_node
                else:
                    writer_node = writer_nodes[writer]
                writer_node.connect(movie_node)
        if stars:
            for star in stars:
                if not star in star_nodes.keys():
                    star_node = Node(nodeType="Star", name = star)
                    star_nodes[star] = star_node
                else:
                    star_node = star_nodes[star]
                star_node.connect(movie_node)
        for genre in genres:
            if not genre in genre_nodes:
                genre_nodes[genre] = [movie_node]
            else:
                genre_nodes[genre].append(movie_node)
    return [movie_nodes,
            star_nodes, 
            writer_nodes, 
            director_nodes, 
            genre_nodes]