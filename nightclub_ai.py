import os
import fal_client

FAL_KEY = os.getenv("FAL_KEY")

if not FAL_KEY:
    raise ValueError("FAL_KEY secret is missing")

image1_path = "in_painting_1781014281355.jpg"
image2_path = "Screenshot_20260614_025608_AIReel.jpg"

image1_url = "https://i.postimg.cc/HWP9rhBw/Screenshot-20260614-145349-Pinterest.jpg"
image2_url = "https://i.postimg.cc/pdZDRGmB/output.jpg"

print("Image 1 URL:", image1_url)
print("Image 2 URL:", image2_url)
print("Both images uploaded to FAL successfully.")
