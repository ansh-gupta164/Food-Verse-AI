"""
Smart Kitchen Recipe Assistant Service: Generates optimized culinary recipes based on
available pantry ingredients, dietary constraints, time limits, and allergen avoidance.
"""

from typing import Any, Dict, List, Optional
from services.ai_service import AIService
from utils.sample_data import SAMPLE_RECIPES
from utils.validators import validate_recipe_inputs


class RecipeService:
    """
    Manages recipe generation and ingredient substitution logic.
    """

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    def generate_recipe(
        self,
        available_ingredients: str,
        cuisine: str = "Any Cuisine",
        dietary_preference: str = "Balanced",
        max_time_minutes: int = 30,
        difficulty: str = "Easy",
        servings: int = 2,
        avoid_ingredients: str = "",
        force_demo: bool = False
    ) -> Dict[str, Any]:
        """
        Generates a tailored recipe based on user constraints.
        """
        # Validate inputs
        is_valid, err_msg = validate_recipe_inputs(available_ingredients, max_time_minutes, servings)
        if not is_valid:
            return {
                "success": False,
                "error": err_msg,
                "data": None
            }

        if force_demo or not self.ai_service.is_live():
            # Return curated recipe matching dietary preference if possible
            chosen = SAMPLE_RECIPES[0]
            if "paneer" in available_ingredients.lower() or "stir-fry" in available_ingredients.lower():
                chosen = SAMPLE_RECIPES[1]

            return {
                "success": True,
                "source": "Curated Demo Recipe",
                "is_ai_generated": False,
                "data": chosen,
                "warning": "Demo Mode: Displaying validated recipe from our curated test kitchen. Configure Gemini API key for dynamic generation."
            }

        prompt = f"""
        You are an executive chef and culinary nutrition expert.
        Create an innovative, delicious recipe utilizing the user's available pantry ingredients and dietary profile:

        - Available Ingredients: {available_ingredients}
        - Preferred Cuisine: {cuisine}
        - Dietary Constraint: {dietary_preference}
        - Maximum Total Cooking Time: {max_time_minutes} minutes
        - Difficulty Level: {difficulty}
        - Servings: {servings}
        - Ingredients/Allergens to Avoid: {avoid_ingredients if avoid_ingredients else 'None'}

        Return a strict JSON object with this exact schema:
        {{
            "title": "Inspiring Culinary Recipe Title",
            "description": "Short appetizing summary of flavor notes and textures",
            "cuisine": "{cuisine}",
            "dietary_preference": "{dietary_preference}",
            "difficulty": "{difficulty}",
            "servings": {servings},
            "prep_time_minutes": 10,
            "cook_time_minutes": 20,
            "ingredients": [
                {{"item": "Specific ingredient name", "quantity": "e.g. 200g or 1 cup"}}
            ],
            "instructions": [
                "Step 1: Specific actionable culinary instruction.",
                "Step 2: Subsequent step with precise timing and heat management."
            ],
            "substitutions": [
                "Alternative ingredient options for flexibility"
            ],
            "approx_nutrition_per_serving": {{
                "calories": 420,
                "protein_g": 25.0,
                "carbs_g": 45.0,
                "fat_g": 14.0,
                "fiber_g": 6.0
            }},
            "allergens": ["Identified allergens present in this recipe"],
            "food_safety_tips": "Crucial food safety advice regarding minimum internal cooking temperature or hygiene."
        }}
        """

        sys_inst = "You are a professional chef. Ensure the recipe strictly adheres to cooking time, dietary constraints, and ingredients to avoid."

        success_ai, raw_text, parsed_json = self.ai_service.generate_text(
            prompt=prompt,
            system_instruction=sys_inst
        )

        if success_ai and parsed_json and isinstance(parsed_json, dict) and "title" in parsed_json:
            return {
                "success": True,
                "source": "Live Gemini AI Chef",
                "is_ai_generated": True,
                "data": parsed_json,
                "warning": None
            }

        # Fallback recipe if AI parsing fails
        return {
            "success": True,
            "source": "Fallback Demo (AI Error)",
            "is_ai_generated": False,
            "data": SAMPLE_RECIPES[0],
            "warning": f"AI Chef response could not be parsed ({raw_text[:80]}...). Loaded curated recipe."
        }
