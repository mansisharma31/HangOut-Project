import tensorflow as tf
import numpy as np
import pandas as pd
import joblib  # For loading encoders and scaler
from itertools import permutations

# Load the saved model and preprocessing objects
model = tf.keras.models.load_model('models/content_model.h5')
encoder_location = joblib.load('models/encoder_location.pkl')
encoder_category = joblib.load('models/encoder_category.pkl')
scaler = joblib.load('models/scaler.pkl')

# Load and preprocess data to get original place details
df = pd.read_csv('places_data.csv')

# ID-to-label mapping from content_based_model.py
id_to_label = {item_id: idx for idx, item_id in enumerate(sorted(df['id'].unique()))}
label_to_id = {idx: item_id for item_id, idx in id_to_label.items()}


# def generate_itineraries_with_age_group(location, budget, duration, age_groups, category=None, top_n=3):
#     # Your existing processing logic
    
#     itineraries_with_scores = []
#     for itinerary in all_itineraries:
#         itinerary_score = sum(predictions[df[df['id'] == place['id']].index[0]] for place in itinerary)
#         itineraries_with_scores.append((itinerary, itinerary_score))

#     # Sort itineraries by score and return the top N
#     itineraries_with_scores.sort(key=lambda x: x[1], reverse=True)

#     top_itineraries = []
#     for i, (itinerary, score) in enumerate(itineraries_with_scores[:top_n]):
#         itinerary_details = {
#             'score': score,
#             'places': []
#         }
#         total_duration = 0
#         total_price = 0
#         for place in itinerary:
#             itinerary_details['places'].append({
#                 'name': place['name'],
#                 'category': place['category'],
#                 'duration': place['duration'],
#                 'price': place['price']
#             })
#             total_duration += place['duration']
#             total_price += place['price']
        
#         itinerary_details['total_duration'] = total_duration
#         itinerary_details['total_price'] = total_price
#         top_itineraries.append(itinerary_details)

#     return top_itineraries


def generate_itineraries_with_age_group(location, budget, duration, age_groups, category=None, top_n=3):
    # Transform location based on user input
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
        lambda x: any(group in x for group in age_groups))]  # Change 'age_group' to 'age'

    # Separate dining places from the rest
    dining_places = filtered_places[filtered_places['category'] == 'dining']
    other_places = filtered_places[filtered_places['category'] != 'dining']
    
    # If duration is >= 2 hours, ensure at least one dining place is included
    if duration >= 2 and dining_places.empty:
        print("Warning: No dining places available for this duration, please check your data!")
        return

    all_itineraries = []

    # Generate possible itineraries by including a dining place
    for dining_place in dining_places.iterrows():
        dining_place = dining_place[1]  # Extract the place data
        
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
        
        if current_duration <= duration and current_budget <= budget and selected_places:
            all_itineraries.append(selected_places)
    
    # Sort itineraries by model predictions
    itineraries_with_scores = []
    for itinerary in all_itineraries:
        itinerary_score = sum(predictions[df[df['id'] == place['id']].index[0]] for place in itinerary)
        itineraries_with_scores.append((itinerary, itinerary_score))
    
    # Sort itineraries by score and return the top N
    itineraries_with_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Display the top itineraries
    for i, (itinerary, score) in enumerate(itineraries_with_scores[:top_n]):
        print(f"--- Itinerary {i+1} (Score: {score:.2f}) ---")
        total_duration = 0
        total_price = 0
        for place in itinerary:
            print(f"Place: {place['name']}, Category: {place['category']}, Duration: {place['duration']} hours, Price: {place['price']}")
            total_duration += place['duration']
            total_price += place['price']
        print(f"Total Duration: {total_duration} hours")
        print(f"Total Price: {total_price}")
        print("------")


# Example usage
user_location = 'New Delhi'       # Replace with user input
user_category = 'dining'          # Replace with user input or None if no preference
user_age_groups = ['41-65', '65 and above']  # Replace with user input (multiple age groups can be selected)
max_budget = 1000                 # Replace with user input
max_duration = 5                  # Replace with user input (in hours)
top_n_recommendations = 3         # Number of itineraries to return

generate_itineraries_with_age_group(user_location, max_budget, max_duration, user_age_groups, user_category, top_n=top_n_recommendations)

