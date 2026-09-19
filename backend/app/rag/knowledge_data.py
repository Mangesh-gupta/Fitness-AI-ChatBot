"""
Curated Fitness, Nutrition, and Supplement Knowledge Base
Used for RAG (Retrieval-Augmented Generation) in ChromaDB.
"""

KNOWLEDGE_DOCUMENTS = [
    {
        "id": "kb_hypertrophy_01",
        "title": "Principles of Muscle Hypertrophy & Progressive Overload",
        "category": "Workout Science",
        "tags": ["hypertrophy", "progressive_overload", "volume", "reps", "intensity"],
        "content": """
Muscle hypertrophy (muscle growth) is primarily driven by mechanical tension, muscle damage, and metabolic stress, with mechanical tension being the dominant driver.

Key Hypertrophy Guidelines:
1. Progressive Overload: The systematic increase in stress placed on the musculoskeletal system. You can achieve this by adding weight (load), increasing repetitions at the same load, improving execution and range of motion (ROM), or decreasing rest intervals.
2. Volume: Optimal weekly volume for most individuals is between 10 to 20 hard working sets per muscle group per week. Beginners can grow effectively on 8-12 sets, while advanced lifters may need 16-22 sets.
3. Rep Ranges: Hypertrophy occurs across a wide spectrum of reps (5 to 30 reps) provided sets are taken within 1 to 3 Reps in Reserve (RIR) or RPE 7-9. For compound movements (squats, deadlifts, presses), 6-10 reps are ideal to manage systemic fatigue. For isolation exercises (lateral raises, leg extensions, curls), 10-20 reps provide excellent localized tension with minimal joint strain.
4. Rest Intervals: Compound lifts require 2-3 minutes of rest for complete phosphocreatine resynthesis and central nervous system recovery. Isolation lifts require 60-90 seconds.
5. Frequency: Training each muscle group 2 times per week produces superior hypertrophic outcomes compared to once per week (the typical bro-split), allowing better volume distribution and higher quality per set.
"""
    },
    {
        "id": "kb_splits_02",
        "title": "Workout Split Programming: PPL vs Upper/Lower vs Full Body",
        "category": "Workout Programming",
        "tags": ["workout_split", "ppl", "upper_lower", "full_body", "programming"],
        "content": """
Selecting the right workout split depends on training experience, recovery capacity, and weekly schedule availability.

1. Push / Pull / Legs (PPL) Split (3 to 6 Days/Week):
   - Push: Chest, Anterior/Lateral Deltoids, Triceps (e.g., Incline Dumbbell Press, Overhead Press, Dips, Lateral Raises, Tricep Pushdowns).
   - Pull: Latissimus Dorsi, Trapezius, Rhomboids, Rear Delts, Biceps (e.g., Barbell Rows, Pull-ups/Lat Pulldowns, Face Pulls, Incline Dumbbell Curls).
   - Legs: Quadriceps, Hamstrings, Glutes, Calves (e.g., Squats, Romanian Deadlifts, Bulgarian Split Squats, Leg Curls, Calf Raises).
   - Best for intermediate to advanced lifters training 4 to 6 days weekly.

2. Upper / Lower Split (4 Days/Week):
   - Day 1: Upper Body Strength Focus
   - Day 2: Lower Body Strength Focus
   - Day 3: Rest
   - Day 4: Upper Body Hypertrophy Focus
   - Day 5: Lower Body Hypertrophy Focus
   - Days 6 & 7: Rest or Active Recovery
   - Excellent balance of recovery and frequency; ideal for beginners and intermediates.

3. Full Body (3 Days/Week):
   - Monday / Wednesday / Friday: Train all major muscle groups with 1-2 compound exercises each session.
   - Ideal for beginners, individuals with limited schedules, or athletes prioritizing other sports.
"""
    },
    {
        "id": "kb_fatloss_03",
        "title": "Science-Based Fat Loss & Caloric Deficit Protocol",
        "category": "Nutrition & Fat Loss",
        "tags": ["fat_loss", "caloric_deficit", "tdee", "neat", "metabolism"],
        "content": """
Fat loss requires a sustained negative energy balance (caloric deficit) where energy expenditure exceeds energy intake.

Calculating Your Energy Target:
1. Basal Metabolic Rate (BMR): The calories your body burns at rest (Mifflin-St Jeor equation).
2. Total Daily Energy Expenditure (TDEE) = BMR × Physical Activity Level (Sedentary: 1.2, Light: 1.375, Moderate: 1.55, Very Active: 1.725).
3. Sustainable Deficit: Aim for a 300 to 500 kcal deficit below maintenance per day. This equates to approximately 0.5% to 1.0% of total body weight lost per week, minimizing muscle loss and hormonal disruption.

Preserving Muscle Mass During a Cut:
- High Protein: Consume 1.8 to 2.4 grams of protein per kilogram of body weight (0.8 to 1.1 g/lb). High protein stimulates muscle protein synthesis (MPS) and has the highest Thermic Effect of Food (TEF ~20-30%).
- Heavy Resistance Training: Continue lifting heavy with high intensity to signal to the body that muscle tissue is essential.
- Non-Exercise Activity Thermogenesis (NEAT): Keep daily step count consistent (8,000 to 12,000 steps/day). NEAT often drops subconsciously during diets.
- Refeed Days: Adding 1-2 maintenance calorie days with increased carbohydrates every 1-2 weeks can replenish muscle glycogen, boost leptin, and reduce diet fatigue.
"""
    },
    {
        "id": "kb_nutrition_04",
        "title": "Macronutrient Distribution & Nutrient Timing",
        "category": "Nutrition Science",
        "tags": ["macronutrients", "protein", "carbohydrates", "fats", "nutrient_timing"],
        "content": """
A balanced macronutrient profile supports muscle hypertrophy, hormonal balance, cognitive function, and athletic performance.

1. Protein (4 kcal/gram):
   - Optimal intake: 1.6 to 2.2 g/kg (0.7-1.0 g/lb) for muscle gain; 2.0 to 2.6 g/kg for aggressive fat loss.
   - Quality sources: Chicken breast, lean beef, salmon, eggs, whey protein isolate, Greek yogurt, tofu, tempeh, lentils.
   - Distribution: 3 to 5 meals per day, each containing 25-45g of protein with at least 2.5-3g of Leucine to trigger the mTOR pathway.

2. Carbohydrates (4 kcal/gram):
   - Primary fuel source for glycolytic energy pathways during high-intensity resistance training.
   - Intake: 3 to 7 g/kg depending on training volume and energy expenditure.
   - Timing: Prioritize complex carbs (oats, brown rice, sweet potatoes) 2-3 hours pre-workout, and fast-digesting carbs (bananas, white rice) immediately post-workout with protein.

3. Dietary Fats (9 kcal/gram):
   - Crucial for steroid hormone production (testosterone, estrogen), cell membrane integrity, and fat-soluble vitamin absorption (A, D, E, K).
   - Intake: Never drop below 0.6 g/kg or 20% of total calories.
   - Healthy sources: Avocados, extra virgin olive oil, nuts, seeds, egg yolks, fatty fish (salmon, mackerel).
"""
    },
    {
        "id": "kb_supplements_05",
        "title": "Evidence-Based Sports Supplements Guide",
        "category": "Supplements",
        "tags": ["creatine", "whey_protein", "pre_workout", "caffeine", "omega3", "supplements"],
        "content": """
The sports supplement industry is filled with hype, but only a small tier of supplements has robust clinical backing (Tier 1 Evidence).

1. Creatine Monohydrate:
   - Mechanism: Phosphocreatine donates phosphate groups to ADP to rapidly regenerate ATP during short-burst, high-intensity exercise.
   - Dosage: 3 to 5 grams daily taken consistently at any time of day. No loading phase is required, though 20g/day for 5-7 days saturates stores faster.
   - Benefits: Increases 1RM strength by 5-15%, boosts power output, increases intracellular hydration, and enhances cognitive function. Safe for long-term daily use in healthy individuals.

2. Whey Protein Isolate & Concentrate:
   - Fast-digesting, complete protein with the highest Biological Value and rich in Leucine.
   - Use: 1 scoop (25-30g) post-workout or between meals to hit daily protein targets conveniently.

3. Pre-Workout & Caffeine:
   - Caffeine Anhydrous: 3-6 mg/kg taken 30-45 minutes pre-exercise blocks adenosine receptors, reducing perceived exertion and enhancing motor unit recruitment.
   - L-Citrulline Malate: 6-8 grams taken 45 minutes pre-workout increases nitric oxide (NO) synthesis, improving blood flow, muscular pump, and metabolite clearance.
   - Beta-Alanine: 3.2-6.4g daily buffers intramuscular carnosine levels, delaying fatigue during sets lasting 60-240 seconds (causes harmless paresthesia/tingling).

4. Health & Foundation Supplements:
   - Omega-3 Fatty Acids (EPA/DHA): 2-3g daily helps resolve muscular inflammation, supports cardiovascular health, and eases joint stiffness.
   - Vitamin D3 + K2: 2000-5000 IU daily optimizes bone mineral density, testosterone synthesis, and immune resilience.
"""
    },
    {
        "id": "kb_recovery_06",
        "title": "Injury Prevention, Joint Warm-up & Deload Protocols",
        "category": "Recovery & Mobility",
        "tags": ["injury_prevention", "mobility", "warm_up", "deload", "joint_health"],
        "content": """
Longevity and injury resilience are the prerequisites for consistent long-term fitness progress.

Dynamic Warm-up Sequence (8-10 Minutes):
1. General Cardiovascular Elevation: 3-5 minutes on an incline treadmill, rowing machine, or jump rope to raise core temperature and synovial fluid circulation.
2. Joint Mobility & Dynamic Stretching:
   - Hips & Knees: Deep bodyweight squats, world's greatest stretch, lateral lunges, leg swings.
   - Shoulders & Upper Back: Band pull-aparts, thoracic spine rotations, face pulls, shoulder dislocates.
3. Movement-Specific Warm-up: Start with the empty barbell/light weights and perform 3-4 progressive sets (e.g., 50% x 5, 70% x 3, 85% x 1) before your first working set.

Managing Joint Discomfort:
- Knee Pain during Squats: Ensure knees track in line with toes, utilize neoprene knee sleeves for compression and warmth, incorporate box squats or leg press to adjust shin angles, and strengthen the VMO (vastus medialis) and hamstrings.
- Lower Back Fatigue: Maintain a braced neutral spine, use a supportive weightlifting belt on heavy compounds, and build core bracing via bird-dogs and McGill big-3 exercises.

Deload Weeks:
- Schedule a deload every 6 to 10 weeks of progressive overload.
- Cut total volume by 40-50% while maintaining the weight on the bar, or keep sets the same while dropping weight by 20%. This allows soft tissues, tendons, and the nervous system to recover completely.
"""
    },
    {
        "id": "kb_dietary_types_07",
        "title": "Dietary Strategies: Ketogenic, Vegan, and Intermittent Fasting",
        "category": "Dietary Approaches",
        "tags": ["keto", "vegan", "intermittent_fasting", "plant_based", "diet_types"],
        "content": """
No single diet fits everyone; nutritional adherence and personal preference dictate long-term success.

1. Plant-Based / Vegan Fitness:
   - Protein Considerations: Plant proteins often have lower digestibility and incomplete amino acid profiles. Combine varied sources (e.g., peas + rice protein, quinoa, soy, hemp) or supplement with branched-chain amino acids (BCAAs).
   - Micronutrient Watchlist: Vitamin B12 (mandatory supplement for vegans), Iron, Zinc, Calcium, and algae-based Omega-3 (DHA/EPA).
   - Target: Aim slightly higher on total protein (1.8-2.4 g/kg) to offset lower bioavailability.

2. Ketogenic Diet (Low-Carb, High-Fat):
   - Macronutrient split: 70-75% Fat, 20-25% Protein, 5-10% Net Carbs (< 30-50g net carbs/day).
   - Adaptation: Shift body to ketone bodies as primary fuel. Initial water weight drops rapidly as glycogen stores deplete.
   - Performance: High-intensity glycolytic output (sprints, heavy sets) may suffer slightly; excellent for satiety and steady aerobic energy.
   - Critical: Supplement sodium, potassium, and magnesium (electrolytes) to avoid the keto flu and muscle cramping.

3. Intermittent Fasting (16/8 Protocol):
   - 16 hours fasting, 8 hours feeding window.
   - Benefits: Effective behavioral tool for restricting calorie intake without obsessive tracking; improves insulin sensitivity.
   - Hypertrophy: Ensure the 8-hour window provides at least 2-3 protein-rich feedings spaced 3-4 hours apart to maximize muscle protein synthesis.
"""
    },
    {
        "id": "kb_home_calisthenics_08",
        "title": "Home Workouts, Calisthenics & Minimal Equipment Training",
        "category": "Home Training",
        "tags": ["home_workout", "calisthenics", "bodyweight", "resistance_bands", "no_gym"],
        "content": """
Building muscle and athletic conditioning does not require a commercial gym membership.

Calisthenics Progressive Overload Strategies:
1. Leverage Manipulation: Change the angle of your body to increase resistance (e.g., Wall push-up -> Knee push-up -> Flat push-up -> Feet-elevated push-up -> Handstand push-up).
2. Tempo & Pause Reps: Introduce a 3-4 second eccentric (lowering) phase and a 2-second pause at maximum muscular stretch to increase mechanical tension without adding weight.
3. Unilateral Variations: Shift from bilateral to unilateral movements (e.g., standard squats to Bulgarian split squats or pistol squats; push-ups to archer push-ups).

Essential Minimalist Home Equipment:
- Pull-Up Bar / Gymnastic Rings: The gold standard for back, rear delts, and bicep development.
- Heavy Resistance Bands: Allows variable resistance for chest presses, banded rows, squats, and shoulder overhead presses.
- Adjustable Dumbbells: Provides scalable loading up to 50+ lbs for a complete home gym setup.
"""
    }
]
