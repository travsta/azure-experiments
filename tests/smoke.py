import http.client
import json
import os

def test_api():
    """
    Test the API by sending a POST request with a JSON payload and checking the response.
    The API endpoint is read from the API_ENDPOINT environment variable.
    """
    # Get the API endpoint from environment variable
    api_endpoint = os.environ.get('API_ENDPOINT')
    if not api_endpoint:
        print("Error: API_ENDPOINT environment variable is not set.")
        return

    try:
        # Extract hostname and path from the API endpoint
        hostname = api_endpoint.split('//')[1].split('/')[0]
        path = '/' + '/'.join(api_endpoint.split('/')[3:])
        
        # Prepare the JSON payload and headers
        payload = json.dumps({"text": "value"})
        headers = {'Content-Type': 'application/json'}
        
        # Create HTTPS connection
        conn = http.client.HTTPSConnection(hostname)
        
        # Send the POST request
        conn.request("POST", path, body=payload, headers=headers)
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
        
        print("Smoke test passed successfully!")
    
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
