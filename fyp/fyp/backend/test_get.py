import urllib.request

try:
    with urllib.request.urlopen('http://127.0.0.1:5001/api/pc-builder', timeout=5) as response:
        print('Status:', response.status)
        print('Response:', response.read().decode('utf-8'))
except Exception as e:
    print('Error:', e)