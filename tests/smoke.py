import http.client
import json

def test_api():
    conn = http.client.HTTPSConnection("exp-p-eu-topic-classifier-api.azurewebsites.net")
    payload = json.dumps({"text": "value"})
    headers = {'Content-Type': 'application/json'}
    
    conn.request("POST", "/api/classify_post", body=payload, headers=headers)
    response = conn.getresponse()
    
    assert response.status == 200
    
    data = response.read().decode('utf-8')
    json_data = json.loads(data)
    
    assert json_data == {"status": "ok"}
    conn.close()

if __name__ == "__main__":
    test_api()