# def generate_itineraries(location, budget, duration, category=None, top_n=3):
#     # Transform location based on user input
#     encoded_location = encoder_location.transform([[location]])
#     encoded_category = encoder_category.transform([[category]]) if category else np.zeros((1, encoder_category.categories_[0].size))
    
#     # Normalize budget and duration
#     normalized_price_duration = scaler.transform([[budget, duration]])
    
#     # Combine all features for user input
#     user_features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

#     # Predict using the loaded model
#     predictions = model.predict(user_features)[0]

#     # Filter places based on budget, duration, and location
#     filtered_places = df[
#         (df['price'] <= budget) &
#         (df['duration'] <= duration) &
#         (df['location'] == location) &
#         ((df['category'] == category) if category else True)  # Category is optional
#     ]
    
#     # Separate dining places from the rest
#     dining_places = filtered_places[filtered_places['category'] == 'dining']
#     other_places = filtered_places[filtered_places['category'] != 'dining']
    
#     # If duration is >= 2 hours, ensure at least one dining place is included
#     if duration >= 2 and dining_places.empty:
#         print("Warning: No dining places available for this duration, please check your data!")
#         return

#     all_itineraries = []

#     # Generate possible itineraries by including a dining place
#     for dining_place in dining_places.iterrows():
#         dining_place = dining_place[1]  # Extract the place data
        
#         current_duration = dining_place['duration']
#         current_budget = dining_place['price']
#         selected_places = [dining_place]
        
#         remaining_duration = duration - current_duration
#         remaining_budget = budget - current_budget
        
#         # Loop over other places and fill the remaining duration and budget
#         for _, place in other_places.iterrows():
#             if current_duration + place['duration'] <= duration and current_budget + place['price'] <= budget:
#                 selected_places.append(place)
#                 current_duration += place['duration']
#                 current_budget += place['price']
            
#             if current_duration >= duration or current_budget >= budget:
#                 break
        
#         if current_duration <= duration and current_budget <= budget and selected_places:
#             all_itineraries.append(selected_places)
    
#     # Sort itineraries by model predictions
#     itineraries_with_scores = []
#     for itinerary in all_itineraries:
#         itinerary_score = sum(predictions[df[df['id'] == place['id']].index[0]] for place in itinerary)
#         itineraries_with_scores.append((itinerary, itinerary_score))
    
#     # Sort itineraries by score and return the top N
#     itineraries_with_scores.sort(key=lambda x: x[1], reverse=True)
    
#     # Display the top itineraries
#     for i, (itinerary, score) in enumerate(itineraries_with_scores[:top_n]):
#         print(f"--- Itinerary {i+1} (Score: {score:.2f}) ---")
#         total_duration = 0
#         total_price = 0
#         for place in itinerary:
#             print(f"Place: {place['name']}, Category: {place['category']}, Duration: {place['duration']} hours, Price: {place['price']}")
#             total_duration += place['duration']
#             total_price += place['price']
#         print(f"Total Duration: {total_duration} hours")
#         print(f"Total Price: {total_price}")
#         print("------")

# # Example usage
# user_location = 'New Delhi'       # Replace with user input
# user_category = None             # Replace with user input or None if no preference
# max_budget = 1000000                 # Replace with user input
# max_duration = 10                  # Replace with user input (in hours)
# top_n_recommendations = 5        # Number of itineraries to return

#generate_itineraries(user_location, max_budget, max_duration, user_category, top_n=top_n_recommendations)

# def generate_itineraries(location, budget, duration, category=None, top_n=3):
#     # Transform location based on user input
#     encoded_location = encoder_location.transform([[location]])
#     encoded_category = encoder_category.transform([[category]]) if category else np.zeros((1, encoder_category.categories_[0].size))
    
#     # Normalize budget and duration
#     normalized_price_duration = scaler.transform([[budget, duration]])
    
#     # Combine all features for user input
#     user_features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

#     # Predict using the loaded model
#     predictions = model.predict(user_features)[0]

#     # Filter places based on budget, duration, and location
#     filtered_places = df[
#         (df['price'] <= budget) &
#         (df['duration'] <= duration) &
#         (df['location'] == location) &
#         ((df['category'] == category) if category else True)  # Category is optional
#     ]

