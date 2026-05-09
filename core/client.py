import requests
from config.config import BASE_URL

class APIClient:

    def get(self, endpoint, headers=None):
        return requests.get(f"{BASE_URL}{endpoint}", headers=headers)

    def post(self, endpoint, json=None, headers=None):
        return requests.post(f"{BASE_URL}{endpoint}", json=json, headers=headers)