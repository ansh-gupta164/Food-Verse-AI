# 🥗 Food Verse AI: Multimodal Food Intelligence Agent

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Gemini%20AI-Multimodal-10B981.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-18%20Passed-success.svg)]()

> **Skill Wallet College Capstone Project**  
> An end-to-end, privacy-respecting Multimodal Food Intelligence Agent combining Google Gemini Vision AI, clinical metabolic calculations (Mifflin-St Jeor), commercial HACCP kitchen hygiene auditing, and culinary meal planning.

---

## 🌟 Executive Summary

**Food Verse AI** bridges the gap between everyday eating decisions, nutritional science, and commercial food safety standards. Using advanced multimodal computer vision powered by Google Gemini and deterministic fallback intelligence, the platform allows users to:

1. **Audit Food & Nutrition**: Visually recognize meals, approximate macronutrients, detect potential allergens, and compute an objective 100-point Nutritional Quality Score.
2. **Detect Perishable Spoilage**: Inspect fruits, vegetables, and dairy for early decay, mold mycelium, and senescence, accompanied by food safety disclaimers.
3. **Audit Kitchen Hygiene**: Review food prep counters, PPE compliance (hairnets, aprons, gloves), and cross-contamination safeguards using a transparent 100-point HACCP rubric.
4. **Formulate Custom Recipes**: Generate chef-crafted recipes tailored to available pantry items, dietary constraints, time limits, and allergen exclusions.
5. **Generate 7-Day Meal Plans**: Calculate exact metabolic requirements (BMR & TDEE) and generate complete weekly plans with an organized supermarket grocery list.

---

## 🏗️ System Architecture

```text
food-verse-ai/
├── .streamlit/
│   ├── config.toml               # Streamlit theme & upload configuration
│   └── secrets.toml.example      # API key secrets template for local & cloud
├── assets/
│   └── samples/                  # High-quality test image assets
├── services/
│   ├── __init__.py
│   ├── ai_service.py             # Centralized Gemini AI client (google-genai SDK)
│   ├── nutrition_service.py      # Multimodal food recognition & health scoring
│   ├── freshness_service.py      # Visual decay & spoilage assessment
│   ├── hygiene_service.py        # HACCP kitchen hygiene audit & video frame sampler
│   ├── recipe_service.py         # AI recipe creation & pantry substitutions
│   └── meal_planner_service.py   # Mifflin-St Jeor calculations & 7-day plans
├── utils/
│   ├── __init__.py
│   ├── constants.py              # Activity multipliers, ratios, disclaimers
│   ├── validators.py             # Input validation, file constraints, JSON parser
│   ├── sample_data.py            # Rich curated fallback datasets for zero-cost demo
│   └── generate_sample_images.py # Local asset generation script
├── tests/
│   ├── __init__.py
│   ├── test_nutrition.py         # Health score rubric & nutrition service tests
│   ├── test_meal_planner.py      # BMR / TDEE Mifflin-St Jeor formula tests
│   └── test_validators.py        # Upload, profile, and JSON parsing tests
├── app.py                        # Streamlit web application entrypoint
├── requirements.txt              # Pinned production dependencies
├── .gitignore                    # Git exclusion rules (secrets, venvs, caches)
└── README.md                     # Documentation & deployment guide
```

---

## 🚀 Key Features by Module

### 1. 🥗 Food Recognition & Nutrition Audit
- Multimodal image analysis (`.jpg`, `.jpeg`, `.png`, `.webp`) up to 10 MB.
- Identifies dishes, cuisines, visible ingredients, and portion size estimates.
- Calculates calories, protein, carbohydrates, fats, and dietary fiber.
- **Rule-Based Nutritional Quality Score (1–100)**: Transparent rubric based on protein density, fiber levels, calorie appropriateness, and lipid balance.
- Interactive Plotly macronutrient distribution donut chart.
- Allergen detection and uncertainty explanations.
- One-click sample presets (Mediterranean Salmon Bowl, Tandoori Paneer Salad).

### 2. 🍎 Food Freshness & Spoilage Assessment
- Identifies produce, dairy, bakery, and meat items.
- Detects surface discoloration, wrinkling, tissue collapse, and fungal mycelium.
- Preliminary classification: `Fresh`, `Moderately Fresh`, or `Potentially Spoiled`.
- Practical storage guidance (temperatures, crisper settings, ethylene separation).
- **Safety Disclaimer**: Prominently highlights that visual checks cannot rule out microscopic pathogens or temperature abuse.

### 3. 🧼 Kitchen Hygiene & Food Safety Assessment
- Visual audit of commercial and residential food preparation environments.
- Optional video frame sampling: Samples up to 5 frames using OpenCV with size and duration limits (≤60s).
- Itemized HACCP observations covering PPE, surface cleanliness, raw vs. ready-to-eat separation, and chemical storage.
- 100-point transparent compliance score (4 categories × 25 points).

### 4. 🍳 Smart Kitchen Recipe Assistant
- Input available pantry ingredients, preferred cuisine, time limit, servings, and difficulty.
- Generates precise ingredient quantities, cooking instructions, smart substitutions, per-serving nutrition, and prep precautions.
- Input validation prevents empty submissions.

### 5. 📅 Personalized 7-Day Meal Planner
- Scientifically validated **Mifflin-St Jeor Equation**:
  - **Male**: $\text{BMR} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age} + 5$
  - **Female**: $\text{BMR} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age} - 161$