#     # Group places by categories
#     categories = filtered_places['category'].unique()
#     categorized_places = {cat: filtered_places[filtered_places['category'] == cat] for cat in categories}

#     # Generate all possible combinations of places that fit the duration and budget
#     all_itineraries = []

#     # Loop over different category combinations
#     for cat_perm in permutations(categories, len(categories)):
#         current_duration = 0
#         current_budget = 0
#         selected_places = []
        
#         for cat in cat_perm:
#             category_places = categorized_places[cat]
#             for _, place in category_places.iterrows():
#                 if current_duration + place['duration'] <= duration and current_budget + place['price'] <= budget:
#                     selected_places.append(place)
#                     current_duration += place['duration']
#                     current_budget += place['price']
#                 if current_duration >= duration:
#                     break
#             if current_duration >= duration:
#                 break
        
#         if current_duration <= duration and current_budget <= budget and selected_places:
#             all_itineraries.append(selected_places)
    
#     # Get the top N itineraries based on their total prediction score
#     itineraries_with_scores = []
#     for itinerary in all_itineraries:
#         # Calculate the total score for the itinerary based on model predictions
#         itinerary_score = sum(predictions[df[df['id'] == place['id']].index[0]] for place in itinerary)
#         itineraries_with_scores.append((itinerary, itinerary_score))
    
#     # Sort itineraries by score and return the top N
#     itineraries_with_scores.sort(key=lambda x: x[1], reverse=True)
    
#     # Display the top itineraries
#     for i, (itinerary, score) in enumerate(itineraries_with_scores[:top_n]):
#         print(f"--- Itinerary {i+1} (Score: {score:.2f}) ---")
#         total_duration = 0
#         total_price = 0
#         for place in itinerary:
#             print(f"Place: {place['name']}, Category: {place['category']}, Duration: {place['duration']} hours, Price: {place['price']}")
#             total_duration += place['duration']
#             total_price += place['price']
#         print(f"Total Duration: {total_duration} hours")
#         print(f"Total Price: {total_price}")
#         print("------")

# # Example usage
# user_location = 'New Delhi'       # Replace with user input
# user_category = None              # Replace with user input or None if no preference
# max_budget = 1000                 # Replace with user input
# max_duration = 5                  # Replace with user input (in hours)
# top_n_recommendations = 3         # Number of itineraries to return

# generate_itineraries(user_location, max_budget, max_duration, user_category, top_n=top_n_recommendations)

# def recommend_places(location, budget, duration, category=None, top_n=5):
#     # Transform location and category based on user input
#     encoded_location = encoder_location.transform([[location]])
#     encoded_category = encoder_category.transform([[category]]) if category else np.zeros((1, encoder_category.categories_[0].size))
    
#     # Normalize budget and duration
#     normalized_price_duration = scaler.transform([[budget, duration]])
    
#     # Combine all features for user input
#     user_features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

#     # Predict using the loaded model
#     predictions = model.predict(user_features)[0]

#     # Filter places based on budget, duration, category, and location
#     filtered_places = df[
#         (df['price'] <= budget) &
#         (df['duration'] <= duration) &
#         (df['location'] == location) &  # Add location filter
#         ((df['category'] == category) if category else True)  # Category is optional
#     ]

#     # Map filtered place IDs to model prediction indices
#     filtered_indices = [id_to_label[place_id] for place_id in filtered_places['id'] if place_id in id_to_label]
#     filtered_predictions = predictions[filtered_indices]

#     # Get top N recommendations based on filtered predictions
#     if len(filtered_predictions) < top_n:
#         top_n = len(filtered_predictions)  # Adjust if fewer than requested places are available
#     top_indices = np.argsort(filtered_predictions)[-top_n:][::-1]  # Top N sorted in descending order

#     # Get recommended place IDs
#     recommended_place_ids = [label_to_id[filtered_indices[idx]] for idx in top_indices]

#     # Retrieve and display details of recommended places
#     recommended_places = df[df['id'].isin(recommended_place_ids)]
#     for _, place in recommended_places.iterrows():
#         print(f"Place ID: {place['id']}")
#         print(f"Name: {place.get('name', 'N/A')}")
#         print(f"Location: {place['location']}")
#         print(f"Category: {place['category']}")
#         print(f"Price: {place['price']}")
#         print(f"Duration: {place['duration']} hours")
#         print("------")

