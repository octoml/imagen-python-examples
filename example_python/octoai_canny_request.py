"""Query ControlNet SDXL."""

import base64
import io
import os
import time

import PIL.Image
import requests
from pathlib import Path
BASE_PATH = Path(__file__).parent.resolve()

prod_token = os.environ.get("OCTOAI_TOKEN")  # noqa
assert prod_token is not None, "OCTOAI_TOKEN environment variable not set"


def _process_test(endpoint_url):
    image_path = BASE_PATH / "logo.png"
    image = PIL.Image.open(image_path)
		
		# Create a BytesIO buffer to hold the image data
    image_buffer = io.BytesIO()
    image.save(image_buffer, format='PNG')
    image_bytes = image_buffer.getvalue()
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')


    model_request = {
        "image": encoded_image,
        "prompt": (
            "aerial view, a futuristic research complex in a bright "
            "foggy jungle, hard lighting"
        ),
        "negative_prompt": "low quality, bad quality, sketches",
        "num_inference_steps":50, 
        "controlnet_conditioning_scale": 0.5,
        "num_images_per_prompt": 1
    }

    prod_token = os.environ.get("OCTOAI_TOKEN")  # noqa
    start = time.time()
    reply = requests.post(
        f"{endpoint_url}",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {prod_token}",
						'X-OctoAI-Queue-Dispatch': 'true'
        },
        json=model_request,
    )
    print(f"Generation took {time.time()-start} seconds")

    assert reply.status_code == 200

    img_list = reply.json()["images"]

    for i, ibytes in enumerate(img_list):
        img_bytes = base64.b64decode(ibytes)
        img = PIL.Image.open(io.BytesIO(img_bytes))
        img.load()
        img.save(f"result_image{i}.png")


if __name__ == "__main__":
    a10 = "https://control-sdxl2-vvwbynjr46vc.octoai.run/canny"
    a100 = "https://controlnet-sdxl-a100-vvwbynjr46vc.octoai.run/canny"

    # Change this line to call either a10 or a100
    _process_test(a100)