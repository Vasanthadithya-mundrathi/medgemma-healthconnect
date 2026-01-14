# Usage Examples

## Basic Usage

### Starting the Application

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the application
streamlit run app.py
```

Open your browser to http://localhost:8501

## Patient Intake Workflow

### Example 1: Text Input

1. **Open the application**
2. **Select "Type symptoms"**
3. **Enter patient information:**
   ```
   I've been experiencing severe headaches for the past week, 
   especially in the morning. The pain is concentrated on the 
   right side of my head. I also feel nauseous and sensitive 
   to light. The headaches last for several hours.
   ```
4. **Click "Process Intake"**
5. **Click "Generate Medical Summary"**
6. **Click "Find Matching Clinical Trials"**

### Example 2: Voice Input (if microphone available)

1. **Open the application**
2. **Select "Use voice input"**
3. **Click "Start Recording"**
4. **Speak clearly:**
   > "I have been experiencing chronic back pain for about six months. 
   > The pain is in my lower back and gets worse when I sit for long periods. 
   > I've tried over-the-counter pain relievers but they only provide 
   > temporary relief."
5. **Review transcription**
6. **Follow steps 5-6 from Example 1**

## Sample Patient Cases

### Case 1: Diabetes Management

**Input:**
```
I was diagnosed with Type 2 diabetes about a year ago. 
Despite medication and dietary changes, my blood sugar 
levels remain high. My HbA1c is 8.2%. I'm interested 
in new treatment options.
```

**Expected Output:**
- Medical summary highlighting diabetes diagnosis, duration, current HbA1c
- Matching clinical trials for diabetes treatment studies
- Eligibility criteria for relevant trials

### Case 2: Hypertension

**Input:**
```
I've had high blood pressure for several years. My typical 
readings are around 150/95. I'm currently on medication but 
would like to explore additional treatment options.
```

**Expected Output:**
- Summary of hypertension with specific blood pressure readings
- Clinical trials for hypertension management
- Information about combination therapy studies

### Case 3: Chronic Pain

**Input:**
```
I've been dealing with chronic pain in my joints for over 
two years. The pain is constant and affects my ability to 
work and sleep. I'm looking for alternatives to opioid 
medications.
```

**Expected Output:**
- Summary emphasizing chronic pain, duration, and impact
- Clinical trials for non-opioid pain management
- Eligibility information

## Privacy Features Demonstration

### Session Management

The system automatically:
- Creates a unique session ID when you start
- Displays time remaining in the sidebar
- Expires sessions after 5 minutes
- Clears all data when session ends

**To test:**
1. Start the application
2. Note the session timer in the sidebar
3. Enter some patient information
4. Wait for session to expire or click "Start New Session"
5. Verify all previous data is cleared

### No Data Persistence

**To verify:**
1. Enter patient information
2. Generate summary
3. Close the browser
4. Check the file system:
   ```bash
   ls data/
   ```
   Should only contain `clinical_trials.json`, no patient data

5. Check for audio files:
   ```bash
   find . -name "*.wav" -o -name "*.mp3"
   ```
   Should return no results

## API Usage (Module Level)

### Using Speech-to-Text Module

```python
from src.speech_to_text import SpeechToText

# Initialize
stt = SpeechToText(language="en-US")

# Text input (testing/fallback)
text = stt.transcribe_from_text("Patient describes symptoms...")

# Voice input (if microphone available)
transcript = stt.listen_and_transcribe(timeout=10)
if transcript:
    print(f"Transcribed: {transcript}")
```

### Using Privacy Manager

```python
from src.privacy_manager import PrivacyManager

# Initialize
pm = PrivacyManager(session_timeout=300)

# Create session
session_id = pm.create_session()

# Validate session
if pm.validate_session(session_id):
    # Process data
    data_hash = pm.hash_data("sensitive information")
    
# End session (clears data)
pm.end_session(session_id)
```

### Using Clinical Trial Matcher

```python
from src.clinical_trial_matcher import ClinicalTrialMatcher

# Initialize
matcher = ClinicalTrialMatcher()
matcher.load_trials_database()
matcher.load_embedding_model()

# Match trials
summary = "Patient with Type 2 diabetes, HbA1c 8.2%"
matches = matcher.match_trials(summary, top_k=5, threshold=0.3)

# Display results
for trial in matches:
    print(matcher.format_trial_summary(trial))