# # Example usage
# user_location = 'New Delhi'       # Replace with user input
# user_category = None        # Replace with user input or None if no preference
# max_budget = 1000                # Replace with user input
# max_duration = 2                 # Replace with user input
# top_n_recommendations = 15    # Number of recommendations to return

# recommend_places(user_location, max_budget, max_duration, user_category, top_n=top_n_recommendations)


# def recommend_places(location, budget, duration, category=None, top_n=5):
#     # Transform location and category based on user input
#     encoded_location = encoder_location.transform([[location]])
#     encoded_category = encoder_category.transform([[category]]) if category else np.zeros((1, encoder_category.categories_[0].size))
    
#     # Normalize budget and duration
#     normalized_price_duration = scaler.transform([[budget, duration]])
    
#     # Combine all features for user input
#     user_features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

#     # Predict using the loaded model
#     predictions = model.predict(user_features)[0]

#     # Filter places based on budget, duration, and category criteria
#     filtered_places = df[
#         (df['price'] <= budget) &
#         (df['duration'] <= duration) &
#         ((df['category'] == category) if category else True)  # Category is optional
#     ]

#     # Map filtered place IDs to model prediction indices
#     filtered_indices = [id_to_label[place_id] for place_id in filtered_places['id'] if place_id in id_to_label]
#     filtered_predictions = predictions[filtered_indices]

#     # Get top N recommendations based on filtered predictions
#     if len(filtered_predictions) < top_n:
#         top_n = len(filtered_predictions)  # Adjust if less than requested places are available
#     top_indices = np.argsort(filtered_predictions)[-top_n:][::-1]  # Top N sorted in descending order

#     # Get recommended place IDs
#     recommended_place_ids = [label_to_id[filtered_indices[idx]] for idx in top_indices]

#     # Retrieve and display details of recommended places
#     recommended_places = df[df['id'].isin(recommended_place_ids)]
#     for _, place in recommended_places.iterrows():
#         print(f"Place ID: {place['id']}")
#         print(f"Name: {place.get('name', 'N/A')}")
#         print(f"Location: {place['location']}")
#         print(f"Category: {place['category']}")
#         print(f"Price: {place['price']}")
#         print(f"Duration: {place['duration']} hours")
#         print("------")

# # Example usage
# user_location = 'Banglore'       # Replace with user input
# user_category = 'dining'         # Replace with user input or None if no preference
# max_budget = 1000                # Replace with user input
# max_duration = 2                 # Replace with user input
# top_n_recommendations = 3        # Number of recommendations to return

# recommend_places(user_location, max_budget, max_duration, user_category, top_n=top_n_recommendations)


# def recommend_places(location, budget, duration, category=None, top_n=5):
#     # Transform location and category based on user input
#     encoded_location = encoder_location.transform([[location]])
#     encoded_category = encoder_category.transform([[category]]) if category else np.zeros((1, encoder_category.categories_[0].size))
    
#     # Normalize budget and duration
#     normalized_price_duration = scaler.transform([[budget, duration]])
    
#     # Combine all features for user input
#     user_features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

#     # Predict using the loaded model
#     predictions = model.predict(user_features)[0]

#     # Filter places based on budget, duration, and category criteria
#     filtered_places = df[
#         (df['price'] <= budget) &
#         (df['duration'] <= duration) &
#         ((df['category'] == category) if category else True)  # Category is optional
#     ]

#     # Map filtered place IDs to model prediction indices
#     filtered_indices = [id_to_label[place_id] for place_id in filtered_places['id'] if place_id in id_to_label]
#     filtered_predictions = predictions[filtered_indices]

#     # Get top N recommendations based on prediction probabilities
#     top_indices = np.argsort(filtered_predictions)[-top_n:][::-1]  # Top N sorted in descending order

#     # Get recommended place IDs
#     recommended_place_ids = [label_to_id[idx] for idx in top_indices]

