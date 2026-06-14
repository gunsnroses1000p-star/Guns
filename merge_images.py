from PIL import Image

image1_path = "in_painting_1781014281355.jpg"
image2_path = "Screenshot_20260614_025608_AIReel.jpg"

img1 = Image.open(image1_path).convert("RGB")
img2 = Image.open(image2_path).convert("RGB")

height = min(img1.height, img2.height)

img1 = img1.resize((int(img1.width * height / img1.height), height))
img2 = img2.resize((int(img2.width * height / img2.height), height))

merged_width = img1.width + img2.width
merged = Image.new("RGB", (merged_width, height))

merged.paste(img1, (0, 0))
merged.paste(img2, (img1.width, 0))

merged.save("merged_output.jpg")

print("Saved merged_output.jpg")
