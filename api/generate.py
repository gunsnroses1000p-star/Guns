import os
import json
import replicate

def handler(request):
    try:
        prompt = request.get("prompt", "A beautiful landscape")

        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": prompt
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "image": output[0]
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }
