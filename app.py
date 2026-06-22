import gradio as gr
import replicate
import tempfile
import os

MODEL_NAME = "luma/dream-machine"

def generate_video(image):
    # Save uploaded image to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        image.save(tmp.name)
        image_path = tmp.name

    # Call Replicate model
    output = replicate.run(
        MODEL_NAME,
        input={
            "image": open(image_path, "rb"),
            "num_frames": 40,
            "fps": 15
        }
    )

    return output

demo = gr.Interface(
    fn=generate_video,
    inputs=gr.Image(type="pil", label="Upload an Image"),
    outputs=gr.Video(label="Generated Video"),
    title="Image → Video Generator (Replicate)",
    description="Generate a video from an image using Replicate's Dream Machine or any other I2V model."
)

demo.launch()

