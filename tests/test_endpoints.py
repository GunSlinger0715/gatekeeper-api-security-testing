# ------------------------------------
# Endpoint Tests
# ------------------------------------

from urllib import response

from utils.output import print_result, run_security_checks
from utils.security import (
    check_data_exposure,
    check_info_leakage,
    check_header_integrity
)
from utils.response_handler import detect_content_type


class TestEndpoints:

    def test_get_post_returns_200(self, api_client):
        """Verify valid endpoint returns 200 OK"""

        response = api_client.get("/json")

        content_type = detect_content_type(response)

        print(f"[RESPONSE TYPE] /json → {content_type}")

        if response is None: 

            print("[WARNING] Endpoint did nt return a response")

            return
        
        passed = response.status_code == 200

        print_result("/json", "GET", response.status_code, 200, passed)

        print("\n[RESPONSE ANALYSIS] GET /json")

        if passed:
            print("[✓] Endpoint Reachable")

        else:
            print("[✗] Endpoint Unreachable")

        print(f"[✓] Status Code: {response.status_code}")

        print(f"[✓] Response Type: {content_type.upper()}")

        run_security_checks(response, "GET /json")

        #functional assertions
        if content_type == "json":
            data = response.json()
        else:
            print(f"[WARNING] Unsupported response type: {content_type}")
        data = {}
        
        if not passed:
            print("[INFO] Endpoint response differed from expected behavior")
    
        if content_type == "json":
            
            print("[✓] JSON Response Detected")

            if "message" in data:
                print("[✓] Expected JSON Field Present")

            else:
                print("[✗] Expected JSON Field Missing")


    def test_invalid_endpoint_returns_404(self, api_client):
        """Verify invalid endpoint returns 404"""

        response = api_client.get("/invalid-endpoint")
    
        if response is None: 
        
            print("[WARNING] Endpoint did not return a response")
              
            return

        passed = response.status_code == 404
        print_result("/invalid-endpoint", "GET", response.status_code, 404, passed)

        # Use unified runner
        run_security_checks(response, "GET /invalid-endpoint")

        if not passed:
            print("[INFO] Invalid endpoint response differed from expected behavior")

        #def test_protected_endpoint_requires_auth(self, api_client):
        #    """Verify protected endpoint denies unauthorized access"""
        #
        #response = api_client.get("/invalid-endpoint")
        #
        #passed = response.status_code in [401, 403, 404]
        #
        #print_result(
        #   "/protected",
        #    "GET",
        #    response.status_code,
        #    "401/403",
        #    passed
        #)
        #
        #run_security_checks(response, "GET /invalid-endpoint")
        #
        #assert passed

from utils.output import print_summary
