import json
from dummy_model import DummyTopicClassifier

def init():
    global model
    model = DummyTopicClassifier()

def run(raw_data):
    try:
        # Parse incoming data
        data = json.loads(raw_data)['text']
        
        # Make prediction
        result = model.predict(data)
        
        # You can add any additional processing here
        
        # Return the result as JSON
        return json.dumps({"result": result})
    except Exception as e:
        error = str(e)
        return json.dumps({"error": error})

# This is for local testing
if __name__ == "__main__":
    init()
    test_data = json.dumps({"text": "This is a test Instagram post about food and travel."})
    result = run(test_data)
    print(result)
