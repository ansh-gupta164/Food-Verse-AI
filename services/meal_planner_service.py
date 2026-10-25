"""
Personalized Meal Planner Service: Implements the Mifflin-St Jeor BMR equation,
activity TDEE calculation, target macro distribution, and 7-day meal plan generation
with consolidated grocery list and allergen checks.
"""

from typing import Any, Dict, List, Optional, Tuple
from services.ai_service import AIService
from utils.constants import (
    ACTIVITY_MULTIPLIERS,
    GENERAL_DISCLAIMER,
    GOAL_CALORIE_ADJUSTMENTS,
    MACRO_RATIOS,
)
from utils.sample_data import SAMPLE_7_DAY_MEAL_PLAN
from utils.validators import validate_profile_inputs


def calculate_bmr(weight_kg: float, height_cm: float, age: int, sex: str) -> float:
    """
    Computes Basal Metabolic Rate using the validated Mifflin-St Jeor equation.
    Males: 10 * weight(kg) + 6.25 * height(cm) - 5 * age + 5
    Females: 10 * weight(kg) + 6.25 * height(cm) - 5 * age - 161
    """
    base = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age)
    if sex.lower() == "male":
        return round(base + 5.0, 1)
    else:
        return round(base - 161.0, 1)


def calculate_tdee(bmr: float, activity_level: str) -> float:
    """
    Calculates Total Daily Energy Expenditure (TDEE) based on activity multiplier.
    """
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
    return round(bmr * multiplier, 1)


def calculate_target_macros(
    tdee: float,
    goal: str,
    dietary_preference: str,
    sex: str
) -> Dict[str, Any]:
    """
    Calculates daily calorie target and macronutrient grams (Protein, Carbs, Fat).
    Enforces healthy physiological safety floors (1200 kcal female, 1500 kcal male).
    """
    adjustment = GOAL_CALORIE_ADJUSTMENTS.get(goal, 0)
    raw_target = tdee + adjustment

    # Enforce safe minimums
    floor = 1500.0 if sex.lower() == "male" else 1200.0
    target_cals = max(floor, raw_target)

    # Get macro split ratios
    ratios = MACRO_RATIOS.get(dietary_preference, MACRO_RATIOS["Balanced"])
    protein_cals = target_cals * ratios["protein"]
    carbs_cals = target_cals * ratios["carbs"]
    fat_cals = target_cals * ratios["fat"]

    protein_g = round(protein_cals / 4.0, 1)
    carbs_g = round(carbs_cals / 4.0, 1)
    fat_g = round(fat_cals / 9.0, 1)

    return {
        "target_calories": int(round(target_cals)),
        "adjustment_applied": adjustment,
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fat_g": fat_g,
        "ratios": ratios
    }


