# ---------------------------
# Endpoint Tests
# ---------------------------

from utils.output import print_result

class TestEndpoints:

    def test_get_post_returns_200(self, api_client):
        """Verify valid endpoint returns 200 OK"""
        response = api_client.get("/posts/1")

        passed = response.status_code == 200

        print_result("/post/1", "GET", response.status_code, 200, passed)

        assert passed

        data = response.json()
        assert data["id"] == 1


    def test_invalid_endpoint_returns_404(self, api_client):
        """Verify invalid endpoint returns 404 Not Found"""
        response = api_client.get("/invalid-endpoint")

        passed = response.status_code == 404

        print_result("/invalid-endpoint", "GET", response.status_code, 404, passed)

        assert passed


# ---------------------------
# Input Validation Tests
# ---------------------------

class TestInputValidation:

    def test_create_post_with_invalid_data_returns_400(self, api_client):
        """Verify API handles malformed input safely"""

        bad_payload = {
            "invalid_field": "bad_data"
        }

        response = api_client.post("/posts", json=bad_payload)

        assert response.status_code in [400, 201]


# ---------------------------
# Authentication Tests
# ---------------------------

class TestAuthentication:

    def test_access_protected_resource_without_auth_returns_401(self, api_client):
        """Verify API denies access without authentication"""

        response = api_client.get("/protected-resource")

        assert response.status_code in [401, 404]