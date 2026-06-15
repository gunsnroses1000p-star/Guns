import os
import replicate

api_token = os.environ.get("REPLICATE_API_TOKEN")

if not api_token:
    raise ValueError("Missing REPLICATE_API_TOKEN")

client = replicate.Client(api_token=api_token)

output = client.run(
    "black-forest-labs/flux-schnell",
    input={
        "prompt": "A futuristic city at night with neon lights, cinematic"
    }
)

print(output)
