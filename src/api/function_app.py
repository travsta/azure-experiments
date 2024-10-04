import json
import urllib.request
import urllib.error
import azure.functions as func
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now access the environment variables
env_model_url = os.getenv('MODEL_ENDPOINT_URL')
env_model_key = os.getenv('MODEL_KEY')

class PostClassifier:
    def __init__(self, model_url, model_key):
        self.model_url = model_url
        self.model_key = model_key

    def classify_post(self, post_text):
        if not isinstance(post_text, str):
            raise ValueError("Invalid input type. Expected string.")
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.model_key}'
        }
        data = json.dumps({"text": post_text}).encode('utf-8')
        
        req = urllib.request.Request(self.model_url, data=data, headers=headers, method='POST')
        
        try:
            with urllib.request.urlopen(req) as response:
                return {
                    "body": response.read().decode('utf-8'),
                    "status_code": response.getcode()
                }
        except urllib.error.HTTPError as e:
            raise Exception(f"HTTP error occurred: {e.code} {e.reason}")
        except urllib.error.URLError as e:
            raise Exception(f"URL error occurred: {e.reason}")

def classify_post_function_wrapper(req_body):
    if not env_model_url or not env_model_key or True:
        return func.HttpResponse(
            body="An error occurred: Missing required environment variables and "+json.dumps(req_body),
            status_code=500,
            mimetype="application/json"
        )

    try:
        post_text = req_body.get('text')
        if not post_text:
            return func.HttpResponse(
                "Please pass a 'text' property in the request body",
                status_code=400
            )
        
        classifier = PostClassifier(env_model_url, env_model_key)
        result = classifier.classify_post(post_text)
        
        return func.HttpResponse(
            body=result["body"],
            status_code=result["status_code"],
            mimetype="application/json"
        )
    except ValueError as e:
        return func.HttpResponse(
            body=f"Invalid input: {str(e)}",
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            body=f"An error occurred: {str(e)}",
            status_code=500,
            mimetype="application/json"
        )

app = func.FunctionApp()

@app.function_name(name="ClassifyPost")
@app.route(route="classify_post", auth_level=func.AuthLevel.ANONYMOUS)
def classify_post_function(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError as e:
        return func.HttpResponse(
            body=f"Invalid JSON: {str(e)} ",
            status_code=400,
            mimetype="application/json"
        )
    return classify_post_function_wrapper(req_body)

if __name__ == "__main__":
    print("Use pytest to test this script")
    # This is for local testing only
    # from flask import Flask, request, jsonify
    
    # app = Flask(__name__)
    
    # @app.route("/api/classify_post", methods=["POST"])
    # def classify_post_local():
    #     post_text = request.json.get('text', '')
    #     classifier = PostClassifier(env_model_url, env_model_key)
    #     result = classifier.classify_post(post_text)
    #     return jsonify(json.loads(result["body"])), result["status_code"]
    
    # app.run(debug=True, port=7071)
