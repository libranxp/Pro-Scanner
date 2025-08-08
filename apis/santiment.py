# apis/santiment.py
import requests, os

def get_dev_activity(symbol):
    url = f"https://api.santiment.net/graphql"
    headers = {"Authorization": f"Bearer {os.environ['SANTIMENT_KEY']}"}
    query = {"query": f'{{ getMetric(metric: "dev_activity"){symbol} }}'}
    return requests.post(url, headers=headers, json=query).json()
