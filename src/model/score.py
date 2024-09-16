import json
from typing import Dict, Any
from dummy_model import DummyTopicClassifier

def init() -> None:
    global model
    model: DummyTopicClassifier = DummyTopicClassifier()

def run(raw_data: str) -> str:
    try:
        # Parse incoming data
        data: Dict[str, Any] = json.loads(raw_data)
        text: str = data['text']
        
        # Make prediction
        result: Dict[str, float] = model.predict(text)
        
        # add any additional processing here
        
        # Return the result as JSON
        return json.dumps({"result": result})
    except Exception as e:
        error: str = str(e)
        return json.dumps({"error": error})

# This is for local testing
if __name__ == "__main__":
    init()
    test_data: str = json.dumps({"text": "This is a test Instagram post about food and travel."})
    result: str = run(test_data)
    print(result)