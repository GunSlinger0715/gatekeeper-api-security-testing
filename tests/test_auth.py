from core.client import APIClient
from core.results import create_finding

client = APIClient()

AUTH_ENDPOINT = [
    "/login",
    "/admin",
    "/signin",
    "/auth",
]


def scan_auth_endpoints():
    findings = []

    for endpoint in AUTH_ENDPOINT:
        response = client.get(endpoint)

        if response and response.status_code == 200:
        
            findings.append(create_finding(
                    finding="Accessible Authentication Endpoint",
                    severity="HIGH",
                    details=f"{endpoint} is accessible without authentication",

                why_it_matters=(
                    "Authentication-related endpoints exposed without "
                    "access controls may increase the risk of " 
                    "unauthorized administrative or account access."
                ),

                recommended_actions=[
                    "Validate authenticaition enforcement on the endpoints.",
                    "Confirm administrtive routes require authorization.",
                    "Review access control and session validation logic."
                
                ]
            ))
    return findings

def test_auth_scanner_runs():
    findings = scan_auth_endpoints()
    assert isinstance(findings, list)

    