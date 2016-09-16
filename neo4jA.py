from py2neo import Graph


class Database:
    graph = None

    def __init__(self):
        self.graph = Graph(bolt=False, host="120.27.42.59:32769", http_port=32769, user="neo4j", password="admin")
        # graph = Graph(bolt=True, host="localhost", password="admin")