"""
Nutrition Audit Service: Handles multimodal food recognition, macronutrient estimation,
rule-based health score evaluation, and allergen awareness.
"""

from typing import Any, Dict, Optional, Tuple
from services.ai_service import AIService
from utils.sample_data import SAMPLE_NUTRITION_ITEMS
from utils.validators import calculate_health_score


class NutritionService:
    """
    Manages food image analysis and nutritional auditing.
    """

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    def audit_food_image(
        self,
        image_bytes: Optional[bytes] = None,
        mime_type: str = "image/jpeg",
        force_demo: bool = False,
        sample_key: str = "salmon_bowl"
    ) -> Dict[str, Any]:
        """
        Analyzes a food image using Gemini multimodal AI or curated demo data.
        """
        if force_demo or not self.ai_service.is_live() or not image_bytes:
            sample = SAMPLE_NUTRITION_ITEMS.get(sample_key, SAMPLE_NUTRITION_ITEMS["salmon_bowl"]).copy()
            health_eval = calculate_health_score(
                calories=sample["calories"],
                protein_g=sample["protein_g"],
                carbs_g=sample["carbs_g"],
                fat_g=sample["fat_g"],
                fiber_g=sample["fiber_g"]
            )
            return {
                "source": "Curated Demo Example",
                "is_ai_generated": False,
                "data": sample,
                "health_evaluation": health_eval,
                "warning": "Demo Mode: Displaying validated sample data. Configure a Gemini API key for live computer vision."
            }

        prompt = """
        You are an expert nutritional scientist and computer vision food analyst.
        Analyze this food image in detail.
        Return a strict JSON object with this exact schema:
        {
            "dish_name": "Name of the dish or meal",
            "cuisine": "Cuisine type (e.g. Mediterranean, Indian, Japanese)",
            "portion_size": "Estimated portion weight/volume (e.g. 1 plate ~350g)",
            "calories": 520,
            "protein_g": 35.0,
            "carbs_g": 45.0,
            "fat_g": 18.0,
            "fiber_g": 7.0,
            "visible_ingredients": ["list", "of", "ingredients", "identified"],
            "allergens": ["list", "of", "potential", "allergens"],
            "uncertainties": ["explanations of any uncertainty regarding hidden oils, sauces, sodium, or exact cuts"],
            "dietary_suggestions": ["practical, balanced suggestions to optimize this meal"]
        }
        Do not invent laboratory-exact precision; provide conservative realistic approximations.
        """

        sys_inst = "You are a professional nutrition intelligence agent. Always respond with valid JSON."
        success, raw_text, parsed_json = self.ai_service.analyze_image(
            image_bytes=image_bytes,
            mime_type=mime_type,
            prompt=prompt,
            system_instruction=sys_inst
        )

        if success and parsed_json and isinstance(parsed_json, dict) and "calories" in parsed_json:
            # Validate and clamp numerical fields
            try:
                calories = float(parsed_json.get("calories", 0))
                protein = float(parsed_json.get("protein_g", 0))
                carbs = float(parsed_json.get("carbs_g", 0))
                fat = float(parsed_json.get("fat_g", 0))
                fiber = float(parsed_json.get("fiber_g", 0))
            except (ValueError, TypeError):
                calories, protein, carbs, fat, fiber = 450.0, 20.0, 50.0, 15.0, 5.0

            health_eval = calculate_health_score(
                calories=calories,
                protein_g=protein,
                carbs_g=carbs,
                fat_g=fat,
                fiber_g=fiber
            )

            return {
                "source": "Live Gemini Multimodal AI",
                "is_ai_generated": True,
                "data": parsed_json,
                "health_evaluation": health_eval,
                "warning": None
            }

        # Fallback if AI response was malformed
        fallback = SAMPLE_NUTRITION_ITEMS["salmon_bowl"].copy()
        health_eval = calculate_health_score(
            calories=fallback["calories"],
            protein_g=fallback["protein_g"],
            carbs_g=fallback["carbs_g"],
            fat_g=fallback["fat_g"],
            fiber_g=fallback["fiber_g"]
        )
        return {
            "source": "Fallback Demo (AI Error)",
            "is_ai_generated": False,
            "data": fallback,
            "health_evaluation": health_eval,
            "warning": f"AI response could not be parsed ({raw_text[:80]}...). Loaded fallback sample."
        }
