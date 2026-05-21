import requests
from config.config import BASE_URL
from core.validator import validate_target


class APIClient:

    def safe_request(
        self,
        method,
        endpoint,
        headers=None,
        json=None
    ):

        try:
            validated_target = validate_target(f"{BASE_URL}{endpoint}")

            response = requests.request(
                method=method,
                url=validated_target, 
                headers=headers,
                json=json,
                timeout=5,
                allow_redirects=False,
                verify=True
            )

            return response

        except requests.exceptions.Timeout:
            print(f"[REQUEST TIMEOUT] {endpoint}")
            return None

        except requests.exceptions.RequestException as e:
            print(f"[REQUEST ERROR] {e}")
            return None

    def get(self, endpoint, headers=None):

        return self.safe_request(
            method="GET",
            endpoint=endpoint,
            headers=headers
        )

    def post(self, endpoint, json=None, headers=None):

        return self.safe_request(
            method="POST",
            endpoint=endpoint,
            headers=headers,
            json=json
        )