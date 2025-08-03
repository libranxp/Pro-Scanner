import requests
import os

def fetch_json(url, headers=None):
    res = requests.get(url, headers=headers)
    return res.json()

def post_json(url, payload, headers=None):
    res = requests.post(url, json=payload, headers=headers)
    return res.json()

