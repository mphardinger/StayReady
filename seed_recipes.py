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

    # ---- Budget pack: cheap, batch-friendly meals for a busy household. ----
    {
        'name': 'One-Pot Chicken Alfredo', 'emoji': '🍝', 'meal_type': 'dinner',
        'time_minutes': 30, 'servings': 5, 'cost_total': 11.00,
        'calories': 560, 'protein_g': 35, 'carbs_g': 52, 'fat_g': 24,
        'description': 'Creamy pasta and chicken in one pot — leftovers reheat great.',
        'instructions': '1. Cube chicken, season, and brown in butter in a big pot; set aside.\n'
                        '2. Add broth, milk, and penne to the pot; simmer 12-14 minutes, stirring.\n'
                        '3. When pasta is tender, stir in parmesan, garlic powder, and the chicken.\n'
                        '4. Rest 5 minutes off heat — the sauce thickens as it sits.',
        'ingredients': [
            ('chicken breast', 1, 'lb'), ('penne', 1, 'lb'), ('chicken broth', 3, 'cups'),
            ('milk', 2, 'cups'), ('parmesan cheese', 1, 'cup'), ('butter', 2, 'tbsp'),
            ('garlic powder', 1, 'tsp'),
        ],
    },
    {
        'name': 'Black Bean Quesadillas', 'emoji': '🫓', 'meal_type': 'dinner',
        'time_minutes': 20, 'servings': 4, 'cost_total': 6.00,
        'calories': 430, 'protein_g': 17, 'carbs_g': 52, 'fat_g': 17,
        'description': 'Crispy, cheesy, and about $1.50 a plate.',
        'instructions': '1. Drain and rinse the beans; mash roughly with cumin and salsa.\n'
                        '2. Spread bean mix on half of each tortilla, top with cheese, and fold.\n'
                        '3. Toast in a dry pan 2-3 minutes per side until golden and melty.\n'
                        '4. Cut into wedges; serve with sour cream.',
        'ingredients': [
            ('black beans', 2, 'cans'), ('flour tortillas', 4, ''), ('cheddar cheese', 2, 'cups'),
            ('salsa', 0.5, 'cup'), ('cumin', 1, 'tsp'), ('sour cream', 0.5, 'cup'),
        ],
    },
    {
        'name': 'Ground Beef Tacos', 'emoji': '🌮', 'meal_type': 'dinner',
        'time_minutes': 25, 'servings': 4, 'cost_total': 11.50,
        'calories': 510, 'protein_g': 27, 'carbs_g': 40, 'fat_g': 26,
        'description': 'Taco night — the easiest dinner to get four people excited about.',
        'instructions': '1. Brown the beef with diced onion; drain the fat.\n'
                        '2. Stir in chili powder, cumin, and a splash of water; simmer 3 minutes.\n'
                        '3. Warm the tortillas in a dry pan.\n'
                        '4. Set out lettuce, tomato, cheese, and salsa — everyone builds their own.',
        'ingredients': [
            ('ground beef', 1, 'lb'), ('tortillas', 8, ''), ('onion', 1, ''),
            ('chili powder', 1, 'tbsp'), ('cumin', 1, 'tsp'), ('lettuce', 2, 'cups'),
            ('tomato', 2, ''), ('cheddar cheese', 1, 'cup'), ('salsa', 0.5, 'cup'),
        ],
    },
    {
        'name': 'Egg Fried Rice', 'emoji': '🍛', 'meal_type': 'dinner',
        'time_minutes': 20, 'servings': 4, 'cost_total': 5.50,
        'calories': 420, 'protein_g': 14, 'carbs_g': 62, 'fat_g': 13,
        'description': 'The best use of day-old rice ever invented.',
        'instructions': '1. Scramble the eggs in a hot oiled pan; set aside.\n'
                        '2. Stir-fry frozen peas and diced carrot 3 minutes.\n'
                        '3. Add cooked rice, breaking up clumps; fry 4-5 minutes without stirring too much.\n'
                        '4. Return eggs, add soy sauce and sesame oil, toss, and top with green onions.',
        'ingredients': [
            ('rice', 3, 'cups'), ('eggs', 4, ''), ('frozen peas', 1, 'cup'),
            ('carrots', 2, ''), ('soy sauce', 3, 'tbsp'), ('sesame oil', 1, 'tbsp'),
            ('green onions', 3, ''), ('vegetable oil', 2, 'tbsp'),
        ],
    },
    {
        'name': 'Chicken Fajita Skillet', 'emoji': '🫑', 'meal_type': 'dinner',
        'time_minutes': 30, 'servings': 4, 'cost_total': 12.00,
        'calories': 460, 'protein_g': 33, 'carbs_g': 38, 'fat_g': 19,
        'description': 'Sizzling peppers and chicken — tortillas or rice, your call.',
        'instructions': '1. Slice chicken, peppers, and onion into strips.\n'
                        '2. Sear chicken in oil with chili powder, cumin, and paprika; set aside.\n'
                        '3. Char the peppers and onion in the same pan 5-6 minutes.\n'
                        '4. Return chicken, squeeze lime over everything, and serve with warm tortillas.',
        'ingredients': [
            ('chicken breast', 1.25, 'lb'), ('bell pepper', 3, ''), ('onion', 1, ''),
            ('tortillas', 8, ''), ('lime', 1, ''), ('chili powder', 1, 'tbsp'),
            ('cumin', 1, 'tsp'), ('paprika', 1, 'tsp'), ('vegetable oil', 2, 'tbsp'),
        ],
    },
    {
        'name': 'Baked Ziti', 'emoji': '🧀', 'meal_type': 'dinner',
        'time_minutes': 50, 'servings': 6, 'cost_total': 12.50,
        'calories': 540, 'protein_g': 26, 'carbs_g': 58, 'fat_g': 23,
        'description': 'Feeds the whole house tonight and somebody\'s lunch tomorrow.',
        'instructions': '1. Heat oven to 400°F. Boil ziti 2 minutes shy of al dente.\n'
                        '2. Brown the sausage; stir in marinara.\n'
                        '3. Toss pasta with sauce, dollop with ricotta, and top with mozzarella.\n'
                        '4. Bake 20 minutes until bubbling and browned on top.',
        'ingredients': [
            ('ziti', 1, 'lb'), ('italian sausage', 1, 'lb'), ('marinara sauce', 1, 'jar'),
            ('ricotta cheese', 1, 'cup'), ('mozzarella', 2, 'cups'),
        ],
    },
    {
        'name': 'Honey Garlic Chicken & Rice', 'emoji': '🍯', 'meal_type': 'dinner',
        'time_minutes': 35, 'servings': 4, 'cost_total': 11.00,
        'calories': 520, 'protein_g': 36, 'carbs_g': 60, 'fat_g': 14,
        'description': 'Sticky-sweet glazed thighs over rice. Cheap cut, big payoff.',
        'instructions': '1. Start the rice.\n'
                        '2. Season and sear chicken thighs 5-6 minutes per side.\n'
                        '3. Whisk honey, soy sauce, garlic, and vinegar; pour over the chicken.\n'
                        '4. Simmer 5 minutes until the glaze coats a spoon. Serve over rice.',
        'ingredients': [
            ('chicken thighs', 1.5, 'lb'), ('rice', 1.5, 'cups'), ('honey', 3, 'tbsp'),
            ('soy sauce', 3, 'tbsp'), ('garlic', 4, 'cloves'), ('vinegar', 1, 'tbsp'),
        ],
    },
    {
        'name': 'Chickpea Coconut Curry', 'emoji': '🍛', 'meal_type': 'dinner',
        'time_minutes': 30, 'servings': 4, 'cost_total': 8.00,
        'calories': 450, 'protein_g': 13, 'carbs_g': 58, 'fat_g': 20,
        'description': 'Pantry-staple curry — vegan, filling, and better the next day.',
        'instructions': '1. Soften diced onion in oil; add garlic, ginger, and curry powder for 1 minute.\n'
                        '2. Add chickpeas, diced tomatoes, and coconut milk; simmer 15 minutes.\n'
                        '3. Stir in spinach until wilted; season with salt.\n'
                        '4. Serve over rice.',
        'ingredients': [
            ('chickpeas', 2, 'cans'), ('coconut milk', 1, 'can'), ('canned diced tomatoes', 1, 'can'),
            ('onion', 1, ''), ('garlic', 3, 'cloves'), ('ginger', 1, 'tbsp'),
            ('curry powder', 2, 'tbsp'), ('spinach', 3, 'cups'), ('rice', 1.5, 'cups'),
            ('vegetable oil', 2, 'tbsp'),
        ],
    },
    {
        'name': 'Slow Cooker Pulled Pork Sandwiches', 'emoji': '🥪', 'meal_type': 'dinner',
        'time_minutes': 300, 'servings': 8, 'cost_total': 16.00,
        'calories': 480, 'protein_g': 30, 'carbs_g': 42, 'fat_g': 21,
        'description': 'Set it in the morning, feed everyone for two days.',
        'instructions': '1. Rub the pork with paprika, garlic powder, salt, and pepper.\n'
                        '2. Slow-cook with a splash of broth on low 8 hours (or high 5).\n'
                        '3. Shred with two forks and mix with BBQ sauce.\n'
                        '4. Pile onto buns — coleslaw on top if you\'re fancy.',
        'ingredients': [
            ('pork shoulder', 3, 'lb'), ('bbq sauce', 1.5, 'cups'), ('burger buns', 8, ''),
            ('paprika', 1, 'tbsp'), ('garlic powder', 1, 'tbsp'), ('chicken broth', 0.5, 'cup'),
        ],
    },
    {
        'name': 'Chili Mac', 'emoji': '🍜', 'meal_type': 'dinner',
        'time_minutes': 30, 'servings': 5, 'cost_total': 10.50,
        'calories': 550, 'protein_g': 30, 'carbs_g': 55, 'fat_g': 22,
        'description': 'Chili and mac & cheese had a baby. One pot, zero complaints.',
        'instructions': '1. Brown the beef with diced onion; drain.\n'
                        '2. Add chili powder, beans, diced tomatoes, broth, and macaroni.\n'
                        '3. Simmer 12 minutes, stirring, until pasta is tender.\n'
                        '4. Kill the heat and stir in the cheddar.',
        'ingredients': [
            ('ground beef', 1, 'lb'), ('macaroni', 2, 'cups'), ('kidney beans', 1, 'can'),
            ('canned diced tomatoes', 1, 'can'), ('beef broth', 2, 'cups'), ('onion', 1, ''),
            ('chili powder', 1.5, 'tbsp'), ('cheddar cheese', 1.5, 'cups'),
        ],
    },
    {
        'name': 'Sausage & Veggie Sheet Pan', 'emoji': '🍳', 'meal_type': 'dinner',
        'time_minutes': 35, 'servings': 4, 'cost_total': 10.50,
        'calories': 440, 'protein_g': 22, 'carbs_g': 34, 'fat_g': 25,
        'description': 'Chop, toss, roast. The dishes basically do themselves.',
        'instructions': '1. Heat oven to 425°F. Slice sausage into coins; chunk the potatoes and peppers.\n'
                        '2. Toss everything with olive oil, paprika, and garlic powder on a sheet pan.\n'
                        '3. Roast 25-30 minutes, flipping once, until potatoes are crisp.',
        'ingredients': [
            ('smoked sausage', 1, 'lb'), ('baby potatoes', 1.5, 'lb'), ('bell pepper', 2, ''),
            ('onion', 1, ''), ('olive oil', 2, 'tbsp'), ('paprika', 1, 'tsp'),
            ('garlic powder', 1, 'tsp'),
        ],
    },
    {
        'name': 'Tuna Pasta Salad', 'emoji': '🥗', 'meal_type': 'lunch',
        'time_minutes': 20, 'servings': 4, 'cost_total': 7.00,
        'calories': 380, 'protein_g': 22, 'carbs_g': 42, 'fat_g': 14,
        'description': 'Make a bowl Sunday, eat cold lunches through Wednesday.',
        'instructions': '1. Boil pasta; rinse under cold water.\n'
                        '2. Mix mayo, a squeeze of lemon, salt, and pepper in a big bowl.\n'
                        '3. Fold in drained tuna, peas, chopped celery, and the pasta.\n'
                        '4. Chill 30 minutes if you can wait.',
        'ingredients': [
            ('pasta', 0.75, 'lb'), ('canned tuna', 2, 'cans'), ('mayonnaise', 0.5, 'cup'),
            ('frozen peas', 1, 'cup'), ('celery', 2, 'stalks'), ('lemon', 1, ''),
        ],
    },
    {
        'name': 'Greek Chicken Rice Bowls', 'emoji': '🥙', 'meal_type': 'lunch',
        'time_minutes': 30, 'servings': 4, 'cost_total': 12.00,
        'calories': 470, 'protein_g': 34, 'carbs_g': 48, 'fat_g': 15,
        'description': 'Meal-prep classic: lemony chicken, rice, crunchy veg, feta.',
        'instructions': '1. Start the rice. Cube chicken and toss with oregano, salt, and lemon juice.\n'
                        '2. Sear chicken 6-8 minutes until cooked through.\n'
                        '3. Dice cucumber and tomatoes.\n'
                        '4. Build bowls: rice, chicken, veg, feta, and a drizzle of olive oil.',
        'ingredients': [
            ('chicken breast', 1.25, 'lb'), ('rice', 1.5, 'cups'), ('cucumber', 1, ''),
            ('tomato', 2, ''), ('feta cheese', 0.75, 'cup'), ('lemon', 2, ''),
            ('oregano', 2, 'tsp'), ('olive oil', 2, 'tbsp'),
        ],
    },
    {
        'name': 'Cold Peanut Noodles', 'emoji': '🥜', 'meal_type': 'lunch',
        'time_minutes': 15, 'servings': 4, 'cost_total': 6.00,
        'calories': 440, 'protein_g': 14, 'carbs_g': 58, 'fat_g': 18,
        'description': 'Fifteen minutes, mostly pantry stuff, weirdly addictive.',
        'instructions': '1. Boil noodles; rinse cold.\n'
                        '2. Whisk peanut butter, soy sauce, vinegar, honey, and a little hot water into a sauce.\n'
                        '3. Toss noodles with sauce, shredded carrot, and sliced green onion.\n'
                        '4. Eat cold or room temp — great for packed lunches.',
        'ingredients': [
            ('spaghetti', 0.75, 'lb'), ('peanut butter', 0.5, 'cup'), ('soy sauce', 3, 'tbsp'),
            ('vinegar', 2, 'tbsp'), ('honey', 1, 'tbsp'), ('carrots', 2, ''),
            ('green onions', 3, ''),
        ],
    },
    {
        'name': 'Peanut Butter Banana Smoothie', 'emoji': '🥤', 'meal_type': 'breakfast',
        'time_minutes': 5, 'servings': 2, 'cost_total': 3.50,
        'calories': 340, 'protein_g': 15, 'carbs_g': 45, 'fat_g': 13,
        'description': 'Breakfast in the time it takes to find your keys.',
        'instructions': '1. Blend bananas, peanut butter, milk, yogurt, and oats until smooth.\n'
                        '2. Add a handful of ice for a thicker shake.\n'
                        '3. Pour and go.',
        'ingredients': [
            ('banana', 2, ''), ('peanut butter', 2, 'tbsp'), ('milk', 1.5, 'cups'),
            ('greek yogurt', 0.5, 'cup'), ('rolled oats', 0.25, 'cup'),
        ],
    },
    {
        'name': 'Upgraded Ramen with Egg & Greens', 'emoji': '🍜', 'meal_type': 'any',
        'time_minutes': 12, 'servings': 2, 'cost_total': 4.00,
        'calories': 420, 'protein_g': 17, 'carbs_g': 52, 'fat_g': 16,
        'description': 'Dorm classic, adult glow-up: soft egg, greens, sesame.',
        'instructions': '1. Cook ramen per the package; add the seasoning to the pot.\n'
                        '2. In the last 2 minutes, drop in spinach and a swirl of beaten egg.\n'
                        '3. Finish with green onion, a drizzle of sesame oil, and sriracha if you like heat.',
        'ingredients': [
            ('ramen noodles', 2, 'packs'), ('eggs', 2, ''), ('spinach', 2, 'cups'),
            ('green onions', 2, ''), ('sesame oil', 1, 'tsp'),
        ],
    },
    {
        'name': 'Grilled Cheese & Tomato Soup', 'emoji': '🥣', 'meal_type': 'any',
        'time_minutes': 20, 'servings': 3, 'cost_total': 7.00,
        'calories': 460, 'protein_g': 16, 'carbs_g': 46, 'fat_g': 24,
        'description': 'The rainy-day double act. Dip aggressively.',
        'instructions': '1. Warm the tomato soup in a pot with a splash of milk.\n'
                        '2. Butter the bread, fill with cheddar, and grill 3 minutes per side until golden.\n'
                        '3. Slice diagonally (mandatory) and serve with the soup.',
        'ingredients': [
            ('tomato soup', 2, 'cans'), ('bread', 6, 'slices'), ('cheddar cheese', 1.5, 'cups'),
            ('butter', 2, 'tbsp'), ('milk', 0.5, 'cup'),
        ],
    },
]


