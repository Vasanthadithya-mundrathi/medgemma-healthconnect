# MedGemma HealthConnect 🏥

Privacy-first healthcare AI system featuring patient intake kiosk with speech-to-text, MedGemma summarization for local processing, and clinical trial matcher agent.

## 🌟 Features

- **🎤 Speech-to-Text Patient Intake**: Voice-enabled patient symptom capture
- **🤖 AI Medical Summarization**: Local MedGemma-powered medical text analysis
- **🔬 Clinical Trial Matching**: Intelligent matching of patient conditions with relevant trials
- **🎨 Streamlit UI**: User-friendly kiosk interface
- **⚡ Edge-Compatible**: 4-bit quantization for efficient deployment
- **🔒 Privacy-First**: Zero PII storage, session-based processing

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Streamlit UI (app.py)                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────┐  ┌────────────────┐  ┌──────────────┐ │
│  │ Speech-to-Text│  │    MedGemma    │  │ Trial Matcher│ │
│  │    Module     │→ │  Summarizer    │→ │    Agent     │ │
│  └───────────────┘  └────────────────┘  └──────────────┘ │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │           Privacy Manager (No PII Storage)           │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Microphone (optional, for voice input)
- 8GB+ RAM recommended
- GPU optional (CPU with quantization works fine)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Vasanthadithya-mundrathi/medgemma-healthconnect.git
cd medgemma-healthconnect
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment (optional)**
```bash
cp .env.example .env
# Edit .env to customize settings
```

5. **Run the application**
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage

### Patient Intake Flow

1. **Step 1: Patient Intake**
   - Choose input method: text or voice
   - Describe symptoms and concerns
   - Process the intake information

2. **Step 2: Medical Summary**
   - Click "Generate Medical Summary"
   - AI analyzes and structures the information
   - Review the generated summary

3. **Step 3: Clinical Trial Matching**
   - Click "Find Matching Clinical Trials"
   - System matches symptoms with relevant trials
   - Explore trial details and eligibility

### Privacy Features

- **No Storage**: Audio and transcripts are never saved to disk
- **Session-Based**: All data expires after 5 minutes
- **Local Processing**: AI runs entirely on your device
- **Anonymized**: No personal identifiers required

## 🔧 Configuration

Edit `.env` file to customize:

```bash
# Model Configuration
MODEL_NAME=google/gemma-2b
QUANTIZATION_BITS=4
USE_FLASH_ATTENTION=false

# Speech Recognition
SPEECH_LANGUAGE=en-US
AUDIO_SAMPLE_RATE=16000

# Privacy Settings
ENABLE_LOGGING=false
STORE_TRANSCRIPTS=false
SESSION_TIMEOUT=300

# Clinical Trials
TRIALS_DATABASE_PATH=./data/clinical_trials.json
```

## 📁 Project Structure

```
medgemma-healthconnect/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment configuration template
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── src/
│   ├── __init__.py
│   ├── speech_to_text.py          # Speech recognition module
│   ├── medgemma_summarizer.py     # MedGemma integration
│   ├── clinical_trial_matcher.py  # Trial matching agent
│   └── privacy_manager.py         # Privacy protection
└── data/
    └── clinical_trials.json       # Clinical trials database (auto-generated)
```

## 🔒 Privacy & Security

### Privacy-First Design Principles

1. **No Persistent Storage**: Patient data is never written to disk
2. **In-Memory Processing**: All operations in RAM only
3. **Automatic Cleanup**: Sessions expire and data is cleared
4. **Local Execution**: No external API calls for sensitive data
5. **No Logging**: Patient information is not logged

### Security Considerations

- Use HTTPS in production
- Implement proper authentication for kiosk access
- Regular security audits recommended
- Compliance with HIPAA and local regulations required

## 🛠️ Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/
```

### Code Quality

```bash
# Format code
black src/ app.py

# Lint code
flake8 src/ app.py

# Type checking
mypy src/
```

## 🎯 Edge Deployment

### Quantization Options

The system supports multiple quantization levels:

- **4-bit**: Best for edge devices (default)
- **8-bit**: Balance between quality and size
- **FP16**: GPU-optimized
- **FP32**: Full precision (development only)

### Hardware Requirements by Quantization

| Quantization | RAM    | Storage | Speed  |
|-------------|--------|---------|--------|
| 4-bit       | 4GB    | 2GB     | Fast   |
| 8-bit       | 6GB    | 4GB     | Medium |
| FP16        | 8GB    | 6GB     | Fast*  |
| FP32        | 16GB   | 12GB    | Slow   |

*GPU required

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## ⚠️ Disclaimer

This is a demonstration system for educational purposes. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns.

## 🙏 Acknowledgments

- Google's Gemma model team
- Hugging Face Transformers library
- Streamlit team
- Open-source medical NLP community

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for privacy-conscious healthcare AI**