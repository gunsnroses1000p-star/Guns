import os
import json
import requests

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Method not allowed"})
        }

    try:
        data = request.get_json()

        image1 = data.get("image1")
        image2 = data.get("image2")
        prompt = data.get("prompt", "")

        token = os.environ.get("REPLICATE_API_TOKEN")

        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers={
                "Authorization": f"Token {token}",
                "Content-Type": "application/json"
            },
            json={
                "version": "black-forest-labs/flux-kontext-max",
                "input": {
                    "prompt": f"Create one seamless photorealistic image using both reference images. {prompt}",
                    "input_images": [image1, image2]
                }
            }
        )

        return {
            "statusCode": 200,
            "body": response.text
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
