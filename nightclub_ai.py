import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

image1_path = "in_painting_1781014281355.jpg"
image2_path = "Screenshot_20260614_025608_AIReel.jpg"

prompt = """
Photorealistic nightclub scene featuring the two reference subjects together in one seamless image.
They are standing close together on a crowded dance floor, smiling and dancing in a natural affectionate pose.
Colorful purple, blue, and pink neon lights, atmospheric haze, disco lights, realistic shadows,
matching lighting on both people, natural body proportions, stylish nightlife clothing,
cinematic photography, sharp facial detail, realistic skin tones, energetic party atmosphere,
shallow depth of field, high-resolution detail.
"""

print("Nightclub AI script created.")
print("Image 1:", image1_path)
print("Image 2:", image2_path)
print("Prompt:", prompt)
