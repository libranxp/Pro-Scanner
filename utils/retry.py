import time
import requests

def safe_request(url, headers=None, params=None, retries=3, delay=2):
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            time.sleep(delay)
    return {}
