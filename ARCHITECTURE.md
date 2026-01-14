# MedGemma HealthConnect - Architecture Documentation

## System Overview

MedGemma HealthConnect is a privacy-first healthcare AI system designed for patient intake with the following key components:

### Core Modules

#### 1. Speech-to-Text Module (`speech_to_text.py`)
- **Purpose**: Convert patient voice input to text
- **Privacy**: No audio storage, in-memory processing only
- **Features**:
  - Real-time transcription
  - Ambient noise adjustment
  - Fallback to text input
  - Multi-language support

#### 2. MedGemma Summarizer (`medgemma_summarizer.py`)
- **Purpose**: Generate medical summaries from patient statements
- **Technology**: 
  - Google Gemma/MedGemma model
  - 4-bit quantization for edge deployment
  - BitsAndBytes optimization
- **Features**:
  - Local inference
  - Structured medical summaries
  - Entity extraction
  - Memory-efficient processing

#### 3. Clinical Trial Matcher (`clinical_trial_matcher.py`)
- **Purpose**: Match patient conditions with relevant clinical trials
- **Technology**:
  - Sentence-BERT embeddings
  - Semantic similarity search
  - Vector-based matching
- **Features**:
  - Pre-computed trial embeddings
  - Fast similarity search
  - Configurable matching threshold
  - Detailed trial information

#### 4. Privacy Manager (`privacy_manager.py`)
- **Purpose**: Ensure no PII storage and data protection
- **Features**:
  - Session-based data management
  - Automatic expiration (5 minutes default)
  - Data hashing for audit trails
  - Zero persistent storage

### Data Flow

```
Patient Input (Voice/Text)
        ↓
  Speech-to-Text
        ↓
   Transcript (In-Memory)
        ↓
  MedGemma Summarizer
        ↓
   Medical Summary (In-Memory)
        ↓
  Clinical Trial Matcher
        ↓
   Trial Recommendations
        ↓
  Display to User
        ↓
  Session Expires → Data Deleted
```

## Privacy Architecture

### Zero Storage Design

1. **No File Writes**: Audio and transcripts never written to disk
2. **Memory Only**: All processing in RAM
3. **Session-Based**: Data tied to temporary sessions
4. **Auto-Cleanup**: Automatic expiration and deletion
5. **No Logging**: Patient data not in logs

### Session Management

```python
Session Lifecycle:
1. Create → UUID-based anonymous ID
2. Process → Data in memory only
3. Expire → 5 minutes (configurable)
4. Delete → All data cleared
```

## Edge Deployment

### Quantization Strategy

The system uses 4-bit quantization by default for edge compatibility:

```python
BitsAndBytesConfig:
- 4-bit quantization (NF4)
- Double quantization enabled
- Float16 compute dtype
- Automatic device mapping
```

### Performance Optimization

1. **Model Loading**: Lazy loading on first use
2. **Caching**: Session-level model caching
3. **Batch Processing**: Support for multiple requests
4. **Memory Management**: Explicit cleanup after inference

## Security Considerations

### Threat Model

**Protected Against:**
- Data breaches (no storage)
- Session hijacking (UUID-based, expiring)
- PII leakage (anonymized processing)
- Model extraction (standard protections)

**Not Protected Against:**
- Physical access to running system
- Screen capture during use
- Network interception (use HTTPS)

### Recommended Production Hardening

1. **Network Security**
   - HTTPS/TLS required
   - Certificate pinning
   - Network isolation

2. **Access Control**
   - Physical kiosk security
   - Automatic screen timeout
   - User authentication

3. **Monitoring**
   - Audit logs (no PII)
   - Session analytics
   - Error tracking

4. **Compliance**
   - HIPAA assessment required
   - GDPR compliance review
   - Local regulation adherence

## Scalability

### Single Kiosk
- Handles sequential patients
- 5-minute session timeout
- Automatic cleanup

### Multiple Kiosks
- Independent instances
- Shared clinical trials DB
- Load balancing recommended

### Cloud Deployment
- Container-based (Docker)
- Kubernetes orchestration
- Horizontal scaling supported

## Future Enhancements

1. **Medical NLP**
   - Specialized medical entity recognition
   - ICD-10 code mapping
   - Drug interaction checking

2. **Multi-Modal**
   - Image upload support
   - Document scanning
   - Vital signs integration

3. **Advanced Matching**
   - Geographic proximity
   - Eligibility pre-screening
   - Trial enrollment status

4. **Offline Mode**
   - Complete offline operation
   - Local model caching
   - Sync-when-online architecture

## Technology Stack

### Core Technologies
- **Python 3.8+**: Main language
- **Streamlit**: UI framework
- **PyTorch**: Deep learning framework
- **Transformers**: Model library
- **BitsAndBytes**: Quantization

### Key Dependencies
- `speechrecognition`: Voice input
- `sentence-transformers`: Embeddings
- `accelerate`: Model loading
- `pydantic`: Data validation

## Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Docker Deployment
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

### Edge Device (Raspberry Pi 4+)
- 4GB+ RAM required
- 4-bit quantization essential
- CPU inference mode
- Reduced model size

## Troubleshooting

### Common Issues

1. **Microphone Not Working**
   - Check permissions
   - Use text input fallback
   - Verify PyAudio installation

2. **Model Loading Slow**
   - First run downloads model
   - Subsequent runs use cache
   - Consider local model storage

3. **Out of Memory**
   - Reduce batch size
   - Use 4-bit quantization
   - Close other applications

4. **Trial Matching Inaccurate**
   - Expand trial database
   - Adjust similarity threshold
   - Improve medical summaries

## Monitoring & Metrics

### Key Metrics (No PII)
- Session count
- Average session duration
- Model inference time
- Trial match success rate
- Error rates

### Health Checks
- Model loaded: Yes/No
- Trials DB loaded: Yes/No
- Available memory
- Active sessions count

## References

- [Gemma Model Documentation](https://ai.google.dev/gemma)
- [Transformers Library](https://huggingface.co/docs/transformers)
- [Streamlit Documentation](https://docs.streamlit.io)
- [HIPAA Guidelines](https://www.hhs.gov/hipaa)
