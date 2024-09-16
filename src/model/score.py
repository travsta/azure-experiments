import json
from typing import Dict, Any
from .dummy_model import DummyTopicClassifier

class Scorer:
    def __init__(self):
        self.model: DummyTopicClassifier = None

    def init(self) -> None:
        """Initialize the model."""
        self.model = DummyTopicClassifier()

    def run(self, raw_data: str) -> str:
        """
        Process the input data and return predictions.

        Args:
            raw_data (str): A JSON string containing the input data.

        Returns:
            str: A JSON string containing the prediction results or an error message.
        """
        if self.model is None:
            return json.dumps({"error": "Model not initialized. Call init() first."})

        try:
            # Parse incoming data
            data: Dict[str, Any] = json.loads(raw_data)
            text: str = data['text']
            
            # Make prediction
            result: Dict[str, float] = self.model.predict(text)
            
            # Add any additional processing here
            
            # Return the result as JSON
            return json.dumps({"result": result})
        except KeyError:
            return json.dumps({"error": "Input data must contain a 'text' field."})
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON input."})
        except Exception as e:
            error: str = str(e)
            return json.dumps({"error": f"An unexpected error occurred: {error}"})

# For Azure ML deployment
scorer = Scorer()

def init():
    scorer.init()

def run(raw_data):
    return scorer.run(raw_data)

# This is for local testing
if __name__ == "__main__":
    scorer = Scorer()
    scorer.init()
    test_data: str = json.dumps({"text": "This is a test Instagram post about food and travel."})
    result: str = scorer.run(test_data)
    print(result)