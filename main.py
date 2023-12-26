import requests


req = requests.get('http://127.0.0.1:8000/work/api/list/?token=abc')

print(req.status_code)
