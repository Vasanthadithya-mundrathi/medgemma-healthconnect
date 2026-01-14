# Security Guide for MedGemma HealthConnect

## Overview

This document outlines security best practices and considerations for deploying and operating MedGemma HealthConnect.

## Threat Model

### Protected Assets

1. **Patient Health Information (PHI)**
   - Symptoms and medical conditions
   - Personal statements
   - Medical summaries

2. **System Integrity**
   - AI models
   - Clinical trials database
   - Application code

3. **Service Availability**
   - Kiosk uptime
   - Model inference capability
   - Session management

### Threat Actors

1. **External Attackers**
   - Network-based attacks
   - Data interception
   - Unauthorized access

2. **Insider Threats**
   - Unauthorized data access
   - System misconfiguration
   - Policy violations

3. **Unintentional**
   - Accidental data exposure
   - Configuration errors
   - Software bugs

## Security Controls

### 1. Data Protection

#### No Persistent Storage
**Control:** Zero-persistence architecture
```python
# ✅ Correct: In-memory only
def process_data(data):
    result = analyze(data)  # Processed in RAM
    return result  # No file writes

# ❌ Incorrect: Writing to disk
def process_data(data):
    with open('data.txt', 'w') as f:
        f.write(data)  # DON'T DO THIS
```

**Verification:**
```bash
# No patient data files should exist
find . -name "*.wav" -o -name "*.mp3"
ls data/transcripts/  # Should not exist
```

#### Session Management
**Control:** Time-based session expiration

```python
# Default: 5 minutes (300 seconds)
SESSION_TIMEOUT=300
```

**Best Practices:**
- Adjust timeout based on use case
- Warn users before expiration
- Clear all data on expiration
- No session persistence across restarts

#### Memory Security
**Control:** Explicit memory cleanup

```python
# Clear sensitive data when done
del sensitive_data
import gc
gc.collect()
```

### 2. Network Security

#### HTTPS/TLS
**Requirement:** HTTPS mandatory in production

**Setup with NGINX:**
```nginx
server {
    listen 443 ssl http2;
    server_name medgemma.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Firewall Configuration
```bash
# Allow only necessary ports
ufw allow 443/tcp  # HTTPS
ufw allow 22/tcp   # SSH (if needed)
ufw enable
```

#### Network Isolation
- Deploy in private network
- Use VPN for remote access
- Restrict outbound connections
- Monitor network traffic

### 3. Access Control

#### Physical Security
- Secure kiosk location
- Prevent unauthorized access
- Screen privacy filters
- Automatic screen lock

#### Authentication (if multi-user)
```python
# Example: Add authentication layer
import streamlit as st

def check_authentication():
    if 'authenticated' not in st.session_state:
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if verify_password(password):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid password")
        st.stop()
```

#### Role-Based Access
- **Patients**: Read-only access to own session
- **Healthcare Staff**: Full access with logging
- **Administrators**: System configuration

### 4. Input Validation

#### Text Input
```python
def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    # Remove potential injection attempts
    text = text.strip()
    # Limit length
    max_length = 5000
    if len(text) > max_length:
        text = text[:max_length]
    # Additional validation as needed
    return text
```

#### File Upload (if implemented)
```python
def validate_file(file):
    """Validate uploaded file"""
    # Check file type
    allowed_types = ['image/png', 'image/jpeg']
    if file.type not in allowed_types:
        raise ValueError("Invalid file type")
    
    # Check file size
    max_size = 10 * 1024 * 1024  # 10 MB
    if file.size > max_size:
        raise ValueError("File too large")
    
    return True
```

### 5. Logging and Monitoring

#### Security Logging
```python
# Log security events (no PII)
logger.info(f"Session created: {session_id[:8]}...")
logger.warning(f"Invalid session attempt: {session_id[:8]}...")
logger.error(f"Authentication failed from IP: {ip_address}")
```

#### What to Log:
- ✅ Session creation/destruction
- ✅ Authentication attempts
- ✅ System errors
- ✅ Security events
- ✅ Performance metrics

#### What NOT to Log:
- ❌ Patient statements
- ❌ Medical summaries
- ❌ Personal information
- ❌ Transcripts
- ❌ Audio data

#### Monitoring Setup
```python
# Example: Prometheus metrics
from prometheus_client import Counter, Histogram

session_counter = Counter('sessions_total', 'Total sessions')
inference_duration = Histogram('inference_seconds', 'Model inference time')
```

### 6. Dependency Security

#### Regular Updates
```bash
# Check for vulnerabilities
pip list --outdated
pip install safety
safety check

