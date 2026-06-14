import os
import requests

FAL_KEY = os.getenv("FAL_KEY")

if not FAL_KEY:
    raise ValueError("FAL_KEY secret is missing")

print("FAL key found. Ready for FAL API.")
