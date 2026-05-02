🔹 GateKeeper

GateKeeper is a Python-based API testing framework designed to validate endpoint behavior and detect potential security issues.

It combines traditional QA validation with lightweight security checks to help testers and developers quickly identify problems in API responses.

🔹 Features

✅ Endpoint validation (200, 404, etc.)

🎯 Human-readable PASS/FAIL output

🎨 Color-coded terminal results

🔐 Data exposure detection (sensitive fields in responses)

🛡️ Information leakage detection (headers like Server, X-Powered-By)


🔹 Example Output

[PASS] GET /post/1 → 200 | OK - Request successful

[WARNING] GET /post/1 - Potential information leakage detected:
 - Header exposed: Server = cloudflare
 - Header exposed: X-Powered-By = Express
----------------------------------------

[PASS] GET /invalid-endpoint → 404 | Not Found - Resource does not exist

[WARNING] GET /invalid-endpoint - Potential information leakage detected:
 - Header exposed: Server = cloudflare
 - Header exposed: X-Powered-By = Express
----------------------------------------
🔹 Purpose

GateKeeper was built to bridge the gap between:

    QA testers who validate functionality
    
    Security engineers who look for vulnerabilities

It provides clear, readable output that helps identify both correctness and potential security concerns in API responses.

🔹 Tech Stack

Python 3

Pytest

🔹 Future Enhancements
    
    Header integrity testing
    
    Token anomaly detection
    
    Schema validation

    Config-based scanning (JSON/YAML)

    CLI interface
