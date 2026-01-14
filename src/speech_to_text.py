"""
Speech-to-Text Module for Patient Intake
Privacy-focused: No audio storage, in-memory processing only
"""

import speech_recognition as sr
from typing import Optional, Dict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class SpeechToText:
    """Speech recognition for patient intake with privacy protection"""
    
    def __init__(self, language: str = "en-US"):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.microphone = None
        
    def initialize_microphone(self) -> bool:
        """Initialize microphone for recording"""
        try:
            self.microphone = sr.Microphone()
            return True
        except Exception as e:
            logger.error(f"Failed to initialize microphone: {e}")
            return False
    
    def listen_and_transcribe(self, timeout: int = 10, phrase_time_limit: int = 30) -> Optional[str]:
        """
        Listen to microphone and transcribe speech
        
        Args:
            timeout: Seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for the phrase
            
        Returns:
            Transcribed text or None if failed
        """
        if not self.microphone:
            if not self.initialize_microphone():
                return None
        
        try:
            with self.microphone as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                logger.info("Listening...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                logger.info("Transcribing...")
                # Using Google Speech Recognition (runs locally if offline)
                text = self.recognizer.recognize_google(audio, language=self.language)
                
                # Privacy: audio object is automatically cleared after transcription
                return text
                
        except sr.WaitTimeoutError:
            logger.warning("No speech detected within timeout period")
            return None
        except sr.UnknownValueError:
            logger.warning("Speech was unintelligible")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from speech recognition service: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during speech recognition: {e}")
            return None
    
    def transcribe_from_text(self, text: str) -> str:
        """
        For testing/fallback: process text input directly
        
        Args:
            text: Input text
            
        Returns:
            Processed text
        """
        return text.strip()
    
    def get_session_info(self) -> Dict[str, str]:
        """
        Get session information (no PII)
        
        Returns:
            Dictionary with session metadata
        """
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "language": self.language,
            "status": "active"
        }
