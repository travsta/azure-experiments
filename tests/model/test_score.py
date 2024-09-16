import json
import pytest
from src.model.score import init, run

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
