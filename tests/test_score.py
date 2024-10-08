import json
import pytest
from unittest.mock import patch, MagicMock
from src.model.score import Scorer
from dummy_model import DummyTopicClassifier  # Changed import to match score.py

@pytest.fixture
def scorer():
    scorer = Scorer()
    scorer.init()
    return scorer

def test_init(scorer):
    """Test that init function initializes the model correctly."""
    print(f"Scorer model type: {type(scorer.model)}")
    print(f"DummyTopicClassifier type: {DummyTopicClassifier}")
    assert isinstance(scorer.model, DummyTopicClassifier), f"Expected DummyTopicClassifier, got {type(scorer.model)}"

def test_run_valid_input(scorer):
    """Test that run function processes valid input correctly."""
    test_input = json.dumps({"text": "This is a test Instagram post."})
    result = scorer.run(test_input)
    result_dict = json.loads(result)
    
    assert "result" in result_dict
    assert isinstance(result_dict["result"], dict)
    assert len(result_dict["result"]) == 5  # Number of topics
    assert all(0 <= prob <= 1 for prob in result_dict["result"].values())
    assert pytest.approx(sum(result_dict["result"].values()), 1e-6) == 1.0

def test_run_invalid_input(scorer):
    """Test that run function handles invalid input gracefully."""
    test_input = json.dumps({"invalid_key": "This should fail."})
    result = scorer.run(test_input)
    result_dict = json.loads(result)
    
    assert "error" in result_dict

def test_run_malformed_json(scorer):
    """Test that run function handles malformed JSON input."""
    test_input = "This is not JSON"
    result = scorer.run(test_input)
    result_dict = json.loads(result)
    
    assert "error" in result_dict

def test_uninitialized_model():
    """Test that run function handles uninitialized model correctly."""
    uninitialized_scorer = Scorer()
    test_input = json.dumps({"text": "This should fail."})
    result = uninitialized_scorer.run(test_input)
    result_dict = json.loads(result)
    
    assert "error" in result_dict
    assert "Model not initialized" in result_dict["error"]

def test_empty_text(scorer):
    """Test that run function handles empty text input."""
    test_input = json.dumps({"text": ""})
    result = scorer.run(test_input)
    result_dict = json.loads(result)
    
    assert "result" in result_dict
    assert isinstance(result_dict["result"], dict)
    assert len(result_dict["result"]) == 5  # Number of topics

def test_very_long_text(scorer):
    """Test that run function handles very long text input."""
    long_text = "a" * 1000000  # 1 million characters
    test_input = json.dumps({"text": long_text})
    result = scorer.run(test_input)
    result_dict = json.loads(result)
    
    assert "result" in result_dict
    assert isinstance(result_dict["result"], dict)
    assert len(result_dict["result"]) == 5  # Number of topics

def test_special_characters(scorer):
    """Test that run function handles text with special characters."""
    special_text = "!@#$%^&*()_+{}[]|\\:;<>?,./"
    test_input = json.dumps({"text": special_text})
    result = scorer.run(test_input)
    result_dict = json.loads(result)
    
    assert "result" in result_dict
    assert isinstance(result_dict["result"], dict)
    assert len(result_dict["result"]) == 5  # Number of topics

def test_unicode_characters(scorer):
    """Test that run function handles text with unicode characters."""
    unicode_text = "こんにちは世界 • Hello World • Bonjour le monde"
    test_input = json.dumps({"text": unicode_text})
    result = scorer.run(test_input)
    result_dict = json.loads(result)
    
    assert "result" in result_dict
    assert isinstance(result_dict["result"], dict)
    assert len(result_dict["result"]) == 5  # Number of topics

def test_missing_text_key(scorer):
    """Test that run function handles missing 'text' key in input."""
    test_input = json.dumps({"not_text": "This should fail."})
    result = scorer.run(test_input)
    result_dict = json.loads(result)
    
    assert "error" in result_dict

@patch('src.model.score.DummyTopicClassifier.predict')
def test_model_error(mock_predict, scorer):
    """Test that run function handles errors from the model."""
    mock_predict.side_effect = Exception("Model prediction error")
    test_input = json.dumps({"text": "This should trigger an error."})
    result = scorer.run(test_input)
    result_dict = json.loads(result)
    
    print(f"Result dict: {result_dict}")
    assert "error" in result_dict, f"Expected 'error' key in result, got: {result_dict}"
    assert "Model prediction error" in result_dict["error"]

def test_non_string_text(scorer):
    """Test that run function handles non-string 'text' value."""
    test_input = json.dumps({"text": 12345})
    result = scorer.run(test_input)
    result_dict = json.loads(result)
    
    assert "error" in result_dict
    assert "Input must be a string" in result_dict["error"]

def test_scorer_initialization():
    """
    Test if the Scorer is initialized correctly with a DummyTopicClassifier.
    """
    scorer = Scorer()
    scorer.init()
    print(f"Scorer model type: {type(scorer.model)}")
    print(f"DummyTopicClassifier type: {DummyTopicClassifier}")
    assert isinstance(scorer.model, DummyTopicClassifier), f"Scorer is not initialized with a DummyTopicClassifier. Got {type(scorer.model)}"

def test_scorer_run_with_environment(scorer):
    """
    Test if the Scorer's run method works correctly with environment variables.
    """
    with patch.dict('os.environ', {'SOME_ENV_VAR': 'test_value'}):
        input_data = json.dumps({"text": "Test post"})
        result = scorer.run(input_data)
        assert 'result' in json.loads(result), "Scorer's run method did not return a result. Check if the method is correctly processing the input and using the model."
