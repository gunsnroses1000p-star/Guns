import os, json, time, base64, urllib.request
from http.server import BaseHTTPRequestHandler
from PIL import Image, ImageDraw
from io import BytesIO

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            token = os.environ.get("REPLICATE_API_TOKEN")
            if not token:
                raise Exception("Missing REPLICATE_API_TOKEN")

            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length).decode("utf-8"))

            image1 = data.get("image1")
            image2 = data.get("image2")
            prompt = data.get("prompt", "")
            direction = data.get("direction", "horizontal")

            if not image1 or not image2:
                raise Exception("Missing image1 or image2")

            def load_image(src):
                if src.startswith("data:"):
                    raw = src.split(",", 1)[1]
                    return Image.open(BytesIO(base64.b64decode(raw))).convert("RGB")
                with urllib.request.urlopen(src) as r:
                    return Image.open(BytesIO(r.read())).convert("RGB")

            img1 = load_image(image1)
            img2 = load_image(image2)

            if direction == "horizontal":
                size = (768, 768)
                img1 = img1.resize(size)
                img2 = img2.resize(size)

                canvas = Image.new("RGB", (1536, 768))
                canvas.paste(img1, (0, 0))
                canvas.paste(img2, (768, 0))

                mask = Image.new("RGB", (1536, 768), "black")
                draw = ImageDraw.Draw(mask)
                draw.rectangle((620, 0, 916, 768), fill="white")

                aspect_ratio = "16:9"
            else:
                size = (768, 768)
                img1 = img1.resize(size)
                img2 = img2.resize(size)

                canvas = Image.new("RGB", (768, 1536))
                canvas.paste(img1, (0, 0))
                canvas.paste(img2, (0, 768))

                mask = Image.new("RGB", (768, 1536), "black")
                draw = ImageDraw.Draw(mask)
                draw.rectangle((0, 620, 768, 916), fill="white")

                aspect_ratio = "9:16"

            def to_data_url(img):
                buf = BytesIO()
                img.save(buf, format="PNG")
                return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

            seamless_prompt = f"""
Create one seamless realistic photograph from this image.
Only repaint the masked middle area.
Blend both sides into one continuous natural scene.
Remove the visible split, border, seam, fade line, or collage effect.
Match lighting, shadows, perspective, colors, background, and depth of field.
Preserve the woman's face, identity, hairstyle, body proportions, outfit details, and realistic anatomy.
Do not create duplicate people. Do not add extra limbs. Do not remove arms or hands.
Make the final image look like one professional photo captured in a single moment.
Photorealistic, cinematic, realistic skin texture, natural proportions.
{prompt}
"""

            payload = {
                "version": "black-forest-labs/flux-fill-pro",
                "input": {
                    "image": to_data_url(canvas),
                    "mask": to_data_url(mask),
                    "prompt": seamless_prompt,
                    "aspect_ratio": aspect_ratio,
                    "output_format": "webp",
                    "output_quality": 90
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

            prediction_url = result.get("urls", {}).get("get")

            for _ in range(60):
                if result.get("status") == "succeeded":
                    break
                if result.get("status") == "failed":
                    raise Exception("Prediction failed: " + str(result.get("error")))
                time.sleep(2)

                poll_req = urllib.request.Request(
                    prediction_url,
                    headers={"Authorization": f"Bearer {token}"},
                    method="GET"
                )
                with urllib.request.urlopen(poll_req) as poll_resp:
                    result = json.loads(poll_resp.read().decode())

            output = result.get("output")
            image_url = output[0] if isinstance(output, list) else output

            if not image_url:
                raise Exception("No image returned from Flux Fill")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"image": image_url}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
          