# Update dependencies
pip install --upgrade -r requirements.txt
```

#### Dependency Scanning
```yaml
# GitHub Actions example
name: Security Scan
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run safety check
        run: |
          pip install safety
          safety check -r requirements.txt
```

### 7. Model Security

#### Model Provenance
- Use official model sources only
- Verify model checksums
- Document model versions
- Test models before deployment

#### Model Access Control
```python
# Restrict model file permissions
os.chmod('models/', 0o700)  # Owner only
```

#### Inference Security
```python
# Limit inference resources
def generate_summary(text, max_tokens=512):
    """Generate with resource limits"""
    # Set timeout
    with timeout(30):  # 30 seconds max
        summary = model.generate(
            text,
            max_new_tokens=max_tokens,
            # Additional safety parameters
        )
    return summary
```

### 8. Container Security (Docker)

#### Dockerfile Best Practices
```dockerfile
# Use specific version (not 'latest')
FROM python:3.10-slim

# Run as non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Read-only root filesystem (where possible)
VOLUME /tmp
```

#### Docker Compose Security
```yaml
services:
  app:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
```

### 9. Compliance

#### HIPAA Considerations
- [ ] Access controls implemented
- [ ] Audit logging enabled (no PHI)
- [ ] Encryption in transit (HTTPS)
- [ ] Automatic session termination
- [ ] No persistent PHI storage
- [ ] Business Associate Agreements (if applicable)
- [ ] Risk assessment completed
- [ ] Breach notification procedure

#### GDPR Considerations
- [ ] Data minimization (only necessary data)
- [ ] Purpose limitation (medical use only)
- [ ] Storage limitation (no persistent storage)
- [ ] Right to erasure (automatic deletion)
- [ ] Privacy by design (architecture)
- [ ] Privacy impact assessment

### 10. Incident Response

#### Detection
Monitor for:
- Unusual access patterns
- Failed authentication attempts
- System errors
- Performance anomalies
- Network anomalies

#### Response Plan
1. **Identify** the incident
2. **Contain** the threat
3. **Eradicate** the cause
4. **Recover** normal operations
5. **Document** lessons learned

#### Emergency Contacts
```
Security Team: security@example.com
System Admin: admin@example.com
Legal: legal@example.com
```

### 11. Security Testing

#### Penetration Testing
- SQL injection attempts
- XSS attacks
- CSRF attacks
- Session hijacking
- Authentication bypass
- Network sniffing

#### Security Audit Checklist
- [ ] No PII in logs
- [ ] No PII in error messages
- [ ] HTTPS enforced
- [ ] Sessions expire properly
- [ ] Data cleared on cleanup
- [ ] Input validation working
- [ ] Authentication secure (if enabled)
- [ ] Dependencies up to date
- [ ] Secrets not in code
- [ ] File permissions correct

## Security Checklist for Deployment

### Pre-Deployment
- [ ] Security review completed
- [ ] Penetration testing done
- [ ] Dependencies scanned
- [ ] Compliance review (HIPAA/GDPR)
- [ ] Access controls tested
- [ ] Logging configured
- [ ] Monitoring setup
- [ ] Incident response plan ready

### Deployment
- [ ] HTTPS configured
- [ ] Firewall rules applied
- [ ] Strong authentication enabled
- [ ] Sessions configured properly
- [ ] Resource limits set
- [ ] Backups configured (config only)
- [ ] Monitoring active
- [ ] Documentation complete

### Post-Deployment
- [ ] Monitor logs regularly
- [ ] Update dependencies monthly
- [ ] Review access logs
- [ ] Test backups
- [ ] Audit compliance quarterly
- [ ] Security training for staff
- [ ] Incident drills

## Reporting Security Issues

### Responsible Disclosure
If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email: security@example.com
3. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

4. Allow reasonable time for fix (90 days)
5. Coordinate disclosure

### Bug Bounty (Future)
Consider implementing a bug bounty program for:
- Critical vulnerabilities
- Privacy bypasses
- Authentication issues
- Data exposure risks

## Resources

### Security Standards
- OWASP Top 10
- CWE Top 25
- NIST Cybersecurity Framework
- ISO 27001

### Healthcare Security
- HIPAA Security Rule
- GDPR
- HITECH Act
- State privacy laws

### Training
- Security awareness training
- Privacy training
- Incident response training
- Compliance training

## Conclusion

Security is an ongoing process, not a one-time implementation. Regular reviews, updates, and testing are essential to maintain a secure system.

**Remember:** The best security feature is the one that's never needed because it prevents issues before they occur.
