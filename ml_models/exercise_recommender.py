import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import random
import os

# Load exercise data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
exercise_data_path = os.path.join(BASE_DIR, 'ml_models/exercise_data.csv')

exercise_data = pd.read_csv(exercise_data_path)

# Body part to muscle group mapping
muscle_group_parts = {
    'Legs': ['Abductors', 'Adductors', 'Calves', 'Glutes', 'Hamstrings', 'Quadriceps'],
    'Back': ['Lats', 'Lower Back', 'Middle Back', 'Traps'],
    'Chest': ['Chest'],
    'Shoulders': ['Shoulders'],
    'Abdominals': ['Abdominals'],
    'Arms': ['Triceps', 'Biceps', 'Forearms']
}

# Encode categorical columns
le_bodypart = LabelEncoder()
le_level = LabelEncoder()

exercise_data['BodyPart_Code'] = le_bodypart.fit_transform(exercise_data['BodyPart'])
exercise_data['Level_Code'] = le_level.fit_transform(exercise_data['Level'])

# Features and target
X = exercise_data[['BodyPart_Code', 'Level_Code']]
y = exercise_data['Title']

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)


def get_exercise_recommendation(muscle_group, level, total_exercises=8):
    # Encode inputs
    body_parts = muscle_group_parts.get(muscle_group, [])
    level_code = le_level.transform([level])[0]

    recommended_exercises = []

    for body_part in body_parts:
        body_part_code = le_bodypart.transform([body_part])[0]

        # Filter possible exercises
        possible_exercises = exercise_data[
            (exercise_data['BodyPart'] == body_part) &
            (exercise_data['Level'] == level)
            ]

        if not possible_exercises.empty:
            # Predict exercises
            predictions = model.predict([[body_part_code, level_code]] * len(possible_exercises))
            unique_predictions = list(set(predictions))
            part_exercises = random.sample(unique_predictions,
                                           min(total_exercises // len(body_parts), len(unique_predictions)))

            for exercise in part_exercises:
                exercise_info = possible_exercises[possible_exercises['Title'] == exercise]
                if not exercise_info.empty:
                    equipment = exercise_info['Equipment'].iloc[0]
                    body_part_desc = exercise_info['BodyPart'].iloc[0]
                    description = exercise_info['Desc'].iloc[0]
                    recommended_exercises.append((exercise, equipment, body_part_desc, description))

    # Fill remaining exercises if needed
    remaining_exercises = total_exercises - len(recommended_exercises)
    if remaining_exercises > 0 and not possible_exercises.empty:
        extra_exercises = random.sample(possible_exercises['Title'].tolist(), remaining_exercises)
        for exercise in extra_exercises:
            exercise_info = possible_exercises[possible_exercises['Title'] == exercise]
            if not exercise_info.empty:
                equipment = exercise_info['Equipment'].iloc[0]
                body_part_desc = exercise_info['BodyPart'].iloc[0]
                description = exercise_info['Desc'].iloc[0]
                recommended_exercises.append((exercise, equipment, body_part_desc, description))

    return recommended_exercises
