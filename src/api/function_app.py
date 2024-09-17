import logging
import json
import requests
import azure.functions as func

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now you can access the environment variables
env_model_url = os.getenv('MODEL_ENDPOINT_URL')
env_model_key = os.getenv('MODEL_KEY')

class PostClassifier:
    @staticmethod
    def classify_post(post_text):
        """
        Classify the given post text.
        
        Args:
            post_text (str): The text of the post to classify.
        
        Returns:
            dict: A dictionary containing the response data and status code.
        """
        if not isinstance(post_text, str):
            return {
                "body": "Input must be a string",
                "status_code": 400
            }

        if not post_text:
            return {
                "body": "Please provide a non-empty text for classification",
                "status_code": 400
            }

        try:
            # this should be the endpoint of the deployed model
            model_url = env_model_url
            model_key = env_model_key
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {model_key}'
            }
            data = json.dumps({"text": post_text})
            
            response = requests.post(model_url, data=data, headers=headers)
            response.raise_for_status()
            
            return {
                "body": response.text,
                "status_code": 200
            }
        except requests.exceptions.RequestException as e:
            return {
                "body": f"Error processing request: {str(e)}",
                "status_code": 500
            }

# ... rest of the file remains the same ...
# Check if we're using the newer programming model
if hasattr(func, 'FunctionApp'):
    app = func.FunctionApp()

    @app.function_name(name="ClassifyPost")
    @app.route(route="classify_post", auth_level=func.AuthLevel.FUNCTION)
    def classify_post_function(req: func.HttpRequest) -> func.HttpResponse:
        logging.info('Python HTTP trigger function processed a request.')

        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                "Invalid JSON in request body",
                status_code=400
            )

        post_text = req_body.get('text')
        if not post_text:
            return func.HttpResponse(
                "Please pass a 'text' property in the request body",
                status_code=400
            )

        result = PostClassifier.classify_post(post_text)
        
        return func.HttpResponse(
            body=result["body"],
            status_code=result["status_code"],
            mimetype="application/json"
        )
else:
    # Older programming model
    def main(req: func.HttpRequest) -> func.HttpResponse:
        logging.info('Python HTTP trigger function processed a request.')

        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                "Invalid JSON in request body",
                status_code=400
            )

        post_text = req_body.get('text')
        if not post_text:
            return func.HttpResponse(
                "Please pass a 'text' property in the request body",
                status_code=400
            )

        result = PostClassifier.classify_post(post_text)
        
        return func.HttpResponse(
            body=result["body"],
            status_code=result["status_code"],
            mimetype="application/json"
        )

if __name__ == "__main__":
    # This is for local testing
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    @app.route("/api/classify_post", methods=["POST"])
    def classify_post_local():
        post_text = request.json.get('text', '')
        result = PostClassifier.classify_post(post_text)
        return jsonify(result["body"]), result["status_code"]
    
    app.run(debug=True, port=7071)