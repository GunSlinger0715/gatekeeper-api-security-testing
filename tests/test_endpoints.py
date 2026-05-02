# ---------------------------
# Endpoint Tests
# ---------------------------

from utils.output import print_result
from utils.security import check_data_exposure, check_info_leakage


class TestEndpoints:

    def test_get_post_returns_200(self, api_client):
        """Verify valid endpoint returns 200 OK"""
        response = api_client.get("/posts/1")

        passed = response.status_code == 200

        print_result("/post/1", "GET", response.status_code, 200, passed)

        #  Data Exposure
        findings = check_data_exposure(response)

        if findings:
            print(f"\n\033[93m[WARNING] GET /post/1 - Potential data exposure detected:\033[0m")
            for f in findings:
                print(f" - {f}")
            print("-" * 40)

        #  Info Leakage
        leaks = check_info_leakage(response)

        if leaks:
            print(f"\n\033[93m[WARNING] GET /post/1 - Potential information leakage detected:\033[0m")
            for l in leaks:
                print(f" - {l}")
            print("-" * 40)

        data = response.json()

        assert passed
        assert data["id"] == 1


    def test_invalid_endpoint_returns_404(self, api_client):
        """Verify invalid endpoint returns 404 Not Found"""
        response = api_client.get("/invalid-endpoint")

        passed = response.status_code == 404

        print_result("/invalid-endpoint", "GET", response.status_code, 404, passed)

        #  Data Exposure
        findings = check_data_exposure(response)

        if findings:
            print(f"\n\033[93m[WARNING] GET /invalid-endpoint - Potential data exposure detected:\033[0m")
            for f in findings:
                print(f" - {f}")
            print("-" * 40)

        #  Info Leakage
        leaks = check_info_leakage(response)

        if leaks:
            print(f"\n\033[93m[WARNING] GET /invalid-endpoint - Potential information leakage detected:\033[0m")
            for l in leaks:
                print(f" - {l}")
            print("-" * 40)

        assert passed