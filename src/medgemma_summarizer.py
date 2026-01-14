"""
MedGemma Integration Module
Handles medical text summarization with edge-compatible quantization
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from typing import Optional, Dict
import logging
import os

logger = logging.getLogger(__name__)


class MedGemmaSummarizer:
    """
    MedGemma model for medical text summarization
    Supports quantization for edge deployment
    """
    
    def __init__(
        self, 
        model_name: str = "google/gemma-2b",
        quantization_bits: int = 4,
        use_flash_attention: bool = False
    ):
        self.model_name = model_name
        self.quantization_bits = quantization_bits
        self.use_flash_attention = use_flash_attention
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self) -> bool:
        """
        Load MedGemma model with quantization
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Loading model: {self.model_name}")
            logger.info(f"Device: {self.device}")
            
            # Configure quantization for edge compatibility
            if self.quantization_bits in [4, 8]:
                logger.info(f"Using {self.quantization_bits}-bit quantization")
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=(self.quantization_bits == 4),
                    load_in_8bit=(self.quantization_bits == 8),
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4"
                )
                
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    quantization_config=quantization_config,
                    device_map="auto",
                    trust_remote_code=True
                )
            else:
                # Full precision or fp16
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map="auto",
                    trust_remote_code=True
                )
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            logger.info("Model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def summarize_patient_intake(self, transcript: str, max_length: int = 512) -> Optional[str]:
        """
        Summarize patient intake transcript
        
        Args:
            transcript: Patient's spoken symptoms and concerns
            max_length: Maximum length of summary
            
        Returns:
            Medical summary or None if failed
        """
        if not self.model or not self.tokenizer:
            logger.error("Model not loaded. Call load_model() first.")
            return None
        
        try:
            # Create a medical summarization prompt
            prompt = f"""Summarize the following patient intake information into a concise medical summary. Focus on symptoms, duration, severity, and relevant medical history.

Patient Statement:
{transcript}

Medical Summary:"""
            
            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            # Generate summary (privacy: no storage, in-memory only)
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_length,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode output
            summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the generated summary part
            if "Medical Summary:" in summary:
                summary = summary.split("Medical Summary:")[-1].strip()
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate summary: {e}")
            return None
    
    def extract_medical_entities(self, text: str) -> Dict[str, list]:
        """
        Extract medical entities from text
        
        Args:
            text: Medical text
            
        Returns:
            Dictionary with extracted entities
        """
        # Simplified extraction for demo
        # In production, use specialized medical NER models
        entities = {
            "symptoms": [],
            "conditions": [],
            "medications": [],
            "duration": []
        }
        
        # Basic keyword extraction (placeholder for actual NER)
        text_lower = text.lower()
        
        # Common symptom keywords
        symptom_keywords = ["pain", "fever", "cough", "headache", "nausea", "fatigue", "dizzy"]
        for keyword in symptom_keywords:
            if keyword in text_lower:
                entities["symptoms"].append(keyword)
        
        return entities
    
    def get_model_info(self) -> Dict[str, str]:
        """
        Get model information
        
        Returns:
            Dictionary with model metadata
        """
        return {
            "model_name": self.model_name,
            "quantization": f"{self.quantization_bits}-bit",
            "device": self.device,
            "loaded": self.model is not None
        }
