# OctoAI Imagen & SDXL Evaluation | Typeface

This repo contains the minimum set of instructions for Typeface to get started using OctoAI's Image Generation and SDXL capabilities. As we continue to roll out new features and functionality, we will update this documentation to support your onboarding on to the OctoAI platform.

We strongly recommend you read our [docs](https://docs.octoai.cloud/docs), which include robust examples and tutorials.

- [SDK & CLI Installation](https://docs.octoai.cloud/docs/installation-links)
- [Python SDK Examples](https://docs.octoai.cloud/docs/use-the-python-client-for-templates)
- [OctoAI Home](https://octoai.cloud/)


### Document Overview
- [Quick Start & Basic Usage](#quick-start--basic-usage)
- [Explore the Image Generation SDXL API with Streamlit](#explore-the-image-generation-sdxl-api-with-streamlit)
- [OctoAI Image Generation API Reference](#octoai-image-generation-api-reference)

## Quick Start & Basic Usage

Install the project requirements and set your environment variables. Then, run the cURL command below to generate an image. (We will share your token separately.) 

Clone this repo:
```bash
# Installs this repo
git clone https://github.com/octoml/typeface-external.git

cd typeface-external

# RECOMMENDED" Create a new conda enviroment - 
# conda create --name octoai

# install requirements
pip install -r requirements.txt

```
Set up OctoAI environment variables:
```bash
export OCTOAI_ACCESS_TOKEN=<sent separately>
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
To make exploring the OctoAI service easier, launch the Streamlit app included in this reposotiry. 

```bash
streamlit run app/1_OctoAI_Eval.py
```

This will launch a Streamlit app that will allow you to explore all the functionality of the OctoAI service, including customization features, such as loras, negative prompts, checkpoints, and more.

## OctoAI Image Generation API Reference
This document describes the arguments you can provide to the Image Generation API. It supports a rich set of configurations for generating images.

### `prompt`
- **Type**: `string`
- **Description**: Describes the image to generate.
- **Constraints**:
    - Maximum of 77 tokens.
    - Supports prompt weighting. For example: `(A tall (beautiful:1.5) woman:1.0) (some other prompt with weight:0.8)`.
    - Weight is the product of all brackets a token is in. The brackets, colons, and weights don't count towards the token count.

### `prompt_2`
- **Type**: `string`
- **Description**: 
    - Default mode (when only `prompt` is set): Input of `prompt` is copied to `prompt_2`.
    - Otherwise, `prompt` is used for "word salad" style control, and `prompt_2` is for more human-readable descriptions.
- **Examples**:
    - `prompt = "photorealistic, high definition, masterpiece, sharp lines"`
    - `prompt_2 = "A portrait of a handsome cat wearing a little hat. The cat is in front of a colorful background."`

### `negative_prompt` (Optional)
- **Type**: `string`
- **Description**: Steer away from certain themes.

### `sampler` (Optional)
- **Type**: `string`
- **Description**: Specifies which scheduler to use for image generation.
- **Default**: `DDIM`
- **Available Values**:
    - `PNDM`: `PNDMScheduler`
    - `KLMS`: `LMSDiscreteScheduler`
    - `DDIM`: `DDIMScheduler`
    - `DDPM`: `DDPMScheduler`
    - `K_EULER`: `EulerDiscreteScheduler`
    - `K_EULER_ANCESTRAL`: `EulerAncestralDiscreteScheduler`
    - `DPMSolverMultistep`: ["DPMSolverMultistepScheduler", {"use_karras_sigmas": False}]
    - `K_DPMPP_2M`: `["DPMSolverMultistepScheduler", {"use_karras_sigmas": True}]
    - `DPM++2MKarras`: `DPMSolverMultistepScheduler`
    - `KLMS`: `LMSDiscreteScheduler`
    - `DPMSingle`: `DPMSolverSinglestepScheduler`
    - `HEUN`: `HeunDiscreteScheduler`
    - `DPM_2`: `KDPM2DiscreteScheduler`
    - `DPM2_ANCESTRAL`: `KDPM2AncestralDiscreteScheduler`
    - `DPM++ SDE Karras`: [DPMSolverSDEScheduler, {"use_karras_sigmas": True}]

### `height` (Optional)
- **Type**: `int`
- **Description**: Specifies the height of the output image.
- **Default**: `1024`

### `width` (Optional)
- **Type**: `int`
- **Description**: Specifies the width of the output image.
- **Default**: `1024`

### Supported Resolutions

| Resolution | Aspect Ratio |
|------------|--------------|
| 1024x1024  | 1:1          |
| 1152x896   | 4:3          |
| 896x1152   | 3:4          |
| 1216x832   | 4:3          |
| 896x1152   | 3:4          |
| 832x1216   | 3:4          |
| 1344x768   | 16:9         |
| 768x1344   | 9:16         |
| 1536x640   | 12:5         |
| 640x1536   | 5:12         |


### `cfg_scale` (Optional)
- **Type**: `float`/`int`
- **Description**: How strictly the process adheres to the prompt.
- **Default**: `12`

### `steps` (Optional)
- **Type**: `int`
- **Description**: Number of diffusion steps.
- **Default**: `30`

### `num_images`
- **Type**: `int`
- **Description**: Number of images to generate.

### `seed` (Optional)
- **Type**: `int`
- **Description**: Fixes random noise for replicable results.
- **Default**: Random

### `style_preset` (Optional)
- **Type**: `string`
- **Description**: Guides the output image style.
- **Available Values**: `3d-model`, `analog-film`, `anime`, ... (include all other styles here)

### `use_refiner`
- **Type**: `bool`
- **Description**: Use the refiner or not.

### `high_noise_frac` (Optional)
- **Type**: `float`/`int`
- **Description**: Determines noise amount using the base model vs. refiner.
- **Default**: `0.8`

### `model`
- **Type**: `string`
- **Description**: Checkpoints supported.
- **Available Values**: `copax-timeless`, `crystal-clear`, ... (include all other models here)

### `loras`
- **Type**: `string`
- **Description**: LoRAs supported in name-weight pairs.
- **Available Values**: `add-detail`, `crayon-style`, ... (include all other LoRAs here)

### `init_image` (Optional)
- **Type**: `string`
- **Description**: Use an image as a starting point. Encoded in base64.

### `strength` (Optional)
- **Type**: `float`/`int`
- **Description**: Noise amount for img2img use cases.
- **Default**: `0.8`

## Notes
- **Img2Img Cases**: `init_image` and `strength` are applicable only for Img2Img cases.
