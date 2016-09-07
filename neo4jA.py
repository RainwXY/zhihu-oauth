from py2neo import Graph


class Database:
    graph = None

    def __init__(self):
        self.graph = Graph(bolt=False, host="115.28.24.246", http_port=32787, user="neo4j", password="admin")
        # graph = Graph(bolt=True, host="localhost", password="admin")