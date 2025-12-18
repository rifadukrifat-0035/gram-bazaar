# backend/app/services/nlp_service.py
import asyncio
import re
from typing import Optional, Dict, Any

class NLPService:
    """
    A rule-based NLP service to extract intent and entities from transcribed text
    using regular expressions, tailored for the Gram-Bazaar API.
    """
    def __init__(self):
        # This regex is more robust and handles variations like "কেজি" and "টাকা"
        self.sell_intent_pattern = re.compile(
            r"(\d+)\s*কেজি\s*(\w+)\s*.*(?:প্রতি কেজি|কেজি)\s*(\d+)\s*টাকা",
            re.IGNORECASE
        )
        self.forecast_intent_pattern = re.compile(r"(\w+)\s*.*দামের পূর্বাভাস", re.IGNORECASE)

    async def extract_intent(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Asynchronously parses text to extract structured intent and entities.
        """
        print(f"NLP Service: Parsing text: '{text}'")
        await asyncio.sleep(0.1) # Simulate NLP processing time

        # Check for SELL intent first
        sell_match = self.sell_intent_pattern.search(text)
        if sell_match:
            groups = sell_match.groups()
            details = {
                "name": groups[1].lower(),          # e.g., "আলু"
                "quantity_kg": float(groups[0]),     # e.g., 50
                "price_per_kg": float(groups[2]),    # e.g., 25
            }
            return {"intent": "SELL_PRODUCT", "details": details}

        # Check for FORECAST intent
        forecast_match = self.forecast_intent_pattern.search(text)
        if forecast_match:
            details = {"crop_name": forecast_match.groups()[0].lower()}
            return {"intent": "GET_FORECAST", "details": details}

        print("NLP Service: Could not extract a valid intent.")
        return None

nlp_service = NLPService()