- TDEE calculated via configurable activity multipliers (1.2 to 1.9).
- Goal-based caloric adjustments with non-crash physiological minimum floors (1200 kcal female / 1500 kcal male).
- Full 7-day schedule (Breakfast, Lunch, Dinner, Snack) with daily macros and notes.
- Consolidated weekly grocery shopping list organized by supermarket aisle.

---

## 💻 Local Installation & Setup

### Prerequisites
- Python 3.10 or 3.11 installed.
- Git installed.

### Windows (PowerShell) Workflow

1. **Clone the repository:**
   ```powershell
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd Food_Verse_AI
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run Unit Tests:**
   ```powershell
   pytest tests/ -v
   ```

5. **Start the Streamlit Application:**
   ```powershell
   streamlit run app.py
   ```
   The application will launch in your default browser at `http://localhost:8501`.

---

## 🔑 AI Configuration & Demo Mode

### 1. Live Gemini AI Mode (Optional)
To activate live multimodal vision with Google Gemini:
- Obtain a free API key from [Google AI Studio](https://aistudio.google.com/).
- **Option A (In-App)**: Open the sidebar, expand **"🔑 Configure Gemini API Key"**, paste your key, and click **"Apply Key"**.
- **Option B (Local Secrets)**: Create a `.streamlit/secrets.toml` file:
  ```toml
  GEMINI_API_KEY = "AIzaSy..."
  ```
- **Option C (Environment Variable)**:
  ```powershell
  $env:GEMINI_API_KEY="AIzaSy..."
  ```

### 2. Zero-Cost Demo Mode (No API Key Required)
If you do not have an API key, **Food Verse AI works 100% out of the box**:
- All modules contain curated benchmark datasets and mathematical algorithms.
- Each module provides an interactive test button (e.g., *"Run Curated Benchmark Demo"*).
- The status indicator in the sidebar will clearly display `🟡 Curated Demo Mode`.

---

## 🧪 Testing and Quality Assurance

The application includes an automated test suite verifying deterministic calculations, validators, and safety bounds:

```powershell
pytest tests/ -v
```

### Verified Test Cases (18 Passed):
- `tests/test_meal_planner.py`:
  - Male Mifflin-St Jeor equation accuracy.
  - Female Mifflin-St Jeor equation accuracy.
  - Activity multiplier TDEE calculations.
  - Caloric floor enforcement and macro distribution.
- `tests/test_nutrition.py`:
  - Rule-based Nutritional Quality Score for balanced meals.
  - Penalties for ultra-processed, low-fiber profiles.
  - Demo mode fallback structure.
- `tests/test_validators.py`:
  - File extension and size limit validation.
  - Physiological profile bounds validation.
  - Recipe pantry input non-empty checks.
  - Structured JSON parsing from raw strings and markdown code fences.

---

## 🌐 Deployment to Streamlit Community Cloud

Deploying your capstone project takes under 3 minutes:

### Step 1: Push Code to GitHub
Open Windows PowerShell in the project directory:

```powershell
# 1. Initialize Git repository
git init

# 2. Add all project files
git add .

# 3. Commit files
git commit -m "Build Food Verse AI capstone application"

# 4. Set main branch
git branch -M main

# 5. Link your remote GitHub repository
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPOSITORY_NAME>.git

# 6. Push to GitHub
git push -u origin main
```

### Step 2: Deploy on Streamlit Community Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **"New app"**.
3. Select your repository: `<YOUR_USERNAME>/<YOUR_REPOSITORY_NAME>`.
4. Branch: `main`.
5. Main file path: `app.py`.
6. *(Optional)* Click **Advanced settings...** -> **Secrets** and add:
   ```toml
   GEMINI_API_KEY = "your-live-gemini-key"
   ```
7. Click **Deploy!**
8. Streamlit will build and launch your application at a public URL (e.g. `https://food-verse-ai.streamlit.app`).

---

## 📋 Skill Wallet Final Submission Checklist

Before submitting to Skill Wallet, verify each item:

- [x] Complete, runnable Python application implemented in repository.
- [x] Streamlit web application running locally without errors.
- [x] All 5 modules functional:
  - [x] Module 1: Food Recognition & Nutrition Audit with Plotly macronutrient chart.
  - [x] Module 2: Food Freshness & Spoilage with safety disclaimers.
  - [x] Module 3: Kitchen Hygiene Audit with itemized HACCP rubric and video frame handler.
  - [x] Module 4: Smart Kitchen Recipe Assistant with ingredient validation and substitutions.
  - [x] Module 5: Personalized 7-Day Meal Planner with Mifflin-St Jeor calculations & grocery list.
- [x] Live Gemini AI integration via official `google-genai` SDK.
- [x] Complete Demo Mode functional without requiring an API key.
- [x] Automated test suite with 18 passing unit tests.
- [x] Clean `.gitignore` ensuring zero secrets or temporary files are committed.
- [x] Code pushed to public/private GitHub repository.
- [x] Application deployed to Streamlit Community Cloud.
- [x] Live public URL verified and submitted to Skill Wallet.

---

## ⚖️ Responsible Use & Medical Disclaimer

**Food Verse AI is created for educational and informational purposes only.**  
Visual food inspections and nutritional calculations are approximations based on typical culinary models and computer vision heuristics. Visual inspection cannot establish microbiological safety, detect odorless bacterial toxins, or confirm continuous sanitation practices. This application is not a substitute for professional medical advice, clinical dietary therapy, or official public health food inspections.
