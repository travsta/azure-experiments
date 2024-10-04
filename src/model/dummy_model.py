import numpy as np
from typing import Dict, List

class DummyTopicClassifier:
    def __init__(self) -> None:
        self.topics: List[str] = ['soccer', 'fashion', 'food', 'technology', 'travel']

    def predict(self, text: str) -> Dict[str, float]:
        """
        Predict topic probabilities for a given text.
        
        Args:
            text (str): The input text to classify.
        
        Returns:
            Dict[str, float]: A dictionary of topic probabilities.
        
        Raises:
            TypeError: If the input is not a string.
        """
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        # Generate random probabilities
        probabilities: np.ndarray = np.random.dirichlet(np.ones(len(self.topics)), size=1)[0]
        return dict(zip(self.topics, probabilities))

    def get_topics(self) -> List[str]:
        """
        Get the list of topics.
        
        Returns:
            List[str]: The list of topics.
        """
        return self.topics

# for local testing
if __name__ == "__main__":
    classifier: DummyTopicClassifier = DummyTopicClassifier()
    sample_text: str = "This is a sample Instagram post."
    result: Dict[str, float] = classifier.predict(sample_text)
    print(f"Sample text: {sample_text}")
    print("Predicted topic probabilities:")
    for topic, prob in result.items():
        print(f"{topic}: {prob:.4f}")