#     # Retrieve and display details of recommended places
#     recommended_places = df[df['id'].isin(recommended_place_ids)]
#     for _, place in recommended_places.iterrows():
#         print(f"Place ID: {place['id']}")
#         print(f"Name: {place.get('name', 'N/A')}")
#         print(f"Location: {place['location']}")
#         print(f"Category: {place['category']}")
#         print(f"Price: {place['price']}")
#         print(f"Duration: {place['duration']} hours")
#         print("------")

# # Example usage
# user_location = 'Banglore'       # Replace with user input
# user_category = 'dining'         # Replace with user input or None if no preference
# max_budget = 1000                # Replace with user input
# max_duration = 2                 # Replace with user input
# top_n_recommendations = 3        # Number of recommendations to return

# recommend_places(user_location, max_budget, max_duration, user_category, top_n=top_n_recommendations)





# import tensorflow as tf
# import numpy as np
# import pandas as pd
# import joblib  # For loading encoders and scaler

# # Load the saved model and preprocessing objects
# model = tf.keras.models.load_model('models/content_model.h5')
# encoder_location = joblib.load('models/encoder_location.pkl')
# encoder_category = joblib.load('models/encoder_category.pkl')
# scaler = joblib.load('models/scaler.pkl')

# # Load and preprocess data to get original place details
# df = pd.read_csv('places_data.csv')

# # ID-to-label mapping from content_based_model.py
# id_to_label = {item_id: idx for idx, item_id in enumerate(sorted(df['id'].unique()))}
# label_to_id = {idx: item_id for item_id, idx in id_to_label.items()}

# def recommend_places(location, budget, duration, category=None, top_n=5):
#     # Transform location and category based on user input
#     encoded_location = encoder_location.transform([[location]])
#     encoded_category = encoder_category.transform([[category]]) if category else np.zeros((1, encoder_category.categories_[0].size))
    
#     # Normalize budget and duration
#     normalized_price_duration = scaler.transform([[budget, duration]])
    
#     # Combine all features for user input
#     user_features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

#     # Predict using the loaded model
#     predictions = model.predict(user_features)[0]

#     # Filter places based on budget, duration, and category criteria
#     filtered_places = df[
#         (df['price'] <= budget) &
#         (df['duration'] <= duration) &
#         ((df['category'] == category) if category else True)  # Category is optional
#     ]

#     # Map filtered place IDs to model prediction indices
#     filtered_indices = [id_to_label[place_id] for place_id in filtered_places['id'] if place_id in id_to_label]
#     filtered_predictions = predictions[filtered_indices]

#     # Get top N recommendations based on prediction probabilities
#     top_indices = np.argsort(filtered_predictions)[-top_n:][::-1]  # Top N sorted in descending order

#     # Get recommended place IDs
#     recommended_place_ids = [label_to_id[idx] for idx in top_indices]

#     return recommended_place_ids

# # Example usage
# user_location = 'Banglore'       # Replace with user input
# user_category = 'dining'         # Replace with user input or None if no preference
# max_budget = 1000                # Replace with user input
# max_duration = 2                 # Replace with user input
# top_n_recommendations = 3        # Number of recommendations to return

# recommended_place_ids = recommend_places(user_location, max_budget, max_duration, user_category, top_n=top_n_recommendations)

# if recommended_place_ids:
#     print("Recommended Place IDs:", recommended_place_ids)
# else:
#     print("No suitable places found.")




# import pandas as pd
# import tensorflow as tf
# import numpy as np
# import joblib  # For loading encoders and scaler

# # Load the saved model and preprocessing objects
# model = tf.keras.models.load_model('models/content_model.h5')
# encoder_location = joblib.load('models/encoder_location.pkl')
# encoder_category = joblib.load('models/encoder_category.pkl')
# scaler = joblib.load('models/scaler.pkl')

# # Load the dataset
# data_path = 'places_data.csv'
# df = pd.read_csv(data_path)

# def recommend_place(location, category, budget, duration):
#     # Filter the DataFrame based on user inputs
#     filtered_df = df[(df['location'].str.lower() == location.lower()) &
#                      (df['price'] <= budget) &
#                      (df['duration'] <= duration)]
    
#     # Check if filtered_df is empty
#     if filtered_df.empty:
#         print("No places found matching the specified location, budget, and duration.")
#         return None

