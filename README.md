# OctoAI Imagen & SDXL Examples

This repo contains a minimum set of instructions to get started using OctoAI's Image Generation and SDXL capabilities. As we continue to roll out new features and functionality, we will update this documentation to support your onboarding on to the OctoAI platform.

We strongly recommend you read our [docs](https://docs.octoai.cloud/docs), which include robust examples and tutorials.

- [SDK & CLI Installation](https://docs.octoai.cloud/docs/installation-links)
- [Python SDK Examples](https://docs.octoai.cloud/docs/use-the-python-client-for-templates)
- [OctoAI Home](https://octoai.cloud/)


### Document Overview
- [Quick Start & Basic Usage](#quick-start--basic-usage)
- [Explore the Image Generation SDXL API with Streamlit](#explore-the-image-generation-sdxl-api-with-streamlit)
- [ControlNet SDXL](#controlnet-sdxl)
- [OctoAI Image Generation API Reference](#octoai-image-generation-api-reference)



## Quick Start & Basic Usage
Run the cURL command below to generate an image. (We will share your token separately.) 

For more advanced examples, clone this repo and install the requirements.txt file to launch an application that will allow you to explore all the functionality of the OctoAI service, including customization features, such as loras, negative prompts, checkpoints, and more.

Set up OctoAI environment variables:

```bash
export OCTOAI_ACCESS_TOKEN=<your_token_here>
export OCTOAI_ENDPOINT_URL=https://image.octoai.run
```

### OctoAI Image Generation cURL Example
Copy and paste the curl command below into your terminal to confirm your OctoAI SDXL endpoint is ready to accept resuts. 

```bash
curl -H 'Content-Type: application/json' -H "Authorization: Bearer $OCTOAI_TOKEN" -X POST "https://image.octoai.run/predict" \
    -d '{
        "prompt": "A cat in a fishbowl hyperrealism",
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft",
				"sampler": "K_DPMPP_2M",
        "cfg_scale": 11,
        "height": 1024,
				"width": 1024,
        "seed": 2748252853,
        "steps": 20,
        "num_images": 1,
        "high_noise_frac": 0.92,
				"strength": 0.92,
        "use_refiner": true,
        "model": "realcartoon",
        "loras": {
            "crayon-style": 0.7,
            "paint-splash": 0.3
        }
    }' | jq -r ".completion.image_0" | base64 -d > catbowl.png  

```
### OctoAI Image Generation Python Example
Check out the example code below. Run the code with:

```bash
python octoai_request.py
```

```python
import requests
import json

# Replace with your actual token
OCTOAI_TOKEN = "your_token_here"

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
    "prompt": "The angel of death Hyperrealistic, splash art, concept art, mid shot, intricately detailed, color depth, dramatic, 2/3 face angle, side light, colorful background",
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
    # Save the response to a JSON file
    with open("response.json", "w") as outfile:
        json.dump(response.json(), outfile)
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)

```

## Explore the Image Generation SDXL API with Streamlit
To make exploring the OctoAI service easier, run the code below to build and launch a Streamlit app to explore the Image Generation SDXL API.

```bash
Clone this repo:
```bash
# Installs this repo
git clone https://github.com/octoml/imagen-python-examples.git

cd imagen-python-examples

# RECOMMENDED" Create a new conda enviroment - 
# conda create --name octoai

# install requirements
pip install -r requirements.txt

```

```bash
streamlit run app/1_OctoAI_Eval.py
```

This will launch a Streamlit app that will allow you to explore all the functionality of the OctoAI service, including customization features, such as loras, negative prompts, checkpoints, and more.
