<p align="center">
  <img src="docs/images/GateKeeper Heimdal.png" width="100%">
</p>

# Project GateKeeper

Project GateKeeper is a modular API security analysis framework designed to combine deterministic API validation with structured security analysis and severity-based risk scoring.

The framework blends traditional QA-style endpoint testing with lightweight security intelligence to identify vulnerabilities, information leakage, misconfigurations, token anomalies, and sensitive data exposure within API responses.

---

# Features

## API Validation
- Endpoint response testing
- HTTP status validation
- Invalid endpoint handling
- Request verification

## Security Analysis
- Information leakage detection
- Missing security header detection
- Misconfigured header analysis
- Header strength validation
- Unauthorized access detection
- Trust-boundary validation
- Missing authentication analysis

## Authorization Validation
- Protected endpoint awareness
- Contextual trust-boundary validation
- Secure authorization behavior scaffolding
- Unauthorized access detection architecture

## Token Analysis
- JWT structure validation
- Token anomaly detection
- Length and entropy analysis

## Sensitive Data Exposure
- Password exposure detection
- Token exposure detection
- Internal field discovery
- Sensitive response analysis

## Risk Scoring Engine
- Weighted severity scoring
- LOW / MEDIUM / HIGH / CRITICAL classification
- Structured findings model
- Severity-aware analysis pipeline

---

# Architecture Highlights

GateKeeper uses a modular architecture with centralized structured findings generation.
The framework validates not only endpoint availability, but also secure endpoint behavior through trust-boundary analysis and structured security enforcement validation.

```python
{
    "finding": "Information Leakage",
    "severity": "MEDIUM",
    "details": "Server header exposed: cloudflare"
}
```

This enables:
- Consistent scoring
- Structured reporting
- Future AI-assisted analysis integration
- Scalable detection expansion
- Standardized JSON export support

---

# Example Output

```text
[WARNING] GET /post/1 - Potential information leakage detected:

 - [MEDIUM] Server header exposed: cloudflare

----------------------------------------

[FAIL] Missing Security Headers:

 - Content-Security-Policy
 - Referrer-Policy
 - Permissions-Policy

----------------------------------------

[SECURITY SCORE] GET /post/1 → 90/100 (MEDIUM RISK)
```

---

# Project Structure

```text
gatekeeper-api-security-testing/
│
├── tests/
│   ├── test_endpoints.py
│   ├── token_analysis.py
│
├── utils/
│   ├── security.py
│   ├── output.py
│   ├── api_client.py
│
├── config/
├── README.md
├── requirements.txt
```

---

# Installation

```bash
git clone https://github.com/GunSlinger0715/gatekeeper-api-security-testing.git

cd gatekeeper-api-security-testing

pip install -r requirements.txt
```

---

# Running GateKeeper

```bash
pytest -s
```

---

# Current Focus

Current development priorities include:
- Structured findings architecture
- Severity-based scoring refinement
- Enhanced token anomaly analysis
- Improved reporting and visualization
- CI/CD integration preparation

---

# Future Roadmap

Planned future enhancements include:
- AI-assisted finding correlation
- Advanced attack pattern recognition
- OWASP API Top 10 expansion
- Enhanced dashboards and reporting
- Config-driven detection rules
- Intelligent anomaly analysis

# License

This project is licensed under the MIT License.

See the LICENSE file for additional details.

---

# Long-Term Vision

GateKeeper is designed to evolve into a scalable intelligent API security analysis platform capable of combining deterministic validation with future AI-assisted security reasoning and attack correlation capabilities.
