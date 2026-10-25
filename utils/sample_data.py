"""
Curated demo datasets and fallback responses for all 5 modules.
Allows seamless demonstration and full functionality even without a Gemini API key.
"""

from typing import Any, Dict, List

# --- MODULE 1: SAMPLE NUTRITION AUDIT ---
SAMPLE_NUTRITION_ITEMS = {
    "salmon_bowl": {
        "dish_name": "Mediterranean Grilled Salmon & Quinoa Bowl",
        "cuisine": "Mediterranean",
        "portion_size": "1 regular bowl (~380 grams)",
        "calories": 540,
        "protein_g": 38.0,
        "carbs_g": 46.0,
        "fat_g": 22.0,
        "fiber_g": 8.0,
        "visible_ingredients": [
            "Pan-seared Atlantic salmon fillet",
            "Fluffy tri-color quinoa",
            "Steamed fresh broccoli florets",
            "Cherry tomato halves",
            "Diced Persian cucumber",
            "Cold-pressed extra virgin olive oil drizzle",
            "Toasted sesame seeds"
        ],
        "allergens": ["Fish (Salmon)", "Sesame"],
        "uncertainties": [
            "Exact cooking oil amount and sodium content in seasoning cannot be determined visually.",
            "Portion density estimated based on standard deep ceramic bowl geometry."
        ],
        "dietary_suggestions": [
            "Outstanding source of heart-healthy Omega-3 fatty acids (EPA/DHA) and complete lean protein.",
            "To boost iron absorption from quinoa and broccoli, squeeze fresh lemon juice over the greens.",
            "Keep sodium moderate by seasoning with dried Mediterranean herbs (oregano, thyme) instead of heavy salt."
        ]
    },
    "paneer_tikka_salad": {
        "dish_name": "Tandoori Paneer Protein Salad",
        "cuisine": "Indian / Fusion",
        "portion_size": "1 plate (~320 grams)",
        "calories": 480,
        "protein_g": 24.0,
        "carbs_g": 28.0,
        "fat_g": 32.0,
        "fiber_g": 6.5,
        "visible_ingredients": [
            "Charred spiced paneer cubes (cottage cheese)",
            "Grilled bell peppers (capsicum)",
            "Red onion petals",
            "Baby spinach & arugula base",
            "Mint coriander Greek yogurt dressing"
        ],
        "allergens": ["Dairy (Paneer, Yogurt)"],
        "uncertainties": [
            "Fat percentage of paneer (low-fat vs full cream) cannot be visually confirmed.",
            "Dressing oil-to-yogurt ratio estimated from surface sheen."
        ],
        "dietary_suggestions": [
            "High calcium and quality vegetarian protein meal with rich bioactive antioxidants from turmeric and paprika.",
            "If targeting fat loss, request low-fat paneer or substitute part of the cheese with grilled tofu."
        ]
    }
}