def insert_recipe(db, household_id, r):
    """Insert one seed-format recipe dict (with ingredients) for a household."""
    cur = db.execute(
        '''INSERT INTO recipes (household_id, name, emoji, description, meal_type,
                                time_minutes, servings, cost_total, calories,
                                protein_g, carbs_g, fat_g, sodium_mg, potassium_mg,
                                phosphorus_mg, fiber_g, sugar_g, tags, instructions)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (household_id, r['name'], r['emoji'], r['description'], r['meal_type'],
         r['time_minutes'], r['servings'], r['cost_total'], r['calories'],
         r['protein_g'], r['carbs_g'], r['fat_g'],
         r.get('sodium_mg', 0), r.get('potassium_mg', 0), r.get('phosphorus_mg', 0),
         r.get('fiber_g', 0), r.get('sugar_g', 0), ','.join(r.get('tags', [])),
         r['instructions']))
    db.executemany(
        'INSERT INTO recipe_ingredients (recipe_id, name, quantity, unit) VALUES (?, ?, ?, ?)',
        [(cur.lastrowid, name, qty, unit) for (name, qty, unit) in r['ingredients']])
    return cur.lastrowid


def seed_household(db, household_id):
    """Insert the starter recipes for a newly created household."""
    for r in SEED_RECIPES:
        insert_recipe(db, household_id, r)


# ---- Diet-targeted pack: renal / low-FODMAP / diabetic + ultra-budget / quick.
# Authored and adversarially verified (two independent checkers per batch)
# on 2026-07-13. Nutrition is per serving and ESTIMATED.
DIET_PACK = [
    {
        'name': 'Lemon Pepper Chicken Skillet', 'emoji': '🍋', 'meal_type': 'dinner',
        'time_minutes': 25, 'servings': 4, 'cost_total': 7.5,
        'calories': 390, 'protein_g': 24, 'carbs_g': 51, 'fat_g': 9,
        'sodium_mg': 300, 'potassium_mg': 480, 'phosphorus_mg': 270,
        'fiber_g': 2.5, 'sugar_g': 4.2, 'tags': ['fodmap'],
        'description': 'One pan, one lemon, and a modest pile of chicken doing big flavor on a small budget.',
        'instructions': '1. Start the rice: combine rice with 2.5 cups water in a pot, bring to a boil, cover, and simmer on low 15 minutes.\n2. Cut chicken into bite-size pieces and season with black pepper, oregano, and a small pinch of salt.\n3. Heat 1 tbsp olive oil in a large skillet over medium-high. Cook chicken 5-6 minutes until browned and cooked through; move to a plate.\n4. Add remaining oil, then sliced bell peppers and zucchini half-moons. Cook 4-5 minutes until just tender.\n5. Return chicken to the skillet, squeeze in the juice of the whole lemon, and toss 1 minute.\n6. Serve over rice with extra black pepper on top.',
        'ingredients': [
            ('chicken breast', 12, 'oz'),
            ('white rice', 1.25, 'cup'),
            ('bell pepper', 2, 'whole'),
            ('zucchini', 1, 'whole'),
            ('olive oil', 2, 'tbsp'),
            ('lemon', 1, 'whole'),
            ('dried oregano', 1, 'tsp'),
            ('black pepper', 0.5, 'tsp'),
            ('salt', 1, 'pinch'),
        ],
    },
    {
        'name': 'Lemon Zucchini Parmesan Pasta', 'emoji': '🍝', 'meal_type': 'lunch',
        'time_minutes': 15, 'servings': 2, 'cost_total': 3.5,
        'calories': 500, 'protein_g': 15, 'carbs_g': 68, 'fat_g': 18,
        'sodium_mg': 380, 'potassium_mg': 285, 'phosphorus_mg': 280,
        'fiber_g': 3.5, 'sugar_g': 3.5, 'tags': ['vegetarian'],
        'description': 'Pantry pasta that tastes like you tried, ready before your group chat finishes arguing.',
        'instructions': '1. Boil a pot of water with a small pinch of salt and cook spaghetti per package directions, about 10 minutes.\n2. While pasta cooks, grate or thinly slice the zucchini into half-moons.\n3. Heat olive oil in a skillet over medium-high and cook zucchini 3-4 minutes with black pepper and red pepper flakes.\n4. Reserve 1/4 cup pasta water, then drain pasta and add it to the skillet.\n5. Toss with the juice of the whole lemon, parmesan, and a splash of pasta water until glossy.\n6. Top with more black pepper and eat immediately.',
        'ingredients': [
            ('spaghetti', 6, 'oz'),
            ('zucchini', 1, 'whole'),
            ('olive oil', 2, 'tbsp'),
            ('parmesan cheese', 0.25, 'cup'),
            ('lemon', 1, 'whole'),
            ('red pepper flakes', 0.25, 'tsp'),
            ('black pepper', 0.25, 'tsp'),
            ('salt', 1, 'pinch'),
        ],
    },
    {
        'name': 'Turkey Cabbage Stir-Fry Bowls', 'emoji': '🥬', 'meal_type': 'dinner',
        'time_minutes': 25, 'servings': 4, 'cost_total': 6.75,
        'calories': 330, 'protein_g': 24, 'carbs_g': 35, 'fat_g': 11,
        'sodium_mg': 450, 'potassium_mg': 480, 'phosphorus_mg': 205,
        'fiber_g': 3.2, 'sugar_g': 4.5, 'tags': ['diabetic', 'fodmap', 'kidney'],
        'description': 'Half a head of cabbage turns one pound of turkey into four honest dinners.',
        'instructions': '1. Cook rice: combine rice with 1.5 cups water, bring to a boil, cover, and simmer on low 15 minutes.\n2. Heat oil in your largest skillet over medium-high. Brown the ground turkey with black pepper and paprika, breaking it up, about 6 minutes.\n3. Add shredded cabbage and sliced bell pepper in batches, stirring as it wilts down, 6-8 minutes.\n4. Add soy sauce, rice vinegar, and a small pinch of salt; toss 1 minute.\n5. Serve over rice and hit it with more vinegar or pepper flakes if you like heat.',
        'ingredients': [
            ('ground turkey', 12, 'oz'),
            ('green cabbage', 0.5, 'head'),
            ('bell pepper', 1, 'whole'),
            ('white rice', 0.75, 'cup'),
            ('vegetable oil', 1, 'tbsp'),
            ('soy sauce', 1, 'tbsp'),
            ('rice vinegar', 1, 'tbsp'),
            ('paprika', 1, 'tsp'),
            ('black pepper', 0.5, 'tsp'),
            ('salt', 1, 'pinch'),
        ],
    },
    {
        'name': 'Green Bean Egg Rice Bowl', 'emoji': '🍚', 'meal_type': 'lunch',
        'time_minutes': 12, 'servings': 2, 'cost_total': 2.75,
        'calories': 410, 'protein_g': 15, 'carbs_g': 55, 'fat_g': 15,
        'sodium_mg': 410, 'potassium_mg': 365, 'phosphorus_mg': 225,
        'fiber_g': 4.5, 'sugar_g': 3, 'tags': ['fodmap', 'kidney', 'vegetarian'],
        'description': 'Leftover rice, three eggs, and a bag of frozen green beans become an actual lunch.',
        'instructions': '1. Microwave the green beans per bag directions, about 4 minutes, and reheat the cooked rice (leftover or instant both work).\n2. Heat vegetable oil in a skillet over medium. Scramble the eggs with black pepper until just set, about 2 minutes.\n3. Divide rice between two bowls and top with green beans and eggs.\n4. Whisk soy sauce, rice vinegar, and sesame oil; drizzle over the bowls.\n5. Finish with red pepper flakes.',
        'ingredients': [
            ('eggs', 3, 'whole'),
            ('cooked white rice', 2, 'cup'),
            ('frozen green beans', 2, 'cup'),
            ('soy sauce', 2, 'tsp'),
            ('rice vinegar', 2, 'tsp'),
            ('sesame oil', 1, 'tsp'),
            ('vegetable oil', 2, 'tsp'),
            ('red pepper flakes', 0.25, 'tsp'),
        ],
    },
    {
        'name': 'Cilantro Lime Chicken Bowls', 'emoji': '🍗', 'meal_type': 'lunch',
        'time_minutes': 20, 'servings': 4, 'cost_total': 6.95,
        'calories': 320, 'protein_g': 24, 'carbs_g': 42, 'fat_g': 6,
        'sodium_mg': 315, 'potassium_mg': 400, 'phosphorus_mg': 220,
        'fiber_g': 2.8, 'sugar_g': 4.5, 'tags': ['fodmap', 'kidney'],
        'description': 'Meal-prep bowls bright enough with lime that nobody misses the salt shaker.',
        'instructions': '1. Cook rice: combine rice with 1.5 cups water, bring to a boil, cover, and simmer on low 15 minutes.\n2. Dice chicken and toss with cumin, smoked paprika, and a small pinch of salt.\n3. Heat olive oil in a skillet over medium-high and cook chicken 5-6 minutes until cooked through.\n4. Add corn and diced bell pepper to the skillet and cook 3 minutes.\n5. Fluff rice with the juice of one lime and half the chopped cilantro.\n6. Divide rice into 4 bowls or containers, top with the chicken mixture, remaining cilantro, and juice from the second lime. Keeps 4 days in the fridge.',
        'ingredients': [
            ('chicken breast', 12, 'oz'),
            ('white rice', 0.75, 'cup'),
            ('frozen corn', 1.5, 'cup'),
            ('bell pepper', 1, 'whole'),
            ('lime', 2, 'whole'),
            ('cilantro', 0.25, 'bunch'),
            ('olive oil', 1, 'tbsp'),
            ('cumin', 1, 'tsp'),
            ('smoked paprika', 1, 'tsp'),
            ('salt', 1, 'pinch'),
        ],
    },
    {
        'name': 'Zucchini Lemon Chicken Rice Bowls', 'emoji': '🍚', 'meal_type': 'dinner',
        'time_minutes': 25, 'servings': 3, 'cost_total': 7.2,
        'calories': 685, 'protein_g': 53.3, 'carbs_g': 78, 'fat_g': 15.3,
        'sodium_mg': 305, 'potassium_mg': 885, 'phosphorus_mg': 465,
        'fiber_g': 2.3, 'sugar_g': 3, 'tags': ['fodmap'],
        'description': "Bright lemony chicken over rice, with garlic-infused oil doing the flavor heavy lifting so your gut doesn't have to.",
        'instructions': '1. Start 1.5 cups rice in a pot or rice cooker per package directions.\n2. Cut chicken breast into bite-size pieces and season with oregano, salt, and pepper.\n3. Heat 1 tbsp garlic-infused oil in a skillet over medium-high and cook chicken 6-7 minutes until cooked through.  Remove to a plate.\n4. Add remaining oil and the sliced zucchini to the same skillet.  Cook 4-5 minutes until browned at the edges.\n5. Return chicken to the pan, squeeze in the juice of the lemon, and toss 1 minute.\n6. Serve over rice and top with sliced green onion tops.',
        'ingredients': [
            ('chicken breast', 1, 'lb'),
            ('white rice', 1.5, 'cup'),
            ('zucchini', 2, 'whole'),
            ('garlic-infused olive oil', 2, 'tbsp'),
            ('lemon', 1, 'whole'),
            ('green onion tops', 0.25, 'cup'),
            ('dried oregano', 1, 'tsp'),
            ('salt', 0.25, 'tsp'),
            ('black pepper', 0.25, 'tsp'),
        ],
    },
    {
        'name': 'Cumin Beef Street Tacos', 'emoji': '🌮', 'meal_type': 'dinner',
        'time_minutes': 15, 'servings': 4, 'cost_total': 8.65,
        'calories': 515, 'protein_g': 29.3, 'carbs_g': 30.5, 'fat_g': 29.5,
        'sodium_mg': 575, 'potassium_mg': 475, 'phosphorus_mg': 560,
        'fiber_g': 3, 'sugar_g': 0.5, 'tags': ['diabetic', 'fodmap'],
        'description': 'Taco night that skips the garlicky seasoning packet and still slaps, cumin and lime carry the whole thing.',
        'instructions': '1. Brown 1 lb ground beef in a skillet over medium-high, about 6 minutes, then drain the fat.\n2. Stir in cumin, smoked paprika, salt, and a splash of water.  Simmer 2 minutes.\n3. Warm corn tortillas in a dry pan or directly over the burner, 20 seconds per side.\n4. Fill tortillas with beef, top with shredded cheddar and sliced green onion tops.\n5. Squeeze lime over everything and eat immediately.',
        'ingredients': [
            ('ground beef', 1, 'lb'),
            ('corn tortillas', 12, 'whole'),
            ('cheddar cheese', 1, 'cup'),
            ('green onion tops', 0.25, 'cup'),
            ('lime', 1, 'whole'),
            ('ground cumin', 1, 'tsp'),
            ('smoked paprika', 1, 'tsp'),
            ('salt', 0.5, 'tsp'),
        ],
    },
    {
        'name': 'Tuna Melt Microwave Potatoes', 'emoji': '🥔', 'meal_type': 'lunch',
        'time_minutes': 12, 'servings': 2, 'cost_total': 3.7,
        'calories': 605, 'protein_g': 27.5, 'carbs_g': 68, 'fat_g': 26,
        'sodium_mg': 600, 'potassium_mg': 1145, 'phosphorus_mg': 375,
        'fiber_g': 4.5, 'sugar_g': 3, 'tags': ['fodmap'],
        'description': 'A hot, cheesy tuna melt baked potato from the microwave in twelve minutes, dorm kitchen approved.',
        'instructions': '1. Stab each potato a few times with a fork and microwave on high 8-10 minutes, flipping once, until a fork slides in easily.\n2. While they cook, mix drained tuna with mayo, a pinch of salt, and black pepper.\n3. Split the potatoes open, mash in the butter, and season the flesh lightly.\n4. Pile the tuna mix on top, cover with shredded cheddar, and microwave 45 more seconds until melty.\n5. Finish with sliced green onion tops.',
        'ingredients': [
            ('russet potatoes', 2, 'whole'),
            ('canned tuna', 1, 'can'),
            ('cheddar cheese', 0.5, 'cup'),
            ('mayonnaise', 2, 'tbsp'),
            ('butter', 1, 'tbsp'),
            ('green onion tops', 2, 'tbsp'),
            ('salt', 0.125, 'tsp'),
            ('black pepper', 0.25, 'tsp'),
        ],
    },
    {
        'name': 'Green Onion Egg Quesadillas', 'emoji': '🧀', 'meal_type': 'lunch',
        'time_minutes': 10, 'servings': 2, 'cost_total': 2.75,
        'calories': 420, 'protein_g': 21, 'carbs_g': 20.5, 'fat_g': 26.5,
        'sodium_mg': 490, 'potassium_mg': 250, 'phosphorus_mg': 480,
        'fiber_g': 2, 'sugar_g': 1, 'tags': ['diabetic', 'fodmap', 'vegetarian'],
        'description': 'Scrambled eggs and sharp cheddar crisped inside corn tortillas, lunch for about a dollar a person.',
        'instructions': '1. Whisk eggs with salt, smoked paprika, and the sliced green onion tops.\n2. Heat half the garlic-infused oil in a skillet over medium and soft-scramble the eggs, about 2 minutes.  Set aside.\n3. Wipe the pan, add remaining oil, and lay in a corn tortilla.\n4. Top with a quarter of the cheddar, half the eggs, another quarter of the cheddar, and a second tortilla.\n5. Cook 2 minutes per side until crisp and melted, then repeat for the second quesadilla.  Cut into wedges.',
        'ingredients': [
            ('eggs', 4, 'whole'),
            ('corn tortillas', 4, 'whole'),
            ('cheddar cheese', 0.5, 'cup'),
            ('garlic-infused olive oil', 1, 'tbsp'),
            ('green onion tops', 2, 'tbsp'),
            ('smoked paprika', 0.25, 'tsp'),
            ('salt', 0.125, 'tsp'),
        ],
    },
    {
        'name': 'Paprika Chicken & Potato Tray Bake', 'emoji': '🍗', 'meal_type': 'dinner',
        'time_minutes': 40, 'servings': 4, 'cost_total': 6,
        'calories': 555, 'protein_g': 31, 'carbs_g': 35.5, 'fat_g': 30.8,
        'sodium_mg': 415, 'potassium_mg': 1215, 'phosphorus_mg': 320,
        'fiber_g': 4, 'sugar_g': 3.8, 'tags': ['diabetic', 'fodmap'],
        'description': 'One pan, five minutes of actual work, and the oven turns cheap chicken thighs into crispy-skinned dinner.',
        'instructions': '1. Heat oven to 425F and line a sheet pan with foil.\n2. Chop potatoes into 1-inch chunks and carrots into thick coins.  Toss with 1 tbsp olive oil, half the paprika, half the salt, and pepper.\n3. Rub chicken thighs with remaining oil, paprika, oregano, salt, and pepper.\n4. Arrange chicken skin-side up on the pan with veggies around it.\n5. Roast 30-35 minutes until chicken hits 165F and potatoes are browned.\n6. Squeeze lemon over the whole pan before serving.',
        'ingredients': [
            ('chicken thighs', 2, 'lb'),
            ('potatoes', 1.5, 'lb'),
            ('carrots', 4, 'whole'),
            ('olive oil', 2, 'tbsp'),
            ('smoked paprika', 2, 'tsp'),
            ('dried oregano', 1, 'tsp'),
            ('salt', 0.5, 'tsp'),
            ('black pepper', 0.5, 'tsp'),
            ('lemon', 1, 'whole'),
        ],
    },
    {
        'name': 'Savory Egg & Oats Bowl', 'emoji': '🍳', 'meal_type': 'breakfast',
        'time_minutes': 10, 'servings': 1, 'cost_total': 1,
        'calories': 315, 'protein_g': 14, 'carbs_g': 30, 'fat_g': 14,
        'sodium_mg': 400, 'potassium_mg': 505, 'phosphorus_mg': 340,
        'fiber_g': 6, 'sugar_g': 1, 'tags': ['diabetic', 'fodmap', 'vegetarian'],
        'description': 'Oatmeal went to culinary school and came back with a runny yolk on top.',
        'instructions': '1. Bring 1 cup water to a boil in a small pot, stir in oats and frozen spinach, and simmer 4-5 minutes until creamy.\n2. Season with a pinch of salt and the pepper, then stir in the parmesan.\n3. While the oats cook, heat oil in a small pan and fry the egg until the white is set but the yolk is still runny.\n4. Pour oats into a bowl, slide the egg on top, and break the yolk over everything.',
        'ingredients': [
            ('rolled oats', 0.5, 'cup'),
            ('eggs', 1, 'large'),
            ('frozen spinach', 0.5, 'cup'),
            ('parmesan cheese', 1, 'tbsp'),
            ('vegetable oil', 1, 'tsp'),
            ('salt', 1, 'pinch'),
            ('black pepper', 0.25, 'tsp'),
        ],
    },
    {
        'name': 'Tuna Cabbage Crunch Bowl', 'emoji': '🥗', 'meal_type': 'lunch',
        'time_minutes': 10, 'servings': 2, 'cost_total': 3.25,
        'calories': 300, 'protein_g': 24, 'carbs_g': 12, 'fat_g': 17,
        'sodium_mg': 630, 'potassium_mg': 600, 'phosphorus_mg': 245,
        'fiber_g': 4.6, 'sugar_g': 5.5, 'tags': ['diabetic', 'fodmap'],
        'description': 'No stove, no microwave, no excuses, just a crunchy protein bomb in ten minutes.',
        'instructions': '1. Shred the cabbage thin and grate the carrot into a large bowl.\n2. In a small bowl, stir together mayo, vinegar, a pinch of salt, and plenty of black pepper.\n3. Drain the tuna and flake it into the cabbage.\n4. Add the dressing, toss until everything is coated, and eat immediately or chill for extra crunch.',
        'ingredients': [
            ('canned tuna', 2, '5 oz can'),
            ('green cabbage', 4, 'cup shredded'),
            ('carrot', 1, 'medium'),
            ('mayonnaise', 3, 'tbsp'),
            ('white vinegar', 1, 'tbsp'),
            ('salt', 1, 'pinch'),
            ('black pepper', 0.5, 'tsp'),
        ],
    },
    {
        'name': 'Crispy Tuna-Oat Patties with Seared Cabbage', 'emoji': '🐟', 'meal_type': 'dinner',
        'time_minutes': 20, 'servings': 2, 'cost_total': 3,
        'calories': 320, 'protein_g': 26, 'carbs_g': 16, 'fat_g': 13,
        'sodium_mg': 610, 'potassium_mg': 550, 'phosphorus_mg': 305,
        'fiber_g': 4, 'sugar_g': 3, 'tags': ['diabetic', 'fodmap'],
        'description': 'Canned tuna cosplaying as crab cakes, and honestly pulling it off.',
        'instructions': '1. Drain the tuna well and mash it in a bowl with the egg, oats, mustard, a pinch of salt, and pepper.\n2. Let the mix sit 5 minutes so the oats soak up moisture, then form 4 patties.\n3. Heat half the oil in a skillet over medium and cook patties 3-4 minutes per side until deep golden. Set aside.\n4. Add remaining oil to the same skillet, throw in the shredded cabbage, and sear over medium-high 4-5 minutes until browned at the edges.\n5. Plate the cabbage, top with patties, and hit everything with black pepper.',
        'ingredients': [
            ('canned tuna', 2, '5 oz can'),
            ('eggs', 1, 'large'),
            ('rolled oats', 0.33, 'cup'),
            ('yellow mustard', 2, 'tsp'),
            ('green cabbage', 3, 'cup shredded'),
            ('vegetable oil', 1.5, 'tbsp'),
            ('salt', 1, 'pinch'),
            ('black pepper', 0.5, 'tsp'),
        ],
    },
    {
        'name': 'Smoky Lentil & Cabbage Skillet', 'emoji': '🍲', 'meal_type': 'dinner',
        'time_minutes': 35, 'servings': 4, 'cost_total': 2.8,
        'calories': 265, 'protein_g': 13, 'carbs_g': 39, 'fat_g': 4.5,
        'sodium_mg': 380, 'potassium_mg': 760, 'phosphorus_mg': 185,
        'fiber_g': 10.5, 'sugar_g': 6.5, 'tags': ['diabetic', 'vegetarian'],
        'description': 'Seventy cents a serving and it still shows up smoky, hearty, and smug about it.',
        'instructions': '1. Rinse the lentils. Heat oil in a large pot over medium, add the diced carrot, and cook 3 minutes.\n2. Add smoked paprika and cumin and stir 30 seconds until fragrant.\n3. Add lentils, canned tomatoes with their juice, 3 cups water, and the salt. Simmer 20 minutes.\n4. Stir in the chopped cabbage and simmer 8-10 more minutes until lentils are tender and the mix is stew-thick.\n5. Taste, add pepper, and serve in bowls.',
        'ingredients': [
            ('dry brown lentils', 1, 'cup'),
            ('green cabbage', 4, 'cup chopped'),
            ('canned diced tomatoes', 1, '14.5 oz can'),
            ('carrot', 1, 'medium'),
            ('vegetable oil', 1, 'tbsp'),
            ('smoked paprika', 2, 'tsp'),
            ('cumin', 1, 'tsp'),
            ('salt', 0.5, 'tsp'),
            ('black pepper', 0.5, 'tsp'),
        ],
    },
    {
        'name': 'Peanut Butter Cinnamon Stovetop Oats', 'emoji': '🥣', 'meal_type': 'breakfast',
        'time_minutes': 8, 'servings': 1, 'cost_total': 0.3,
        'calories': 250, 'protein_g': 9, 'carbs_g': 31, 'fat_g': 10,
        'sodium_mg': 220, 'potassium_mg': 270, 'phosphorus_mg': 225,
        'fiber_g': 5, 'sugar_g': 2.2, 'tags': ['diabetic', 'fodmap', 'kidney', 'vegetarian'],
        'description': 'Thirty cents, one pot, and it tastes like a warm peanut butter cookie that skipped the sugar.',
        'instructions': '1. Bring 1 cup water and a pinch of salt to a boil in a small pot.\n2. Stir in the oats and cinnamon, drop heat to low, and simmer 4-5 minutes, stirring once or twice.\n3. Kill the heat and stir in the peanut butter until melted and creamy.\n4. Scrape into a bowl and dust with a little extra cinnamon.',
        'ingredients': [
            ('rolled oats', 0.5, 'cup'),
            ('peanut butter', 1, 'tbsp'),
            ('cinnamon', 0.5, 'tsp'),
            ('salt', 1, 'pinch'),
        ],
    },
]
SEED_RECIPES.extend(DIET_PACK)

# Extended nutrition (per serving, estimates) + diet tags for the original
# recipes, same authoring/verification pass. Merged at import time.
SEED_NUTRITION = {
    'Veggie Scramble': {'sodium_mg': 530, 'potassium_mg': 500, 'phosphorus_mg': 400, 'fiber_g': 2, 'sugar_g': 3.5, 'tags': ['diabetic', 'fodmap', 'vegetarian']},
    'Overnight Oats with Berries': {'sodium_mg': 80, 'potassium_mg': 480, 'phosphorus_mg': 410, 'fiber_g': 8, 'sugar_g': 30, 'tags': ['vegetarian']},
    'Freezer Breakfast Burritos': {'sodium_mg': 1130, 'potassium_mg': 640, 'phosphorus_mg': 470, 'fiber_g': 3, 'sugar_g': 2.5, 'tags': []},
    'Chicken Caesar Wraps': {'sodium_mg': 1040, 'potassium_mg': 780, 'phosphorus_mg': 480, 'fiber_g': 3.5, 'sugar_g': 3, 'tags': ['diabetic']},
    'Hearty Lentil Soup': {'sodium_mg': 930, 'potassium_mg': 1000, 'phosphorus_mg': 320, 'fiber_g': 9.5, 'sugar_g': 4.5, 'tags': ['diabetic', 'vegetarian']},
    'Turkey Avocado Melt': {'sodium_mg': 1510, 'potassium_mg': 1000, 'phosphorus_mg': 500, 'fiber_g': 9.5, 'sugar_g': 3, 'tags': ['diabetic']},
    'Southwest Quinoa Bowl': {'sodium_mg': 320, 'potassium_mg': 1030, 'phosphorus_mg': 450, 'fiber_g': 11.5, 'sugar_g': 2.5, 'tags': ['vegetarian']},
    'Sheet-Pan Lemon Chicken & Veggies': {'sodium_mg': 420, 'potassium_mg': 1150, 'phosphorus_mg': 480, 'fiber_g': 6.5, 'sugar_g': 3.5, 'tags': ['diabetic']},
    'Spaghetti with Meat Sauce': {'sodium_mg': 950, 'potassium_mg': 780, 'phosphorus_mg': 440, 'fiber_g': 4, 'sugar_g': 7, 'tags': []},
    'Slow Cooker Beef Chili': {'sodium_mg': 680, 'potassium_mg': 1130, 'phosphorus_mg': 490, 'fiber_g': 7, 'sugar_g': 4.5, 'tags': ['diabetic']},
    'Baked Salmon, Rice & Broccoli': {'sodium_mg': 600, 'potassium_mg': 890, 'phosphorus_mg': 390, 'fiber_g': 4, 'sugar_g': 7, 'tags': ['diabetic']},
    'Veggie Tofu Stir-Fry': {'sodium_mg': 720, 'potassium_mg': 540, 'phosphorus_mg': 310, 'fiber_g': 3.6, 'sugar_g': 6, 'tags': ['diabetic', 'vegetarian']},
    'Loaded Baked Potato Night': {'sodium_mg': 450, 'potassium_mg': 990, 'phosphorus_mg': 280, 'fiber_g': 4.3, 'sugar_g': 2.5, 'tags': ['vegetarian']},
    'One-Pot Chicken Alfredo': {'sodium_mg': 960, 'potassium_mg': 680, 'phosphorus_mg': 630, 'fiber_g': 2.4, 'sugar_g': 5.4, 'tags': []},
    'Black Bean Quesadillas': {'sodium_mg': 1150, 'potassium_mg': 725, 'phosphorus_mg': 560, 'fiber_g': 12, 'sugar_g': 3.3, 'tags': ['vegetarian']},
    'Ground Beef Tacos': {'sodium_mg': 950, 'potassium_mg': 710, 'phosphorus_mg': 475, 'fiber_g': 3.8, 'sugar_g': 5, 'tags': ['diabetic']},
    'Egg Fried Rice': {'sodium_mg': 780, 'potassium_mg': 345, 'phosphorus_mg': 205, 'fiber_g': 3.5, 'sugar_g': 3, 'tags': ['vegetarian']},
    'Chicken Fajita Skillet': {'sodium_mg': 730, 'potassium_mg': 725, 'phosphorus_mg': 450, 'fiber_g': 4, 'sugar_g': 6, 'tags': ['diabetic']},
    'Baked Ziti': {'sodium_mg': 1175, 'potassium_mg': 700, 'phosphorus_mg': 540, 'fiber_g': 3, 'sugar_g': 5, 'tags': []},
    'Honey Garlic Chicken & Rice': {'sodium_mg': 820, 'potassium_mg': 400, 'phosphorus_mg': 230, 'fiber_g': 0.7, 'sugar_g': 13, 'tags': []},
    'Chickpea Coconut Curry': {'sodium_mg': 520, 'potassium_mg': 950, 'phosphorus_mg': 280, 'fiber_g': 7, 'sugar_g': 4.5, 'tags': ['vegetarian']},
    'Slow Cooker Pulled Pork Sandwiches': {'sodium_mg': 840, 'potassium_mg': 570, 'phosphorus_mg': 260, 'fiber_g': 1.5, 'sugar_g': 18, 'tags': []},
    'Chili Mac': {'sodium_mg': 800, 'potassium_mg': 700, 'phosphorus_mg': 480, 'fiber_g': 4, 'sugar_g': 3, 'tags': []},
    'Sausage & Veggie Sheet Pan': {'sodium_mg': 1000, 'potassium_mg': 1200, 'phosphorus_mg': 320, 'fiber_g': 5, 'sugar_g': 5, 'tags': ['diabetic']},
    'Tuna Pasta Salad': {'sodium_mg': 520, 'potassium_mg': 420, 'phosphorus_mg': 280, 'fiber_g': 4.5, 'sugar_g': 2.5, 'tags': ['diabetic']},
    'Greek Chicken Rice Bowls': {'sodium_mg': 620, 'potassium_mg': 850, 'phosphorus_mg': 400, 'fiber_g': 1.8, 'sugar_g': 3, 'tags': []},
    'Cold Peanut Noodles': {'sodium_mg': 830, 'potassium_mg': 500, 'phosphorus_mg': 285, 'fiber_g': 5, 'sugar_g': 8.5, 'tags': ['vegetarian']},
    'Peanut Butter Banana Smoothie': {'sodium_mg': 180, 'potassium_mg': 940, 'phosphorus_mg': 390, 'fiber_g': 5, 'sugar_g': 26, 'tags': ['vegetarian']},
    'Upgraded Ramen with Egg & Greens': {'sodium_mg': 1900, 'potassium_mg': 400, 'phosphorus_mg': 230, 'fiber_g': 3, 'sugar_g': 1.5, 'tags': []},
    'Grilled Cheese & Tomato Soup': {'sodium_mg': 1550, 'potassium_mg': 670, 'phosphorus_mg': 410, 'fiber_g': 3.8, 'sugar_g': 21.7, 'tags': ['vegetarian']},
}
for _r in SEED_RECIPES:
    _r.update(SEED_NUTRITION.get(_r['name'], {}))
