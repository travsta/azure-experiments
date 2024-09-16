import json
import pytest
from unittest.mock import patch
from src.api.function_app import PostClassifier

@pytest.fixture
def mock_requests_post():
    with patch('src.api.function_app.requests.post') as mock_post:
        yield mock_post

def test_classify_post_valid_input(mock_requests_post):
    """Test classify_post function with valid input."""
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.text = json.dumps({"result": {"topic1": 0.5, "topic2": 0.5}})

    response = PostClassifier.classify_post("Test post")
    
    assert response["status_code"] == 200
    assert "result" in json.loads(response["body"])

def test_classify_post_empty_text():
    """Test classify_post function with empty text."""
    response = PostClassifier.classify_post("")
    
    assert response["status_code"] == 400
    assert "Please provide a non-empty text" in response["body"]

def test_classify_post_model_error(mock_requests_post):
    """Test classify_post function when model endpoint returns an error."""
    mock_requests_post.side_effect = Exception("Model endpoint error")

    response = PostClassifier.classify_post("Test post")
    
    assert response["status_code"] == 500
    assert "Error processing request" in response["body"]

# Additional tests...

def test_classify_post_very_long_text(mock_requests_post):
    """Test classify_post function with a very long input text."""
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.text = json.dumps({"result": {"topic1": 1.0}})

    long_text = "a" * 10000  # 10,000 character string
    response = PostClassifier.classify_post(long_text)
    
    assert response["status_code"] == 200
    assert "result" in json.loads(response["body"])

def test_classify_post_special_characters(mock_requests_post):
    """Test classify_post function with text containing special characters."""
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.text = json.dumps({"result": {"topic1": 1.0}})

    special_text = "!@#$%^&*()_+{}[]|\\:;\"'<>,.?/~`"
    response = PostClassifier.classify_post(special_text)
    
    assert response["status_code"] == 200
    assert "result" in json.loads(response["body"])

def test_classify_post_non_ascii_characters(mock_requests_post):
    """Test classify_post function with text containing non-ASCII characters."""
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.text = json.dumps({"result": {"topic1": 1.0}})

    non_ascii_text = "こんにちは世界 • Hello World • Bonjour le monde"
    response = PostClassifier.classify_post(non_ascii_text)
    
    assert response["status_code"] == 200
    assert "result" in json.loads(response["body"])

def test_classify_post_model_timeout(mock_requests_post):
    """Test classify_post function when model endpoint times out."""
    mock_requests_post.side_effect = requests.exceptions.Timeout("Request timed out")

    response = PostClassifier.classify_post("Test post")
    
    assert response["status_code"] == 500
    assert "Error processing request" in response["body"]

def test_classify_post_model_connection_error(mock_requests_post):
    """Test classify_post function when there's a connection error to the model endpoint."""
    mock_requests_post.side_effect = requests.exceptions.ConnectionError("Connection failed")

    response = PostClassifier.classify_post("Test post")
    
    assert response["status_code"] == 500
    assert "Error processing request" in response["body"]

def test_classify_post_model_invalid_response(mock_requests_post):
    """Test classify_post function when model returns an invalid JSON response."""
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.text = "This is not JSON"

    response = PostClassifier.classify_post("Test post")
    
    assert response["status_code"] == 200
    assert "This is not JSON" in response["body"]

def test_classify_post_model_http_error(mock_requests_post):
    """Test classify_post function when model endpoint returns an HTTP error."""
    mock_requests_post.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found")

    response = PostClassifier.classify_post("Test post")
    
    assert response["status_code"] == 500
    assert "Error processing request" in response["body"]