import pytest
from src.model.dummy_model import DummyTopicClassifier

def test_dummy_classifier_initialization():
    """Test that the DummyTopicClassifier initializes with the correct topics."""
    classifier = DummyTopicClassifier()
    expected_topics = ['soccer', 'fashion', 'food', 'technology', 'travel']
    assert classifier.get_topics() == expected_topics

def test_dummy_classifier_prediction():
    """Test that the predict method returns a dictionary with correct keys and valid probabilities."""
    classifier = DummyTopicClassifier()
    sample_text = "This is a test post."
    result = classifier.predict(sample_text)
    
    assert isinstance(result, dict)
    assert set(result.keys()) == set(classifier.get_topics())
    assert all(0 <= prob <= 1 for prob in result.values())
    assert pytest.approx(sum(result.values()), 1e-6) == 1.0

def test_dummy_classifier_consistency():
    """Test that multiple calls to predict with the same input produce different results."""
    classifier = DummyTopicClassifier()
    sample_text = "Another test post."
    result1 = classifier.predict(sample_text)
    result2 = classifier.predict(sample_text)
    
    assert result1 != result2  # This should be true most of the time due to randomness

def test_get_topics():
    """Test that get_topics returns the correct list of topics."""
    classifier = DummyTopicClassifier()
    expected_topics = ['soccer', 'fashion', 'food', 'technology', 'travel']
    assert classifier.get_topics() == expected_topics

def test_prediction_input_type():
    """Test that the predict method handles different input types correctly."""
    classifier = DummyTopicClassifier()
    
    # Test with string input
    result = classifier.predict("Test post")
    assert isinstance(result, dict)
    
    # Test with non-string input (should raise TypeError)
    with pytest.raises(TypeError):
        classifier.predict(123)

# New tests for edge cases and error scenarios

def test_empty_input():
    """Test that the predict method handles empty input."""
    classifier = DummyTopicClassifier()
    result = classifier.predict("")
    assert isinstance(result, dict)
    assert set(result.keys()) == set(classifier.get_topics())

def test_very_long_input():
    """Test that the predict method handles very long input."""
    classifier = DummyTopicClassifier()
    long_text = "a" * 1000000  # 1 million characters
    result = classifier.predict(long_text)
    assert isinstance(result, dict)
    assert set(result.keys()) == set(classifier.get_topics())

def test_special_characters():
    """Test that the predict method handles input with special characters."""
    classifier = DummyTopicClassifier()
    special_text = "!@#$%^&*()_+{}[]|\\:;<>?,./"
    result = classifier.predict(special_text)
    assert isinstance(result, dict)
    assert set(result.keys()) == set(classifier.get_topics())

def test_unicode_characters():
    """Test that the predict method handles input with unicode characters."""
    classifier = DummyTopicClassifier()
    unicode_text = "こんにちは世界 • Hello World • Bonjour le monde"
    result = classifier.predict(unicode_text)
    assert isinstance(result, dict)
    assert set(result.keys()) == set(classifier.get_topics())

def test_probability_sum():
    """Test that the sum of probabilities is always 1."""
    classifier = DummyTopicClassifier()
    texts = ["", "Short text", "a" * 1000000, "!@#$%^&*()", "こんにちは世界"]
    for text in texts:
        result = classifier.predict(text)
        assert pytest.approx(sum(result.values()), 1e-6) == 1.0