import azure.functions as func
import logging
import json
import requests

app = func.FunctionApp()

@app.route(route="classify_post")
def classify_post(req: func.HttpRequest) -> func.HttpResponse:
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
        
        return func.HttpResponse(
            response.text,
            mimetype="application/json",
            status_code=200
        )
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling model endpoint: {str(e)}")
        return func.HttpResponse(
            "Error processing request",
            status_code=500
        )

if __name__ == "__main__":
    # This is for local testing
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    @app.route("/api/classify_post", methods=["POST"])
    def classify_post_local():
        # Simulate the Azure Function locally
        class MockHttpRequest:
            def __init__(self, json_data):
                self._json = json_data
            
            def get_json(self):
                return self._json
        
        mock_req = MockHttpRequest(request.json)
        response = classify_post(mock_req)
        return response.get_body(), response.status_code, {"Content-Type": response.mimetype}
    
    app.run(debug=True, port=7071)
