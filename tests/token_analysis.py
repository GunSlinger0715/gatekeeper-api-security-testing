import re
import base64
import json
from token_analysis import analyze_tokens


TOKEN_PATTERNS = [
    r"Bearer\s+([A-Za-z0-9\-._~+/]+=*)",
    r"api[_-]?key['\"]?\s*[:=]\s*['\"]([A-Za-z0-9\-._]+)",
    r"token['\"]?\s*[:=]\s*['\"]([A-Za-z0-9\-._]+)"
]


def extract_candidate_tokens(text):
    """
    Extract possible authentication tokens from text.
    """

    tokens = []

    for pattern in TOKEN_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)

        for match in matches:
            if isinstance(match, tuple):
                tokens.extend(match)
            else:
                tokens.append(match)

    return list(set(tokens))


def classify_token(token):
    """
    Classify token type based on structure.
    """

    if token.count(".") == 2:
        return {
            "token": token,
            "type": "JWT",
            "confidence": "HIGH"
        }

    if len(token) >= 32:
        return {
            "token": token,
            "type": "Opaque Token",
            "confidence": "MEDIUM"
        }

    return {
        "token": token,
        "type": "Unknown",
        "confidence": "LOW"
    }


# Classify Token
def analyze_tokens(text):
    """
    Extract and classify tokens from input text.
    """

    results = []

    tokens = extract_candidate_tokens(text)

    for token in tokens:
        results.append(classify_token(token))

    return results

def decode_base64url(data):
    """"

    Decode Base64URL encoding strings safely. 

    """

    padding = '=' * (-len(data) % 4)

    try:
        return base64.urlsafe_b64decode(data + padding)
    except Exception: 
        return None
    
   def validate_jwt(token):
    """
    Validate JWT structure and detect common security issues.
    """

    findings = []

    parts = token.split(".")

    # JWT should contain exactly 3 parts
    if len(parts) != 3:
        findings.append({
            "finding": "Malformed JWT Structure",
            "severity": "HIGH",
            "details": "JWT does not contain 3 segments"
        })

        return findings

    header_b64, payload_b64, signature_b64 = parts

    # Decode Header
    header_raw = decode_base64url(header_b64)

    if not header_raw:
        findings.append({
            "finding": "Invalid JWT Header Encoding",
            "severity": "HIGH",
            "details": "Unable to decode JWT header"
        })

        return findings

    # Decode Payload
    payload_raw = decode_base64url(payload_b64)

    if not payload_raw:
        findings.append({
            "finding": "Invalid JWT Payload Encoding",
            "severity": "HIGH",
            "details": "Unable to decode JWT payload"
        })

        return findings

    # Parse JSON
    try:
        header = json.loads(header_raw)
    except Exception:
        findings.append({
            "finding": "Malformed JWT Header JSON",
            "severity": "HIGH",
            "details": "JWT header is not valid JSON"
        })

        return findings

    try:
        payload = json.loads(payload_raw)
    except Exception:
        findings.append({
            "finding": "Malformed JWT Payload JSON",
            "severity": "HIGH",
            "details": "JWT payload is not valid JSON"
        })

        return findings

    # Detect insecure algorithm
    alg = header.get("alg", "").lower()

    if alg == "none":
        findings.append({
            "finding": "JWT Uses Insecure Algorithm",
            "severity": "CRITICAL",
            "details": "JWT uses alg=none"
        })

    # Success case
    if not findings:
        findings.append({
            "finding": "Valid JWT Structure",
            "severity": "INFO",
            "details": "JWT structure appears valid"
        })

    return findings