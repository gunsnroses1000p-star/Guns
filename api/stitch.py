import json
import os
import time
import urllib.request
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            token = os.environ.get("REPLICATE_API_TOKEN")
            if not token:
                raise Exception("Missing REPLICATE_API_TOKEN")

            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)

            image1 = data.get("image1", "")
            image2 = data.get("image2", "")
            direction = data.get("direction", "horizontal")
            prompt = data.get("prompt", "seamless blend, perfect transition")

            if not image1 or not image2:
                raise Exception("Both images are required")

            # Upload base64 images to Replicate file upload endpoint
            def upload_image(b64_data):
                # Strip data URI prefix if present
                if "," in b64_data:
                    b64_data = b64_data.split(",", 1)[1]
                import base64
                image_bytes = base64.b64decode(b64_data)
                upload_req = urllib.request.Request(
                    "https://api.replicate.com/v1/files",
                    data=image_bytes,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "image/png"
                    },
                    method="POST"
                )
                with urllib.request.urlopen(upload_req) as resp:
                    result = json.loads(resp.read().decode())
                return result.get("urls", {}).get("get") or result.get("url")

            # Only upload if base64, otherwise use as-is (URL)
            if image1.startswith("data:") or (len(image1) > 500 and not image1.startswith("http")):
                image1_url = upload_image(image1)
            else:
                image1_url = image1

            if image2.startswith("data:") or (len(image2) > 500 and not image2.startswith("http")):
                image2_url = upload_image(image2)
            else:
                image2_url = image2

            if direction == "horizontal":
                stitch_instruction = "Place the first image on the left and the second image on the right, blending them into one seamless wide panoramic image with a smooth natural transition in the middle."
            else:
                stitch_instruction = "Place the first image on top and the second image on the bottom, blending them into one seamless tall image with a smooth natural transition in the middle."

            full_prompt = (
                f"{stitch_instruction} "
                f"First image: {image1_url} "
                f"Second image: {image2_url} "
                f"{prompt}"
            )

            payload = {
                "input": {
                    "prompt": full_prompt,
                    "aspect_ratio": "21:9" if direction == "horizontal" else "9:21",
                    "output_format": "webp",
                    "output_quality": 90,
                    "go_fast": True,
                    "megapixels": "1"
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

            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode())

            # Poll if not complete
            prediction_url = result.get("urls", {}).get("get")
            for _ in range(60):
                status = result.get("status")
                if status == "succeeded":
                    break
                if status == "failed":
                    raise Exception("Prediction failed: " + str(result.get("error")))
                if prediction_url:
                    time.sleep(2)
                    poll_req = urllib.request.Request(
                        prediction_url,
                        headers={"Authorization": f"Bearer {token}"},
                        method="GET"
                    )
                    with urllib.request.urlopen(poll_req) as poll_resp:
                        result = json.loads(poll_resp.read().decode())
                else:
                    break

            output = result.get("output")
            image_url = output[0] if isinstance(output, list) else output

            if not image_url:
                raise Exception("No image returned from model")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"image": image_url}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
