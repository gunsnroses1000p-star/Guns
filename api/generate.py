import os
import json
import replicate
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        try:
            token = os.environ.get("REPLICATE_API_TOKEN")

            if not token:
                self.send_json(500, {"error": "Missing REPLICATE_API_TOKEN in Vercel"})
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            data = json.loads(body.decode("utf-8"))
            prompt = data.get("prompt", "A cute orange cat")

            client = replicate.Client(api_token=token)

            output = client.run(
                "black-forest-labs/flux-schnell",
                input={
                    "prompt": prompt
                }
            )

            if isinstance(output, list):
                image_url = output[0]
            else:
                image_url = str(output)

            self.send_json(200, {"image": image_url})

        except Exception as e:
            self.send_json(500, {"error": str(e)})
