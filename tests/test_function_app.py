import json
import pytest
from unittest.mock import patch, MagicMock
import azure.functions as func
import urllib.error
from src.api.function_app import classify_post_function_wrapper, PostClassifier

@pytest.fixture
def mock_env_variables():
    with patch.dict('os.environ', {
        'MODEL_ENDPOINT_URL': 'http://test-url.com',
        'MODEL_KEY': 'test-key'
    }):
        yield

class TestClassifyPostFunction:
    def test_classify_post_function_wrapper(self, mock_env_variables):
        req_body = {"text": "Test post"}

        with patch.object(PostClassifier, 'classify_post', return_value={"body": json.dumps({"result": {"topic1": 0.5, "topic2": 0.5}}), "status_code": 200}):
            response = classify_post_function_wrapper(req_body)

        assert response is not None
        assert isinstance(response, func.HttpResponse)
        assert response.status_code == 200
        assert json.loads(response.get_body()) == {"result": {"topic1": 0.5, "topic2": 0.5}}

    def test_classify_post_function_wrapper_missing_text(self, mock_env_variables):
        req_body = {}  # Missing 'text' key

        response = classify_post_function_wrapper(req_body)

        assert response is not None
        assert isinstance(response, func.HttpResponse)
        assert response.status_code == 400
        assert "Please pass a 'text' property in the request body" in response.get_body().decode()

    def test_classify_post_function_wrapper_exception(self, mock_env_variables):
        req_body = {"text": "Test post"}

        with patch.object(PostClassifier, 'classify_post', side_effect=Exception("Test exception")):
            response = classify_post_function_wrapper(req_body)

        assert response is not None
        assert isinstance(response, func.HttpResponse)
        assert response.status_code == 500
        assert "An error occurred: Test exception" in response.get_body().decode()

    @patch('urllib.request.urlopen')
    def test_classify_post_function_wrapper_api_error(self, mock_urlopen, mock_env_variables):
        req_body = {"text": "Test post"}
        mock_urlopen.side_effect = urllib.error.URLError("API error")

        response = classify_post_function_wrapper(req_body)

        assert response is not None
        assert isinstance(response, func.HttpResponse)
        assert response.status_code == 500
        assert "An error occurred: URL error occurred: API error" in response.get_body().decode()

    @patch.dict('os.environ', {}, clear=True)
    def test_classify_post_function_wrapper_missing_env_variables(self):
        req_body = {"text": "Test post"}

        response = classify_post_function_wrapper(req_body)

        assert response is not None
        assert isinstance(response, func.HttpResponse)
        assert response.status_code == 500
        assert "An error occurred: Missing required environment variables" in response.get_body().decode()

    def test_classify_post_function_wrapper_invalid_input_type(self, mock_env_variables):
        req_body = {"text": 12345}  # Invalid input type (integer instead of string)

        response = classify_post_function_wrapper(req_body)

        assert response is not None
        assert isinstance(response, func.HttpResponse)
        assert response.status_code == 400
        assert "Invalid input: Invalid input type. Expected string" in response.get_body().decode()

    @patch('urllib.request.urlopen')
    def test_classify_post_http_error(self, mock_urlopen, mock_env_variables):
        req_body = {"text": "Test post"}
        mock_response = MagicMock()
        mock_response.getcode.return_value = 404
        mock_response.read.return_value = b'Not Found'
        mock_urlopen.side_effect = urllib.error.HTTPError('http://test-url.com', 404, 'Not Found', {}, mock_response)

        response = classify_post_function_wrapper(req_body)

        assert response is not None
        assert isinstance(response, func.HttpResponse)
        assert response.status_code == 500
        assert "An error occurred: HTTP error occurred: 404 Not Found" in response.get_body().decode()

if __name__ == "__main__":
    pytest.main()
