import numpy as np
from typing import Dict

class DummyTopicClassifier:
    def __init__(self):
        self.topics = ['soccer', 'fashion', 'food', 'technology', 'travel']

    def predict(self, text: str) -> Dict[str, float]:
        """
        Predict topic probabilities for a given text.
        
        Args:
            text (str): The input text to classify.
        
        Returns:
            Dict[str, float]: A dictionary of topic probabilities.
        """
        # Generate random probabilities
        probabilities = np.random.dirichlet(np.ones(len(self.topics)), size=1)[0]
        return dict(zip(self.topics, probabilities))

    def get_topics(self) -> List[str]:
        """
        Get the list of topics.
        
        Returns:
            List[str]: The list of topics.
        """
        return self.topics

if __name__ == "__main__":
    classifier = DummyTopicClassifier()
    sample_text = "This is a sample Instagram post."
    result = classifier.predict(sample_text)
    print(f"Sample text: {sample_text}")
    print("Predicted topic probabilities:")
    for topic, prob in result.items():
        print(f"{topic}: {prob:.4f}")
