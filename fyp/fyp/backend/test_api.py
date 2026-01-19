import urllib.request
import json

try:
    data = json.dumps({'message': 'best cpu for gaming'}).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:5001/api/pc-builder', data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=10) as response:
        result = json.loads(response.read().decode('utf-8'))
        print('Success:', result.get('success'))
        print('Response:', repr(result.get('response')))
except Exception as e:
    print('Error:', e)