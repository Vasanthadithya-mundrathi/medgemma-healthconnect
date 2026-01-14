"""
Basic tests for MedGemma HealthConnect modules
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from speech_to_text import SpeechToText
from privacy_manager import PrivacyManager
from clinical_trial_matcher import ClinicalTrialMatcher


def test_speech_to_text_initialization():
    """Test speech-to-text module initialization"""
    stt = SpeechToText()
    assert stt.language == "en-US"
    print("✅ SpeechToText initialization: PASSED")


def test_speech_to_text_text_input():
    """Test text input fallback"""
    stt = SpeechToText()
    text = "I have a headache and fever"
    result = stt.transcribe_from_text(text)
    assert result == text
    print("✅ SpeechToText text input: PASSED")


def test_privacy_manager_session():
    """Test privacy manager session creation"""
    pm = PrivacyManager(session_timeout=60)
    session_id = pm.create_session()
    assert session_id is not None
    assert pm.validate_session(session_id)
    print("✅ PrivacyManager session creation: PASSED")


def test_privacy_manager_expiration():
    """Test session expiration"""
    pm = PrivacyManager(session_timeout=60)
    session_id = pm.create_session()
    pm.end_session(session_id)
    assert not pm.validate_session(session_id)
    print("✅ PrivacyManager session expiration: PASSED")


def test_privacy_manager_hash():
    """Test data hashing"""
    pm = PrivacyManager()
    data = "sensitive patient information"
    hash1 = pm.hash_data(data)
    hash2 = pm.hash_data(data)
    assert hash1 == hash2  # Same input produces same hash
    assert len(hash1) == 64  # SHA-256 produces 64 character hex string
    print("✅ PrivacyManager data hashing: PASSED")


def test_clinical_trial_matcher_database():
    """Test clinical trial matcher database loading"""
    matcher = ClinicalTrialMatcher()
    success = matcher.load_trials_database()
    assert success
    assert len(matcher.trials_data) > 0
    print("✅ ClinicalTrialMatcher database loading: PASSED")


def test_clinical_trial_matcher_details():
    """Test getting trial details"""
    matcher = ClinicalTrialMatcher()
    matcher.load_trials_database()
    
    if matcher.trials_data:
        trial_id = matcher.trials_data[0]['trial_id']
        details = matcher.get_trial_details(trial_id)
        assert details is not None
        assert details['trial_id'] == trial_id
        print("✅ ClinicalTrialMatcher trial details: PASSED")


def test_clinical_trial_matcher_format():
    """Test trial summary formatting"""
    matcher = ClinicalTrialMatcher()
    matcher.load_trials_database()
    
    if matcher.trials_data:
        trial = matcher.trials_data[0]
        summary = matcher.format_trial_summary(trial)
        assert len(summary) > 0
        assert trial['title'] in summary
        print("✅ ClinicalTrialMatcher formatting: PASSED")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Running MedGemma HealthConnect Tests")
    print("="*60 + "\n")
    
    tests = [
        test_speech_to_text_initialization,
        test_speech_to_text_text_input,
        test_privacy_manager_session,
        test_privacy_manager_expiration,
        test_privacy_manager_hash,
        test_clinical_trial_matcher_database,
        test_clinical_trial_matcher_details,
        test_clinical_trial_matcher_format,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: FAILED - {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
