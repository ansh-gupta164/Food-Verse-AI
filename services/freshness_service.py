"""
Food Freshness & Spoilage Assessment Service: Analyzes visual indicators of degradation,
mold, bruising, and senescence with safety warnings and storage recommendations.
"""

from typing import Any, Dict, Optional
from services.ai_service import AIService
from utils.constants import FRESHNESS_DISCLAIMER
from utils.sample_data import SAMPLE_FRESHNESS_ITEMS


class FreshnessService:
    """
    Manages food freshness and spoilage visual analysis.
    """

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    def assess_freshness(
        self,
        image_bytes: Optional[bytes] = None,
        mime_type: str = "image/jpeg",
        force_demo: bool = False,
        sample_key: str = "apple_fresh"
    ) -> Dict[str, Any]:
        """
        Assesses freshness using multimodal Gemini or curated demo data.
        """
        if force_demo or not self.ai_service.is_live() or not image_bytes:
            sample = SAMPLE_FRESHNESS_ITEMS.get(sample_key, SAMPLE_FRESHNESS_ITEMS["apple_fresh"]).copy()
            return {
                "source": "Curated Demo Assessment",
                "is_ai_generated": False,
                "data": sample,
                "safety_disclaimer": FRESHNESS_DISCLAIMER,
                "warning": "Demo Mode: Displaying validated benchmark assessment. Configure Gemini API key for live analysis."
            }

        prompt = """
        You are an expert post-harvest agricultural scientist and food safety auditor.
        Examine this food item image for signs of freshness, ripening, or degradation.
        Analyze visible traits: discoloration, surface bruising, dehydration/wrinkling, liquid exudation, mycelium/mold spores, texture collapse.

        Return a strict JSON object with this exact schema:
        {
            "food_item": "Identified item (e.g. Red Gala Apple, Fresh Spinach, Raw Chicken Breast)",
            "category": "Produce / Dairy / Bakery / Raw Meat / Seafood",
            "visual_indicators": [
                "List specific visible physical characteristics observed (skin integrity, discoloration, spotting, etc.)"
            ],
            "classification": "Fresh" | "Moderately Fresh" | "Potentially Spoiled",
            "confidence_explanation": "Explanation of visual certainty and limitations (e.g., subsurface decay cannot be ruled out)",
            "storage_guidance": "Recommended temperature, humidity, and storage protocols to extend shelf-life",
            "action_recommendation": "Clear next steps (e.g., consume immediately, cook to 74C, freeze, or discard immediately)"
        }

        Safety constraints:
        1. Never classify spoiled food as safe.
        2. If mold, sliminess, or deep discoloration is visible, classify as 'Potentially Spoiled' and advise discarding.
        """

        sys_inst = "You are a food safety vision specialist. Always output valid JSON and prioritize consumer health."
        success, raw_text, parsed_json = self.ai_service.analyze_image(
            image_bytes=image_bytes,
            mime_type=mime_type,
            prompt=prompt,
            system_instruction=sys_inst
        )

        if success and parsed_json and isinstance(parsed_json, dict) and "classification" in parsed_json:
            # Enforce valid classification enum
            classification = parsed_json.get("classification", "Moderately Fresh")
            if classification not in ["Fresh", "Moderately Fresh", "Potentially Spoiled"]:
                classification = "Moderately Fresh"
                parsed_json["classification"] = classification

            return {
                "source": "Live Gemini Multimodal AI",
                "is_ai_generated": True,
                "data": parsed_json,
                "safety_disclaimer": FRESHNESS_DISCLAIMER,
                "warning": None
            }

        fallback = SAMPLE_FRESHNESS_ITEMS["apple_fresh"].copy()
        return {
            "source": "Fallback Demo (AI Error)",
            "is_ai_generated": False,
            "data": fallback,
            "safety_disclaimer": FRESHNESS_DISCLAIMER,
            "warning": f"AI vision analysis could not be completed ({raw_text[:80]}...). Displaying baseline sample."
        }
