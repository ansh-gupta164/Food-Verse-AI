"""
Unit tests for nutrition calculations and scoring rules.
"""

from services.ai_service import AIService
from services.nutrition_service import NutritionService
from utils.validators import calculate_health_score


def test_health_score_balanced_meal():
    # Healthy balanced salmon bowl
    result = calculate_health_score(
        calories=500.0,
        protein_g=35.0,  # 140 cals = 28% -> +15
        carbs_g=45.0,
        fat_g=18.0,      # 162 cals = 32% -> +10
        fiber_g=8.0      # >=8g -> +20
        # 500 cals -> +10
    )
    assert 1 <= result["score"] <= 100
    assert result["score"] >= 80
    assert result["rating"] == "Excellent Nutritional Quality"
    assert len(result["breakdown"]) > 0


def test_health_score_low_nutrient_density():
    # Ultra-processed sugary meal
    result = calculate_health_score(
        calories=850.0,
        protein_g=5.0,   # 20 cals = 2.3% -> +2
        carbs_g=150.0,   # high carbs
        fat_g=25.0,
        fiber_g=1.0      # low fiber -> -5
    )
    assert 1 <= result["score"] <= 100
    assert result["score"] < 50
    assert result["rating"] == "Low Nutritional Density"


def test_nutrition_service_demo_fallback():
    # With a mock AI service that is offline, verify demo fallback works cleanly
    ai_service = AIService(override_key="")
    service = NutritionService(ai_service=ai_service)
    result = service.audit_food_image(image_bytes=None, force_demo=True)

    assert result["is_ai_generated"] is False
    assert "data" in result
    assert "dish_name" in result["data"]
    assert "health_evaluation" in result
    assert result["health_evaluation"]["score"] >= 70