# --- MODULE 2: SAMPLE FRESHNESS ASSESSMENTS ---
SAMPLE_FRESHNESS_ITEMS = {
    "apple_fresh": {
        "food_item": "Red Gala Apple",
        "category": "Fresh Produce / Fruit",
        "visual_indicators": [
            "Firm, smooth, intact epidermal skin with uniform natural pigmentation.",
            "Absence of soft indentations, bruising, mold colonies, or skin punctures.",
            "Intact natural stem attached with no weeping or wrinkling around the calyx."
        ],
        "classification": "Fresh",
        "confidence_explanation": "Visual structural integrity, skin tension, and color distribution indicate prime freshness with high confidence.",
        "storage_guidance": "Store in the refrigerator crisper drawer at 1°C - 4°C to retain moisture and crispness for up to 3-4 weeks. Keep separate from ethylene-sensitive leafy greens.",
        "action_recommendation": "Optimal for fresh raw consumption, salads, or juicing. Wash under cold running water before eating."
    },
    "banana_moderate": {
        "food_item": "Cavendish Banana (Ripened)",
        "category": "Fresh Produce / Fruit",
        "visual_indicators": [
            "Golden yellow peel exhibiting prominent brown 'sugar spots' (senescence spotting).",
            "Stem is turning fibrous brown, but peel remains completely intact without deep pulp ruptures.",
            "No white, grey, or fuzzy fungal mycelium visible on stem or tip."
        ],
        "classification": "Moderately Fresh",
        "confidence_explanation": "Moderate maturity stage: starch conversion to sugars is peaked. Structurally edible, but shelf life at room temperature is short (<48 hours).",
        "storage_guidance": "Consume promptly within 1-2 days, or peel and freeze chunks in an airtight container for future smoothies and baking.",
        "action_recommendation": "Excellent for banana bread, smoothies, or oatmeal topping due to high natural sweetness."
    },
    "strawberry_spoiled": {
        "food_item": "Fresh Strawberries (Pre-packed)",
        "category": "Fresh Produce / Berries",
        "visual_indicators": [
            "Visible grey fuzzy fungal mycelium (Botrytis cinerea / grey mold) growing over multiple drupelets.",
            "Localized tissue softening, cell wall collapse, and liquid exudation.",
            "Dull, dark discoloration surrounding the mold epicenter."
        ],
        "classification": "Potentially Spoiled",
        "confidence_explanation": "Clear presence of sporulating fungal hyphae and soft decay indicates microbial breakdown of plant tissue.",
        "storage_guidance": "Do not attempt to refrigerate or salvage. Spores readily cross-contaminate adjacent berries in the container.",
        "action_recommendation": "Do not consume. Discard the affected berries and inspect neighboring fruit thoroughly for micro-spores."
    }
}


# --- MODULE 3: SAMPLE HYGIENE ASSESSMENTS ---
SAMPLE_HYGIENE_REPORT = {
    "overall_score": 82,
    "rating": "Acceptable / Good Standard",
    "summary": "The food preparation environment demonstrates good general cleanliness and active cross-contamination safeguards, with minor procedural opportunities in storage sealing and personal PPE coverage.",
    "rubric_breakdown": {
        "Surface Cleanliness & Sanitation": 22,   # max 25
        "Cross-Contamination Prevention": 23,     # max 25
        "Personal Protective Equipment (PPE)": 18, # max 25
        "Food Storage & Chemical Separation": 19  # max 25
    },
    "observations": [
        {
            "category": "Cross-Contamination Prevention",
            "observation": "Color-coded cutting boards are present on prep table (red for raw meat, green for produce).",
            "risk": "Low risk of cross-contamination if standard operating procedures are enforced.",
            "action": "Ensure knives and tongs are dedicated to specific board stations and sanitized between uses."
        },
        {
            "category": "Personal Hygiene / PPE",
            "observation": "Food handler is wearing clean apron; hair restraint is worn, but single-use gloves are not visible during ready-to-eat assembly.",
            "risk": "Moderate risk of bare-hand contact transferring transient hand microflora to ready-to-eat salads.",
            "action": "Implement strict barrier protection (tongs, deli papers, or single-use certified food-handling gloves) for ready-to-eat foods."
        },
        {
            "category": "Surface Cleanliness",
            "observation": "Stainless steel preparation counters are clean, wiped dry, and free of food debris buildup.",
            "risk": "Low microbial harboring risk on active food contact zones.",
            "action": "Maintain 2-hour sanitation cycle with verified test strips for sanitizer solution ppm."
        },
        {
            "category": "Storage & Environment",
            "observation": "One ingredient container on the upper shelf is uncovered without a date label.",
            "risk": "Risk of airborne particulate contamination and failure of First-In, First-Out (FIFO) stock rotation.",
            "action": "Cover all stored ingredients with airtight lids and affix standardized date/time labels."
        }
    ]
}


