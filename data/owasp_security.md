**Cheat sheet** for the **OWASP Top 10:2025 (RC1)**, formatted for easy pasting into your docs/RAG. I’ve included crisp explanations, concrete prevention steps, and minimal code snippets you can drop into reviews. Citations to the OWASP RC1 pages are at the end of relevant sections.

---

# OWASP Top 10:2025 (RC1) — Python Secure Coding Cheat Sheet

> Source order (RC1): **A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Logging & Alerting Failures, A10 Mishandling of Exceptional Conditions.** ([OWASP][1])

---

## A01:2025 — Broken Access Control

**What it is:** Users can act outside their permissions (read/modify resources they don’t own).
**Pitfalls:** IDORs, missing object-level checks, trusting client claims (e.g., `role` in JWT), path/parameter tampering.
**Prevent:** Server-side authZ on _every_ request; deny-by-default; RBAC/ABAC; enforce ownership in queries; protect admin routes.

```python
# Flask + SQLAlchemy: enforce object ownership
from flask import abort, request
from flask_login import current_user, login_required
from models import Document

@app.get("/docs/<int:doc_id>")
@login_required
def get_doc(doc_id):
    doc = Document.query.filter_by(id=doc_id, owner_id=current_user.id).first()
    if not doc:
        abort(404)
    return {"id": doc.id, "title": doc.title}
```

---

## A02:2025 — Security Misconfiguration

**What it is:** Insecure defaults, debug left on, sloppy CORS, missing headers, verbose errors.
**Prevent:** Hardened defaults, config-as-code, least privilege for services, proper CORS/headers, disable debug in prod.

```python
# Flask hardening preview
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)
app.config.update(DEBUG=False, PROPAGATE_EXCEPTIONS=False)
Talisman(app, force_https=True)  # HSTS + baseline headers (tune CSP for your app)
```

---

## A03:2025 — Software Supply Chain Failures

**What it is:** Compromise via dependencies, registries, build systems, artifacts (expanded beyond “Vulnerable & Outdated Components”).
**Prevent:** Pin & verify (hash-pinned `requirements.txt`), use trusted indexes, SBOM, signature verification, minimal build perms, CI policy gates.

```bash
# Generate hashes and enforce them
pip-compile --generate-hashes pyproject.toml -o requirements.txt
pip install --require-hashes -r requirements.txt

# Audit in CI
pip install pip-audit && pip-audit --strict
```

---

## A04:2025 — Cryptographic Failures

**What it is:** Weak/incorrect crypto; exposed secrets; poor TLS; storing sensitive data in plaintext.
**Prevent:** Use modern libs (AES-GCM/ChaCha20-Poly1305), KMS/secret managers, rotate keys, strong password hashing (Argon2/bcrypt), TLS 1.2+.

```python
# Symmetric encryption with cryptography
from cryptography.fernet import Fernet
key = Fernet.generate_key()
f = Fernet(key)
ct = f.encrypt(b"secret")
pt = f.decrypt(ct)

# Password hashing with bcrypt
from bcrypt import hashpw, gensalt, checkpw
hashed = hashpw(password.encode(), gensalt())
assert checkpw(password.encode(), hashed)
```

---

## A05:2025 — Injection

**What it is:** Untrusted data reaches interpreters (SQL/NoSQL/OS/LDAP/template).
**Prevent:** Parameterized queries, safe ORMs, input validation (type/length/allowlist), avoid `shell=True`, avoid string-built templates/queries.

```python
# SQLAlchemy parameterization
from sqlalchemy import text
stmt = text("SELECT * FROM users WHERE email = :email")
rows = db.session.execute(stmt, {"email": email}).all()

# Commands without shell
import subprocess
subprocess.run(["ping", "-c", "1", ip_address], check=True)
```

---

## A06:2025 — Insecure Design

**What it is:** Missing or ineffective security controls due to design flaws (not just bugs).
**Prevent:** Threat modeling (STRIDE), misuse/abuse cases, secure defaults, rate limits, defense-in-depth, segregation of duties.

```python
# Example: conservative session defaults
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,     # only over HTTPS
    SESSION_COOKIE_SAMESITE="Lax"
)
```

---

## A07:2025 — Authentication Failures

**What it is:** Weak auth flows, poor session management, missing MFA, predictable tokens.
**Prevent:** MFA for high-risk actions, strong password policy with rate limits, vetted frameworks, secure session cookies, short-lived tokens.

```python
# Time-bound signed token (itsdangerous)
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
s = URLSafeTimedSerializer("app-secret")
token = s.dumps({"uid": user.id})
try:
    data = s.loads(token, max_age=900)  # 15 minutes
except (BadSignature, SignatureExpired):
    abort(401)
```

