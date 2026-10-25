"""
Food Verse AI: Multimodal Food Intelligence Agent
College Capstone Project for Skill Wallet
Entry point for Streamlit Web Application
"""

import io
import os
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from services.ai_service import AIService
from services.freshness_service import FreshnessService
from services.hygiene_service import HygieneService
from services.meal_planner_service import (
    MealPlannerService,
    calculate_bmr,
    calculate_target_macros,
    calculate_tdee,
)
from services.nutrition_service import NutritionService
from services.recipe_service import RecipeService
from utils.constants import (
    ACTIVITY_MULTIPLIERS,
    APP_NAME,
    APP_SUBTITLE,
    APP_VERSION,
    DIFFICULTY_LEVELS,
    FRESHNESS_DISCLAIMER,
    GENERAL_DISCLAIMER,
    GOAL_CALORIE_ADJUSTMENTS,
    HYGIENE_DISCLAIMER,
    MACRO_RATIOS,
    MAX_IMAGE_SIZE_MB,
    MAX_VIDEO_SIZE_MB,
    SUPPORTED_CUISINES,
    SUPPORTED_IMAGE_TYPES,
    SUPPORTED_VIDEO_TYPES,
)
from utils.sample_data import (
    SAMPLE_7_DAY_MEAL_PLAN,
    SAMPLE_FRESHNESS_ITEMS,
    SAMPLE_HYGIENE_REPORT,
    SAMPLE_NUTRITION_ITEMS,
    SAMPLE_RECIPES,
)
from utils.validators import (
    calculate_health_score,
    validate_profile_inputs,
    validate_recipe_inputs,
    validate_uploaded_file,
)

# ---------------------------------------------------------
# Streamlit Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title=f"{APP_NAME} | {APP_SUBTITLE}",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Custom Styling (Light Theme, Modern Emerald Accents)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Global font & container adjustments */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Top banner */
    .hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%);
        padding: 2.2rem 2.4rem;
        border-radius: 16px;
        color: #ffffff;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.2);
    }
    .hero-banner h1 {
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
        color: #ffffff !important;
    }
    .hero-banner p {
        font-size: 1.1rem;
        margin-top: 0.4rem;
        margin-bottom: 0;
        color: #a7f3d0;
        font-weight: 500;
    }

    /* Metric & Highlight Cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px -4px rgba(0,0,0,0.06);
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 0.2rem;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0f172a;
    }

    /* Badges */
    .status-badge-live {
        display: inline-block;
        background: #ecfdf5;
        color: #065f46;
        border: 1px solid #a7f3d0;
        padding: 0.35rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
    }
    .status-badge-demo {
        display: inline-block;
        background: #fffbeb;
        color: #b45309;
        border: 1px solid #fde68a;
        padding: 0.35rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
    }

    /* Score badges */
    .score-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.6rem 1.4rem;
        border-radius: 9999px;
        font-size: 1.4rem;
        font-weight: 800;
        color: white;
    }

    /* Result containers */
    .result-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.5rem;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Disclaimer box */
    .disclaimer-box {
        background: #f8fafc;
        border-left: 4px solid #94a3b8;
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.86rem;
        color: #475569;
        margin-top: 1.5rem;
    }

    .warning-box {
        background: #fff1f2;
        border-left: 4px solid #f43f5e;
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.88rem;
        color: #9f1239;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Session State & Services Initialization
# ---------------------------------------------------------
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

# Central AI and Domain Services
ai_service = AIService(override_key=st.session_state.user_api_key)
nutrition_service = NutritionService(ai_service=ai_service)
freshness_service = FreshnessService(ai_service=ai_service)
hygiene_service = HygieneService(ai_service=ai_service)
recipe_service = RecipeService(ai_service=ai_service)
meal_planner_service = MealPlannerService(ai_service=ai_service)

# ---------------------------------------------------------
# Sidebar Navigation & Settings
# ---------------------------------------------------------
with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=400&q=80",
        caption="Food Verse AI Intelligence Engine",
        use_container_width=True,
    )
    st.title("🥗 Food Verse AI")
    st.caption(f"Version {APP_VERSION} | Capstone Edition")

    # Navigation Menu
    nav_selection = st.radio(
        "Select Module:",
        options=[
            "🏠 Dashboard & Overview",
            "🥗 1. Nutrition Audit & Recognition",
            "🍎 2. Food Freshness & Spoilage",
            "🧼 3. Kitchen Hygiene & Safety",
            "🍳 4. Smart Recipe Assistant",
            "📅 5. Personalized Meal Planner",
        ],
        index=0,
    )

    st.markdown("---")
    st.subheader("⚙️ AI Configuration")

    # API Status Card
    status_info = ai_service.get_status_info()
    if status_info["is_live"]:
        st.markdown(
            f'<div class="status-badge-live">🟢 {status_info["badge"]}</div>',
            unsafe_allow_html=True,
        )
        st.caption(status_info["status_text"])
    else:
        st.markdown(
            f'<div class="status-badge-demo">🟡 {status_info["badge"]}</div>',
            unsafe_allow_html=True,
        )
        st.caption(status_info["status_text"])

    with st.expander("🔑 Configure Gemini API Key", expanded=False):
        st.write(
            "Enter your Google Gemini API key to activate live multimodal vision. "
            "Leave blank to use verified zero-cost demo intelligence."
        )
        api_input = st.text_input(
            "Gemini API Key:",
            value=st.session_state.user_api_key,
            type="password",
            placeholder="AIzaSy...",
            help="Get your free API key at aistudio.google.com",
        )
        if st.button("Apply Key", use_container_width=True):
            st.session_state.user_api_key = api_input
            st.rerun()

        if st.session_state.user_api_key:
            if st.button("Clear Key (Return to Demo)", use_container_width=True):
                st.session_state.user_api_key = ""
                st.rerun()

    st.markdown("---")
    st.caption("College Capstone Project for Skill Wallet.")