# --- MODULE 4: CURATED RECIPES ---
SAMPLE_RECIPES = [
    {
        "title": "Zesty Mediterranean Chickpea & Quinoa Skillet",
        "description": "A vibrant, plant-forward one-pan skillet bursting with roasted garlic, zesty lemon, spinach, and protein-dense chickpeas.",
        "cuisine": "Mediterranean",
        "dietary_preference": "Vegetarian",
        "difficulty": "Easy",
        "servings": 2,
        "prep_time_minutes": 10,
        "cook_time_minutes": 15,
        "ingredients": [
            {"item": "Cooked or canned chickpeas (rinsed & drained)", "quantity": "1 can (400g / 240g drained)"},
            {"item": "Pre-cooked quinoa or rice", "quantity": "1.5 cups"},
            {"item": "Baby spinach leaves", "quantity": "2 large handfuls (60g)"},
            {"item": "Cherry tomatoes (halved)", "quantity": "1 cup (150g)"},
            {"item": "Garlic cloves (minced)", "quantity": "3 cloves"},
            {"item": "Extra virgin olive oil", "quantity": "1.5 tbsp"},
            {"item": "Lemon (juiced & zested)", "quantity": "1 whole"},
            {"item": "Crumbled feta cheese (optional)", "quantity": "40g"},
            {"item": "Salt, black pepper, dried oregano", "quantity": "To taste"}
        ],
        "instructions": [
            "Warm extra virgin olive oil in a wide skillet over medium heat. Add minced garlic and sauté for 60 seconds until fragrant.",
            "Tumble in the rinsed chickpeas and halved cherry tomatoes. Sauté for 4-5 minutes until tomatoes blister lightly.",
            "Stir in the cooked quinoa, oregano, salt, and freshly ground black pepper. Toss until evenly warmed through (3 minutes).",
            "Turn off the heat, fold in fresh baby spinach and allow it to wilt gently in the residual pan heat.",
            "Finish with fresh lemon juice, lemon zest, and crumbled feta cheese. Serve warm immediately."
        ],
        "substitutions": [
            "Substitute chickpeas with cannellini beans or diced firm tofu.",
            "Substitute quinoa with brown rice, farro, or cauliflower rice for lower carbs.",
            "Omit feta or use dairy-free almond feta for a 100% vegan adaptation."
        ],
        "approx_nutrition_per_serving": {
            "calories": 410,
            "protein_g": 16.5,
            "carbs_g": 52.0,
            "fat_g": 15.0,
            "fiber_g": 11.0
        },
        "allergens": ["Dairy (if using feta)"],
        "food_safety_tips": "Ensure canned legumes are thoroughly rinsed under cold potable water to remove excess preserving brine and oligosaccharides."
    },
    {
        "title": "Crispy Garlic-Herb Paneer & Vegetable Stir-Fry",
        "description": "Golden pan-seared paneer cubes tossed with crisp bell peppers, broccoli florets, and an aromatic ginger-garlic herb glaze.",
        "cuisine": "Indian / Fusion",
        "dietary_preference": "Vegetarian",
        "difficulty": "Easy",
        "servings": 2,
        "prep_time_minutes": 12,
        "cook_time_minutes": 12,
        "ingredients": [
            {"item": "Paneer (cubed into 2cm pieces)", "quantity": "200g"},
            {"item": "Mixed bell peppers (diced)", "quantity": "1.5 cups"},
            {"item": "Broccoli florets", "quantity": "1 cup"},
            {"item": "Fresh ginger & garlic (finely grated)", "quantity": "1 tbsp each"},
            {"item": "Cold-pressed sesame or olive oil", "quantity": "1 tbsp"},
            {"item": "Low-sodium soy sauce or tamari", "quantity": "1.5 tbsp"},
            {"item": "Cracked black pepper & chili flakes", "quantity": "1 tsp"}
        ],
        "instructions": [
            "Heat half the oil in a non-stick pan over medium-high heat. Sear paneer cubes for 2-3 minutes per side until lightly golden. Set aside.",
            "In the same pan, heat the remaining oil. Sauté ginger and garlic for 30 seconds until aromatic.",
            "Toss in the broccoli florets and bell peppers. Stir-fry briskly for 4-5 minutes until crisp-tender.",
            "Return the seared paneer to the skillet. Drizzle with low-sodium soy sauce and sprinkle black pepper and chili flakes.",
            "Toss vigorously for 1 minute to coat everything in the savory glaze. Serve immediately over grains or enjoyed as is."
        ],
        "substitutions": [
            "Use extra firm tofu instead of paneer for a lactose-free or vegan option.",
            "Add button mushrooms or snap peas based on kitchen availability."
        ],
        "approx_nutrition_per_serving": {
            "calories": 375,
            "protein_g": 21.0,
            "carbs_g": 14.0,
            "fat_g": 26.0,
            "fiber_g": 4.5
        },
        "allergens": ["Dairy (Paneer)", "Soy (Soy sauce)"],
        "food_safety_tips": "Keep paneer refrigerated at <=4°C until ready for immediate cooking. Ensure center reaches hot temperature."
    }
]


