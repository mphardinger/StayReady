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
