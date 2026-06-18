import json
import os
import replicate
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)

            image = data.get("image", "")
            prompt = data.get("prompt", "cinematic motion, smooth camera movement")
            duration = int(data.get("duration", 5))
            output = replicate.run(
                "wan-video/wan-2.2-i2v-fast",
                input={
                    "image": image,
                    "prompt": prompt,
                    "duration": duration
                }
            )

            video_url = output[0] if isinstance(output, list) else output

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "video": str(video_url)
            }).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())
