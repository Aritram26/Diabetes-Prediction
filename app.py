# app.py
from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the model and scaler with error handling
try:
    model = pickle.load(open('model.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))
except FileNotFoundError:
    print("Error: Model or scaler files not found.")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)

@app.route('/', methods=['GET', 'POST'])
def predict():
    prediction = None
    if request.method == 'POST':
        # Input validation and handling for missing or null values
        try:
            preg = int(request.form['preg'])
            plas = int(request.form['plas'])
            pres = int(request.form['pres'])
            skin = int(request.form['skin'])
            test = int(request.form['test'])
            mass = float(request.form['mass'])
            pedi = float(request.form['pedi'])
            age = int(request.form['age'])
        except ValueError:
            print("Error: Invalid input values.")
            return render_template('index.html', prediction="Error: Invalid input values.")
        
        # Prepare the feature array
        features = np.array([[preg, plas, pres, skin, test, mass, pedi, age]])
        features = scaler.transform(features)
        
        # Make prediction
        try:
            prediction = model.predict(features)[0]
            prediction = "Positive" if prediction == 1 else "Negative"
        except Exception as e:
            print(f"Error: {e}")
            return render_template('index.html', prediction="Error: Prediction failed.")
    
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)