#     # Preprocess the filtered data for model prediction
#     encoded_locations = encoder_location.transform(filtered_df[['location']])
#     encoded_categories = encoder_category.transform(filtered_df[['category']])
#     normalized_price_duration = scaler.transform(filtered_df[['price', 'duration']])

#     # Combine all features
#     filtered_features = np.hstack([encoded_locations, encoded_categories, normalized_price_duration])

#     # Generate predictions for each place in the filtered data
#     predictions = model.predict(filtered_features)
#     recommended_index = np.argmax(predictions)

#     # Ensure recommended_index is within bounds
#     if recommended_index < len(filtered_df):
#         recommended_item = filtered_df.iloc[recommended_index]
#         return recommended_item
#     else:
#         print("Recommended index is out of bounds.")
#         return None

# # Example of using recommend_place function
# user_location = 'Banglore'  # Replace with user input
# user_category = 'dining'      # Replace with user input
# max_budget = 700           # Replace with user input
# max_duration = 2            # Replace with user input

# recommended_place = recommend_place(user_location, user_category, max_budget, max_duration)
# if recommended_place is not None:
#     print("Recommended Place:")
#     print(recommended_place)
# else:
#     print("No suitable place found.")



# import tensorflow as tf
# import numpy as np
# import joblib  # For loading encoders and scaler

# # Load the saved model and preprocessing objects
# model = tf.keras.models.load_model('models/content_model.h5')
# encoder_location = joblib.load('models/encoder_location.pkl')
# encoder_category = joblib.load('models/encoder_category.pkl')
# scaler = joblib.load('models/scaler.pkl')

# # ID-to-label mapping from content_based_model.py
# id_to_label = {0: 'id1', 1: 'id2', 2: 'id3'}  # Replace with actual mapping

# def recommend_place(location, category, budget, duration):
#     # Transform location and category based on user input
#     encoded_location = encoder_location.transform([[location]])
#     encoded_category = encoder_category.transform([[category]])

#     # Normalize budget and duration
#     normalized_price_duration = scaler.transform([[budget, duration]])

#     # Combine all features
#     user_features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

#     # Predict using the loaded model
#     predictions = model.predict(user_features)
#     recommended_index = np.argmax(predictions)

#     # Retrieve recommended item ID using label-to-id mapping from training
#     label_to_id = {idx: item_id for item_id, idx in id_to_label.items()}
#     recommended_item_id = label_to_id.get(recommended_index)

#     return recommended_item_id

# # Example usage
# user_location = 'Banglore'       # Replace with user input
# user_category = 'dining'           # Replace with user input
# max_budget = 700               # Replace with user input
# max_duration = 2                 # Replace with user input

# recommended_place_id = recommend_place(user_location, user_category, max_budget, max_duration)

# if recommended_place_id is not None:
#     print("Recommended Place ID:", recommended_place_id)
# else:
#     print("No suitable place found.")




# import pandas as pd
# import tensorflow as tf
# import numpy as np
# import joblib  # For loading encoders and scaler

# # Load the saved model and preprocessing objects
# model = tf.keras.models.load_model('models/content_model.h5')
# encoder_location = joblib.load('models/encoder_location.pkl')
# encoder_category = joblib.load('models/encoder_category.pkl')
# scaler = joblib.load('models/scaler.pkl')

# def recommend_place(location, budget, duration):
#     # Transform location and category based on user input
#     encoded_location = encoder_location.transform([[location]])
#     encoded_category = encoder_category.transform([['category']])  # Assume a placeholder category for prediction

#     # Normalize budget and duration
#     normalized_price_duration = scaler.transform([[budget, duration]])

#     # Combine all features
#     user_features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

#     # Predict using the loaded model
#     predictions = model.predict(user_features)
#     recommended_index = np.argmax(predictions)

#     # Retrieve recommended item ID using label-to-id mapping from training
#     label_to_id = {idx: item_id for item_id, idx in id_to_label.items()}
#     recommended_item_id = label_to_id.get(recommended_index)

#     return recommended_item_id

# # Example usage
# user_location = 'Banglore'  # Replace with user input
# max_budget = 1000           # Replace with user input
# max_duration = 2            # Replace with user input

# recommended_place_id = recommend_place(user_location, max_budget, max_duration)

