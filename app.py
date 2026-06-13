import requests

try:
    r = requests.get("https://huggingface.co")
    print("Status:", r.status_code)
except Exception as e:
    print("Error:", e)
