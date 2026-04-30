# Color codes
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def print_result(endpoint, method, status_code, expected, passed):
    if passed:
        print(f"{GREEN}[PASS]{RESET} {method} {endpoint} → {status_code} | {get_status_message(status_code)}")
    else:
        print(f"{RED}[FAIL]{RESET} {method} {endpoint} → {status_code}")
        print(f"{RED}       Expected: {expected}{RESET}")
        print(f"{RED}       Reason: {get_status_message(status_code)}{RESET}")


def get_status_message(status_code):
    messages = {
        200: "OK - Request successful",
        201: "Created - Resource created successfully",
        400: "Bad Request - Invalid input",
        401: "Unauthorized - Authentication required",
        403: "Forbidden - Access denied",
        404: "Not Found - Resource does not exist",
        500: "Server Error - Internal issue"
    }
    return messages.get(status_code, "Unknown response")