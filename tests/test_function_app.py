import azure.functions as func
import json
import pytest
from unittest.mock import patch, MagicMock
from src.api.function_app import classify_post

@pytest.fixture
def mock_requests_post():
    with patch('src.api.function_app.requests.post') as mock_post:
        yield mock_post

def test_classify_post_valid_input(mock_requests_post):
    """Test classify_post function with valid input."""
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.text = json.dumps({"result": {"topic1": 0.5, "topic2": 0.5}})

    req = func.HttpRequest(
        method='POST',
        body=json.dumps({"text": "Test post"}).encode('utf-8'),
        url='/api/classify_post'
    )

    response = classify_post(req)
    
    assert response.status_code == 200
    assert "result" in json.loads(response.get_body())

def test_classify_post_invalid_json():
    """Test classify_post function with invalid JSON input."""
    req = func.HttpRequest(
        method='POST',
        body="This is not JSON".encode('utf-8'),
        url='/api/classify_post'
    )

    response = classify_post(req)
    
    assert response.status_code == 400
    assert "Invalid JSON" in response.get_body().decode()

def test_classify_post_missing_text():
    """Test classify_post function with missing 'text' field."""
    req = func.HttpRequest(
        method='POST',
        body=json.dumps({"not_text": "Test post"}).encode('utf-8'),
        url='/api/classify_post'
    )

    response = classify_post(req)
    
    assert response.status_code == 400
    assert "Please pass a 'text' property" in response.get_body().decode()

def test_classify_post_model_error(mock_requests_post):
    """Test classify_post function when model endpoint returns an error."""
    mock_requests_post.side_effect = Exception("Model endpoint error")

    req = func.HttpRequest(
        method='POST',
        body=json.dumps({"text": "Test post"}).encode('utf-8'),
        url='/api/classify_post'
    )

    response = classify_post(req)
    
    assert response.status_code == 500
    assert "Error processing request" in response.get_body().decode()
