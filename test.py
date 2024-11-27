import unittest
from unittest.mock import patch
from flask import jsonify
import json

# Import the app from the application module
from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.client = app.test_client()
        self.client.testing = True

    @patch('app.requests.get')
    def test_call_lambda_1_success(self, mock_get):
        # Mock a successful response from Lambda 1
        mock_response = {
            "results": {"message": "Lambda 1 success"}
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        # Call the endpoint
        response = self.client.get('/call-lambda-1')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"lambda_1_response": mock_response["results"]})

    @patch('app.requests.get')
    def test_call_lambda_1_failure(self, mock_get):
        # Mock a failed response from Lambda 1
        mock_get.side_effect = Exception("Lambda 1 failed")
        
        # Call the endpoint
        response = self.client.get('/call-lambda-1')
        
        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json)

    @patch('app.requests.get')
    def test_call_lambda_2_success(self, mock_get):
        # Mock a successful response from Lambda 2
        mock_response = {
            "results": {"message": "Lambda 2 success"}
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        # Call the endpoint
        response = self.client.get('/call-lambda-2')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"lambda_2_response": mock_response["results"]})

    @patch('app.requests.get')
    def test_call_lambda_2_failure(self, mock_get):
        # Mock a failed response from Lambda 2
        mock_get.side_effect = Exception("Lambda 2 failed")
        
        # Call the endpoint
        response = self.client.get('/call-lambda-2')
        
        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json)


if __name__ == '__main__':
    unittest.main()
