# ------------------------------------
# Endpoint Tests
# ------------------------------------

from utils.output import print_result, run_security_checks
from utils.security import (
    check_data_exposure,
    check_info_leakage,
    check_header_integrity
)


class TestEndpoints:

    def test_get_post_returns_200(self, api_client):
        """Verify valid endpoint returns 200 OK"""

        response = api_client.get("/posts/1")

        passed = response.status_code == 200
        print_result("/post/1", "GET", response.status_code, 200, passed)

        run_security_checks(response, "GET /post/1")

        #functional assertions
        data = response.json()
        assert passed
        assert data["id"] == 1

        # Functional assertions
        data = response.json()
        assert passed
        assert data["id"] == 1


    def test_invalid_endpoint_returns_404(self, api_client):
        """Verify invalid endpoint returns 404"""

        response = api_client.get("/invalid-endpoint")

        passed = response.status_code == 404
        print_result("/invalid-endpoint", "GET", response.status_code, 404, passed)

        # Use unified runner
        run_security_checks(response, "GET /invalid-endpoint")

        assert passed

        # ------------------------
        # Info Leakage
        # ------------------------
        print("-" * 40)

        # ------------------------
        # Header Integrity
        # ------------------------
        header_results = check_header_integrity(response)

        if header_results["missing_headers"]:
            print("\n\033[91m[FAIL] Missing Security Headers:\033[0m")
            for h in header_results["missing_headers"]:
                print(f"  - {h}")

        if header_results["misconfigured_headers"]:
            print("\n\033[93m[WARN] Misconfigured Headers:\033[0m")
            for h, val in header_results["misconfigured_headers"]:
                print(f"  - {h}: {val}")

        print("-" * 40)

from utils.output import print_summary

def teardown_module(module):
    print_summary()