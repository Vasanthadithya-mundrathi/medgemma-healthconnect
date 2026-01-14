# Deployment Guide

## Quick Deploy Options

### Option 1: Local Development

```bash
# Clone repository
git clone https://github.com/Vasanthadithya-mundrathi/medgemma-healthconnect.git
cd medgemma-healthconnect

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

Access at: http://localhost:8501

### Option 2: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    && rm -rf /var/lib/apt/lists/*

# Copy application
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run application
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

Build and run:

```bash
docker build -t medgemma-healthconnect .
docker run -p 8501:8501 medgemma-healthconnect
```

### Option 3: Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  medgemma-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - MODEL_NAME=google/gemma-2b
      - QUANTIZATION_BITS=4
      - SESSION_TIMEOUT=300
    volumes:
      - model-cache:/root/.cache
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  model-cache:
```

Deploy:

```bash
docker-compose up -d
```

### Option 4: Kubernetes Deployment

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: medgemma-healthconnect
spec:
  replicas: 2
  selector:
    matchLabels:
      app: medgemma
  template:
    metadata:
      labels:
        app: medgemma
    spec:
      containers:
      - name: app
        image: medgemma-healthconnect:latest
        ports:
        - containerPort: 8501
        env:
        - name: QUANTIZATION_BITS
          value: "4"
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
        livenessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: medgemma-service
spec:
  selector:
    app: medgemma
  ports:
  - port: 80
    targetPort: 8501
  type: LoadBalancer
```

Deploy:

```bash
kubectl apply -f k8s-deployment.yaml
```

## Edge Device Deployment

### Raspberry Pi 4 (4GB+)

1. **Prepare Device**
```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Python 3.10
sudo apt-get install python3.10 python3.10-venv python3-pip

# Install system dependencies
sudo apt-get install portaudio19-dev python3-pyaudio
```

2. **Install Application**
```bash
git clone https://github.com/Vasanthadithya-mundrathi/medgemma-healthconnect.git
cd medgemma-healthconnect

python3.10 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

3. **Configure for Edge**
Edit `.env`:
```bash
QUANTIZATION_BITS=4  # Essential for Pi
MODEL_NAME=google/gemma-2b  # Smaller model
```

4. **Run as Service**
Create `/etc/systemd/system/medgemma.service`:
```ini
[Unit]
Description=MedGemma HealthConnect
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/medgemma-healthconnect
Environment="PATH=/home/pi/medgemma-healthconnect/venv/bin"
ExecStart=/home/pi/medgemma-healthconnect/venv/bin/streamlit run app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable medgemma
sudo systemctl start medgemma
```

### NVIDIA Jetson Nano

Similar to Raspberry Pi, but with GPU support:

```bash
# Install CUDA toolkit
sudo apt-get install nvidia-jetpack

# Use FP16 quantization
QUANTIZATION_BITS=16
```

## Production Deployment Checklist

### Security
- [ ] HTTPS/TLS enabled
- [ ] Firewall configured
- [ ] Regular security updates
- [ ] Access control implemented
- [ ] Audit logging enabled (no PII)

### Privacy
- [ ] No PII storage verified
- [ ] Session expiration tested
- [ ] Data cleanup confirmed
- [ ] Privacy notice displayed
- [ ] Compliance review completed

### Performance
- [ ] Model pre-loaded
- [ ] Memory limits set
- [ ] Timeout configured
- [ ] Error handling tested
- [ ] Load testing completed

### Monitoring
- [ ] Health checks enabled
- [ ] Metrics collection
- [ ] Error alerting
- [ ] Uptime monitoring
- [ ] Resource monitoring

### Backup & Recovery
- [ ] Configuration backed up
- [ ] Model cache location documented
- [ ] Recovery procedures tested
- [ ] Failover plan created

## Environment Variables

### Required
```bash
MODEL_NAME=google/gemma-2b
QUANTIZATION_BITS=4
```

### Optional
```bash
SPEECH_LANGUAGE=en-US
AUDIO_SAMPLE_RATE=16000
ENABLE_LOGGING=false
STORE_TRANSCRIPTS=false
SESSION_TIMEOUT=300
TRIALS_DATABASE_PATH=./data/clinical_trials.json
```

## Performance Tuning

### Memory Optimization
```python
# In .env
QUANTIZATION_BITS=4  # Reduces memory by 75%
```

### CPU vs GPU
```python
# Automatic detection
device = "cuda" if torch.cuda.is_available() else "cpu"
```

### Batch Size
```python
# For multiple kiosks
MAX_CONCURRENT_SESSIONS=5
```

## Troubleshooting Production Issues

### Issue: High Memory Usage
**Solution:**
- Use 4-bit quantization
- Reduce concurrent sessions
- Implement memory limits

### Issue: Slow Response Times
**Solution:**
- Pre-load models at startup
- Use GPU if available
- Increase hardware resources

### Issue: Session Timeouts
**Solution:**
- Adjust SESSION_TIMEOUT
- Implement session warnings
- Add keep-alive pings

### Issue: Model Download Failures
**Solution:**
- Pre-download models
- Use local model cache
- Check network connectivity

## Scaling Strategies

### Vertical Scaling
- Increase RAM
- Add GPU
- Faster CPU

### Horizontal Scaling
- Multiple kiosk instances
- Load balancer
- Shared trial database

### Hybrid Approach
- Edge devices for intake
- Cloud for analytics
- Federated learning

## Support & Maintenance

### Regular Updates
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Pull latest code
git pull origin main

# Restart service
sudo systemctl restart medgemma
```

### Monitoring Commands
```bash
# Check service status
sudo systemctl status medgemma

# View logs
sudo journalctl -u medgemma -f

# Check resource usage
htop
```

### Backup Configuration
```bash
# Backup configuration
cp .env .env.backup

# Backup trial database
cp data/clinical_trials.json data/clinical_trials.backup.json
```
