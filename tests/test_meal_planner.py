"""
Unit tests for Mifflin-St Jeor equation and meal planner calculations.
"""

from services.meal_planner_service import (
    calculate_bmr,
    calculate_target_macros,
    calculate_tdee,
)


def test_bmr_male_mifflin_st_jeor():
    # 75 kg, 175 cm, 25 years old Male
    # Formula: 10 * 75 + 6.25 * 175 - 5 * 25 + 5
    # = 750 + 1093.75 - 125 + 5 = 1723.75 -> 1723.8
    bmr = calculate_bmr(weight_kg=75.0, height_cm=175.0, age=25, sex="Male")
    assert abs(bmr - 1723.8) < 0.2


def test_bmr_female_mifflin_st_jeor():
    # 60 kg, 165 cm, 28 years old Female
    # Formula: 10 * 60 + 6.25 * 165 - 5 * 28 - 161
    # = 600 + 1031.25 - 140 - 161 = 1330.25 -> 1330.2
    bmr = calculate_bmr(weight_kg=60.0, height_cm=165.0, age=28, sex="Female")
    assert abs(bmr - 1330.2) < 0.2


def test_tdee_calculation():
    bmr = 1500.0
    tdee_sedentary = calculate_tdee(bmr, "Sedentary (desk job, little or no exercise)")
    assert abs(tdee_sedentary - 1800.0) < 0.1

    tdee_moderate = calculate_tdee(bmr, "Moderately Active (moderate exercise 3-5 days/week)")
    assert abs(tdee_moderate - 2325.0) < 0.1


def test_calorie_floor_and_macro_splits():
    # Target should respect 1500 kcal minimum floor for males
    low_tdee = 1300.0
    targets = calculate_target_macros(
        tdee=low_tdee,
        goal="Fat Loss (Sustainable Deficit)",
        dietary_preference="Balanced",
        sex="Male"
    )
    assert targets["target_calories"] >= 1500
    assert targets["protein_g"] > 0
    assert targets["carbs_g"] > 0
    assert targets["fat_g"] > 0