---

## A08:2025 — Software or Data Integrity Failures

**What it is:** Trusting updates/artifacts/data without integrity checks; unsafe deserialization; pipeline tampering.
**Prevent:** Sign & verify artifacts, checksums, immutable builds, enforce code review, avoid `pickle`/unsafe loaders, strict parsers.

```python
# Safe (de)serialization preference
import json
safe_obj = json.loads(request.data)      # define schema and validate!
# Avoid: pickle.loads(untrusted_bytes)

# Example payload signing (HMAC)
import hmac, hashlib
def valid_sig(body, sig, key):
    mac = hmac.new(key, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, sig)
```

---

## A09:2025 — Logging & Alerting Failures

**What it is:** Insufficient/incorrect logging, noisy alerts, missing detections; incidents go unnoticed.
**Prevent:** Structured logs with context (who/what/where), centralize to SIEM, mask secrets/PII, define alert use-cases, test detections.

```python
# Structured logging with structlog
import structlog, logging
logging.basicConfig(level=logging.INFO)
log = structlog.get_logger()
log.info("login_success", user_id=user.id, ip=request.remote_addr)
```

([OWASP][2])

---

## A10:2025 — Mishandling of Exceptional Conditions

**What it is:** Failing to prevent, detect, and respond to unusual/error conditions → crashes, undefined behavior, security gaps.
**Examples:** Uncaught exceptions leak stack traces; retry storms; resource exhaustion; ambiguous error messages; unsafe fallbacks.
**Prevent:** Explicit error handling, least-privilege fallbacks, backoffs/circuit breakers, safe defaults, controlled error messages, health checks.

```python
# Flask: safe error handlers + generic messages
from flask import jsonify

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error="Bad Request"), 400

@app.errorhandler(500)
def server_error(e):
    # Log detailed info internally, return generic message to clients
    app.logger.exception("Unhandled exception")
    return jsonify(error="Internal Server Error"), 500

# Resilient outbound call: timeout + retries + circuit breaker (simplified)
import requests, time
def fetch(url, attempts=3, timeout=3):
    for i in range(attempts):
        try:
            return requests.get(url, timeout=timeout)
        except requests.RequestException:
            time.sleep(0.5 * (2 ** i))
    raise RuntimeError("Upstream unavailable")
```

([OWASP][3])

---

## Cross-Cutting Python Review Tips

- **Input validation:** Prefer pydantic/typed DTOs or JSON schema validation on all external inputs.
- **CORS:** Narrow origins, methods, and headers; avoid `'*'` with credentials.
- **Headers:** HSTS, CSP (nonces or hashes), X-Content-Type-Options, Referrer-Policy.
- **Rate limiting:** Add app- and auth-layer limits (Flask-Limiter, Django throttling).
- **Secrets:** Never commit secrets; use env vars, Secret Managers, or Vault; rotate regularly.
- **Testing:** Add security unit/integration tests (authZ checks, negative tests, error paths).
- **CI/CD:** Pin dependencies, audit on every build, sign artifacts, enforce code reviews.

---

## Notes on 2025 Changes (from 2021)

- **New:** **A03 Software Supply Chain Failures**, **A10 Mishandling of Exceptional Conditions**.
- **Terminology updates:** Logging & Alerting (A09); Authentication Failures (A07).
- **Consolidations/clarifications** called out by OWASP in the RC1 intro page. ([OWASP][1])

---

### Primary Sources

- OWASP **Top 10:2025 RC1 — Introduction & Category List.** ([OWASP][1])
- OWASP **A10: Mishandling of Exceptional Conditions** details. ([OWASP][3])
- OWASP **A09: Logging & Alerting Failures** page. ([OWASP][2])

> RC1 means wording and ordering are official as a release candidate (published early Nov 2025). Check the OWASP site for final tweaks as they move from RC to final. ([OWASP][4])

---

[1]: https://owasp.org/Top10/2025/0x00_2025-Introduction/?utm_source=chatgpt.com "Introduction - OWASP Top 10:2025 RC1"
[2]: https://owasp.org/Top10/2025/A09_2025-Logging_and_Alerting_Failures/?utm_source=chatgpt.com "A09 Logging and Alerting Failures - OWASP Top 10:2025 RC1"
[3]: https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/?utm_source=chatgpt.com "A10 Mishandling of Exceptional Conditions - OWASP Top 10:2025 RC1"
[4]: https://owasp.org/Top10/?form=MG0AV3&utm_source=chatgpt.com "OWASP Top 10:2025 RC1"