# if recommended_place_id is not None:
#     print("Recommended Place ID:", recommended_place_id)
# else:
#     print("No suitable place found.")



# # recommendation_test.py
# import pandas as pd
# from sklearn.preprocessing import OneHotEncoder, StandardScaler
# import tensorflow as tf
# import numpy as np

# # Load CSV data for feature extraction
# data_path = 'places_data.csv'
# df = pd.read_csv(data_path)

# # Preprocess categorical data
# encoder_location = OneHotEncoder(sparse_output=False)
# encoded_location = encoder_location.fit_transform(df[['location']])

# encoder_category = OneHotEncoder(sparse_output=False)
# encoded_category = encoder_category.fit_transform(df[['category']])

# # Normalize numerical data
# scaler = StandardScaler()
# normalized_price_duration = scaler.fit_transform(df[['price', 'duration']])

# # Combine all features
# features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

# # Load the saved model
# model = tf.keras.models.load_model('models/content_model.h5')

# def recommend_place(location, budget, duration):
#     # Filter the DataFrame based on user inputs
#     filtered_df = df[(df['location'].str.lower() == location.lower()) &
#                      (df['price'] <= budget) &
#                      (df['duration'] <= duration)]

#     # Check if filtered_df is empty
#     if filtered_df.empty:
#         print("No places found matching the specified location, budget, and duration.")
#         return None

#     # Extract relevant features for model prediction
#     filtered_df_features = filtered_df[['price', 'duration']]

#     # Generate predictions
#     predictions = model.predict_proba(filtered_df_features)[:, 1]  # Use probability for recommendation
#     recommended_index = np.argmax(predictions)

#     # Ensure recommended_index is within bounds
#     if recommended_index < len(filtered_df):
#         recommended_item = filtered_df.iloc[recommended_index]
#         return recommended_item
#     else:
#         print("Recommended index is out of bounds.")
#         return None


    # Preprocess the filtered features
    # encoded_location = encoder_location.transform(filtered_df[['location']])
    # encoded_category = encoder_category.transform(filtered_df[['category']])
    # normalized_price_duration = scaler.transform(filtered_df[['price', 'duration']])
    
    # filtered_features = np.hstack([encoded_location, encoded_category, normalized_price_duration])
    
    # # Get predictions for each item in the filtered data
    # predictions = model.predict(filtered_features)
    
    # # Get the index of the highest-scored item for each recommendation
    # recommended_index = np.argmax(predictions, axis=1)
    # recommended_items = filtered_df.iloc[recommended_index]
    
    # return recommended_items

# # Example of using recommend_place function
# user_location = 'Banglore'  # Replace with user input
# max_budget = 1000        # Replace with user input
# max_duration = 2         # Replace with user input

# recommended_places = recommend_place(user_location, max_budget, max_duration)
# if recommended_places is not None:
#     print("Recommended Places:")
#     print(recommended_places)



# # recommendation_test.py
# import pandas as pd
# from sklearn.preprocessing import OneHotEncoder, StandardScaler
# import tensorflow as tf
# import numpy as np

# # Load the CSV data for feature extraction
# data_path = 'places_data.csv'
# df = pd.read_csv(data_path)

# # Preprocess categorical data (e.g., location, category)
# encoder_location = OneHotEncoder(sparse_output=False)
# encoded_location = encoder_location.fit_transform(df[['location']])

# encoder_category = OneHotEncoder(sparse_output=False)
# encoded_category = encoder_category.fit_transform(df[['category']])

# # Normalize numerical data (e.g., price, duration)
# scaler = StandardScaler()
# normalized_price_duration = scaler.fit_transform(df[['price', 'duration']])

# # Combine all features into a single dataset
# features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

# # Load the saved model
# model = tf.keras.models.load_model('models/content_model.h5')

# # Generate recommendations for a sample item (e.g., first item in the dataset)
# sample_item_features = features[9].reshape(1, -1)  # Reshape to match input shape

# # Get model predictions
# predictions = model.predict(sample_item_features)
# recommended_item_index = np.argmax(predictions)

# # Display recommended item details
# recommended_item = df.iloc[recommended_item_index]
# print("Recommended Item:")
# print(recommended_item)

