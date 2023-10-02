# Image Generation API Reference | ControlNet - Canny

## Parameters

### `prompt` (Optional[str])
The prompt or prompts to guide image generation. If not defined, you need to pass `prompt_embeds`.

### `prompt_2` (Optional[str])
The prompt or prompts to be sent to `tokenizer_2` and `text_encoder_2`. If not defined, the prompt is used in both text-encoders.

### `image` (bytes)
The `ControlNet` input condition to provide guidance to the `unet` for generation. If the type is specified as `torch.FloatTensor`, it is passed to `ControlNet` as is. `PIL.Image.Image` can also be accepted as an image. The dimensions of the output image default to the image's dimensions. If height and/or width are passed, the image is resized accordingly. If multiple `ControlNets` are specified in `init`, images must be passed as a list such that each element of the list can be correctly batched for input to a single `ControlNet`.

### `height` (Optional[int])
The height in pixels of the generated image. Anything below 512 pixels won't work well for `stabilityai/stable-diffusion-xl-base-1.0` and checkpoints that are not specifically fine-tuned on low resolutions.

### `width` (Optional[int])
The width in pixels of the generated image. Anything below 512 pixels won't work well for `stabilityai/stable-diffusion-xl-base-1.0` and checkpoints that are not specifically fine-tuned on low resolutions.

### `num_inference_steps` (Optional[int])
The number of denoising steps. More denoising steps usually lead to a higher-quality image at the expense of slower inference.

### `guidance_scale` (Optional[float])
A higher guidance scale value encourages the model to generate images closely linked to the text prompt at the expense of lower image quality. Guidance scale is enabled when `guidance_scale > 1`.

### `negative_prompt` (Optional[str])
The prompt or prompts to guide what to not include in image generation. If not defined, you need to pass `negative_prompt_embeds` instead. Ignored when not using guidance (`guidance_scale < 1`).

### `negative_prompt_2` (Optional[str])
The prompt or prompts to guide what to not include in image generation. This is sent to `tokenizer_2` and `text_encoder_2`. If not defined, `negative_prompt` is used in both text-encoders.

### `num_images_per_prompt` (Optional[int])
The number of images to generate per prompt.

### `eta` (Optional[float])
Corresponds to parameter eta (η) from the DDIM paper. Only applies to the `DDIMScheduler` and is ignored in other schedulers.

### `low_threshold` (Optional[int])
Canny low threshold.

### `high_threshold` (Optional[int])
Canny high threshold.

### `controlnet_conditioning_scale` (Optional[float])
The outputs of the `ControlNet` are multiplied by `controlnet_conditioning_scale` before they are added to the residual in the original `unet`. If multiple `ControlNets` are specified in `init`, you can set the corresponding scale as a list.

### `control_guidance_start` (Optional[float])
The percentage of total steps at which the `ControlNet` starts applying.

### `control_guidance_end` (Optional[float])
The percentage of total steps at which the `ControlNet` stops applying.

### `guess_mode` (Optional[bool])
The `ControlNet` encoder tries to recognize the content of the input image even if you remove all prompts. A `guidance_scale` value between 3.0 and 5.0 is recommended.

### `original_size` (Optional[tuple[int]])
If `original_size` is not the same as `target_size`, the image will appear to be down- or upsampled. `original_size` defaults to `(width, height)` if not specified. Part of SDXL's micro-conditioning as explained in section 2.2 of the [SDXL paper](https://huggingface.co/papers/2307.01952).

### `crops_coords_top_left` (Optional[tuple[int]])
`crops_coords_top_left` can be used to generate an image that appears to be "cropped" from the position `crops_coords_top_left` downwards. Favorable, well-centered images are usually achieved by setting `crops_coords_top_left` to `(0, 0)`. Part of SDXL's micro-conditioning as explained in section 2.2 of the [SDXL paper](https://huggingface.co/papers/2307.01952).

### `target_size` (Optional[tuple[int]])
For most cases, `target_size` should be set to the desired height and width of the generated image. If not specified, it will default to `(width, height)`. Part of SDXL's micro-conditioning as explained in section 2.2 of the [SDXL paper](https://huggingface.co/papers/2307.01952).

### `negative_original_size` (Optional[tuple[int]])
To negatively condition the generation process based on a specific image resolution. Part of SDXL's micro-conditioning as explained in section 2.2 of the [SDXL paper](https://huggingface.co/papers/2307.01952).

### `negative_crops_coords_top_left` (Optional[tuple[int]])
To negatively condition the generation process based on specific crop coordinates. Part of SDXL's micro-conditioning as explained in section 2.2 of the [SDXL paper](https://huggingface.co/papers/2307.01952).

### `negative_target_size` (Optional[tuple[int]])
To negatively condition the generation process based on a target image resolution. It should be the same as the `target_size` for most cases. Part of SDXL's micro-conditioning as explained in section 2.2 of the [SDXL paper](https://huggingface.co/papers/2307.01952).

### `seed` (Optional[int])
Set this to a fixed number if you want to reproduce image output.

**Note:** Parameter defaults are indicated where applicable.