# =========================================================
# MODULE: DASHBOARD & OVERVIEW
# =========================================================
if nav_selection == "🏠 Dashboard & Overview":
    st.markdown(
        f"""
        <div class="hero-banner">
            <h1>{APP_NAME}</h1>
            <p>{APP_SUBTITLE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        ### Welcome to the Multimodal Food Intelligence Agent
        **Food Verse AI** is an end-to-end, privacy-respecting computer vision and nutritional intelligence platform designed to 
        democratize healthy eating, culinary innovation, and commercial food safety compliance.
        """
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Modules</div>
                <div class="metric-value">5 Integrated</div>
                <div style="color: #10b981; font-size: 0.85rem; font-weight:600; margin-top:0.3rem;">Vision + Nutrition + Safety</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">AI Engine</div>
                <div class="metric-value">Gemini 2.5</div>
                <div style="color: #0284c7; font-size: 0.85rem; font-weight:600; margin-top:0.3rem;">google-genai SDK</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Zero-Cost Demo</div>
                <div class="metric-value">100% Ready</div>
                <div style="color: #f59e0b; font-size: 0.85rem; font-weight:600; margin-top:0.3rem;">Deterministic offline math</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Clinical Accuracy</div>
                <div class="metric-value">Mifflin-St Jeor</div>
                <div style="color: #8b5cf6; font-size: 0.85rem; font-weight:600; margin-top:0.3rem;">BMR / TDEE standards</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Explore the 5 Intelligence Modules")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            """
            #### 🥗 1. Food Recognition & Nutrition Audit
            Upload any food plate image or use test presets. The system performs multimodal visual identification of ingredients, 
            approximates macro breakdown (calories, protein, carbs, fat, fiber), checks for common allergens, and computes a 
            transparent rule-based Nutritional Quality Score (1–100).
            
            #### 🍎 2. Food Freshness & Spoilage Assessment
            Analyzes raw produce, dairy, and perishables for early fungal mycelium, senescence sugar spots, tissue softening, and dehydration. 
            Provides clear consumer handling advice, storage instructions, and microbiological safety disclaimers.
            
            #### 🧼 3. Kitchen Hygiene & Safety Audit
            Audits commercial and domestic food preparation environments. Evaluates PPE (hairnets, aprons, gloves), cross-contamination prevention 
            (color-coded boards), and surface sanitation with itemized HACCP corrective action plans and bounded video frame sampling.
            """
        )

    with col_b:
        st.markdown(
            """
            #### 🍳 4. Smart Kitchen Recipe Assistant
            Enter what is currently inside your refrigerator and pantry. Generates customized culinary recipes with exact ingredient quantities, 
            step-by-step instructions, dietary compliance (Vegetarian, Vegan, Keto, etc.), allergen warnings, and practical substitutions.
            
            #### 📅 5. Personalized 7-Day Meal Planner
            Calculates your exact Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) using the scientifically validated 
            Mifflin-St Jeor equations. Produces a full 7-day meal plan with daily macros, health notes, and a consolidated shopping list organized by supermarket aisle.
            """
        )

    st.markdown(
        f"""
        <div class="disclaimer-box">
            <strong>Educational & Informational Disclaimer:</strong><br>
            {GENERAL_DISCLAIMER}
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# MODULE 1: FOOD RECOGNITION AND NUTRITION AUDIT
# =========================================================
elif nav_selection == "🥗 1. Nutrition Audit & Recognition":
    st.header("🥗 Module 1: Food Recognition & Nutrition Audit")
    st.write(
        "Upload a food image to identify dishes, estimate macronutrients, check allergens, "
        "and calculate a transparent rule-based health quality score."
    )

    tab_upload, tab_presets = st.tabs(["📤 Upload Image", "🖼️ Interactive Test Presets"])

    active_image = None
    active_bytes = None
    active_mime = "image/jpeg"
    force_demo_mode = False
    chosen_preset_key = "salmon_bowl"

    with tab_upload:
        uploaded_file = st.file_uploader(
            "Upload food image (JPG, PNG, WEBP):",
            type=SUPPORTED_IMAGE_TYPES,
            key="nutri_upload",
        )
        if uploaded_file is not None:
            is_valid, err = validate_uploaded_file(
                uploaded_file.name, uploaded_file.size, SUPPORTED_IMAGE_TYPES, MAX_IMAGE_SIZE_MB
            )
            if not is_valid:
                st.error(err)
            else:
                active_bytes = uploaded_file.getvalue()
                active_image = Image.open(io.BytesIO(active_bytes))
                ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
                active_mime = f"image/{ext if ext != 'jpg' else 'jpeg'}"

    with tab_presets:
        st.write("Test immediate recognition using benchmark sample assets:")
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            if st.button("Load Preset: Mediterranean Salmon & Quinoa Bowl", use_container_width=True):
                sample_path = "assets/samples/salmon_bowl.jpg"
                if os.path.exists(sample_path):
                    active_image = Image.open(sample_path)
                    with open(sample_path, "rb") as f:
                        active_bytes = f.read()
                    active_mime = "image/jpeg"
                    chosen_preset_key = "salmon_bowl"
                    st.session_state["nutri_selected_preset"] = "salmon_bowl"
        with p_col2:
            if st.button("Load Preset: Tandoori Paneer Protein Salad", use_container_width=True):
                chosen_preset_key = "paneer_tikka_salad"
                st.session_state["nutri_selected_preset"] = "paneer_tikka_salad"
                # Generate in-memory preview
                active_image = Image.new("RGB", (600, 400), color=(255, 250, 240))
                active_bytes = None  # Will trigger curated data directly

    if "nutri_selected_preset" in st.session_state and not active_bytes:
        chosen_preset_key = st.session_state["nutri_selected_preset"]

    # Display image preview if available
    if active_image is not None:
        st.markdown("---")
        col_img, col_act = st.columns([1, 1])
        with col_img:
            st.image(active_image, caption="Active Food Image", use_container_width=True)
        with col_act:
            st.markdown("### Run Intelligence Audit")
            st.write("Click below to execute multimodal nutritional analysis:")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                run_ai = st.button("🚀 Analyze with Gemini Vision", type="primary", use_container_width=True)
            with col_b2:
                run_demo = st.button("🧪 Run Curated Benchmark Demo", use_container_width=True)

            if run_ai or run_demo:
                force_demo = run_demo or not ai_service.is_live()
                with st.spinner("Analyzing visible ingredients and estimating nutrition metrics..."):
                    result = nutrition_service.audit_food_image(
                        image_bytes=active_bytes,
                        mime_type=active_mime,
                        force_demo=force_demo,
                        sample_key=chosen_preset_key,
                    )

                st.session_state["nutri_result"] = result

    # Display Results
    if "nutri_result" in st.session_state:
        res = st.session_state["nutri_result"]
        data = res["data"]
        eval_data = res["health_evaluation"]

        st.markdown("---")
        if res["warning"]:
            st.warning(res["warning"])

        st.subheader(f"🍽️ {data.get('dish_name', 'Analyzed Meal')}")
        st.caption(f"Cuisine: **{data.get('cuisine', 'Global')}** | Portion Size: **{data.get('portion_size', '1 Serving')}** | Source: **{res['source']}**")

        # Top Macro Metrics Cards
        m_c1, m_c2, m_c3, m_c4, m_c5 = st.columns(5)
        with m_c1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Calories</div>
                    <div class="metric-value">{data.get('calories', 0):.0f} <span style="font-size:0.9rem; font-weight:500;">kcal</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m_c2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Protein</div>
                    <div class="metric-value">{data.get('protein_g', 0):.1f} <span style="font-size:0.9rem; font-weight:500;">g</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m_c3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Carbohydrates</div>
                    <div class="metric-value">{data.get('carbs_g', 0):.1f} <span style="font-size:0.9rem; font-weight:500;">g</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m_c4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Healthy Fats</div>
                    <div class="metric-value">{data.get('fat_g', 0):.1f} <span style="font-size:0.9rem; font-weight:500;">g</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m_c5:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Dietary Fiber</div>
                    <div class="metric-value">{data.get('fiber_g', 0):.1f} <span style="font-size:0.9rem; font-weight:500;">g</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Plotly Donut Chart + Health Score Breakdown
        st.markdown("<br>", unsafe_allow_html=True)
        col_chart, col_score = st.columns([1, 1])

        with col_chart:
            st.markdown("#### Macronutrient Energy Distribution")
            prot_cals = data.get("protein_g", 0) * 4
            carb_cals = data.get("carbs_g", 0) * 4
            fat_cals = data.get("fat_g", 0) * 9

            df_macros = pd.DataFrame(
                {
                    "Nutrient": ["Protein (4 kcal/g)", "Carbohydrates (4 kcal/g)", "Fats (9 kcal/g)"],
                    "Calories": [prot_cals, carb_cals, fat_cals],
                }
            )
            fig = px.pie(
                df_macros,
                values="Calories",
                names="Nutrient",
                hole=0.55,
                color_discrete_sequence=["#10b981", "#3b82f6", "#f59e0b"],
            )
            fig.update_layout(
                margin=dict(t=20, b=20, l=20, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_score:
            st.markdown("#### Rule-Based Health Quality Score")
            score_val = eval_data["score"]
            score_col = eval_data["color"]

            st.markdown(
                f"""
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.2rem; text-align: center;">
                    <div style="font-size: 0.9rem; font-weight: 600; color: #64748b; margin-bottom: 0.5rem;">NUTRITIONAL QUALITY SCORE</div>
                    <div class="score-pill" style="background-color: {score_col};">{score_val} / 100</div>
                    <div style="font-weight: 700; color: {score_col}; margin-top: 0.6rem; font-size: 1.1rem;">{eval_data['rating']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("**Transparent Scoring Rubric Breakdown:**")
            for item in eval_data["breakdown"]:
                st.write(f"• `{item}`")

        # Ingredients, Allergens & Suggestions
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("#### 🥗 Visible Ingredients Identified")
            for ing in data.get("visible_ingredients", []):
                st.write(f"• {ing}")

            st.markdown("#### ⚠️ Potential Allergens")
            allergens = data.get("allergens", [])
            if allergens:
                for a in allergens:
                    st.markdown(f"- 🔴 **{a}**")
            else:
                st.write("No major common allergens visually detected.")

        with col_right:
            st.markdown("#### 🔍 Visual Uncertainty & Estimation Limitations")
            for uncert in data.get("uncertainties", []):
                st.write(f"• *{uncert}*")

            st.markdown("#### 💡 Balanced Dietary Recommendations")
            for sug in data.get("dietary_suggestions", []):
                st.write(f"✓ {sug}")

        st.markdown(
            f"""
            <div class="disclaimer-box">
                <strong>Nutritional Estimation Disclaimer:</strong><br>
                {GENERAL_DISCLAIMER}
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# MODULE 2: FOOD FRESHNESS AND SPOILAGE ASSESSMENT
# =========================================================
elif nav_selection == "🍎 2. Food Freshness & Spoilage":
    st.header("🍎 Module 2: Food Freshness & Spoilage Assessment")
    st.write(
        "Upload images of produce, dairy, or perishables to inspect visible decay, mold, and senescence. "
        "Returns classification, confidence explanation, storage recommendations, and critical safety disclaimers."
    )

    tab_fresh_upload, tab_fresh_presets = st.tabs(["📤 Upload Food Item", "🧪 Test Freshness Presets"])

    fresh_bytes = None
    fresh_image = None
    fresh_mime = "image/jpeg"
    fresh_preset_key = "apple_fresh"

    with tab_fresh_upload:
        up_fresh = st.file_uploader(
            "Upload food image (JPG, PNG, WEBP):",
            type=SUPPORTED_IMAGE_TYPES,
            key="fresh_upload",
        )
        if up_fresh is not None:
            is_valid, err = validate_uploaded_file(
                up_fresh.name, up_fresh.size, SUPPORTED_IMAGE_TYPES, MAX_IMAGE_SIZE_MB
            )
            if not is_valid:
                st.error(err)
            else:
                fresh_bytes = up_fresh.getvalue()
                fresh_image = Image.open(io.BytesIO(fresh_bytes))
                ext = up_fresh.name.rsplit(".", 1)[-1].lower()
                fresh_mime = f"image/{ext if ext != 'jpg' else 'jpeg'}"

    with tab_fresh_presets:
        st.write("Select a curated benchmark item with verified physical traits:")
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            if st.button("Preset: Fresh Apple", use_container_width=True):
                path = "assets/samples/apple_fresh.jpg"
                if os.path.exists(path):
                    fresh_image = Image.open(path)
                    with open(path, "rb") as f:
                        fresh_bytes = f.read()
                    fresh_preset_key = "apple_fresh"
                    st.session_state["fresh_selected_preset"] = "apple_fresh"
        with col_p2:
            if st.button("Preset: Ripened Banana", use_container_width=True):
                path = "assets/samples/banana_spot.jpg"
                if os.path.exists(path):
                    fresh_image = Image.open(path)
                    with open(path, "rb") as f:
                        fresh_bytes = f.read()
                    fresh_preset_key = "banana_moderate"
                    st.session_state["fresh_selected_preset"] = "banana_moderate"
        with col_p3:
            if st.button("Preset: Decayed Berries", use_container_width=True):
                path = "assets/samples/strawberry_decay.jpg"
                if os.path.exists(path):
                    fresh_image = Image.open(path)
                    with open(path, "rb") as f:
                        fresh_bytes = f.read()
                    fresh_preset_key = "strawberry_spoiled"
                    st.session_state["fresh_selected_preset"] = "strawberry_spoiled"

    if "fresh_selected_preset" in st.session_state and not fresh_bytes:
        fresh_preset_key = st.session_state["fresh_selected_preset"]

    if fresh_image is not None:
        st.markdown("---")
        col_img, col_ctrl = st.columns([1, 1])
        with col_img:
            st.image(fresh_image, caption="Perishable Item Image", use_container_width=True)
        with col_ctrl:
            st.markdown("### Execute Freshness Inspection")
            st.write("Scan surface tension, epidermal discoloration, bruising, and fungal sporulation:")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                btn_ai = st.button("🚀 Analyze with Gemini Vision", type="primary", key="fresh_btn_ai", use_container_width=True)
            with col_b2:
                btn_demo = st.button("🧪 Run Curated Demo Audit", key="fresh_btn_demo", use_container_width=True)

            if btn_ai or btn_demo:
                force_demo = btn_demo or not ai_service.is_live()
                with st.spinner("Analyzing surface pigmentation and morphology..."):
                    res = freshness_service.assess_freshness(
                        image_bytes=fresh_bytes,
                        mime_type=fresh_mime,
                        force_demo=force_demo,
                        sample_key=fresh_preset_key,
                    )
                st.session_state["fresh_result"] = res

    if "fresh_result" in st.session_state:
        f_res = st.session_state["fresh_result"]
        data = f_res["data"]

        st.markdown("---")
        if f_res["warning"]:
            st.warning(f_res["warning"])

        # Classification Badge
        cls_name = data.get("classification", "Moderately Fresh")
        if cls_name == "Fresh":
            badge_color = "#10b981"
            icon = "🟢"
        elif cls_name == "Moderately Fresh":
            badge_color = "#f59e0b"
            icon = "🟡"
        else:
            badge_color = "#ef4444"
            icon = "🔴"

        st.markdown(
            f"""
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
                <div style="font-size: 0.85rem; font-weight: 700; color: #64748b; text-transform: uppercase;">PRELIMINARY CLASSIFICATION</div>
                <div style="display: flex; align-items: center; gap: 12px; margin-top: 0.5rem;">
                    <span style="font-size: 2rem;">{icon}</span>
                    <span style="font-size: 1.8rem; font-weight: 800; color: {badge_color};">{cls_name}</span>
                </div>
                <div style="color: #334155; font-size: 1rem; margin-top: 0.4rem;">
                    Identified Item: <strong>{data.get('food_item', 'Perishable')}</strong> | Category: <strong>{data.get('category', 'Produce')}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("#### 🔬 Observed Visual Indicators")
            for ind in data.get("visual_indicators", []):
                st.write(f"• {ind}")

            st.markdown("#### 🎯 Confidence & Uncertainty Assessment")
            st.info(data.get("confidence_explanation", "Visual inspection limited to surface features."))

        with col_f2:
            st.markdown("#### 📦 Recommended Storage Guidance")
            st.success(data.get("storage_guidance", "Store in clean refrigerator crisper."))

            st.markdown("#### 📋 Action Recommendation")
            st.write(data.get("action_recommendation", "Inspect thoroughly before consumption."))

        st.markdown(
            f"""
            <div class="warning-box">
                <strong>CRITICAL FOOD SAFETY NOTICE:</strong><br>
                {FRESHNESS_DISCLAIMER}
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# MODULE 3: KITCHEN HYGIENE AND FOOD SAFETY ASSESSMENT
# =========================================================
elif nav_selection == "🧼 3. Kitchen Hygiene & Safety":
    st.header("🧼 Module 3: Kitchen Hygiene & Food Safety Assessment")
    st.write(
        "Upload an image of a food preparation area or commercial kitchen (or an optional short video clip). "
        "Evaluates PPE, cross-contamination safeguards, and surface sanitation using a transparent 100-point HACCP rubric."
    )

    tab_img, tab_vid, tab_hygiene_preset = st.tabs(["📷 Upload Kitchen Image", "🎥 Upload Bounded Video", "🧪 Preset Benchmark"])

    hyg_img_bytes = None
    hyg_vid_bytes = None
    hyg_image = None
    hyg_mime = "image/jpeg"

    with tab_img:
        up_hyg = st.file_uploader(
            "Upload kitchen photo (JPG, PNG, WEBP):",
            type=SUPPORTED_IMAGE_TYPES,
            key="hyg_img_up",
        )
        if up_hyg is not None:
            is_valid, err = validate_uploaded_file(
                up_hyg.name, up_hyg.size, SUPPORTED_IMAGE_TYPES, MAX_IMAGE_SIZE_MB
            )
            if not is_valid:
                st.error(err)
            else:
                hyg_img_bytes = up_hyg.getvalue()
                hyg_image = Image.open(io.BytesIO(hyg_img_bytes))
                ext = up_hyg.name.rsplit(".", 1)[-1].lower()
                hyg_mime = f"image/{ext if ext != 'jpg' else 'jpeg'}"

    with tab_vid:
        st.write("Upload a short kitchen walkthrough video (Max 25 MB, <=60s):")
        up_vid = st.file_uploader(
            "Upload MP4 / MOV video:",
            type=SUPPORTED_VIDEO_TYPES,
            key="hyg_vid_up",
        )
        if up_vid is not None:
            is_valid, err = validate_uploaded_file(
                up_vid.name, up_vid.size, SUPPORTED_VIDEO_TYPES, MAX_VIDEO_SIZE_MB
            )
            if not is_valid:
                st.error(err)
            else:
                hyg_vid_bytes = up_vid.getvalue()
                st.video(hyg_vid_bytes)
                st.caption(f"Video uploaded: {up_vid.name} ({(len(hyg_vid_bytes)/(1024*1024)):.1f} MB)")

    with tab_hygiene_preset:
        if st.button("Load Preset: Commercial Kitchen Prep Line", use_container_width=True):
            path = "assets/samples/kitchen_prep.jpg"
            if os.path.exists(path):
                hyg_image = Image.open(path)
                with open(path, "rb") as f:
                    hyg_img_bytes = f.read()
                hyg_mime = "image/jpeg"
                st.session_state["hyg_use_preset"] = True

    if hyg_image is not None:
        st.image(hyg_image, caption="Kitchen Prep Station", use_container_width=True)

    if hyg_img_bytes is not None or hyg_vid_bytes is not None:
        st.markdown("---")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            run_h_ai = st.button("🚀 Run Multimodal AI Hygiene Audit", type="primary", use_container_width=True)
        with col_b2:
            run_h_demo = st.button("🧪 Run Curated Benchmark Audit", use_container_width=True)

        if run_h_ai or run_h_demo:
            force_demo = run_h_demo or not ai_service.is_live()
            with st.spinner("Analyzing HACCP compliance, PPE, and surface cleanliness..."):
                h_res = hygiene_service.assess_kitchen_hygiene(
                    image_bytes=hyg_img_bytes,
                    video_bytes=hyg_vid_bytes,
                    mime_type=hyg_mime,
                    force_demo=force_demo,
                )
            st.session_state["hygiene_result"] = h_res

    if "hygiene_result" in st.session_state:
        h_res = st.session_state["hygiene_result"]
        h_data = h_res["data"]

        st.markdown("---")
        if h_res["warning"]:
            st.warning(h_res["warning"])

        score = h_data.get("overall_score", 80)
        rating_text = h_data.get("rating", "Standard Standard")

        if score >= 80:
            score_col = "#10b981"
        elif score >= 65:
            score_col = "#f59e0b"
        else:
            score_col = "#ef4444"

        # Overall Score Header
        col_s1, col_s2 = st.columns([1, 2])
        with col_s1:
            st.markdown(
                f"""
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.5rem; text-align: center;">
                    <div style="font-size: 0.85rem; font-weight: 700; color: #64748b;">HYGIENE COMPLIANCE SCORE</div>
                    <div class="score-pill" style="background-color: {score_col}; margin: 0.8rem auto;">{score} / 100</div>
                    <div style="font-size: 1.1rem; font-weight: 800; color: {score_col};">{rating_text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_s2:
            st.markdown("#### Executive Summary")
            st.write(h_data.get("summary", "Visual conditions inspected."))

            rubric = h_data.get("rubric_breakdown", {})
            if rubric:
                st.markdown("**Transparent Category Scores (Max 25 pts each):**")
                r_cols = st.columns(len(rubric))
                for idx, (cat_name, cat_score) in enumerate(rubric.items()):
                    with r_cols[idx]:
                        st.metric(label=cat_name, value=f"{cat_score}/25")

        # Itemized HACCP Observations
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Itemized Audit Observations & Corrective Actions")

        observations = h_data.get("observations", [])
        for i, obs in enumerate(observations):
            with st.expander(f"Observation {i+1}: {obs.get('category', 'General')} - {obs.get('observation', '')[:60]}...", expanded=True):
                col_o1, col_o2 = st.columns(2)
                with col_o1:
                    st.markdown(f"**Visual Finding:**\n{obs.get('observation', 'N/A')}")
                    st.markdown(f"**Potential Hazard / Risk:**\n{obs.get('risk', 'N/A')}")
                with col_o2:
                    st.success(f"**Recommended Action / SOP:**\n{obs.get('action', 'N/A')}")

        st.markdown(
            f"""
            <div class="disclaimer-box">
                <strong>Hygiene Audit Advisory:</strong><br>
                {HYGIENE_DISCLAIMER}
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# MODULE 4: SMART KITCHEN RECIPE ASSISTANT
# =========================================================
elif nav_selection == "🍳 4. Smart Recipe Assistant":
    st.header("🍳 Module 4: Smart Kitchen Recipe Assistant")
    st.write(
        "Enter what you have available in your pantry. Food Verse AI creates optimized recipes with exact quantities, "
        "step-by-step instructions, nutritional breakdown, allergen checks, and practical substitutions."
    )

    with st.form("recipe_form"):
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            pantry_inputs = st.text_area(
                "Available Ingredients (comma-separated):",
                value="Chickpeas, Quinoa, Spinach, Cherry Tomatoes, Garlic, Olive Oil, Lemon",
                help="List raw ingredients available in your kitchen.",
                height=100,
            )
            cuisine = st.selectbox("Preferred Cuisine:", options=SUPPORTED_CUISINES, index=1)
            diet_pref = st.selectbox(
                "Dietary Constraint:",
                options=["Balanced", "Vegetarian", "Vegan", "Keto", "High Protein", "Gluten-Free"],
                index=1,
            )

        with col_r2:
            avoid = st.text_input(
                "Ingredients or Allergens to Avoid (optional):",
                value="Peanuts, Shellfish",
                placeholder="e.g. Dairy, Cilantro, Peanuts",
            )
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                max_time = st.number_input("Max Cooking Time (mins):", min_value=10, max_value=180, value=25, step=5)
            with col_t2:
                servings = st.number_input("Number of Servings:", min_value=1, max_value=12, value=2, step=1)

            diff = st.selectbox("Difficulty Level:", options=DIFFICULTY_LEVELS, index=1)

        submitted = st.form_submit_button("🍳 Generate Customized Recipe", type="primary", use_container_width=True)

    if submitted:
        with st.spinner("Formulating chef-grade recipe with balanced macronutrients..."):
            r_output = recipe_service.generate_recipe(
                available_ingredients=pantry_inputs,
                cuisine=cuisine,
                dietary_preference=diet_pref,
                max_time_minutes=int(max_time),
                difficulty=diff,
                servings=int(servings),
                avoid_ingredients=avoid,
                force_demo=not ai_service.is_live(),
            )
        st.session_state["recipe_result"] = r_output

    if "recipe_result" in st.session_state:
        rec_res = st.session_state["recipe_result"]
        if not rec_res.get("success"):
            st.error(rec_res.get("error", "Recipe generation failed."))
        else:
            r = rec_res["data"]
            if rec_res.get("warning"):
                st.warning(rec_res["warning"])

            st.markdown("---")
            st.markdown(f"## 🍽️ {r.get('title', 'Chef Creation')}")
            st.markdown(f"*{r.get('description', '')}*")

            # Quick specs
            st.caption(
                f"⏱️ Prep: **{r.get('prep_time_minutes', 10)}m** | "
                f"🍳 Cook: **{r.get('cook_time_minutes', 15)}m** | "
                f"👥 Servings: **{r.get('servings', 2)}** | "
                f"🌍 Cuisine: **{r.get('cuisine', 'Global')}** | "
                f"🏷️ Difficulty: **{r.get('difficulty', 'Easy')}**"
            )

            # Nutrition Cards
            nut = r.get("approx_nutrition_per_serving", {})
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.metric("Calories", f"{nut.get('calories', 0)} kcal")
            with c2:
                st.metric("Protein", f"{nut.get('protein_g', 0)} g")
            with c3:
                st.metric("Carbs", f"{nut.get('carbs_g', 0)} g")
            with c4:
                st.metric("Fat", f"{nut.get('fat_g', 0)} g")
            with c5:
                st.metric("Fiber", f"{nut.get('fiber_g', 0)} g")

            # Ingredients and Instructions
            col_ing, col_inst = st.columns([1, 1.2])
            with col_ing:
                st.markdown("### 🛒 Ingredients & Exact Quantities")
                for item in r.get("ingredients", []):
                    if isinstance(item, dict):
                        st.write(f"• **{item.get('item', '')}**: {item.get('quantity', '')}")
                    else:
                        st.write(f"• {item}")

                st.markdown("### 🔄 Smart Substitutions")
                for sub in r.get("substitutions", []):
                    st.write(f"✓ {sub}")

            with col_inst:
                st.markdown("### 👨‍🍳 Step-by-Step Instructions")
                for step in r.get("instructions", []):
                    st.markdown(f"{step}")

                st.markdown("### 🛡️ Food Safety & Prep Precaution")
                st.info(r.get("food_safety_tips", "Wash hands and check internal temperature before serving."))


# =========================================================
# MODULE 5: PERSONALIZED MEAL PLANNER
# =========================================================
elif nav_selection == "📅 5. Personalized Meal Planner":
    st.header("📅 Module 5: Personalized 7-Day Meal Planner")
    st.write(
        "Calculate your scientifically verified Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) "
        "using the Mifflin-St Jeor formula, then generate an aligned 7-day meal plan with consolidated grocery list."
    )

    with st.form("meal_planner_form"):
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            age = st.number_input("Age (Years):", min_value=12, max_value=120, value=25, step=1)
            sex = st.selectbox("Biological Sex (required for Mifflin-St Jeor formula):", options=["Male", "Female"], index=0)
            height_cm = st.number_input("Height (cm):", min_value=80.0, max_value=250.0, value=175.0, step=0.5)
            weight_kg = st.number_input("Weight (kg):", min_value=30.0, max_value=300.0, value=72.0, step=0.5)

        with col_p2:
            activity = st.selectbox("Activity Level:", options=list(ACTIVITY_MULTIPLIERS.keys()), index=2)
            goal = st.selectbox("Primary Physiological Goal:", options=list(GOAL_CALORIE_ADJUSTMENTS.keys()), index=0)
            diet_type = st.selectbox("Dietary Preference:", options=["Balanced", "Vegetarian", "Vegan", "Keto"], index=0)
            allergies = st.text_input("Allergies & Intolerances (e.g., Peanuts, Lactose):", value="None")
            budget = st.selectbox("Daily Food Budget:", options=["Economic / Student Friendly", "Moderate / Standard", "Gourmet / Premium"], index=1)

        generate_plan_btn = st.form_submit_button("📅 Calculate Energy & Generate 7-Day Plan", type="primary", use_container_width=True)

    if generate_plan_btn:
        with st.spinner("Computing Mifflin-St Jeor metabolic requirements & formulating 7-day schedule..."):
            p_output = meal_planner_service.generate_plan(
                age=int(age),
                height_cm=float(height_cm),
                weight_kg=float(weight_kg),
                sex=sex,
                activity_level=activity,
                goal=goal,
                dietary_preference=diet_type,
                allergies=allergies,
                daily_budget=budget,
                force_demo=not ai_service.is_live(),
            )
        st.session_state["plan_result"] = p_output

    if "plan_result" in st.session_state:
        plan_res = st.session_state["plan_result"]
        if not plan_res.get("success"):
            st.error(plan_res.get("error", "Failed to calculate plan."))
        else:
            calc = plan_res["calculations"]
            plan_obj = plan_res["plan"]

            if plan_res.get("warning"):
                st.warning(plan_res["warning"])

            st.markdown("---")
            st.markdown("### 🧮 Metabolic Profile (Mifflin-St Jeor Equation)")

            # Explanation of the math
            st.markdown(
                f"""
                - **Mifflin-St Jeor BMR Equation**: `BMR = 10 × weight (kg) + 6.25 × height (cm) - 5 × age {'+ 5' if sex == 'Male' else '- 161'}`
                - **Calculated Basal Metabolic Rate (BMR)**: **{calc['bmr']:.1f} kcal/day**
                - **Estimated Maintenance (TDEE)**: **{calc['tdee']:.1f} kcal/day** (Activity Multiplier applied)
                - **Caloric Goal Adjustment**: **{calc['target_calories']} kcal/day** (*{calc['goal']}*)
                """
            )

            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("Daily Calorie Target", f"{calc['target_calories']} kcal")
            with col_m2:
                st.metric("Target Protein", f"{calc['protein_g']} g (~{(calc['protein_g']*4/calc['target_calories']*100):.0f}%)")
            with col_m3:
                st.metric("Target Carbs", f"{calc['carbs_g']} g (~{(calc['carbs_g']*4/calc['target_calories']*100):.0f}%)")
            with col_m4:
                st.metric("Target Fats", f"{calc['fat_g']} g (~{(calc['fat_g']*9/calc['target_calories']*100):.0f}%)")

            st.markdown("---")
            st.markdown("### 🗓️ Complete 7-Day Meal Schedule")

            days_list = plan_obj.get("days", [])
            for day_info in days_list:
                day_title = day_info.get("day", "Day")
                day_cals = day_info.get("estimated_calories", calc["target_calories"])
                day_p = day_info.get("protein_g", calc["protein_g"])
                day_c = day_info.get("carbs_g", calc["carbs_g"])
                day_f = day_info.get("fat_g", calc["fat_g"])

                with st.expander(f"📍 {day_title} — {day_cals} kcal (P: {day_p}g | C: {day_c}g | F: {day_f}g)", expanded=False):
                    meals = day_info.get("meals", {})
                    st.markdown(f"**🍳 Breakfast:** {meals.get('breakfast', 'N/A')}")
                    st.markdown(f"**🥗 Lunch:** {meals.get('lunch', 'N/A')}")
                    st.markdown(f"**🍲 Dinner:** {meals.get('dinner', 'N/A')}")
                    st.markdown(f"**🍎 Snack:** {meals.get('snack', 'N/A')}")
                    if "notes" in day_info and day_info["notes"]:
                        st.caption(f"💡 *{day_info['notes']}*")

            # Consolidated Grocery List
            st.markdown("---")
            st.markdown("### 🛒 Consolidated 7-Day Grocery List (Organized by Supermarket Aisle)")

            grocery = plan_obj.get("grocery_list", {})
            g_cols = st.columns(len(grocery) if grocery else 1)
            for idx, (category, items) in enumerate(grocery.items()):
                with g_cols[idx]:
                    st.markdown(f"#### {category}")
                    for it in items:
                        st.write(f"• {it}")

            st.markdown(
                f"""
                <div class="disclaimer-box">
                    <strong>Dietary Planning Disclaimer:</strong><br>
                    {GENERAL_DISCLAIMER}
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 1.5rem 0;">
        <strong>Food Verse AI: Multimodal Food Intelligence Agent</strong> • Skill Wallet College Capstone Project<br>
        Built with Streamlit, Google Gemini AI (google-genai SDK), Pillow, Pandas, and Plotly.
    </div>
    """,
    unsafe_allow_html=True,
)
