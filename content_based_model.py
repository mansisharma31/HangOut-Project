import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import tensorflow as tf
import numpy as np
import os
import joblib  # For saving encoders and scaler

print("Loading data...")
data_path = 'places_data.csv'
df = pd.read_csv(data_path)

# Preprocess categorical data
print("Encoding categorical data...")
encoder_location = OneHotEncoder(sparse_output=False)
encoded_location = encoder_location.fit_transform(df[['location']])

encoder_category = OneHotEncoder(sparse_output=False)
encoded_category = encoder_category.fit_transform(df[['category']])

# Normalize numerical data
print("Normalizing numerical data...")
scaler = StandardScaler()
normalized_price_duration = scaler.fit_transform(df[['price', 'duration']])

# Combine all features
print("Combining features...")
features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

# Map 'id' to a sequential range of values
print("Mapping item IDs to sequential labels...")
unique_ids = sorted(df['id'].unique())
id_to_label = {item_id: idx for idx, item_id in enumerate(unique_ids)}
labels = df['id'].map(id_to_label).values

# Define the model
num_classes = len(unique_ids)
print("Defining the model with", num_classes, "output classes...")
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(features.shape[1],)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

print("Compiling the model...")
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

print("Training the model...")
model.fit(features, labels, epochs=10, batch_size=8, validation_split=0.2)

# Save the trained model
print("Saving the model and preprocessing objects...")
os.makedirs("models", exist_ok=True)
model.save('models/content_model.h5')

