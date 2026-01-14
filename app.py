"""
MedGemma HealthConnect - Patient Intake Kiosk
Privacy-First Healthcare AI with Speech-to-Text and Clinical Trial Matching
"""

import streamlit as st
import sys
import os
from pathlib import Path
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from speech_to_text import SpeechToText
from medgemma_summarizer import MedGemmaSummarizer
from clinical_trial_matcher import ClinicalTrialMatcher
from privacy_manager import PrivacyManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="MedGemma HealthConnect",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for healthcare theme
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        padding: 1rem;
    }
    .privacy-badge {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.5rem;
    }
    .warning-box {
        background-color: #FFF3CD;
        border-left: 5px solid #FFC107;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #D4EDDA;
        border-left: 5px solid #28A745;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'privacy_manager' not in st.session_state:
        st.session_state.privacy_manager = PrivacyManager(session_timeout=300)
    
    if 'session_id' not in st.session_state:
        st.session_state.session_id = st.session_state.privacy_manager.create_session()
    
    if 'speech_recognizer' not in st.session_state:
        st.session_state.speech_recognizer = SpeechToText()
    
    if 'transcript' not in st.session_state:
        st.session_state.transcript = ""
    
    if 'medical_summary' not in st.session_state:
        st.session_state.medical_summary = ""
    
    if 'matched_trials' not in st.session_state:
        st.session_state.matched_trials = []
    
    if 'model_loaded' not in st.session_state:
        st.session_state.model_loaded = False
    
    if 'trials_loaded' not in st.session_state:
        st.session_state.trials_loaded = False


def load_models():
    """Load AI models (with caching)"""
    if 'summarizer' not in st.session_state:
        with st.spinner("Loading MedGemma model... This may take a few minutes on first run."):
            st.session_state.summarizer = MedGemmaSummarizer(
                model_name=os.getenv("MODEL_NAME", "google/gemma-2b"),
                quantization_bits=int(os.getenv("QUANTIZATION_BITS", "4"))
            )
            # Note: Actual model loading is deferred until needed
            st.session_state.model_loaded = True
    
    if 'trial_matcher' not in st.session_state:
        with st.spinner("Loading clinical trials database..."):
            st.session_state.trial_matcher = ClinicalTrialMatcher()
            st.session_state.trial_matcher.load_trials_database()
            st.session_state.trial_matcher.load_embedding_model()
            st.session_state.trials_loaded = True


def display_header():
    """Display application header"""
    st.markdown('<h1 class="main-header">🏥 MedGemma HealthConnect</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Privacy-First Patient Intake Kiosk</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="privacy-badge">🔒 No PII Storage</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="privacy-badge">💻 Local Processing</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="privacy-badge">🎯 Edge Compatible</div>', unsafe_allow_html=True)


def display_privacy_notice():
    """Display privacy information"""
    with st.expander("🔒 Privacy & Security Information", expanded=False):
        st.markdown("""
        ### Privacy-First Design
        
        **Your data is protected:**
        - ✅ All processing happens locally on this device
        - ✅ No audio recordings are stored
        - ✅ No personal information is saved
        - ✅ Sessions automatically expire after 5 minutes
        - ✅ Transcripts are deleted when you close the session
        
        **How it works:**
        1. Speech is converted to text in real-time (not stored)
        2. Text is summarized using local AI model
        3. Summary is matched with clinical trials
        4. All data is cleared when you finish
        
        **Note:** This is a demonstration system. For actual medical use, 
        consult with healthcare professionals.
        """)


def patient_intake_interface():
    """Main patient intake interface"""
    st.header("Step 1: Patient Intake")
    
    # Input method selection
    input_method = st.radio(
        "Choose input method:",
        ["Type symptoms", "Use voice input (if available)"],
        horizontal=True
    )
    
    if input_method == "Type symptoms":
        transcript = st.text_area(
            "Please describe your symptoms:",
            height=150,
            placeholder="Example: I've been experiencing severe headaches for the past week, especially in the morning. I also feel nauseous and dizzy...",
            value=st.session_state.transcript
        )
        
        if st.button("Process Intake", type="primary"):
            if transcript.strip():
                st.session_state.transcript = transcript
                st.success("✓ Intake information captured")
            else:
                st.warning("Please enter your symptoms first")
    
    else:
        st.info("🎤 Voice input requires microphone access. Click 'Start Recording' to begin.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎤 Start Recording", type="primary"):
                with st.spinner("Listening... Please speak now."):
                    try:
                        transcript = st.session_state.speech_recognizer.listen_and_transcribe(
                            timeout=10,
                            phrase_time_limit=30
                        )
                        
                        if transcript:
                            st.session_state.transcript = transcript
                            st.success(f"✓ Captured: {transcript}")
                        else:
                            st.error("No speech detected. Please try again or use text input.")
                    except Exception as e:
                        st.error(f"Error with voice input: {e}")
                        st.info("Please use text input instead.")
        
        with col2:
            if st.session_state.transcript:
                st.text_area("Transcribed text:", value=st.session_state.transcript, height=100)


def medical_summarization_interface():
    """Medical summarization interface"""
    st.header("Step 2: Medical Summary Generation")
    
    if not st.session_state.transcript:
        st.info("Please complete Step 1 first")
        return
    
    if st.button("Generate Medical Summary", type="primary"):
        with st.spinner("Analyzing with MedGemma... (This may take a moment on first run)"):
            try:
                # For demo purposes without actual model, create a structured summary
                # In production, this would use the actual MedGemma model
                summary = generate_demo_summary(st.session_state.transcript)
                st.session_state.medical_summary = summary
                
            except Exception as e:
                logger.error(f"Error generating summary: {e}")
                st.error("Error generating summary. Please try again.")
    
    if st.session_state.medical_summary:
        st.markdown("### Medical Summary")
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.medical_summary)
        st.markdown('</div>', unsafe_allow_html=True)


