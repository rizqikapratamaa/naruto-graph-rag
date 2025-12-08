import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class Neo4jConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            uri = os.getenv("NEO4J_URI")
            user = os.getenv("NEO4J_USER")
            password = os.getenv("NEO4J_PASSWORD")
            cls._instance = GraphDatabase.driver(uri, auth=(user, password))
        return cls._instance

    @staticmethod
    def get_driver():
        return Neo4jConnection()

    @staticmethod
    def close():
        if Neo4jConnection._instance:
            Neo4jConnection._instance.close()

def get_driver():
    return Neo4jConnection.get_driver()