# Save encoders and scaler for use in recommendation_test.py
joblib.dump(encoder_location, 'models/encoder_location.pkl')
joblib.dump(encoder_category, 'models/encoder_category.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
print("Model and preprocessing objects saved.")




# # content_based_model.py
# import pandas as pd
# from sklearn.preprocessing import OneHotEncoder, StandardScaler
# import tensorflow as tf
# import numpy as np
# import os

# print("Loading data...")
# data_path = 'places_data.csv'
# df = pd.read_csv(data_path)

# # Preprocess categorical data (e.g., location, category)
# print("Encoding categorical data...")
# encoder_location = OneHotEncoder(sparse_output=False)
# encoded_location = encoder_location.fit_transform(df[['location']])

# encoder_category = OneHotEncoder(sparse_output=False)
# encoded_category = encoder_category.fit_transform(df[['category']])

# # Normalize numerical data (e.g., price, duration)
# print("Normalizing numerical data...")
# scaler = StandardScaler()
# normalized_price_duration = scaler.fit_transform(df[['price', 'duration']])

# # Combine all features into a single dataset
# print("Combining features...")
# features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

# # Map 'id' to a sequential range of values
# print("Mapping item IDs to sequential labels...")
# unique_ids = sorted(df['id'].unique())
# id_to_label = {item_id: idx for idx, item_id in enumerate(unique_ids)}
# labels = df['id'].map(id_to_label).values

# # Define the model
# num_classes = len(unique_ids)
# print("Defining the model with", num_classes, "output classes...")
# model = tf.keras.models.Sequential([
#     tf.keras.layers.Dense(128, activation='relu', input_shape=(features.shape[1],)),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dense(num_classes, activation='softmax')
# ])

# print("Compiling the model...")
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# print("Training the model...")
# model.fit(features, labels, epochs=10, batch_size=8, validation_split=0.2)

# # Save the trained model
# print("Saving the model...")
# os.makedirs("models", exist_ok=True)
# model.save('models/content_model.h5')
# print("Model saved as 'content_model.h5' in the 'models' folder.")




# # content_based_model.py
# import pandas as pd
# from sklearn.preprocessing import OneHotEncoder, StandardScaler
# import tensorflow as tf
# import numpy as np
# import os

# print("Loading data...")
# data_path = 'places_data.csv'  # Ensure the CSV file is in the same folder as this script
# df = pd.read_csv(data_path)

# # Preprocess categorical data (e.g., location, category)
# print("Encoding categorical data...")
# encoder_location = OneHotEncoder(sparse_output=False)
# encoded_location = encoder_location.fit_transform(df[['location']])

# encoder_category = OneHotEncoder(sparse_output=False)
# encoded_category = encoder_category.fit_transform(df[['category']])

# # Normalize numerical data (e.g., price, duration)
# print("Normalizing numerical data...")
# scaler = StandardScaler()
# normalized_price_duration = scaler.fit_transform(df[['price', 'duration']])

# # Combine all features into a single dataset
# print("Combining features...")
# features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

# # Map 'id' to a sequential range of values
# print("Mapping item IDs to sequential labels...")
# unique_ids = sorted(df['id'].unique())
# id_to_label = {item_id: idx for idx, item_id in enumerate(unique_ids)}
# labels = df['id'].map(id_to_label).values

# # Define the model
# num_classes = len(unique_ids)
# print("Defining the model with", num_classes, "output classes...")
# model = tf.keras.models.Sequential([
#     tf.keras.layers.Dense(128, activation='relu', input_shape=(features.shape[1],)),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dense(num_classes, activation='softmax')  # Output layer with classes for each item
# ])

# print("Compiling the model...")
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# print("Training the model...")
# model.fit(features, labels, epochs=10, batch_size=8, validation_split=0.2)

# # Save the trained model
# print("Saving the model...")
# os.makedirs("models", exist_ok=True)
# model.save('models/content_model.h5')
# print("Model saved as 'content_model.h5' in the 'models' folder.")




# # content_based_model.py
# import pandas as pd
# from sklearn.preprocessing import OneHotEncoder, StandardScaler
# import tensorflow as tf
# import numpy as np
# import os

# print("Loading data...")
# data_path = 'places_data.csv'  # Ensure the CSV file is in the same folder as this script
# df = pd.read_csv(data_path)

# # Preprocess categorical data (e.g., location, category)
# print("Encoding categorical data...")
# encoder_location = OneHotEncoder(sparse_output=False)
# encoded_location = encoder_location.fit_transform(df[['location']])

# encoder_category = OneHotEncoder(sparse_output=False)
# encoded_category = encoder_category.fit_transform(df[['category']])

# # Normalize numerical data (e.g., price, duration)
# print("Normalizing numerical data...")
# scaler = StandardScaler()
# normalized_price_duration = scaler.fit_transform(df[['price', 'duration']])

# # Combine all features into a single dataset
# print("Combining features...")
# features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

# # Labels (Item IDs) - These serve as targets for learning item embeddings
# labels = df['id'].values

# print("Defining the model...")
# model = tf.keras.models.Sequential([
#     tf.keras.layers.Dense(128, activation='relu', input_shape=(features.shape[1],)),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dense(len(labels), activation='softmax')  # Output layer with classes for each item ID
# ])

# print("Compiling the model...")
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# print("Training the model...")
# model.fit(features, labels, epochs=10, batch_size=8, validation_split=0.2)

# # Save the trained model
# print("Saving the model...")
# os.makedirs("models", exist_ok=True)
# model.save('models/content_model.h5')
# print("Model saved as 'content_model.h5' in the 'models' folder.")





# # content_based_model.py
# import pandas as pd
# from sklearn.preprocessing import OneHotEncoder, StandardScaler
# import tensorflow as tf
# import numpy as np
# import os

# # Load the CSV data file
# data_path = 'places_data.csv'  # Make sure the CSV file is in the same folder as this script
# df = pd.read_csv(data_path)

# # Check the data to understand its structure
# print(df.head())

# # One-hot encode categorical data (e.g., location, category)
# encoder = OneHotEncoder(sparse_output=False)
# encoded_location = encoder.fit_transform(df[['location']])
# encoded_category = encoder.fit_transform(df[['category']])

# # Normalize numerical data (e.g., price, duration)
# scaler = StandardScaler()
# normalized_price_duration = scaler.fit_transform(df[['price', 'duration']])

# # Combine all features into a single dataset
# features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

# # Labels (Item IDs) - These serve as targets for learning item embeddings
# labels = df['id'].values

# # Confirm shapes of features and labels
# print("Features shape:", features.shape)
# print("Labels shape:", labels.shape)

# # Define a simple neural network model
# model = tf.keras.models.Sequential([
#     tf.keras.layers.Dense(128, activation='relu', input_shape=(features.shape[1],)),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dense(len(labels), activation='softmax')  # Output layer with classes for each item ID
# ])

# # Compile the model
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# # Train the model
# model.fit(features, labels, epochs=10, batch_size=8, validation_split=0.2)

# # Ensure the models directory exists
# os.makedirs("models", exist_ok=True)

# # Save the trained model
# model.save('models/content_model.h5')
# print("Model saved as 'content_model.h5' in the 'models' folder.")






# # content_based_model.py
# import pandas as pd
# from sklearn.preprocessing import OneHotEncoder, StandardScaler
# import tensorflow as tf
# import numpy as np
# import os

# # Load CSV data
# data_path = 'places_data.csv'
# df = pd.read_csv(data_path)

# # Preprocessing categorical data (location, category)
# encoder = OneHotEncoder(sparse=False)
# encoded_location = encoder.fit_transform(df[['location']])
# encoded_category = encoder.fit_transform(df[['category']])

# # Normalizing numerical data (price, duration)
# scaler = StandardScaler()
# normalized_price_duration = scaler.fit_transform(df[['price', 'duration']])

# # Combine all features into a single dataset
# features = np.hstack([encoded_location, encoded_category, normalized_price_duration])

# # Labels (Item IDs) - used as targets for learning item embeddings
# labels = df['id'].values

# # Define a simple neural network model
# model = tf.keras.models.Sequential([
#     tf.keras.layers.Dense(128, activation='relu', input_shape=(features.shape[1],)),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dense(len(labels), activation='softmax')  # Output layer with classes for each item ID
# ])

# # Compile the model
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# # Train the model
# model.fit(features, labels, epochs=10, batch_size=8, validation_split=0.2)

# # Save the trained model
# os.makedirs("models", exist_ok=True)
# model.save('models/content_model.h5')
# print("Model saved as 'content_model.h5' in the 'models' folder.")
