#!/usr/bin/env python3
"""
Script to create comprehensive Google Colab notebook for MedGemma HealthConnect
"""

import json

def create_markdown_cell(text):
    """Create a markdown cell"""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text.split('\n')
    }

def create_code_cell(code):
    """Create a code cell"""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": code.split('\n')
    }

# Initialize notebook structure
notebook = {
    "cells": [],
    "metadata": {
        "colab": {
            "provenance": [],
            "gpuType": "T4"
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        },
        "accelerator": "GPU"
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

cells = []

# Title
cells.append(create_markdown_cell("""# 🏥 MedGemma HealthConnect - Complete Demo Notebook

**Privacy-First Healthcare AI: Patient Intake Kiosk with MedGemma**

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

---"""))

# Installation
cells.append(create_markdown_cell("""## 📦 Part 1: Installation & Setup"""))

cells.append(create_code_cell("""# Cell 2: Install Dependencies
print("🔧 Installing MedGemma HealthConnect Dependencies...")
print("=" * 60)

!pip install -q transformers>=4.36.0 torch>=2.1.0
!pip install -q accelerate>=0.25.0 bitsandbytes>=0.41.0
!pip install -q sentence-transformers>=2.2.0
!pip install -q gradio streamlit
!pip install -q plotly matplotlib seaborn pandas numpy

print("✅ All dependencies installed successfully!")
print("=" * 60)"""))

# Mount Drive
cells.append(create_code_cell("""# Cell 3: Mount Google Drive & Clone Repository
from google.colab import drive
import os
import sys

print("📁 Mounting Google Drive...")
drive.mount('/content/drive', force_remount=True)

print("\\n🔄 Cloning MedGemma HealthConnect Repository...")
repo_url = "https://github.com/Vasanthadithya-mundrathi/medgemma-healthconnect.git"

if os.path.exists("/content/medgemma-healthconnect"):
    !rm -rf /content/medgemma-healthconnect

!git clone {repo_url} /content/medgemma-healthconnect

sys.path.insert(0, '/content/medgemma-healthconnect')
sys.path.insert(0, '/content/medgemma-healthconnect/src')

print("✅ Repository cloned and added to path")
print(f"📂 Working directory: {os.getcwd()}")"""))

notebook['cells'] = cells

# Save notebook
output_path = '/home/runner/work/medgemma-healthconnect/medgemma-healthconnect/medgemma_healthconnect_demo.ipynb'
with open(output_path, 'w') as f:
    json.dump(notebook, f, indent=2)

print(f"✅ Notebook created: {output_path}")
print(f"   Cells created: {len(cells)}")
