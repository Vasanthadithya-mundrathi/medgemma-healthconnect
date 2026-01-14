"""
Clinical Trial Matcher Agent
Matches patient conditions with relevant clinical trials
Privacy-focused: Uses only anonymized medical summaries
"""

from typing import List, Dict, Optional
import json
import logging
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

logger = logging.getLogger(__name__)


class ClinicalTrialMatcher:
    """
    Agent for matching patient conditions with clinical trials
    Uses semantic similarity for matching
    """
    
    def __init__(self, trials_database_path: Optional[str] = None):
        self.trials_database_path = trials_database_path or "./data/clinical_trials.json"
        self.trials_data = []
        self.embedding_model = None
        self.trial_embeddings = None
        
    def load_trials_database(self) -> bool:
        """
        Load clinical trials database
        
        Returns:
            True if successful, False otherwise
        """
        try:
            trials_path = Path(self.trials_database_path)
            if not trials_path.exists():
                logger.warning(f"Trials database not found at {self.trials_database_path}")
                # Create sample database
                self._create_sample_database()
                
            with open(self.trials_database_path, 'r') as f:
                self.trials_data = json.load(f)
                
            logger.info(f"Loaded {len(self.trials_data)} clinical trials")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load trials database: {e}")
            return False
    
    def _create_sample_database(self):
        """Create sample clinical trials database"""
        sample_trials = [
            {
                "trial_id": "NCT00000001",
                "title": "Phase III Study of Novel Diabetes Treatment",
                "condition": "Type 2 Diabetes",
                "description": "Evaluating effectiveness of new diabetes medication for blood sugar control",
                "eligibility": "Adults 18-65 with Type 2 Diabetes, HbA1c > 7.5%",
                "location": "Multiple Sites",
                "status": "Recruiting"
            },
            {
                "trial_id": "NCT00000002",
                "title": "Hypertension Management Study",
                "condition": "Hypertension",
                "description": "Testing combination therapy for blood pressure control",
                "eligibility": "Adults with systolic BP > 140 mmHg",
                "location": "Multiple Sites",
                "status": "Recruiting"
            },
            {
                "trial_id": "NCT00000003",
                "title": "Chronic Pain Relief Clinical Trial",
                "condition": "Chronic Pain",
                "description": "Novel non-opioid pain management approach",
                "eligibility": "Adults with chronic pain > 6 months",
                "location": "Multiple Sites",
                "status": "Recruiting"
            },
            {
                "trial_id": "NCT00000004",
                "title": "Asthma Control Enhancement Study",
                "condition": "Asthma",
                "description": "Investigating new inhaler technology for asthma management",
                "eligibility": "Adults and children with moderate to severe asthma",
                "location": "Multiple Sites",
                "status": "Recruiting"
            },
            {
                "trial_id": "NCT00000005",
                "title": "Migraine Prevention Trial",
                "condition": "Migraine",
                "description": "Evaluating preventive medication for chronic migraine sufferers",
                "eligibility": "Adults with 4+ migraines per month",
                "location": "Multiple Sites",
                "status": "Recruiting"
            }
        ]
        
        # Ensure directory exists
        Path(self.trials_database_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.trials_database_path, 'w') as f:
            json.dump(sample_trials, f, indent=2)
        
        self.trials_data = sample_trials
    
    def load_embedding_model(self) -> bool:
        """
        Load sentence embedding model for semantic matching
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Loading embedding model for trial matching...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Pre-compute trial embeddings
            if self.trials_data:
                trial_texts = [
                    f"{trial['condition']} {trial['description']}" 
                    for trial in self.trials_data
                ]
                self.trial_embeddings = self.embedding_model.encode(trial_texts)
                
            logger.info("Embedding model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            return False
    
    def match_trials(
        self, 
        medical_summary: str, 
        top_k: int = 3,
        threshold: float = 0.3
    ) -> List[Dict]:
        """
        Match patient summary with clinical trials
        
        Args:
            medical_summary: Anonymized medical summary
            top_k: Number of top matches to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of matching trials with similarity scores
        """
        if not self.embedding_model or not self.trials_data:
            logger.error("Model or database not loaded")
            return []
        
        try:
            # Encode query (medical summary)
            query_embedding = self.embedding_model.encode([medical_summary])[0]
            
            # Calculate similarities
            similarities = np.dot(self.trial_embeddings, query_embedding)
            
            # Get top matches
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            matches = []
            for idx in top_indices:
                similarity = float(similarities[idx])
                if similarity >= threshold:
                    trial = self.trials_data[idx].copy()
                    trial['similarity_score'] = round(similarity, 3)
                    matches.append(trial)
            
            logger.info(f"Found {len(matches)} matching trials")
            return matches
            
        except Exception as e:
            logger.error(f"Failed to match trials: {e}")
            return []
    
    def get_trial_details(self, trial_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific trial
        
        Args:
            trial_id: Clinical trial ID
            
        Returns:
            Trial details or None if not found
        """
        for trial in self.trials_data:
            if trial['trial_id'] == trial_id:
                return trial
        return None
    
    def format_trial_summary(self, trial: Dict) -> str:
        """
        Format trial information for display
        
        Args:
            trial: Trial dictionary
            
        Returns:
            Formatted string
        """
        summary = f"""
**{trial['title']}**
- Trial ID: {trial['trial_id']}
- Condition: {trial['condition']}
- Status: {trial['status']}
- Description: {trial['description']}
- Eligibility: {trial['eligibility']}
- Location: {trial['location']}
"""
        if 'similarity_score' in trial:
            summary += f"- Match Score: {trial['similarity_score']:.1%}\n"
        
        return summary.strip()