# --- MODULE 5: SAMPLE 7-DAY MEAL PLAN ---
SAMPLE_7_DAY_MEAL_PLAN = {
    "meta": {
        "calculated_bmr": 1680,
        "calculated_tdee": 2352,
        "target_calories": 1950,
        "macro_targets": {"protein_g": 122, "carbs_g": 244, "fat_g": 54},
        "plan_type": "Balanced Healthy Lifestyle"
    },
    "days": [
        {
            "day": "Day 1 (Monday)",
            "meals": {
                "breakfast": "Steel-cut oatmeal (60g) cooked with almond milk, topped with 1 sliced banana, chia seeds, and a scoop of whey/plant protein.",
                "lunch": "Mediterranean grilled chicken or tofu salad bowl with quinoa, cucumber, cherry tomatoes, kalamata olives, and olive oil vinaigrette.",
                "dinner": "Pan-seared salmon or grilled paneer with roasted asparagus, sweet potato mash (150g), and steamed greens.",
                "snack": "A handful of raw almonds (25g) and 1 green apple."
            },
            "estimated_calories": 1940,
            "protein_g": 125,
            "carbs_g": 235,
            "fat_g": 52,
            "notes": "Excellent dietary fiber (>32g) supporting stable blood glucose."
        },
        {
            "day": "Day 2 (Tuesday)",
            "meals": {
                "breakfast": "Whole-grain toast (2 slices) with mashed avocado (50g), 2 poached eggs (or scrambled tofu), and baby spinach.",
                "lunch": "Spiced brown rice bowl with sautéed black beans or chickpeas, roasted bell peppers, salsa, and guacamole.",
                "dinner": "Herb-roasted turkey breast or lentil curry (dal) with steamed basmati rice and a side of cucumber raita.",
                "snack": "Greek yogurt (150g) with a drizzle of honey and mixed berries."
            },
            "estimated_calories": 1960,
            "protein_g": 120,
            "carbs_g": 245,
            "fat_g": 55,
            "notes": "High micronutrient diversity with rich folate and potassium."
        },
        {
            "day": "Day 3 (Wednesday)",
            "meals": {
                "breakfast": "Berry protein smoothie: frozen blueberries, spinach, unsweetened almond milk, protein powder, and ground flaxseed.",
                "lunch": "Whole-wheat pita pocket stuffed with falafel or grilled chicken breast, shredded lettuce, tomato, and tahini sauce.",
                "dinner": "Stir-fried tofu or lean beef with broccoli, baby corn, snap peas, and buckwheat soba noodles in ginger-soy glaze.",
                "snack": "Carrot and bell pepper sticks with 3 tbsp hummus."
            },
            "estimated_calories": 1920,
            "protein_g": 122,
            "carbs_g": 240,
            "fat_g": 51,
            "notes": "Antioxidant-dense meals targeting anti-inflammatory recovery."
        },
        {
            "day": "Day 4 (Thursday)",
            "meals": {
                "breakfast": "Cottage cheese (paneer) bowl with sliced peaches or papaya, toasted pumpkin seeds, and a sprinkle of cinnamon.",
                "lunch": "Hearty minestrone bean soup with a side toasted sourdough slice and mixed garden herb salad.",
                "dinner": "Baked white fish (cod/tilapia) or marinated tempeh with garlic-roasted green beans and herb-seasoned baby potatoes.",
                "snack": "1 boiled egg (or edamame pods, 100g) with sea salt."
            },
            "estimated_calories": 1955,
            "protein_g": 126,
            "carbs_g": 238,
            "fat_g": 53,
            "notes": "Moderate sodium, easily digestible weekday evening meals."
        },
        {
            "day": "Day 5 (Friday)",
            "meals": {
                "breakfast": "Rolled oats overnight soaked in kefir or yogurt, chia seeds, diced mango, and crushed walnuts.",
                "lunch": "Grilled vegetable and halloumi (or smoked tofu) wrap with sundried tomato tapenade and mixed greens.",
                "dinner": "One-pot chicken/chickpea vegetable stew with carrots, celery, leeks, and roasted barley.",
                "snack": "2 rice cakes with 1 tbsp peanut butter and dark chocolate nibs."
            },
            "estimated_calories": 1980,
            "protein_g": 118,
            "carbs_g": 250,
            "fat_g": 56,
            "notes": "Probiotic-rich gut microbiome support."
        },
        {
            "day": "Day 6 (Saturday)",
            "meals": {
                "breakfast": "Weekend protein pancakes (oats, banana, egg whites/flax) served with warm maple syrup and fresh strawberries.",
                "lunch": "Rainbow quinoa salad bowl with edamame, shredded red cabbage, carrots, cilantro, and peanut lime dressing.",
                "dinner": "Homemade thin-crust vegetable pizza on whole-wheat pita with mozzarella/cashew cheese, mushrooms, and basil.",
                "snack": "Air-popped popcorn (30g) lightly misted with olive oil and nutritional yeast."
            },
            "estimated_calories": 1965,
            "protein_g": 121,
            "carbs_g": 246,
            "fat_g": 54,
            "notes": "Satisfying weekend variety maintaining nutritional adherence."
        },
        {
            "day": "Day 7 (Sunday)",
            "meals": {
                "breakfast": "Mediterranean shakshuka (poached eggs in aromatic spiced tomato-pepper sauce) with crusty whole-grain bread.",
                "lunch": "Lemon herb grilled protein with roasted butternut squash, steamed green peas, and fresh mint salad.",
                "dinner": "Comforting yellow lentil soup (tadka dal) with cauliflower-cumin rice and spiced pickled cucumber.",
                "snack": "Orange slices and a small portion of mixed roasted seeds."
            },
            "estimated_calories": 1930,
            "protein_g": 124,
            "carbs_g": 236,
            "fat_g": 52,
            "notes": "Gentle restorative Sunday digestion reset."
        }
    ],
    "grocery_list": {
        "Produce": [
            "Bananas (6-7 units)",
            "Apples (4 units)",
            "Blueberries / Strawberries (2 punnets)",
            "Baby spinach (300g)",
            "Broccoli (2 heads)",
            "Cherry tomatoes (500g)",
            "Cucumbers (4 units)",
            "Avocados (2 units)",
            "Bell peppers (4 mixed colors)",
            "Carrots (500g)",
            "Lemons (4 units)",
            "Garlic & Ginger roots"
        ],
        "Proteins & Dairy / Alternatives": [
            "Eggs (1 dozen) or Tofu blocks (3 packs)",
            "Salmon fillets or Fresh Paneer (400g)",
            "Skinless chicken breasts or Tempeh (600g)",
            "Greek yogurt or Coconut yogurt (500g)",
            "Cottage cheese (250g)"
        ],
        "Grains & Pantry Legumes": [
            "Rolled or steel-cut oats (500g)",
            "Quinoa (500g)",
            "Brown rice or Basmati (500g)",
            "Canned chickpeas & black beans (4 cans)",
            "Whole-wheat pita or wraps (1 pack)",
            "Raw almonds, walnuts, chia seeds (100g each)",
            "Extra virgin olive oil",
            "Natural peanut butter"
        ],
        "Herbs & Seasonings": [
            "Dried oregano, thyme, cumin, turmeric",
            "Low-sodium soy sauce",
            "Cinnamon powder",
            "Sea salt & whole black peppercorns"
        ]
    }
}
