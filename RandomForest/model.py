import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import itertools

def find_optimal_combination(partial_input):
    """
    Find the combination of missing inputs that maximizes the predicted score.

    Args:
    model: Trained Random Forest model.
    partial_input (dict): Partial input provided by the user.

    Returns:
    dict: Combination of inputs that maximizes the score.
    float: The maximum predicted score.
    """
    # Load the dataset
    file_path = 'RandomForest/recommendation_system_dataset.csv'
    df = load_dataset(file_path)
    # Splitting the data into train and test sets
    X = df.drop('score', axis=1)
    y = df['score']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Training the model
    model = train_random_forest(X_train, y_train)
    # Model Evaluation
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)
    # Define the possible values for each component
    possible_values = {
        'intro_component': [4, 5, 6],
        'education_component': [1, 2, 3],
        'work_component': [12, 13, 15],
        'portfolio_component': [7, 8, 14],
        'skills_component': [9, 10, 11]
    }

    # Remove the keys already provided by the user
    for key in partial_input:
        possible_values.pop(key, None)

    # Generate all possible combinations for the missing components
    keys, values = zip(*possible_values.items())
    combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]

    # Initialize variables to store the best combination and its score
    best_combination = None
    max_score = -1

    # Evaluate each combination
    for combination in combinations:
        # Merge the user input with the current combination
        full_input = {**partial_input, **combination}
        predicted_score = make_prediction(model, full_input)

        # Update the best combination if a higher score is found
        if predicted_score > max_score:
            max_score = predicted_score
            best_combination = full_input

    return best_combination, max_score



# Function to load the dataset
def load_dataset(file_path):
    return pd.read_csv(file_path)

# Function to train the Random Forest model
def train_random_forest(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=0)
    model.fit(X_train, y_train)
    return model

# Function for making predictions
def make_prediction(model, input_data):
    input_df = pd.DataFrame([input_data])
    return model.predict(input_df)[0]