"""Starter recipe set seeded into every new household.

Placeholder homestyle recipes (standing in for Nick's Kitchen until real ones
are added). calories/protein_g/carbs_g/fat_g are PER SERVING; cost_total is
for the whole recipe in dollars.
"""

SEED_RECIPES = [
    {
        'name': 'Veggie Scramble', 'emoji': '🍳', 'meal_type': 'breakfast',
        'time_minutes': 15, 'servings': 2, 'cost_total': 4.50,
        'calories': 320, 'protein_g': 22, 'carbs_g': 8, 'fat_g': 22,
        'description': 'Fluffy eggs loaded with peppers, spinach, and cheddar.',
        'instructions': '1. Dice the bell pepper and roughly chop the spinach.\n'
                        '2. Whisk eggs with a pinch of salt and pepper.\n'
                        '3. Melt butter in a nonstick pan over medium heat, soften the pepper 2 minutes.\n'
                        '4. Add spinach until wilted, pour in eggs, and stir gently until just set.\n'
                        '5. Fold in cheddar and serve hot.',
        'ingredients': [
            ('eggs', 5, ''), ('bell pepper', 1, ''), ('spinach', 2, 'cups'),
            ('cheddar cheese', 0.5, 'cup'), ('butter', 1, 'tbsp'),
        ],
    },
    {
        'name': 'Overnight Oats with Berries', 'emoji': '🥣', 'meal_type': 'breakfast',
        'time_minutes': 10, 'servings': 2, 'cost_total': 3.00,
        'calories': 350, 'protein_g': 12, 'carbs_g': 55, 'fat_g': 9,
        'description': 'Mix the night before, grab and go in the morning.',
        'instructions': '1. Stir oats, milk, yogurt, honey, and chia seeds in two jars.\n'
                        '2. Refrigerate overnight (or at least 4 hours).\n'
                        '3. Top with berries before eating.',
        'ingredients': [
            ('rolled oats', 1, 'cup'), ('milk', 1, 'cup'), ('greek yogurt', 0.5, 'cup'),
            ('honey', 2, 'tbsp'), ('mixed berries', 1, 'cup'), ('chia seeds', 1, 'tbsp'),
        ],
    },
    {
        'name': 'Freezer Breakfast Burritos', 'emoji': '🌯', 'meal_type': 'breakfast',
        'time_minutes': 35, 'servings': 6, 'cost_total': 12.00,
        'calories': 450, 'protein_g': 24, 'carbs_g': 38, 'fat_g': 22,
        'description': 'Make a batch on Sunday, microwave all week. Peak Stay Ready.',
        'instructions': '1. Dice and pan-fry the potatoes until crispy; set aside.\n'
                        '2. Brown the sausage, then scramble the eggs in the same pan.\n'
                        '3. Fill tortillas with potatoes, sausage, eggs, cheese, and salsa.\n'
                        '4. Roll tightly, wrap in foil, and freeze.\n'
                        '5. Reheat 2 minutes in the microwave (unwrapped) when needed.',
        'ingredients': [
            ('flour tortillas', 6, ''), ('eggs', 8, ''), ('breakfast sausage', 0.5, 'lb'),
            ('cheddar cheese', 1.5, 'cup'), ('salsa', 0.75, 'cup'), ('potatoes', 2, ''),
        ],
    },
    {
        'name': 'Chicken Caesar Wraps', 'emoji': '🥗', 'meal_type': 'lunch',
        'time_minutes': 20, 'servings': 4, 'cost_total': 10.00,
        'calories': 420, 'protein_g': 32, 'carbs_g': 30, 'fat_g': 18,
        'description': 'A caesar salad you can eat with one hand.',
        'instructions': '1. Season chicken with salt and pepper; pan-sear 5-6 minutes per side, then slice.\n'
                        '2. Chop romaine and toss with dressing and parmesan.\n'
                        '3. Pile chicken and salad into tortillas and roll up.',
        'ingredients': [
            ('chicken breast', 1, 'lb'), ('romaine lettuce', 1, 'head'),
            ('caesar dressing', 0.5, 'cup'), ('parmesan cheese', 0.5, 'cup'),
            ('flour tortillas', 4, ''),
        ],
    },
    {
        'name': 'Hearty Lentil Soup', 'emoji': '🍲', 'meal_type': 'lunch',
        'time_minutes': 40, 'servings': 6, 'cost_total': 7.50,
        'calories': 290, 'protein_g': 16, 'carbs_g': 45, 'fat_g': 5,
        'description': 'Cheap, filling, and it freezes like a dream.',
        'instructions': '1. Dice onion, carrots, and celery; mince garlic.\n'
                        '2. Sweat the vegetables in olive oil 5 minutes.\n'
                        '3. Add cumin, lentils, tomatoes, and broth; bring to a boil.\n'
                        '4. Simmer 30 minutes until lentils are tender. Season to taste.',
        'ingredients': [
            ('dry lentils', 2, 'cups'), ('carrots', 3, ''), ('celery', 3, 'stalks'),
            ('onion', 1, ''), ('garlic', 3, 'cloves'), ('canned diced tomatoes', 1, 'can'),
            ('vegetable broth', 6, 'cups'), ('cumin', 1, 'tsp'), ('olive oil', 2, 'tbsp'),
        ],
    },
    {
        'name': 'Turkey Avocado Melt', 'emoji': '🥪', 'meal_type': 'lunch',
        'time_minutes': 12, 'servings': 2, 'cost_total': 7.00,
        'calories': 480, 'protein_g': 28, 'carbs_g': 35, 'fat_g': 24,
        'description': 'Crispy, melty, ready in 12 minutes flat.',
        'instructions': '1. Butter the outside of each bread slice.\n'
                        '2. Layer turkey, tomato slices, avocado, and provolone between slices.\n'
                        '3. Grill in a pan over medium heat 3-4 minutes per side until golden.',
        'ingredients': [
            ('sourdough bread', 4, 'slices'), ('sliced turkey', 6, 'oz'), ('avocado', 1, ''),
            ('provolone cheese', 2, 'slices'), ('tomato', 1, ''), ('butter', 1, 'tbsp'),
        ],
    },
    {
        'name': 'Southwest Quinoa Bowl', 'emoji': '🍚', 'meal_type': 'lunch',
        'time_minutes': 25, 'servings': 4, 'cost_total': 9.00,
        'calories': 410, 'protein_g': 15, 'carbs_g': 58, 'fat_g': 14,
        'description': 'Bright, zesty meal-prep favorite that keeps for days.',
        'instructions': '1. Rinse quinoa and cook per package directions.\n'
                        '2. Drain and rinse black beans; halve the tomatoes; dice avocado.\n'
                        '3. Whisk olive oil, lime juice, chili powder, and salt into a dressing.\n'
                        '4. Toss everything together and top with cilantro.',
        'ingredients': [
            ('quinoa', 1.5, 'cups'), ('canned black beans', 1, 'can'), ('corn', 1, 'cup'),
            ('cherry tomatoes', 1, 'cup'), ('avocado', 1, ''), ('lime', 2, ''),
            ('cilantro', 0.5, 'cup'), ('olive oil', 2, 'tbsp'), ('chili powder', 1, 'tsp'),
        ],
    },
    {
        'name': 'Sheet-Pan Lemon Chicken & Veggies', 'emoji': '🍗', 'meal_type': 'dinner',
        'time_minutes': 40, 'servings': 4, 'cost_total': 12.50,
        'calories': 430, 'protein_g': 38, 'carbs_g': 22, 'fat_g': 20,
        'description': 'One pan, no fuss, big flavor.',
        'instructions': '1. Heat oven to 425°F. Halve the potatoes and cut broccoli into florets.\n'
                        '2. Toss everything with olive oil, minced garlic, oregano, salt, and lemon juice.\n'
                        '3. Spread on a sheet pan, chicken in the middle.\n'
                        '4. Roast 30-35 minutes until chicken hits 165°F.',
        'ingredients': [
            ('chicken thighs', 1.5, 'lb'), ('broccoli', 1, 'head'), ('baby potatoes', 1, 'lb'),
            ('lemon', 2, ''), ('olive oil', 3, 'tbsp'), ('garlic', 4, 'cloves'),
            ('oregano', 1, 'tsp'),
        ],
    },
    {
        'name': 'Spaghetti with Meat Sauce', 'emoji': '🍝', 'meal_type': 'dinner',
        'time_minutes': 30, 'servings': 5, 'cost_total': 11.00,
        'calories': 520, 'protein_g': 28, 'carbs_g': 62, 'fat_g': 16,
        'description': 'The weeknight classic everybody actually eats.',
        'instructions': '1. Boil salted water and cook spaghetti to al dente.\n'
                        '2. Meanwhile, brown the beef with diced onion and garlic in olive oil.\n'
                        '3. Stir in marinara and simmer 10 minutes.\n'
                        '4. Toss sauce with pasta and finish with parmesan.',
        'ingredients': [
            ('spaghetti', 1, 'lb'), ('ground beef', 1, 'lb'), ('marinara sauce', 1, 'jar'),
            ('onion', 1, ''), ('garlic', 3, 'cloves'), ('parmesan cheese', 0.5, 'cup'),
            ('olive oil', 1, 'tbsp'),
        ],
    },
    {
        'name': 'Slow Cooker Beef Chili', 'emoji': '🌶️', 'meal_type': 'dinner',
        'time_minutes': 240, 'servings': 6, 'cost_total': 14.00,
        'calories': 460, 'protein_g': 32, 'carbs_g': 35, 'fat_g': 20,
        'description': 'Ten minutes of prep, then the slow cooker does the rest.',
        'instructions': '1. Brown the beef with diced onion and garlic; drain.\n'
                        '2. Add everything to the slow cooker with chili powder and tomato paste.\n'
                        '3. Cook on high 4 hours (or low 7-8).\n'
                        '4. Serve topped with cheddar.',
        'ingredients': [
            ('ground beef', 1.5, 'lb'), ('canned kidney beans', 2, 'cans'),
            ('canned diced tomatoes', 2, 'can'), ('tomato paste', 2, 'tbsp'),
            ('onion', 1, ''), ('garlic', 3, 'cloves'), ('chili powder', 2, 'tbsp'),
            ('beef broth', 1, 'cup'), ('cheddar cheese', 1, 'cup'),
        ],
    },
    {
        'name': 'Baked Salmon, Rice & Broccoli', 'emoji': '🐟', 'meal_type': 'dinner',
        'time_minutes': 30, 'servings': 4, 'cost_total': 18.00,
        'calories': 490, 'protein_g': 34, 'carbs_g': 42, 'fat_g': 18,
        'description': 'Honey-garlic glazed salmon with the classic sides.',
        'instructions': '1. Start the rice. Heat oven to 400°F.\n'
                        '2. Whisk soy sauce, honey, and minced garlic; brush over salmon.\n'
                        '3. Bake salmon 12-14 minutes; steam broccoli alongside.\n'
                        '4. Serve salmon over rice with buttered broccoli.',
        'ingredients': [
            ('salmon fillets', 4, ''), ('jasmine rice', 1.5, 'cups'), ('broccoli', 1, 'head'),
            ('soy sauce', 2, 'tbsp'), ('honey', 1, 'tbsp'), ('garlic', 2, 'cloves'),
            ('butter', 1, 'tbsp'),
        ],
    },
    {
        'name': 'Veggie Tofu Stir-Fry', 'emoji': '🥦', 'meal_type': 'dinner',
        'time_minutes': 25, 'servings': 4, 'cost_total': 8.50,
        'calories': 380, 'protein_g': 18, 'carbs_g': 40, 'fat_g': 16,
        'description': 'Crispy tofu and crunchy veggies in a quick soy-ginger sauce.',
        'instructions': '1. Start the rice. Press tofu, cube it, and toss with cornstarch.\n'
                        '2. Pan-fry tofu in sesame oil until golden; set aside.\n'
                        '3. Stir-fry peppers, carrots, and snap peas 4 minutes; add garlic and ginger.\n'
                        '4. Return tofu, add soy sauce, and toss. Serve over rice.',
        'ingredients': [
            ('firm tofu', 14, 'oz'), ('bell pepper', 2, ''), ('snap peas', 2, 'cups'),
            ('carrots', 2, ''), ('garlic', 2, 'cloves'), ('ginger', 1, 'tbsp'),
            ('soy sauce', 3, 'tbsp'), ('jasmine rice', 1.5, 'cups'), ('sesame oil', 1, 'tbsp'),
            ('cornstarch', 2, 'tbsp'),
        ],
    },
    {
        'name': 'Loaded Baked Potato Night', 'emoji': '🥔', 'meal_type': 'any',
        'time_minutes': 60, 'servings': 4, 'cost_total': 6.50,
        'calories': 400, 'protein_g': 14, 'carbs_g': 52, 'fat_g': 16,
        'description': 'Bake potatoes, put out toppings, let everyone build their own.',
        'instructions': '1. Heat oven to 425°F. Scrub potatoes, poke with a fork, rub with oil and salt.\n'
                        '2. Bake 50-60 minutes until a knife slides in easily.\n'
                        '3. Split and load with butter, cheese, sour cream, and green onions.',
        'ingredients': [
            ('russet potatoes', 4, ''), ('cheddar cheese', 1, 'cup'), ('sour cream', 0.5, 'cup'),
            ('butter', 2, 'tbsp'), ('green onions', 3, ''), ('olive oil', 1, 'tbsp'),
        ],
    },
]


def seed_household(db, household_id):
    """Insert the starter recipes for a newly created household."""
    for r in SEED_RECIPES:
        cur = db.execute(
            '''INSERT INTO recipes (household_id, name, emoji, description, meal_type,
                                    time_minutes, servings, cost_total, calories,
                                    protein_g, carbs_g, fat_g, instructions)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (household_id, r['name'], r['emoji'], r['description'], r['meal_type'],
             r['time_minutes'], r['servings'], r['cost_total'], r['calories'],
             r['protein_g'], r['carbs_g'], r['fat_g'], r['instructions']))
        recipe_id = cur.lastrowid
        db.executemany(
            'INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit) VALUES (?, ?, ?, ?)',
            [(recipe_id, name, qty, unit) for (name, qty, unit) in r['ingredients']])