```

### Using MedGemma Summarizer (requires model)

```python
from src.medgemma_summarizer import MedGemmaSummarizer

# Initialize with quantization
summarizer = MedGemmaSummarizer(
    model_name="google/gemma-2b",
    quantization_bits=4
)

# Load model (first time only)
if summarizer.load_model():
    # Generate summary
    transcript = "Patient statement about symptoms..."
    summary = summarizer.summarize_patient_intake(transcript)
    print(summary)
```

## Configuration Examples

### Changing Session Timeout

Edit `.env`:
```bash
SESSION_TIMEOUT=600  # 10 minutes instead of 5
```

### Using Different Model

Edit `.env`:
```bash
MODEL_NAME=google/gemma-7b  # Larger model (requires more RAM)
QUANTIZATION_BITS=8  # 8-bit quantization for better quality
```

### Changing Language

Edit `.env`:
```bash
SPEECH_LANGUAGE=es-ES  # Spanish
# or
SPEECH_LANGUAGE=fr-FR  # French
```

## Troubleshooting Examples

### Issue: Microphone Not Working

**Solution:**
```python
# In the UI, select "Type symptoms" instead
# Or check microphone permissions:
# - Windows: Settings > Privacy > Microphone
# - macOS: System Preferences > Security & Privacy > Microphone
# - Linux: Check ALSA/PulseAudio configuration
```

### Issue: Model Loading Fails

**Solution:**
```python
# Use smaller model or increase quantization
# Edit .env:
MODEL_NAME=google/gemma-2b  # Smaller model
QUANTIZATION_BITS=4  # More aggressive quantization
```

### Issue: Out of Memory

**Solution:**
```bash
# Increase quantization in .env:
QUANTIZATION_BITS=4  # Most memory efficient

# Or close other applications
# Or use CPU instead of GPU (automatic fallback)
```

## Advanced Usage

### Custom Clinical Trials Database

1. **Edit `data/clinical_trials.json`:**
```json
[
  {
    "trial_id": "NCT12345678",
    "title": "Your Custom Trial",
    "condition": "Specific Condition",
    "description": "Trial description...",
    "eligibility": "Inclusion/exclusion criteria",
    "location": "Geographic location",
    "status": "Recruiting"
  }
]
```

2. **Restart the application**

### Integration with Existing Systems

```python
# Example: Integrate with electronic health records (EHR)
from src.medgemma_summarizer import MedGemmaSummarizer

def process_patient_intake(patient_id, transcript):
    """
    Process patient intake and update EHR
    (Example - not production code)
    """
    # Generate summary
    summarizer = MedGemmaSummarizer()
    summary = summarizer.summarize_patient_intake(transcript)
    
    # Match trials
    matcher = ClinicalTrialMatcher()
    trials = matcher.match_trials(summary)
    
    # Return results (don't store sensitive data)
    return {
        "summary": summary,
        "trial_count": len(trials),
        "trials": trials
    }
```

## Best Practices

### For Healthcare Providers

1. **Always verify AI-generated summaries**
2. **Use as a screening tool, not diagnostic tool**
3. **Maintain professional judgment**
4. **Explain AI assistance to patients**
5. **Comply with local regulations**

### For Patients

1. **Be specific about symptoms**
2. **Include duration and severity**
3. **Mention relevant medical history**
4. **Don't rely solely on this tool**
5. **Consult healthcare professionals**

### For Developers

1. **Test privacy features thoroughly**
2. **Monitor session timeouts**
3. **Validate model outputs**
4. **Keep dependencies updated**
5. **Follow security best practices**

## Testing the System

### Manual Testing Checklist

- [ ] Start application successfully
- [ ] Create session with ID
- [ ] Enter text symptoms
- [ ] Generate medical summary
- [ ] Match clinical trials
- [ ] Verify session timer
- [ ] Test "Start New Session" button
- [ ] Verify data cleared after new session
- [ ] Check no files created in data/
- [ ] Close and reopen - verify no persistence

### Performance Testing

```bash
# Monitor memory usage
htop  # or Task Manager on Windows

# Check model loading time
time streamlit run app.py
```

## Additional Resources

- **Medical Terminology:** Consult medical dictionaries
- **Clinical Trials:** Visit ClinicalTrials.gov for real data
- **Privacy Regulations:** Review HIPAA, GDPR guidelines
- **AI Ethics:** Follow responsible AI principles
