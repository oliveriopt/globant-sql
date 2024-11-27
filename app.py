from flask import Flask, request, jsonify
import requests
import pandas as pd
from io import StringIO

app = Flask(__name__)

# Lambda URLs
LAMBDA_URL_1 = "https://iqcfqrojtvytayjd7a7oofx4ia0rohab.lambda-url.us-east-2.on.aws/"
LAMBDA_URL_2 = "https://incunbm66qxyn2cu562vpweg3y0loejd.lambda-url.us-east-2.on.aws/"

@app.route('/call-lambda-1', methods=['GET'])
def call_lambda_1():
    try:
        response = requests.get(LAMBDA_URL_1)
        response.raise_for_status()  # Raise an error if the request failed
        
        lambda_1_data = response.json()
        
        return jsonify({"lambda_1_response": lambda_1_data["results"]})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/call-lambda-2', methods=['GET'])
def call_lambda_2():
    try:
        response = requests.get(LAMBDA_URL_2)

        response.raise_for_status()  # Raise an error if the request failed
        
        lambda_2_data = response.json()
        
        return jsonify({"lambda_2_response": lambda_2_data["results"]})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
