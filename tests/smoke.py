import http.client
import json

def test_api():
    conn = http.client.HTTPSConnection("https://exp-p-eu-topic-classifier-api.azurewebsites.net/api/classify_post")
    conn.request("POST", "/health")
    response = conn.getresponse()
    
    assert response.status == 200
    
    data = response.read().decode('utf-8')
    json_data = json.loads(data)
    
    assert json_data == {"status": "ok"}
    conn.close()

if __name__ == "__main__":
    test_api()
