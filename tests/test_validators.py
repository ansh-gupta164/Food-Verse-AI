"""
Unit tests for input validation, file uploads, and JSON parsing.
"""

from utils.validators import (
    calculate_health_score,
    extract_and_parse_json,
    validate_profile_inputs,
    validate_recipe_inputs,
    validate_uploaded_file,
)


def test_validate_uploaded_file_valid():
    is_valid, err = validate_uploaded_file("photo.jpg", 2 * 1024 * 1024, ["jpg", "png"], 10)
    assert is_valid is True
    assert err == ""


def test_validate_uploaded_file_unsupported_ext():
    is_valid, err = validate_uploaded_file("document.pdf", 500 * 1024, ["jpg", "png"], 10)
    assert is_valid is False
    assert "Unsupported file type" in err


def test_validate_uploaded_file_oversized():
    is_valid, err = validate_uploaded_file("large.png", 15 * 1024 * 1024, ["jpg", "png"], 10)
    assert is_valid is False
    assert "exceeds maximum allowed limit" in err


def test_validate_profile_inputs_valid():
    is_valid, err = validate_profile_inputs(
        age=25,
        height_cm=175.0,
        weight_kg=70.0,
        sex="Male",
        activity_level="Moderately Active",
        goal="Maintenance"
    )
    assert is_valid is True
    assert err == ""


def test_validate_profile_inputs_invalid_age():
    is_valid, err = validate_profile_inputs(
        age=5,
        height_cm=175.0,
        weight_kg=70.0,
        sex="Male",
        activity_level="Moderately Active",
        goal="Maintenance"
    )
    assert is_valid is False
    assert "Age must be between" in err


def test_validate_profile_inputs_invalid_sex():
    is_valid, err = validate_profile_inputs(
        age=25,
        height_cm=175.0,
        weight_kg=70.0,
        sex="Unknown",
        activity_level="Moderately Active",
        goal="Maintenance"
    )
    assert is_valid is False
    assert "Sex must be 'Male' or 'Female'" in err


def test_validate_recipe_inputs_empty():
    is_valid, err = validate_recipe_inputs("", 30, 2)
    assert is_valid is False
    assert "at least one available ingredient" in err


def test_validate_recipe_inputs_valid():
    is_valid, err = validate_recipe_inputs("chickpeas, spinach, tomatoes", 25, 4)
    assert is_valid is True
    assert err == ""


def test_extract_and_parse_json_raw():
    text = '{"name": "Apple", "calories": 95}'
    parsed = extract_and_parse_json(text)
    assert parsed is not None
    assert parsed["name"] == "Apple"
    assert parsed["calories"] == 95


def test_extract_and_parse_json_markdown_block():
    text = """
    Here is your recipe analysis:
    ```json
    {
        "title": "Avocado Toast",
        "prep_time": 5
    }
    ```
    Enjoy your cooking!
    """
    parsed = extract_and_parse_json(text)
    assert parsed is not None
    assert parsed["title"] == "Avocado Toast"
    assert parsed["prep_time"] == 5


def test_extract_and_parse_json_invalid():
    text = "This is plain conversational text without JSON."
    parsed = extract_and_parse_json(text)
    assert parsed is None
