"""
Validation utilities for inputs, uploaded files, and AI JSON responses.
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple


def validate_uploaded_file(file_name: str, file_size_bytes: int, allowed_extensions: List[str], max_size_mb: int) -> Tuple[bool, str]:
    """
    Validates uploaded file extension and size.
    """
    if not file_name:
        return False, "No file provided."

    ext = file_name.rsplit(".", 1)[-1].lower() if "." in file_name else ""
    if ext not in [e.lower() for e in allowed_extensions]:
        return False, f"Unsupported file type (.{ext}). Allowed formats: {', '.join(allowed_extensions)}."

    size_mb = file_size_bytes / (1024 * 1024)
    if size_mb > max_size_mb:
        return False, f"File size ({size_mb:.1f} MB) exceeds maximum allowed limit of {max_size_mb} MB."

    return True, ""


def validate_profile_inputs(
    age: int,
    height_cm: float,
    weight_kg: float,
    sex: str,
    activity_level: str,
    goal: str
) -> Tuple[bool, str]:
    """
    Validates user physiological profile parameters for BMR and TDEE calculations.
    """
    if not (12 <= age <= 120):
        return False, "Age must be between 12 and 120 years."

    if not (80.0 <= height_cm <= 250.0):
        return False, "Height must be between 80 cm and 250 cm."

    if not (30.0 <= weight_kg <= 300.0):
        return False, "Weight must be between 30 kg and 300 kg."

    if sex not in ["Male", "Female"]:
        return False, "Sex must be 'Male' or 'Female' for the Mifflin-St Jeor equation."

    if not activity_level:
        return False, "Please select an activity level."

    if not goal:
        return False, "Please select a primary goal."

    return True, ""


def validate_recipe_inputs(ingredients: str, max_time_min: int, servings: int) -> Tuple[bool, str]:
    """
    Validates user inputs for recipe generation.
    """
    cleaned = [i.strip() for i in ingredients.split(",") if i.strip()]
    if not cleaned or len(cleaned) == 0:
        return False, "Please enter at least one available ingredient."

    if max_time_min < 5 or max_time_min > 360:
        return False, "Cooking time must be between 5 and 360 minutes."

    if servings < 1 or servings > 24:
        return False, "Number of servings must be between 1 and 24."

    return True, ""


def extract_and_parse_json(text: str) -> Optional[Dict[str, Any]]:
    """
    Safely extracts and parses JSON from text, handling markdown code fences.
    """
    if not text:
        return None

    # Strip markdown code fences if present
    cleaned = text.strip()
    json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if json_match:
        cleaned = json_match.group(1).strip()
    else:
        # Check if text contains a raw JSON object
        brace_start = cleaned.find("{")
        brace_end = cleaned.rfind("}")
        if brace_start != -1 and brace_end != -1 and brace_end > brace_start:
            cleaned = cleaned[brace_start : brace_end + 1]

    try:
        return json.loads(cleaned)
    except Exception:
        return None


def calculate_health_score(
    calories: float,
    protein_g: float,
    carbs_g: float,
    fat_g: float,
    fiber_g: float
) -> Dict[str, Any]:
    """
    Calculates a transparent, rule-based Nutritional Quality Score (1-100).
    Rubric:
    - Base score: 50
    - Protein density (+15 max): Reward meals with good protein ratio (>=15g / 400kcal)
    - Fiber content (+20 max): Dietary fiber benefits digestion & satiety (>=6g is optimal)
    - Calorie density balance (+10 max): 300-650 kcal is typical healthy main meal
    - Fat balance (+10 / -10): Healthy fat ratio vs excessive saturated profile
    - Extreme carbs/sugars penalty (-15 max if carbs > 65% of calories with low fiber)
    """
    score = 50.0
    breakdown = []

    # 1. Protein density
    protein_cals = protein_g * 4
    if calories > 0:
        protein_ratio = protein_cals / calories
        if protein_ratio >= 0.20:
            score += 15
            breakdown.append("+15: High protein density (>=20% of calories)")
        elif protein_ratio >= 0.12:
            score += 10
            breakdown.append("+10: Moderate protein density (12-19% of calories)")
        else:
            score += 2
            breakdown.append("+2: Lower protein density (<12% of calories)")
    else:
        score += 5

    # 2. Dietary Fiber
    if fiber_g >= 8:
        score += 20
        breakdown.append("+20: Exceptional dietary fiber (>=8g)")
    elif fiber_g >= 5:
        score += 15
        breakdown.append("+15: Good dietary fiber (5-7g)")
    elif fiber_g >= 2:
        score += 8
        breakdown.append("+8: Moderate dietary fiber (2-4g)")
    else:
        score -= 5
        breakdown.append("-5: Very low fiber (<2g)")

    # 3. Caloric Appropriateness for typical single serving
    if 300 <= calories <= 700:
        score += 10
        breakdown.append("+10: Balanced meal energy density (300-700 kcal)")
    elif calories < 300:
        score += 5
        breakdown.append("+5: Light meal/snack portion (<300 kcal)")
    else:
        score -= 8
        breakdown.append("-8: High energy density (>700 kcal single serving)")

    # 4. Fat balance
    fat_cals = fat_g * 9
    if calories > 0:
        fat_ratio = fat_cals / calories
        if 0.15 <= fat_ratio <= 0.35:
            score += 10
            breakdown.append("+10: Balanced lipid profile (15-35% fat calories)")
        elif fat_ratio > 0.50:
            score -= 10
            breakdown.append("-10: High fat concentration (>50% fat calories)")

    # 5. Excess refined carbs check
    carbs_cals = carbs_g * 4
    if calories > 0 and (carbs_cals / calories) > 0.65 and fiber_g < 3:
        score -= 10
        breakdown.append("-10: High carbohydrate ratio with low fiber")

    # Clamping between 1 and 100
    final_score = int(max(1, min(100, round(score))))

    if final_score >= 80:
        rating = "Excellent Nutritional Quality"
        color = "#10b981"  # Emerald
    elif final_score >= 65:
        rating = "Good Balanced Choice"
        color = "#059669"  # Green
    elif final_score >= 50:
        rating = "Moderate / Average"
        color = "#f59e0b"  # Amber
    else:
        rating = "Low Nutritional Density"
        color = "#ef4444"  # Red

    return {
        "score": final_score,
        "rating": rating,
        "color": color,
        "breakdown": breakdown
    }
