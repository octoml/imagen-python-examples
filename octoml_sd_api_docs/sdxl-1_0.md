# Image Generation API Reference | SDXL 1.0

## Overview
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
