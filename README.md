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
- Secure authorization behavior validation scaffolding
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
- Future intelligence-correlation integration
- Scalable detection expansion
- Standardized JSON export support

---

# Example Output

```text
[SECURITY FINDING] GET /post/1 - Potential information leakage detected:

 - [MEDIUM] Server header exposed: cloudflare

----------------------------------------

[FAIL] Missing Security Headers:

 - Content-Security-Policy
 - Referrer-Policy
 - Permissions-Policy

----------------------------------------

[SECURITY SCORE] GET /post/1 → 90/100 
```

---

# Project Structure

```text
## Project Structure

gatekeeper-api-security-testing/

├── core/
│   ├── client.py
│   ├── orchestration.py
│   └── results.py
│
├── security/
│   ├── security.py
│   ├── token_analysis.py
│   └── scoring.py
│
├── reporting/
│   ├── output.py
│   └── export.py
│
├── config/
│   ├── colors.py
│   ├── settings.py
│   └── protected_endpoints.json
│
├── tests/
│   ├── test_endpoints.py
│   └── token_analysis.py
│
├── docs/
│
├── README.md
├── requirements.txt
├── LICENSE
└── conftest.py
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

## Continuous Integration

GateKeeper uses GitHub Actions for automated continuous integration testing.

Every push and pull request to the `main` branch automatically triggers:

- Dependency installation
- Environment validation
- Automated pytest execution

This ensures the project remains stable, portable, and regression-resistant as the architecture evolves.

Engineering Philosophy:
> From Validation to Intelligence.  
> From GateKeeper to Heimdall.

---

# Current Focus

Current development priorities include:
- Structured findings architecture
- Severity-based scoring refinement
- Enhanced token anomaly analysis
- Improved reporting and visualization
- CI/CD workflow refinement

---

# Future Roadmap

Planned future enhancements include:
- Assisted finding correlation and intelligence aggregation
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

GateKeeper is designed to evolve beyond lightweight API security testing into a scalable, context-aware security analysis platform capable of adapting to increasingly complex API ecosystems and response behaviors.

Future architectural development will focus on intelligent response analysis, adaptive validation logic, and resilient trust-aware security workflows, including:
- Adaptive response-type detection and schema-aware validation
- Dynamic handling of JSON, HTML, XML, and text-based API responses
- Intelligent response classification and contextual trust-boundary analysis
- Resilient parser routing and graceful handling of unexpected response formats

Future ecosystem development may include behavioral API telemetry analysis, anomaly inspection workflows, and structured intelligence persistence across modular security subsystems.


