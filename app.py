from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import joblib
import pandas as pd
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the model and other necessary objects
model = tf.keras.models.load_model('../model_training/models/content_model.h5')
encoder_location = joblib.load('../model_training/models/encoder_location.pkl')
encoder_category = joblib.load('../model_training/models/encoder_category.pkl')
scaler = joblib.load('../model_training/models/scaler.pkl')
df = pd.read_csv('../model_training/places_data.csv')

# Your recommendation function (same as before)
def generate_itineraries_with_age_group(location, budget, duration, age_groups, category=None, top_n=3):
    # Encode location and category
    encoded_location = encoder_location.transform([[location]])
    encoded_category = encoder_category.transform([[category]]) if category else np.zeros((1, encoder_category.categories_[0].size))
    
    # Normalize budget and duration
    normalized_price_duration = scaler.transform([[budget, duration]])
    
    # Combine all features for user input
    user_features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

    # Predict using the loaded model
    predictions = model.predict(user_features)[0]

    # Filter places based on budget, duration, location, and age group
    filtered_places = df[
        (df['price'] <= budget) &
        (df['duration'] <= duration) &
        (df['location'] == location) &
        ((df['category'] == category) if category else True)  # Category is optional
    ]
    
    # Filter places by age group
    filtered_places = filtered_places[filtered_places['age'].apply(
        lambda x: any(group in x for group in age_groups))]

    # Separate dining places from the rest
    dining_places = filtered_places[filtered_places['category'] == 'dining']
    other_places = filtered_places[filtered_places['category'] != 'dining']
    
    # Check if a dining place is needed but unavailable
    if duration >= 2 and dining_places.empty:
        return {"error": "No dining places available for the specified duration and budget."}

    all_itineraries = []

    # Generate possible itineraries by including a dining place
    for _, dining_place in dining_places.iterrows():
        current_duration = dining_place['duration']
        current_budget = dining_place['price']
        selected_places = [dining_place]
        
        remaining_duration = duration - current_duration
        remaining_budget = budget - current_budget
        
        # Loop over other places and fill the remaining duration and budget
        for _, place in other_places.iterrows():
            if current_duration + place['duration'] <= duration and current_budget + place['price'] <= budget:
                selected_places.append(place)
                current_duration += place['duration']
                current_budget += place['price']
            
            if current_duration >= duration or current_budget >= budget:
                break
        
        # If itinerary is valid, add it to all_itineraries
        if selected_places:
            all_itineraries.append(selected_places)
    
    # Sort itineraries by model predictions
    itineraries_with_scores = []
    for itinerary in all_itineraries:
        itinerary_score = sum(predictions[df[df['id'] == place['id']].index[0]] for place in itinerary)
        itineraries_with_scores.append((itinerary, itinerary_score))
    
    # Sort itineraries by score and return the top N
    itineraries_with_scores.sort(key=lambda x: x[1], reverse=True)

    # Structure itineraries for JSON response
    recommendations = []
    for itinerary, score in itineraries_with_scores[:top_n]:
        itinerary_details = {
            "score": score,
            "places": [
                {
                    "name": place["name"],
                    "category": place["category"],
                    "duration": place["duration"],
                    "price": place["price"]
                }
                for _, place in itinerary
            ],
            "total_duration": sum(place["duration"] for _, place in itinerary),
            "total_price": sum(place["price"] for _, place in itinerary)
        }
        recommendations.append(itinerary_details)
    
    return recommendations
  # E.g., [{'score': 9.5, 'places': [...]}, ...]

# Define the API route
@app.route('/api/getRecommendations', methods=['POST'])
def get_recommendations():
    data = request.json  # Get JSON data from request
    location = data.get('location')
    budget = float(data.get('budget'))
    duration = float(data.get('duration'))
    age_groups = data.get('ageGroups')
    category = data.get('category', None)  # Optional
    print("backend")

    # Get recommendations
    recommendations = generate_itineraries_with_age_group(
        location, budget, duration, age_groups, category, top_n=3
    )

    # Send recommendations as JSON response
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)

