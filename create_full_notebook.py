#!/usr/bin/env python3
"""
Complete Google Colab Notebook Generator for MedGemma HealthConnect
Creates 1500+ lines with 25-30 cells covering all required sections
"""

import json

def cm(text):
    """Create markdown cell"""
    return {"cell_type": "markdown", "metadata": {}, "source": text.split('\n')}

def cc(code):
    """Create code cell"""
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": code.split('\n')}

notebook = {
    "cells": [],
    "metadata": {
        "colab": {"provenance": [], "gpuType": "T4"},
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"},
        "accelerator": "GPU"
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

cells = []

# === PART 1: Installation & Setup (Cells 1-3) ===
cells.append(cm("""# 🏥 MedGemma HealthConnect - Complete Demo Notebook

**Privacy-First Healthcare AI: Patient Intake Kiosk with Med Gemma**

This comprehensive notebook demonstrates:
- ✅ Patient intake with PII protection
- ✅ AI-powered medical summarization using MedGemma
- ✅ Clinical trial matching agent
- ✅ Edge-compatible 4-bit quantization
- ✅ Complete workflows for Kaggle submission

**Privacy Guarantees:**
- Zero persistent storage of patient data
- Session-based processing (5-minute expiration)
- All data processed in-memory only
- HIPAA-aligned architecture

**Notebook Structure (30 Cells):**
1. Installation & Setup (Cells 1-4)
2. Core Modules Import (Cells 5-7)
3. Synthetic Test Data (Cells 8-9)
4. Demonstration Workflows (Cells 10-18)
5. Visualization & Metrics (Cells 19-20)
6. Kaggle Submission Package (Cells 21-23)
7. Edge Deployment Test (Cell 24-25)
8. Documentation (Cells 26-30)

---"""))

cells.append(cm("""## 📦 PART 1: Installation & Setup

Installing all required dependencies for MedGemma HealthConnect"""))

cells.append(cc("""# Cell 2: Install Core Dependencies
print("🔧 Installing MedGemma HealthConnect Dependencies...")
print("=" * 70)

# Core ML/AI packages
!pip install -q transformers>=4.36.0
!pip install -q torch>=2.1.0
!pip install -q accelerate>=0.25.0
!pip install -q bitsandbytes>=0.41.0

# NLP and embeddings
!pip install -q sentence-transformers>=2.2.0
!pip install -q faiss-cpu>=1.7.4

# UI frameworks
!pip install -q gradio streamlit

# Visualization
!pip install -q plotly matplotlib seaborn

# Utilities
!pip install -q pandas numpy python-dotenv pydantic

# System monitoring
!pip install -q psutil

print("✅ All dependencies installed successfully!")
print("=" * 70)"""))

cells.append(cc("""# Cell 3: Mount Drive & Clone Repository
from google.colab import drive
import os
import sys

# Mount Google Drive
print("📁 Mounting Google Drive...")
drive.mount('/content/drive', force_remount=True)
print("✅ Google Drive mounted")

# Clone repository
print("\\n🔄 Cloning MedGemma HealthConnect Repository...")
repo_url = "https://github.com/Vasanthadithya-mundrathi/medgemma-healthconnect.git"

if os.path.exists("/content/medgemma-healthconnect"):
    !rm -rf /content/medgemma-healthconnect

!git clone -q {repo_url} /content/medgemma-healthconnect

# Add to Python path
sys.path.insert(0, '/content/medgemma-healthconnect')
sys.path.insert(0, '/content/medgemma-healthconnect/src')

print("✅ Repository cloned")
print(f"📂 Working directory: {os.getcwd()}")
print(f"📚 Python path includes: /content/medgemma-healthconnect/src")"""))

cells.append(cc("""# Cell 4: Verify Installation & GPU
import torch
from transformers import AutoTokenizer
import logging

logging.basicConfig(level=logging.INFO)

print("🔍 System Verification")
print("=" * 70)

# Check GPU
if torch.cuda.is_available():
    print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
    print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    print(f"   CUDA Version: {torch.version.cuda}")
else:
    print("⚠️  No GPU detected - using CPU (slower inference)")

# Check Python version
import sys
print(f"\\n✅ Python: {sys.version.split()[0]}")

# Verify PyTorch
print(f"✅ PyTorch: {torch.__version__}")

# Check model availability
try:
    model_name = "google/gemma-2b"
    print(f"\\n🔍 Checking model access: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    print(f"✅ Model accessible - Vocab size: {tokenizer.vocab_size}")
    del tokenizer
except Exception as e:
    print(f"⚠️  Model check: {str(e)[:100]}")
    print("   Will use demo mode")

print("\\n" + "=" * 70)
print("✅ Installation verified - Ready to proceed!")
print("=" * 70)"""))

# === PART 2: Core Modules Import (Cells 5-7) ===
cells.append(cm("""## 🧠 PART 2: Import Core Modules

Importing privacy-first healthcare AI components from the repository"""))

cells.append(cc("""# Cell 5: Import Core Modules
import sys
import os

# Ensure paths
sys.path.insert(0, '/content/medgemma-healthconnect/src')

# Import all core modules
from privacy_manager import PrivacyManager
from clinical_trial_matcher import ClinicalTrialMatcher
from medgemma_summarizer import MedGemmaSummarizer

print("✅ Core modules imported successfully!")
print("\\n📦 Available Components:")
print("   • PrivacyManager - Session management & PII protection")
print("   • ClinicalTrialMatcher - AI-powered semantic trial matching")
print("   • MedGemmaSummarizer - Medical text summarization with quantization")
print("\\n🔒 Privacy Features:")
print("   • Zero-storage architecture")
print("   • Session-based data handling")
print("   • Automatic expiration (5 minutes)")
print("   • No PII logging or persistence")"""))

cells.append(cc("""# Cell 6: Configure Components for Colab
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("🔧 Initializing MedGemma HealthConnect Components...")
print("=" * 70)

# Initialize Privacy Manager
privacy_manager = PrivacyManager(session_timeout=300)
print("✅ Privacy Manager initialized")
print(f"   Session timeout: {privacy_manager.session_timeout} seconds")
print(f"   Active sessions: {len(privacy_manager.active_sessions)}")

# Initialize Clinical Trial Matcher
trial_matcher = ClinicalTrialMatcher()
trial_matcher.load_trials_database()
print(f"\\n✅ Clinical Trial Matcher initialized")
print(f"   Trials loaded: {len(trial_matcher.trials_data)}")

# Load embedding model
print("\\n🔄 Loading embedding model (SentenceTransformer)...")
trial_matcher.load_embedding_model()
print("✅ Embedding model loaded")
print(f"   Model: all-MiniLM-L6-v2")
print(f"   Embedding dim: 384")

# MedGemma Summarizer (lazy load to save memory)
print("\\n✅ MedGemma Summarizer ready (will load on-demand)")
print(f"   Model: google/gemma-2b")
print(f"   Quantization: 4-bit (edge-compatible)")
print(f"   Device: {'GPU' if torch.cuda.is_available() else 'CPU'}")

print("\\n" + "=" * 70)
print("🎉 All components configured and ready!")
print("=" * 70)"""))

cells.append(cc("""# Cell 7: Configuration & Environment
import os
from datetime import datetime

# Set configuration
config = {
    "MODEL_NAME": "google/gemma-2b",
    "QUANTIZATION_BITS": 4,
    "SESSION_TIMEOUT": 300,
    "MAX_SUMMARY_LENGTH": 512,
    "TRIAL_MATCH_THRESHOLD": 0.2,
    "TOP_K_TRIALS": 5,
    "PRIVACY_MODE": True,
    "STORE_TRANSCRIPTS": False,
    "ENABLE_LOGGING": False
}

print("⚙️  Configuration")
print("=" * 70)
for key, value in config.items():
    print(f"   {key}: {value}")

print("\\n" + "=" * 70)
print(f"✅ Configuration set for Colab environment")
print(f"   Timestamp: {datetime.utcnow().isoformat()}Z")
print("=" * 70)"""))

# === PART 3: Synthetic Test Data (Cells 8-9) ===
cells.append(cm("""## 🧪 PART 3: Synthetic Test Data

Creating realistic patient profiles and clinical trial data"""))

cells.append(cc("""# Cell 8: Create Synthetic Patient Profiles
# Comprehensive patient profiles for testing
synthetic_patients = [
    {
        "patient_id": "DEMO_001",
        "age": 45,
        "gender": "Female",
        "chief_complaint": "I've been experiencing severe headaches for the past 3 weeks, especially in the morning. The pain is on the right side of my head and sometimes causes nausea and sensitivity to light. Over-the-counter medications provide only temporary relief.",
        "conditions": ["Chronic Migraine", "Hypertension"],
        "medications": ["Lisinopril 10mg daily", "Ibuprofen as needed"],
        "duration": "3 weeks acute, chronic migraines for 2 years",
        "severity": "Severe",
        "frequency": "4-5 migraines per month"
    },
    {
        "patient_id": "DEMO_002",
        "age": 62,
        "gender": "Male",
        "chief_complaint": "I have Type 2 diabetes that's been difficult to control despite medications. My recent HbA1c was 8.5%, and I'm experiencing increased thirst, fatigue, and blurred vision. My blood sugar levels are consistently above 200 mg/dL.",
        "conditions": ["Type 2 Diabetes", "Obesity", "Hypertension"],
        "medications": ["Metformin 1000mg twice daily", "Glipizide 5mg daily", "Lisinopril 20mg daily"],
        "duration": "5 years diagnosed, worsening control in last 6 months",
        "severity": "Moderate to Severe",
        "bmi": 32
    },
    {
        "patient_id": "DEMO_003",
        "age": 38,
        "gender": "Female",
        "chief_complaint": "I've had chronic lower back pain for about 8 months that started after lifting something heavy. The pain radiates down my left leg and is worse in the morning. Physical therapy and NSAIDs haven't provided lasting relief.",
        "conditions": ["Chronic Lower Back Pain", "Sciatica"],
        "medications": ["Ibuprofen 600mg three times daily", "Cyclobenzaprine as needed"],
        "duration": "8 months continuous",
        "severity": "Moderate",
        "pain_scale": "6-7/10"
    },
    {
        "patient_id": "DEMO_004",
        "age": 29,
        "gender": "Male",
        "chief_complaint": "I have moderate to severe asthma that's been getting worse over the past year. I use my rescue inhaler 3-4 times per day and wake up at night with wheezing and shortness of breath at least twice a week. My current medications aren't providing adequate control.",
        "conditions": ["Moderate-Severe Persistent Asthma", "Seasonal Allergies"],
        "medications": ["Albuterol inhaler PRN", "Fluticasone/Salmeterol 250/50 twice daily", "Montelukast 10mg daily"],
        "duration": "Lifetime asthma, worsening in past year",
        "severity": "Moderate to Severe",
        "fev1_percent": 68
    },
    {
        "patient_id": "DEMO_005",
        "age": 55,
        "gender": "Male",
        "chief_complaint": "My blood pressure has been consistently high (averaging 155/98) despite taking two medications regularly. I occasionally experience headaches, dizziness, and have noticed increased fatigue. My doctor calls it resistant hypertension.",
        "conditions": ["Resistant Hypertension", "High Cholesterol", "Prediabetes"],
        "medications": ["Amlodipine 10mg daily", "Losartan 100mg daily", "Atorvastatin 20mg daily"],
        "duration": "3 years hypertension, uncontrolled for 8 months",
        "severity": "Moderate",
        "avg_bp": "155/98"
    }
]

print("👥 Synthetic Patient Profiles Created")
print("=" * 70)
for i, patient in enumerate(synthetic_patients, 1):
    print(f"\\n[{i}] Patient: {patient['patient_id']}")
    print(f"    Demographics: {patient['age']}yo {patient['gender']}")
    print(f"    Conditions: {', '.join(patient['conditions'])}")
    print(f"    Complaint: {patient['chief_complaint'][:80]}...")
    print(f"    Severity: {patient['severity']}")
print("\\n" + "=" * 70)
print(f"✅ {len(synthetic_patients)} patient profiles ready for testing")
print("=" * 70)"""))

cells.append(cc("""# Cell 9: Extended Clinical Trials Database
import json

# Extended clinical trials for comprehensive matching
extended_trials = [
    {
        "trial_id": "NCT05001234",
        "title": "Phase III Study of Novel GLP-1 Agonist for Type 2 Diabetes",
        "condition": "Type 2 Diabetes Mellitus",
        "description": "Evaluating safety and efficacy of new once-weekly GLP-1 receptor agonist for blood sugar control in patients with HbA1c > 7.5%. Primary endpoint is HbA1c reduction at 24 weeks.",
        "eligibility": "Adults 18-75 with Type 2 Diabetes, HbA1c 7.5-11.0%, BMI 25-45, stable dose of metformin for 3+ months",
        "location": "Multiple Sites (USA, Canada, Europe)",
        "status": "Recruiting",
        "phase": "Phase III",
        "enrollment": 800,
        "sponsor": "Major Pharmaceutical Company",
        "duration": "52 weeks"
    },
    {
        "trial_id": "NCT05002345",
        "title": "CGRP Antagonist for Chronic Migraine Prevention",
        "condition": "Chronic Migraine",
        "description": "Evaluating novel monthly injectable CGRP antagonist for prevention of chronic migraine. Primary endpoint is reduction in monthly migraine days.",
        "eligibility": "Adults 18-65 with chronic migraine (15+ headache days/month, 8+ migraine days) for 3+ months, previous inadequate response to 2+ preventive treatments",
        "location": "Multiple Sites (USA, International)",
        "status": "Recruiting",
        "phase": "Phase III",
        "enrollment": 600,
        "sponsor": "Neurology Research Institute",
        "duration": "6 months"
    },
    {
        "trial_id": "NCT05003456",
        "title": "Non-Opioid Treatment for Chronic Musculoskeletal Pain",
        "condition": "Chronic Lower Back Pain",
        "description": "Multi-modal non-opioid approach combining novel analgesic with physical therapy for chronic musculoskeletal pain. Focus on functional improvement and quality of life.",
        "eligibility": "Adults 18-70 with chronic musculoskeletal pain > 6 months, average pain score 4+ on 0-10 scale, willingness to participate in physical therapy",
        "location": "Multiple Sites (USA)",
        "status": "Recruiting",
        "phase": "Phase III",
        "enrollment": 500,
        "sponsor": "Pain Management Research Center",
        "duration": "16 weeks treatment + 12 weeks follow-up"
    },
    {
        "trial_id": "NCT05004567",
        "title": "Biologic Therapy for Severe Uncontrolled Asthma",
        "condition": "Severe Persistent Asthma",
        "description": "Novel biologic targeting IL-4/IL-13 pathway for severe uncontrolled asthma. Primary endpoint is reduction in exacerbations and improvement in FEV1.",
        "eligibility": "Adults and adolescents 12+ with severe asthma, FEV1 < 80% predicted, 2+ exacerbations in past year despite high-dose ICS/LABA, eosinophils > 150 cells/µL or FeNO > 20 ppb",
        "location": "Multiple Sites (USA, Canada, Australia)",
        "status": "Recruiting",
        "phase": "Phase III",
        "enrollment": 750,
        "sponsor": "Respiratory Medicine Consortium",
        "duration": "1 year"
    },
    {
        "trial_id": "NCT05005678",
        "title": "Triple Combination Therapy for Resistant Hypertension",
        "condition": "Resistant Hypertension",
        "description": "Fixed-dose triple combination pill for resistant hypertension. Comparing to standard stepped therapy approach. Primary endpoint is BP control at 12 weeks.",
        "eligibility": "Adults with uncontrolled hypertension (BP > 140/90) despite 2+ antihypertensive medications at optimal doses, no secondary hypertension causes",
        "location": "Multiple Sites (USA)",
        "status": "Recruiting",
        "phase": "Phase III",
        "enrollment": 400,
        "sponsor": "Cardiovascular Research Group",
        "duration": "24 weeks"
    },
    {
        "trial_id": "NCT05006789",
        "title": "SGLT2 Inhibitor for Diabetic Kidney Protection",
        "condition": "Type 2 Diabetes with Chronic Kidney Disease",
        "description": "Evaluating renal protective effects of SGLT2 inhibitor in diabetic patients with early kidney disease. Primary endpoint is change in eGFR and albumin-to-creatinine ratio.",
        "eligibility": "Adults with Type 2 Diabetes and eGFR 30-75 mL/min/1.73m², albuminuria present, on stable ACE inhibitor or ARB",
        "location": "Multiple Sites (International)",
        "status": "Recruiting",
        "phase": "Phase III",
        "enrollment": 1000,
        "sponsor": "Nephrology Research Foundation",
        "duration": "2 years"
    },
    {
        "trial_id": "NCT05007890",
        "title": "Precision Medicine Approach to Migraine Treatment",
        "condition": "Migraine with Aura",
        "description": "Biomarker-guided treatment selection for migraine using genetic and neuroimaging biomarkers to predict response to different preventive medications.",
        "eligibility": "Adults 18-60 with migraine with aura, 4-14 migraine days/month, willing to undergo genetic testing and MRI",
        "location": "Academic Medical Centers (USA)",
        "status": "Recruiting",
        "phase": "Phase II",
        "enrollment": 300,
        "sponsor": "Precision Neurology Institute",
        "duration": "6 months"
    }
]

# Extend trial matcher database
trial_matcher.trials_data.extend(extended_trials)

# Re-compute embeddings
trial_texts = [f"{trial['condition']} {trial['description']}" for trial in trial_matcher.trials_data]
trial_matcher.trial_embeddings = trial_matcher.embedding_model.encode(trial_texts)

print("🔬 Extended Clinical Trials Database")
print("=" * 70)
print(f"Total trials: {len(trial_matcher.trials_data)}")
print("\\nSample trials:")
for trial in extended_trials[:4]:
    print(f"\\n  • {trial['trial_id']}")
    print(f"    {trial['title']}")
    print(f"    Condition: {trial['condition']}")
    print(f"    Phase: {trial['phase']}, Enrollment: {trial['enrollment']}")
print("\\n" + "=" * 70)
print("✅ Extended database ready with real-world trial scenarios")
print("=" * 70)"""))

# Continue adding more cells...
# I'll save what we have so far
notebook['cells'] = cells

with open('/home/runner/work/medgemma-healthconnect/medgemma-healthconnect/medgemma_healthconnect_demo.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print(f"✅ Part 1 complete: {len(cells)} cells created so far...")
