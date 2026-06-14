import os
import fal_client

FAL_KEY = os.getenv("FAL_KEY")

if not FAL_KEY:
    raise ValueError("FAL_KEY secret is missing")

image1_path = "in_painting_1781014281355.jpg"
image2_path = "Screenshot_20260614_025608_AIReel.jpg"

image1_url = fal_client.upload_file(image1_path)
image2_url = fal_client.upload_file(image2_path)

print("Image 1 URL:", image1_url)
print("Image 2 URL:", image2_url)
print("Both images uploaded to FAL successfully.")
