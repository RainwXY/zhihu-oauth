from py2neo import Graph


class Database:
    graph = None

    def __init__(self):
        self.graph = Graph(bolt=True, host="neo4j.t0.daoapp.io", bolt_port=61652, password="admin")
        # graph = Graph(bolt=True, host="localhost", password="admin")