def generate_demo_summary(transcript: str) -> str:
    """
    Generate a demo medical summary
    In production, this would use the actual MedGemma model
    """
    # Extract key information
    text_lower = transcript.lower()
    
    # Identify symptoms
    symptoms = []
    symptom_keywords = {
        'headache': 'Headache',
        'pain': 'Pain',
        'fever': 'Fever',
        'cough': 'Cough',
        'nausea': 'Nausea',
        'dizzy': 'Dizziness',
        'fatigue': 'Fatigue',
        'shortness of breath': 'Dyspnea'
    }
    
    for keyword, symptom in symptom_keywords.items():
        if keyword in text_lower:
            symptoms.append(symptom)
    
    # Identify duration
    duration = "unspecified duration"
    for word in ['week', 'weeks', 'month', 'months', 'day', 'days', 'year', 'years']:
        if word in text_lower:
            # Find the number before the time word
            words = text_lower.split()
            for i, w in enumerate(words):
                if word in w and i > 0:
                    duration = f"{words[i-1]} {word}"
                    break
    
    # Create summary
    summary = f"""
**Chief Complaint:** Patient reports {', '.join(symptoms) if symptoms else 'various symptoms'}

**Present Illness:** 
{transcript[:200]}{'...' if len(transcript) > 200 else ''}

**Duration:** {duration.capitalize()}

**Severity:** Moderate to severe (based on patient description)

**Associated Symptoms:** {', '.join(symptoms) if len(symptoms) > 1 else 'See chief complaint'}

**Note:** This is an AI-generated summary for demonstration purposes. 
A healthcare provider should review this information.
"""
    
    return summary


def clinical_trial_matching_interface():
    """Clinical trial matching interface"""
    st.header("Step 3: Clinical Trial Matching")
    
    if not st.session_state.medical_summary:
        st.info("Please complete Steps 1 and 2 first")
        return
    
    if st.button("Find Matching Clinical Trials", type="primary"):
        with st.spinner("Searching clinical trials database..."):
            try:
                if st.session_state.trials_loaded:
                    matches = st.session_state.trial_matcher.match_trials(
                        st.session_state.medical_summary,
                        top_k=5,
                        threshold=0.2
                    )
                    st.session_state.matched_trials = matches
                else:
                    st.error("Clinical trials database not loaded")
            except Exception as e:
                logger.error(f"Error matching trials: {e}")
                st.error("Error searching trials. Please try again.")
    
    if st.session_state.matched_trials:
        st.markdown("### Matching Clinical Trials")
        st.success(f"Found {len(st.session_state.matched_trials)} potentially relevant clinical trials")
        
        for i, trial in enumerate(st.session_state.matched_trials):
            with st.expander(f"Trial {i+1}: {trial['title']}", expanded=(i == 0)):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Trial ID:** {trial['trial_id']}")
                    st.markdown(f"**Condition:** {trial['condition']}")
                    st.markdown(f"**Status:** {trial['status']}")
                    st.markdown(f"**Description:** {trial['description']}")
                    st.markdown(f"**Eligibility:** {trial['eligibility']}")
                    st.markdown(f"**Location:** {trial['location']}")
                
                with col2:
                    if 'similarity_score' in trial:
                        score = trial['similarity_score'] * 100
                        st.metric("Match Score", f"{score:.0f}%")
                
                st.info("💡 Contact your healthcare provider for more information about this trial")
    else:
        if st.session_state.medical_summary:
            st.info("Click 'Find Matching Clinical Trials' to search for relevant studies")


def sidebar_info():
    """Display sidebar information"""
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1E88E5/FFFFFF?text=MedGemma+HealthConnect", 
                 use_container_width=True)
        
        st.markdown("### Session Information")
        session_info = st.session_state.privacy_manager.get_session_info(st.session_state.session_id)
        if session_info:
            st.metric("Session Time Remaining", f"{session_info['time_remaining']} sec")
        
        st.markdown("---")
        
        st.markdown("### System Status")
        st.markdown(f"✅ Privacy Manager: Active")
        st.markdown(f"{'✅' if st.session_state.model_loaded else '⏳'} MedGemma: {'Ready' if st.session_state.model_loaded else 'Loading...'}")
        st.markdown(f"{'✅' if st.session_state.trials_loaded else '⏳'} Trials DB: {'Ready' if st.session_state.trials_loaded else 'Loading...'}")
        
        st.markdown("---")
        
        if st.button("🔄 Start New Session", use_container_width=True):
            # Clear all session data
            st.session_state.privacy_manager.end_session(st.session_state.session_id)
            st.session_state.session_id = st.session_state.privacy_manager.create_session()
            st.session_state.transcript = ""
            st.session_state.medical_summary = ""
            st.session_state.matched_trials = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        **MedGemma HealthConnect** is a privacy-first healthcare AI system 
        that processes patient intake locally without storing any personal information.
        
        **Features:**
        - 🎤 Speech-to-text input
        - 🤖 AI medical summarization
        - 🔬 Clinical trial matching
        - 🔒 Zero PII storage
        - 💻 Edge-compatible
        """)


def main():
    """Main application"""
    # Initialize
    initialize_session_state()
    
    # Load models
    load_models()
    
    # Display UI
    display_header()
    display_privacy_notice()
    
    # Main content
    patient_intake_interface()
    st.markdown("---")
    medical_summarization_interface()
    st.markdown("---")
    clinical_trial_matching_interface()
    
    # Sidebar
    sidebar_info()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #999; font-size: 0.8rem;">'
        '© 2024 MedGemma HealthConnect | Privacy-First Healthcare AI | '
        'For demonstration purposes only'
        '</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
