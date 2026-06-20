print("IMAGE API LOADED")
import json
import os
import urllib.request
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            token = os.environ.get("REPLICATE_API_TOKEN")
            if not token:
                raise Exception("Missing REPLICATE_API_TOKEN in Vercel")

            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)

            prompt = data.get("prompt", "")
            negative = data.get("negative", "")
            aspect_ratio = data.get("aspect_ratio", "1:1")
            image = data.get("image", "")
            if negative:
                prompt = prompt + ". Avoid: " + negative

            input_data = {
            "prompt": prompt,
            "go_fast": True,
            "megapixels": "1",
            "num_outputs": 1,
            "aspect_ratio": aspect_ratio,
            "output_format": "webp",
            "output_quality": 80,
            "extra_lora": "gunsnroses1000p-star/gnrwoman01",
            "extra_lora_scale": 1.1,
        }

        if image and image.startswith("http"):
            input_data["image"] = image

        payload = {
            "input": input_data
        }
            }

            req = urllib.request.Request(
                "https://api.replicate.com/v1/models/black-forest-labs/flux-dev-lora/predictions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "Prefer": "wait"
                },
                method="POST"
            )

            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))

            if result.get("error"):
    raise Exception(result.get("error"))

if result.get("status") == "failed":
    raise Exception(str(result))

output = result.get("output")

if not output:
    self.send_response(500)
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps({
        "error": "No image returned",
        "replicate_result": result
    }).encode())
    return

image_url = output[0] if isinstance(output, list) else output

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"image": image_url}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
