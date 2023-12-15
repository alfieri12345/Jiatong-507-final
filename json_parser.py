import json

def read_data():
    with open("data_cache", "r") as f:
        datas = json.load(f)
    return datas

class Node:
    def __init__(self, nodeType, name, year = None, length = None, imdb_rating = None, total_rating_person = None, genres = None, intro = None):
        self.type = nodeType
        self.name = name
        if self.type == "Movie":
            self.year = year
            self.length = length
            self.imdb_rating = imdb_rating
            self.total_rating_person = total_rating_person
            self.genres = genres
            self.intro = intro
        self.neighbour = {}

    def connect(self, node):
        '''connect function
        connect two nodes
        Parameters  
        ----------
        node: Node
            the node that need to be connected with current node

        Returns
        -------
        None
        '''
        self.neighbour[node.name] = node
        node.neighbour[self.name] = self
    def get_info(self):
        return [self.name, self.year, self.length, self.imdb_rating, self.total_rating_person, self.genres, self.intro, self.neighbour]
    