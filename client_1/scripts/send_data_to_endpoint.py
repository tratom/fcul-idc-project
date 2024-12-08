import requests
import csv
import time
import json
from sklearn.metrics import confusion_matrix, classification_report

# Endpoint del server
url = "http://localhost:8000/predict"

# File dei dati
file_path = "test.csv"

# Initialize lists to store expected and predicted activities
expected_activities = []
predicted_activities = []

# Funzione per inviare dati
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
    expected_activity = data["activity"]  # L'attività attesa dal CSV
    expected_activities.append(int(expected_activity))  # Append to expected list
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()  # Supponendo che il server restituisca una risposta JSON
        
        # Confronta l'attività attesa con la risposta
        predicted_activity = int(response_data.get("prediction"))  # Adatta questa chiave al tuo JSON di risposta
        predicted_activities.append(predicted_activity)  # Append to predicted list
        
        match = "CORRECT" if str(predicted_activity) == expected_activity else "INCORRECT"
        print(f"Expected: {expected_activity}, Predicted: {predicted_activity}, Match: {match}")
        
    except Exception as e:
        print(f"Errore durante l'invio dei dati: {e}")

# Legge i dati dal file CSV e invia le richieste
with open(file_path, mode='r') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        send_data(row)
        time.sleep(0.1)  # Pausa tra le richieste per evitare sovraccarico del server

# Calculate and display the confusion matrix
if expected_activities and predicted_activities:
    print("\nConfusion Matrix:")
    print(confusion_matrix(expected_activities, predicted_activities))
    
    print("\nClassification Report:")
    print(classification_report(expected_activities, predicted_activities))
else:
    print("No data to calculate confusion matrix.")