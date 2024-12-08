import requests
import csv
import time
import json
from sklearn.metrics import confusion_matrix, classification_report

# Endpoint of the server
url = "http://localhost:8000/predict"

# File of data
file_path = "test.csv"

# Initialize lists to store expected and predicted activities
expected_activities = []
predicted_activities = []

# Function to send data
def send_data(data):
    headers = {"Content-Type": "application/json"}
    payload = {
        "acceleration_x": float(data["acceleration_x"]),
        "acceleration_y": float(data["acceleration_y"]),
        "acceleration_z": float(data["acceleration_z"]),
        "gyro_x": float(data["gyro_x"]),
        "gyro_y": float(data["gyro_y"]),
        "gyro_z": float(data["gyro_z"])
    }
    expected_activity = data["activity"]  # The activity from the csv file
    expected_activities.append(int(expected_activity))  # Append to expected list
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()  # Assuming the server returns a JSON response
        
        # Confront the activity against the anwser
        predicted_activity = int(response_data.get("prediction"))  # Adapt this key to your response JSON
        predicted_activities.append(predicted_activity)  # Append to predicted list
        
        match = "CORRECT" if str(predicted_activity) == expected_activity else "INCORRECT"
        print(f"Expected: {expected_activity}, Predicted: {predicted_activity}, Match: {match}")
        
    except Exception as e:
        print(f"Errore durante l'invio dei dati: {e}")

# Load the csv file
with open(file_path, mode='r') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        send_data(row)
        time.sleep(0.1)  # Do a break between sending the data

# Calculate and display the confusion matrix
if expected_activities and predicted_activities:
    print("\nConfusion Matrix:")
    print(confusion_matrix(expected_activities, predicted_activities))
    
    print("\nClassification Report:")
    print(classification_report(expected_activities, predicted_activities))
else:
    print("No data to calculate confusion matrix.")