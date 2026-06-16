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

            prompt = data.get("prompt", "A cute orange cat, photorealistic")

            payload = {
                "version": "black-forest-labs/flux-schnell",
                "input": {
                    "prompt": prompt,
                    "num_outputs": 1,
                    "aspect_ratio": "1:1",
                    "output_format": "webp"
                }
            }

            req = urllib.request.Request(
                "https://api.replicate.com/v1/models/black-forest-labs/flux-schnell/predictions",
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

            output = result.get("output")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "image": output[0] if isinstance(output, list) else output
            }).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
