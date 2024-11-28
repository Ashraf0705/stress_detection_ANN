import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Load the trained model and scaler
MODEL_PATH = 'detection/ml/models/stress_model.h5'
SCALER_PATH = 'detection/ml/models/scaler.pkl'

model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def predict_stress(input_data):
    """
    Predicts stress level based on input data.

    Parameters:
    input_data (list): A list containing the following parameters in order:
        [Snoring Rate, Respiratory Rate, Body Temperature, Limb Movement, 
         Blood Oxygen, Eye Movement, Sleep Hours, Heart Rate]

    Returns:
    str: 'Detected' if stress is present, otherwise 'Not Detected'.
    """
    # Normalize the input data
    input_data = np.array(input_data).reshape(1, -1)
    scaled_data = scaler.transform(input_data)
    
    # Make a prediction
    prediction = model.predict(scaled_data)
    
    # Interpret the result
    if prediction[0][0] > 0.5:  # Assuming sigmoid activation in the output layer
        return "Detected"
    else:
        return "Not Detected"

if __name__ == "__main__":
    # Example input: replace with real test data
    sample_input = [3.5, 16.0, 36.5, 5.0, 95.0, 0.5, 7.0, 72.0]
    result = predict_stress(sample_input)
    print("Stress Prediction:", result)
