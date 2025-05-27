import redis
import pickle
import json

class RedisClient:
    def __init__(self, host='localhost', port=6379):
        self.client = redis.Redis(host=host, port=port, decode_responses=False)

    def set_embeddings(self, key, embeddings):
        serialized = pickle.dumps(embeddings)
        self.client.set(key, serialized)

    def get_embeddings(self, key):
        serialized = self.client.get(key)
        if serialized:
            return pickle.loads(serialized)
        return None

    def set_list(self, key, lst):
        self.client.delete(key)
        for item in lst:
            json_item = json.dumps(item)
            self.client.rpush(key, json_item.encode('utf-8'))

    def get_list(self, key):
        return [json.loads(item.decode('utf-8')) for item in self.client.lrange(key, 0, -1)]

    def append_to_list(self, key, item):
        json_item = json.dumps(item)
        self.client.rpush(key, json_item.encode('utf-8'))