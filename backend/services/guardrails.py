import re
from config import MIN_SCORE_THRESHOLD
#Sets minimum score for retried chunks. Establish list of some most common injection wording. 
#Same for medical advice. Install verifier of presence of injection in prompt. Same for ma. 
#Check whether the most confident chunk supases confidence threshold. Function triggering both
#checks. Same for relevance validation.

class Guardrails:
    def __init__(self, min_score_threshold=MIN_SCORE_THRESHOLD):
        self.min_score_threshold = min_score_threshold

        # Prompt injection patterns
        self.injection_patterns = [
            r"ignore previous instructions",
            r"act as",
            r"system prompt",
            r"you are now",
            r"pretend to be",
            r"jailbreak"
        ]

        # Medical advice patterns
        self.medical_patterns = [
            r"should i",
            r"what should i do",
            r"recommend treatment",
            r"what treatment",
            r"diagnose",
            r"am i sick",
            r"what do i have",
            r"is this dangerous",
            r"personal advice"
        ]

    # -----------------------------
    # 1. Prompt Injection Detection
    # -----------------------------
    def is_prompt_injection(self, user_input):
        user_input_lower = user_input.lower()

        for pattern in self.injection_patterns:
            if re.search(pattern, user_input_lower):
                return True

        return False

    # -----------------------------
    # 2. Medical Advice Detection
    # -----------------------------
    def is_medical_query(self, user_input):
        user_input_lower = user_input.lower()

        for pattern in self.medical_patterns:
            if re.search(pattern, user_input_lower):
                return True

        return False

    # -----------------------------
    # 3. Retrieval Quality Check
    # -----------------------------
    def is_low_confidence(self, scores):
        """
        scores: list of FAISS similarity scores
        """
        if not scores:
            return True

        best_score = min(scores)

        return best_score > self.min_score_threshold

    # -----------------------------
    # 4. Main Guardrail Entry Point
    # -----------------------------
    def validate_input(self, user_input):
        if self.is_prompt_injection(user_input):
            return False, "Prompt injection attempt detected. Request rejected."

        if self.is_medical_query(user_input):
            return False, "I cannot provide diagnosis, treatment advice, or personalized medical recommendations."

        return True, None

    def validate_retrieval(self, scores):
        if self.is_low_confidence(scores):
            return False, "I could not find relevant information in the Omnipod 5 user guide."

        return True, None