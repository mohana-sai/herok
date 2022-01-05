import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# initializing flask
app = Flask(__name__)

# Load the model to flask in read mode
model = pickle.load(open('model.pkl', 'rb'))

# creating a home function to redirect to root that is index file
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output))


@app.route('/predict_api', methods=['GET'])
def predict_api():
    '''
    For direct API calls request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)