import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Create folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Start date
start_date = datetime(2024, 10, 1)

# Food list (non-negotiable + gluten, lactose, eggs, beans)
foods = [
    'roti', 'paratha', 'bread', 'pasta', 'naan', 'whole wheat bread',
    'paneer curry', 'curd', 'milk', 'butter chicken',
    'boiled eggs', 'omelette', 'egg curry',
    'rajma', 'chole', 'dal', 'beans curry',
    'idli', 'dosa', 'rice', 'chicken curry', 'fish', 'vegetables', 'salad',
    'overnight oats', 'poha', 'upma', 'biryani', 'pulao'
]

# Meal context options
meal_times = ['Morning', 'Afternoon', 'Evening']
portions = ['Small', 'Medium', 'Large']
coffee_options = ['Yes', 'No']
sleep_options = ['Poor', 'Okay', 'Good']
stress_options = ['Low', 'Medium', 'High']
locations = ['Home', 'Restaurant', 'Office', 'Street']

# Symptom options (non-negotiable)
symptom_types = ['None', 'Bloating', 'Gas', 'Acidity', 'Fatigue', 'Brain fog', 'Nausea', 'Bowel movement']

data = []
meal_id = 1

# Generate 90 days, 2-3 meals per day
for day in range(90):
    current_date = start_date + timedelta(days=day)
    meals_today = random.randint(2, 3)
    
    # Daily state (affects all meals)
    daily_sleep = random.choice(sleep_options)
    daily_stress = random.choice(stress_options)
    
    for meal_num in range(meals_today):
        # Meal time
        meal_time = meal_times[meal_num]
        
        # Pick food and context
        food = random.choice(foods)
        portion = random.choice(portions)
        had_coffee = random.choice(coffee_options)
        location = random.choice(locations)
        
        # Base symptom chance
        symptom_chance = 0.05  # much lower base
        
        # Trigger increments (realistic)
        gluten_foods = ['roti', 'paratha', 'bread', 'pasta', 'naan', 'whole wheat bread']
        dairy_foods = ['paneer curry', 'curd', 'milk', 'butter chicken']
        egg_foods = ['boiled eggs', 'omelette', 'egg curry']
        bean_foods = ['rajma', 'chole', 'dal', 'beans curry', 'overnight oats']
        
        if food in gluten_foods:
            symptom_chance += 0.2
        if food in dairy_foods:
            symptom_chance += 0.25
        if food in egg_foods:
            symptom_chance += 0.15
        if food in bean_foods:
            symptom_chance += 0.15
        if had_coffee == 'Yes':
            symptom_chance += 0.15
        if portion == 'Large':
            symptom_chance += 0.1
        if daily_sleep == 'Poor':
            symptom_chance += 0.15
        elif daily_sleep == 'Okay':
            symptom_chance += 0.05
        if daily_stress == 'High':
            symptom_chance += 0.15
        elif daily_stress == 'Medium':
            symptom_chance += 0.05
        if meal_time == 'Evening' and portion == 'Large':
            symptom_chance += 0.1
        if location == 'Street':
            symptom_chance += 0.1
        
        symptom_chance = min(symptom_chance, 0.9)
        
        # Determine if symptom occurs
        has_symptom = random.random() < symptom_chance
        
        if has_symptom:
            if food in dairy_foods:
                symptom = random.choice(['Bloating', 'Gas', 'Acidity', 'Nausea'])
            elif food in gluten_foods:
                symptom = random.choice(['Bloating', 'Fatigue', 'Brain fog', 'Bowel movement'])
            elif food in egg_foods:
                symptom = random.choice(['Bloating', 'Fatigue', 'Nausea'])
            elif food in bean_foods:
                symptom = random.choice(['Bloating', 'Gas', 'Bowel movement'])
            elif had_coffee == 'Yes':
                symptom = random.choice(['Acidity', 'Fatigue', 'Nausea'])
            else:
                symptom = random.choice(['Bloating', 'Gas', 'Acidity', 'Fatigue', 'Nausea', 'Bowel movement'])
            
            severity = random.randint(3, 10)
            hours_after = random.randint(1, 4)
        else:
            symptom = 'None'
            severity = 0
            hours_after = 0
        
        data.append({
            'meal_id': meal_id,
            'date': current_date.strftime('%Y-%m-%d'),
            'meal_time': meal_time,
            'food': food,
            'portion_size': portion,
            'had_coffee': had_coffee,
            'sleep_quality': daily_sleep,
            'stress_level': daily_stress,
            'location': location,
            'symptom': symptom,
            'symptom_severity': severity,
            'hours_after_meal': hours_after
        })
        
        meal_id += 1

# Create DataFrame
df = pd.DataFrame(data)

# Save
df.to_csv('data/foodsense_meals_symptoms.csv', index=False)

print(f"✅ Generated {len(df)} meal records over 90 days")
print(f"✅ Total symptoms: {len(df[df['symptom'] != 'None'])}")
print(f"✅ Symptom rate: {len(df[df['symptom'] != 'None']) / len(df) * 100:.1f}%")
print("\n📊 Breakdown by symptom type:")
print(df['symptom'].value_counts())

