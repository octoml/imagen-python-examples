import requests
import json
import os
import base64

# Load token from environment variable or set it here
OCTOAI_TOKEN = os.getenv("OCTOAI_TOKEN")

# Define the API endpoint
url = "https://image.octoai.run/predict"

# Define the payload as a dictionary
payload = {
    "cfg_scale": 11,
    "width": 1024,
    "height": 1024,
    "high_noise_frac": 0.92,
    "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft",
    "num_images": 1,
    "prompt": "A cat in a fishbowl hyperrealism",
    "sampler": "K_DPMPP_2M",
    "seed": 2748252853,
    "steps": 20,
    "use_refiner": True,
		"model": "realcartoon",
    "loras": {
        "crayon-style": 0.7,
        "paint-splash": 0.3
    }
}

# Define headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OCTOAI_TOKEN}"
}

# Send the POST request
response = requests.post(url, data=json.dumps(payload), headers=headers)

# Check the response status code
if response.status_code == 200:
    blob = response.json()
    image_base64 = blob["completion"]["image_0"]
    image_data = base64.b64decode(image_base64)
    
    # Save the response to a JSON file
    with open("octoai_response.json", "w") as outfile:
        json.dump(blob, outfile)
        
    # Save base 64 image to a file
    with open("octoai_example_image.png", "wb") as outfile:
        outfile.write(image_data)
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)