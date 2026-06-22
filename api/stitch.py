import json
import os
import time
import base64
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

            # Upload a single base64 image to Replicate file storage
            def upload_image(b64_data):
                if "," in b64_data:
                    header, b64_data = b64_data.split(",", 1)
                    # Detect mime type
                    mime = "image/png"
                    if "jpeg" in header or "jpg" in header:
                        mime = "image/jpeg"
                    elif "webp" in header:
                        mime = "image/webp"
                else:
                    mime = "image/png"

                image_bytes = base64.b64decode(b64_data)
                upload_req = urllib.request.Request(
                    "https://api.replicate.com/v1/files",
                    data=image_bytes,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": mime
                    },
                    method="POST"
                )
                with urllib.request.urlopen(upload_req) as resp:
                    result = json.loads(resp.read().decode())
                url = result.get("urls", {}).get("get") or result.get("url")
                if not url:
                    raise Exception("Failed to upload image to Replicate: " + json.dumps(result))
                return url

            # Upload both images
            if image1.startswith("data:") or (len(image1) > 300 and not image1.startswith("http")):
                image1_url = upload_image(image1)
            else:
                image1_url = image1

            if image2.startswith("data:") or (len(image2) > 300 and not image2.startswith("http")):
                image2_url = upload_image(image2)
            else:
                image2_url = image2

            # Build a prompt that instructs the model to blend both images
            prompt = """
Combine these two images into one single realistic seamless photo.
Use the left image as the main base scene.
Preserve the woman's face, body, hairstyle, and identity from the images.
Create one continuous environment with matching lighting, shadows, colors, camera angle, and depth of field.
Remove any visible split, border, fade line, or collage effect.
Make it look like one natural professional photograph.
Photorealistic, cinematic, ultra detailed, realistic skin texture, natural proportions.
"""
                aspect_ratio = "9:16"

            # Use flux-dev with image prompt weights for both source images
            payload = {
                "version": "black-forest-labs/flux-dev",
                "input": {
                    "prompt": stitch_prompt,
                    "image_prompt": image1_url,
                    "image_prompt2": image2_url,
                    "aspect_ratio": aspect_ratio,
                    "output_format": "webp",
                    "output_quality": 90,
                    "num_inference_steps": 28,
                    "guidance": 3.5
                }
            }

            req = urllib.request.Request(
                "https://api.replicate.com/v1/predictions",
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

            # Poll until complete (max 120s)
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
                raise Exception("No image returned from model. Status: " + str(result.get("status")) + " Error: " + str(result.get("error")))

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"image": image_url}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
