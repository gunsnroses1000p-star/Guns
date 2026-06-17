import os
import json
import replicate

client = replicate.Client(
    api_token=os.environ["REPLICATE_API_TOKEN"]
)

def handler(request):
    try:
        body = json.loads(request.body)

        image = body.get("image")
        prompt = body.get("prompt", "")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Video endpoint reached",
                "image": image,
                "prompt": prompt
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }
