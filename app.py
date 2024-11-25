from flask import Flask, request, jsonify
import requests
import pandas as pd
from io import StringIO

app = Flask(__name__)

# Lambda URLs
LAMBDA_URL_1 = "https://iqcfqrojtvytayjd7a7oofx4ia0rohab.lambda-url.us-east-2.on.aws/"
LAMBDA_URL_2 = "https://incunbm66qxyn2cu562vpweg3y0loejd.lambda-url.us-east-2.on.aws/"


@app.route('/call-lambda-2', methods=['GET'])
def call_lambda_2():
    # Get inputs from query parameters
    input_string = request.args.get('input_string', default='', type=str)
    year = request.args.get('year', default=0, type=int)

    # Validate inputs
    if not input_string or not year:
        return jsonify({"error": "Both 'input_string' and 'year' are required."}), 400

    try:
        response = requests.get(LAMBDA_URL_2, params={"input_string": input_string, "year": year})
        response.raise_for_status()  # Raise an error if the request failed
        
        # Convert the JSON response into a pandas DataFrame
        lambda_2_data = response.json()
        df_lambda_2 = json_to_dataframe(lambda_2_data)
        
        # Convert the DataFrame to JSON and return
        return jsonify({"lambda_2_response": df_lambda_2.to_dict(orient='records')})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
