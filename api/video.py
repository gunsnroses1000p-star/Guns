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

            provider = data.get("provider", "wan")
            image = data.get("image", "") or data.get("image_url", "")
            prompt = data.get("prompt", "cinematic motion, smooth camera movement")
            duration = int(data.get("duration", 5))

            if provider == "kling" and duration not in [5, 10]:
                duration = 10

            if provider == "wan":
                duration = 5

            if provider == "luma" and duration not in [5, 9]:
                duration = 9

            if provider == "pixverse" and duration not in [5, 8]:
                duration = 8

            if provider == "wan":
                model = "wan-video/wan-2.2-i2v-fast"
                input_data = {
                    "image": image,
                    "prompt": prompt
                }

            elif provider == "kling":
                model = "kwaivgi/kling-v2.1"
                input_data = {
                    "start_image": image,
                    "prompt": prompt,
                    "duration": duration
                }

            elif provider == "luma":
                model = "luma/ray-flash-2-720p"
                input_data = {
                    "image": image,
                    "prompt": prompt
                }

            elif provider == "pixverse":
                model = "pixverse/pixverse-v5"
                input_data = {
                    "image": image,
                    "prompt": prompt
                }

            elif provider == "fal":
                model = "fal-ai/wan-i2v"
                input_data = {
                    "image_url": image,
                    "prompt": prompt
                }

            elif provider == "replicate":
                model = "stability-ai/stable-video-diffusion"
                input_data = {
                    "input_image": image,
                    "motion_bucket_id": 127,
                    "cond_aug": 0.02
                }

            else:
                raise Exception("Unknown video provider: " + provider)

            output = replicate.run(
                model,
                input=input_data
            )

            if isinstance(output, list):
                video_url = output[0]
            else:
                video_url = output

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "video": str(video_url),
                "provider": provider,
                "model": model
            }).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())
