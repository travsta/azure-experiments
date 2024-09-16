import azure.functions as func
import logging
import json
import requests

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
        if not post_text:
            return {
                "body": "Please provide a non-empty text for classification",
                "status_code": 400
            }

        try:
            # this should be the endpoint of the deployed model
            model_url = "MODEL_ENDPOINT_URL"
            model_key = "MODEL_KEY"
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
                "body": "Error processing request",
                "status_code": 500
            }

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