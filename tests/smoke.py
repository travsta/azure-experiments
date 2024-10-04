import http.client
import json

def test_api():
    """
    Test the API by sending a POST request with a JSON payload and checking the response.
    """
    try:
        # Establish a connection to the API endpoint
        conn = http.client.HTTPSConnection("exp-p-eu-topic-classifier-api.azurewebsites.net")
        
        # Prepare the JSON payload and headers
        payload = json.dumps({"text": "value"})
        headers = {'Content-Type': 'application/json'}
        
        # Send the POST request
        conn.request("POST", "/api/classify_post", body=payload, headers=headers)
        response = conn.getresponse()
        
        # Check if the response status is 200 OK
        assert response.status == 200, f"Expected status 200, got {response.status}"
        
        # Read and decode the response data
        data = response.read().decode('utf-8')
        json_data = json.loads(data)
        
        # Check if the response JSON matches the expected output
        expected_response = {"status": "ok"}
        assert json_data == expected_response, (
            f"Expected response {expected_response}, got {json_data}. "
            f"Full response: {data}"
        )
    
    except http.client.HTTPException as e:
        print(f"HTTP error occurred: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
    except AssertionError as e:
        print(f"Assertion error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure the connection is closed
        conn.close()

if __name__ == "__main__":
    test_api()