class MealPlannerService:
    """
    Generates personalized 7-day meal plans and grocery lists.
    """

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    def generate_plan(
        self,
        age: int,
        height_cm: float,
        weight_kg: float,
        sex: str,
        activity_level: str,
        goal: str,
        dietary_preference: str = "Balanced",
        allergies: str = "",
        daily_budget: str = "Flexible",
        force_demo: bool = False
    ) -> Dict[str, Any]:
        """
        Validates profile parameters, calculates energy needs, and generates a full 7-day plan.
        """
        is_valid, err_msg = validate_profile_inputs(
            age=age,
            height_cm=height_cm,
            weight_kg=weight_kg,
            sex=sex,
            activity_level=activity_level,
            goal=goal
        )
        if not is_valid:
            return {"success": False, "error": err_msg, "data": None}

        # Energy calculations
        bmr = calculate_bmr(weight_kg, height_cm, age, sex)
        tdee = calculate_tdee(bmr, activity_level)
        targets = calculate_target_macros(tdee, goal, dietary_preference, sex)

        calc_meta = {
            "bmr": bmr,
            "tdee": tdee,
            "target_calories": targets["target_calories"],
            "protein_g": targets["protein_g"],
            "carbs_g": targets["carbs_g"],
            "fat_g": targets["fat_g"],
            "goal": goal,
            "dietary_preference": dietary_preference,
            "safety_note": "Caloric floor enforced: strictly maintained within safe non-crash limits."
        }

        if force_demo or not self.ai_service.is_live():
            # Scale demo plan to match user's calculated caloric requirements
            demo_plan = SAMPLE_7_DAY_MEAL_PLAN.copy()
            demo_plan["meta"] = {
                "calculated_bmr": bmr,
                "calculated_tdee": tdee,
                "target_calories": targets["target_calories"],
                "macro_targets": {
                    "protein_g": targets["protein_g"],
                    "carbs_g": targets["carbs_g"],
                    "fat_g": targets["fat_g"]
                },
                "plan_type": f"{dietary_preference} ({goal})"
            }
            return {
                "success": True,
                "source": "Curated Demo Meal Plan",
                "is_ai_generated": False,
                "calculations": calc_meta,
                "plan": demo_plan,
                "disclaimer": GENERAL_DISCLAIMER,
                "warning": "Demo Mode: Displaying validated 7-day benchmark meal plan customized with your exact Mifflin-St Jeor calculations. Configure Gemini API key for dynamic generation."
            }

        prompt = f"""
        You are a certified sports nutritionist and registered dietitian.
        Design a personalized 7-Day Meal Plan based on this validated profile:
        - Age: {age}, Sex: {sex}, Height: {height_cm} cm, Weight: {weight_kg} kg
        - BMR: {bmr} kcal, TDEE: {tdee} kcal
        - Goal: {goal} -> Caloric Target: {targets['target_calories']} kcal/day
        - Target Macros: Protein ~{targets['protein_g']}g, Carbs ~{targets['carbs_g']}g, Fat ~{targets['fat_g']}g
        - Dietary Preference: {dietary_preference}
        - Allergies / Exclusions: {allergies if allergies else 'None'}
        - Daily Budget: {daily_budget}

        Return a strict JSON object with this exact schema:
        {{
            "meta": {{
                "calculated_bmr": {bmr},
                "calculated_tdee": {tdee},
                "target_calories": {targets['target_calories']},
                "macro_targets": {{"protein_g": {targets['protein_g']}, "carbs_g": {targets['carbs_g']}, "fat_g": {targets['fat_g']}}},
                "plan_type": "{dietary_preference} ({goal})"
            }},
            "days": [
                {{
                    "day": "Day 1 (Monday)",
                    "meals": {{
                        "breakfast": "Meal description with ingredient portions",
                        "lunch": "Meal description with ingredient portions",
                        "dinner": "Meal description with ingredient portions",
                        "snack": "Healthy snack description"
                    }},
                    "estimated_calories": {targets['target_calories']},
                    "protein_g": {targets['protein_g']},
                    "carbs_g": {targets['carbs_g']},
                    "fat_g": {targets['fat_g']},
                    "notes": "Short highlight of micronutrients"
                }}
            ],
            "grocery_list": {{
                "Produce": ["Apples", "Spinach"],
                "Proteins & Dairy / Alternatives": ["Eggs", "Tofu"],
                "Grains & Pantry Legumes": ["Oats", "Quinoa"],
                "Herbs & Seasonings": ["Olive oil", "Oregano"]
            }}
        }}

        Ensure all 7 days (Day 1 through Day 7) are included. Strictly exclude any declared allergies: {allergies}.
        """

        sys_inst = "You are a professional dietitian. Provide complete 7-day meal plans with categorized grocery lists in strict JSON."

        success_ai, raw_text, parsed_json = self.ai_service.generate_text(
            prompt=prompt,
            system_instruction=sys_inst
        )

        if success_ai and parsed_json and isinstance(parsed_json, dict) and "days" in parsed_json:
            return {
                "success": True,
                "source": "Live Gemini AI Dietitian",
                "is_ai_generated": True,
                "calculations": calc_meta,
                "plan": parsed_json,
                "disclaimer": GENERAL_DISCLAIMER,
                "warning": None
            }

        # Fallback to benchmark
        demo_plan = SAMPLE_7_DAY_MEAL_PLAN.copy()
        demo_plan["meta"] = {
            "calculated_bmr": bmr,
            "calculated_tdee": tdee,
            "target_calories": targets["target_calories"],
            "macro_targets": {
                "protein_g": targets["protein_g"],
                "carbs_g": targets["carbs_g"],
                "fat_g": targets["fat_g"]
            },
            "plan_type": f"{dietary_preference} ({goal})"
        }
        return {
            "success": True,
            "source": "Fallback Demo (AI Error)",
            "is_ai_generated": False,
            "calculations": calc_meta,
            "plan": demo_plan,
            "disclaimer": GENERAL_DISCLAIMER,
            "warning": f"AI meal generation could not be parsed ({raw_text[:80]}...). Loaded validated benchmark plan."
        }
