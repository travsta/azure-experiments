import json
import pytest
from unittest.mock import patch
from src.model.score import init, run
from src.model.dummy_model import DummyTopicClassifier

@pytest.fixture(scope="module")
def initialized_model():
    init()
    return None

def test_init():
    """Test that init function runs without errors."""
    init()

def test_run_valid_input(initialized_model):
    """Test that run function processes valid input correctly."""
    test_input = json.dumps({"text": "This is a test Instagram post."})
    result = run(test_input)
    result_dict = json.loads(result)
    
    assert "result" in result_dict
    assert isinstance(result_dict["result"], dict)
    assert len(result_dict["result"]) == 5  # Number of topics
    assert all(0 <= prob <= 1 for prob in result_dict["result"].values())
    assert pytest.approx(sum(result_dict["result"].values()), 1e-6) == 1.0

def test_run_invalid_input(initialized_model):
    """Test that run function handles invalid input gracefully."""
    test_input = json.dumps({"invalid_key": "This should fail."})
    result = run(test_input)
    result_dict = json.loads(result)
    
    assert "error" in result_dict

def test_run_malformed_json(initialized_model):
    """Test that run function handles malformed JSON input."""
    test_input = "This is not JSON"
    result = run(test_input)
    result_dict = json.loads(result)
    
    assert "error" in result_dict

# New tests for edge cases and error scenarios

def test_empty_text(initialized_model):
    """Test that run function handles empty text input."""
    test_input = json.dumps({"text": ""})
    result = run(test_input)
    result_dict = json.loads(result)
    
    assert "result" in result_dict
    assert isinstance(result_dict["result"], dict)
    assert len(result_dict["result"]) == 5  # Number of topics

def test_very_long_text(initialized_model):
    """Test that run function handles very long text input."""
    long_text = "a" * 1000000  # 1 million characters
    test_input = json.dumps({"text": long_text})
    result = run(test_input)
    result_dict = json.loads(result)
    
    assert "result" in result_dict
    assert isinstance(result_dict["result"], dict)
    assert len(result_dict["result"]) == 5  # Number of topics

def test_special_characters(initialized_model):
    """Test that run function handles text with special characters."""
    special_text = "!@#$%^&*()_+{}[]|\\:;<>?,./"
    test_input = json.dumps({"text": special_text})
    result = run(test_input)
    result_dict = json.loads(result)
    
    assert "result" in result_dict
    assert isinstance(result_dict["result"], dict)
    assert len(result_dict["result"]) == 5  # Number of topics

def test_unicode_characters(initialized_model):
    """Test that run function handles text with unicode characters."""
    unicode_text = "こんにちは世界 • Hello World • Bonjour le monde"
    test_input = json.dumps({"text": unicode_text})
    result = run(test_input)
    result_dict = json.loads(result)
    
    assert "result" in result_dict
    assert isinstance(result_dict["result"], dict)
    assert len(result_dict["result"]) == 5  # Number of topics

def test_missing_text_key(initialized_model):
    """Test that run function handles missing 'text' key in input."""
    test_input = json.dumps({"not_text": "This should fail."})
    result = run(test_input)
    result_dict = json.loads(result)
    
    assert "error" in result_dict

@patch.object(DummyTopicClassifier, 'predict')
def test_model_error(mock_predict, initialized_model):
    """Test that run function handles errors from the model."""
    mock_predict.side_effect = Exception("Model prediction error")
    test_input = json.dumps({"text": "This should trigger an error."})
    result = run(test_input)
    result_dict = json.loads(result)
    
    assert "error" in result_dict
    assert "Model prediction error" in result_dict["error"]

def test_non_string_text(initialized_model):
    """Test that run function handles non-string 'text' value."""
    test_input = json.dumps({"text": 12345})
    result = run(test_input)
    result_dict = json.loads(result)
    
    assert "error" in result_dict