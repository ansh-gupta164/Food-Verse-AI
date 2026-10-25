"""
Constants and configuration values for Food Verse AI.
"""

APP_NAME = "Food Verse AI"
APP_SUBTITLE = "Multimodal Food Intelligence Agent"
APP_VERSION = "1.0.0"

# AI Model Configuration
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
FALLBACK_GEMINI_MODEL = "gemini-1.5-flash"

# File Upload Limits
SUPPORTED_IMAGE_TYPES = ["jpg", "jpeg", "png", "webp"]
SUPPORTED_VIDEO_TYPES = ["mp4", "mov", "avi", "mkv"]
MAX_IMAGE_SIZE_MB = 10
MAX_VIDEO_SIZE_MB = 25
MAX_VIDEO_FRAMES = 5

# Harris-Benedict / Mifflin-St Jeor Activity Multipliers
ACTIVITY_MULTIPLIERS = {
    "Sedentary (desk job, little or no exercise)": 1.2,
    "Lightly Active (light exercise/sports 1-3 days/week)": 1.375,
    "Moderately Active (moderate exercise 3-5 days/week)": 1.55,
    "Very Active (hard exercise/sports 6-7 days/week)": 1.725,
    "Extra Active (intense daily exercise/physical job)": 1.9,
}

# Caloric Adjustments by Goal
GOAL_CALORIE_ADJUSTMENTS = {
    "Fat Loss (Sustainable Deficit)": -400,
    "Maintenance (Energy Balance)": 0,
    "Muscle Gain (Controlled Surplus)": 300,
}

# Macro Split Percentages (Protein, Carbs, Fat) by Dietary Preference
MACRO_RATIOS = {
    "Balanced": {"protein": 0.25, "carbs": 0.50, "fat": 0.25},
    "Vegetarian": {"protein": 0.20, "carbs": 0.55, "fat": 0.25},
    "Vegan": {"protein": 0.20, "carbs": 0.60, "fat": 0.20},
    "Keto": {"protein": 0.25, "carbs": 0.05, "fat": 0.70},
}

# Cuisines & Cooking Difficulty
SUPPORTED_CUISINES = [
    "Any Cuisine",
    "Italian",
    "Indian",
    "Mediterranean",
    "Mexican",
    "Asian / Stir-Fry",
    "American",
    "Middle Eastern",
    "Continental",
]

DIFFICULTY_LEVELS = ["Any Difficulty", "Easy (Quick & Simple)", "Intermediate", "Advanced / Gourmet"]

# Responsible Use & Educational Disclaimers
GENERAL_DISCLAIMER = (
    "Educational & Informational Purpose Only: Food Verse AI utilizes automated multimodal "
    "computer vision and nutritional estimation heuristics. Nutritional values are approximations "
    "based on visible cues and typical preparation models. Visual inspection of freshness or "
    "hygiene cannot detect invisible bacterial pathogens, toxins, temperature abuse, or microbiological "
    "safety. Always follow certified public health guidelines and consult a registered dietitian or "
    "healthcare provider for medical conditions."
)

FRESHNESS_DISCLAIMER = (
    "Safety Notice: Visual inspection cannot establish microbiological safety. Bacterial growth, "
    "enterotoxins, and chemical spoilage can occur without visible discoloration or mold. If food "
    "exhibits off-odors, improper storage history, or signs of decay, discard it immediately. "
    "When in doubt, throw it out."
)

HYGIENE_DISCLAIMER = (
    "Audit Notice: Single-frame or sampled visual hygiene analysis provides advisory observations "
    "of visible conditions only. It cannot verify continuous behaviors such as handwashing frequency, "
    "sanitizer contact time, core temperature holding, or equipment internal sanitation."
)
