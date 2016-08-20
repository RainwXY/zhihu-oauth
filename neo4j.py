from py2neo import Graph


class Database:
    graph = None

    def __init__(self):
        self.graph = Graph(bolt=False, host="neo4j.t0.daoapp.io", http_port=61646, password="admin")
        # graph = Graph(bolt=True, host="localhost", password="admin")