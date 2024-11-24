from pymongo import MongoClient

class MongoDBConfig:
    """Singleton class to hold MongoDB connection settings."""
    _instance = None
    _config = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_config(self, db_name, username, password, cluster_name):
        """Set MongoDB configuration."""
        cls = type(self)
        cls._config = {
            'db_name': db_name,
            'username': username,
            'password': password,
            'cluster_name': cluster_name
        }

    def get_config(self):
        """Get MongoDB configuration."""
        return self._config


class Client:
    def __init__(self):
        self.config = MongoDBConfig().get_config()

    def connect(self):
        db_name = self.config['db_name']
        username = self.config['username']
        password = self.config['password']
        cluster_name = self.config['cluster_name']
        MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster_name}"
        client = MongoClient(MONGO_URI)
        db = client[str(db_name)]
        return db

if __name__ == "__main__":
    client = Client()
    db = client.connect()