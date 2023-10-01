import streamlit as st
from octoai.client import Client
from pathlib import Path
from pydantic import BaseModel
from typing import List, Dict
import json
from hashlib import sha256
import yaml
from octoai.types import Image
st.set_page_config(layout="wide")

BASE_PATH = Path(__file__).parent
ENV_PATH = BASE_PATH / "conf.yaml"
CONF = yaml.safe_load(ENV_PATH.open())

IMAGES_PATH = BASE_PATH / "generated_images"

# Create a directory to store the images
IMAGES_PATH.mkdir(parents=True, exist_ok=True)

# Load token from yaml file
OCTOAI_TOKEN = CONF["token"]
OCTOAI_ENDPOINT = CONF["endpoint"]
client = Client(token=OCTOAI_TOKEN)
endpoint = OCTOAI_ENDPOINT + "/predict"
healthcheck = OCTOAI_ENDPOINT + "/healthcheck"

class Config(BaseModel):
    prompt: str
    prompt_2: str
    negative_prompt: str
    sampler: str
    cfg_scale: float
    height: int
    width: int
    seed: int
    steps: int
    num_images: int
    high_noise_frac: float
    strength: float
    use_refiner: bool
    model: str # coming soon
    loras: Dict[str, float] # coming soon
    
# Create an instance of the Config Pydantic model with default values

config = Config(
    prompt="a cat in a fishbowl hyperrealistic painting",
    prompt_2="a happy little cat in a fishbowl with happy little fish",
    negative_prompt="ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft",
    sampler="DPM++2MKarras",
    cfg_scale=7.5,
    height=1024,
    width=1024,
    seed=42,
    steps=20,
    num_images=1,
    high_noise_frac=0.92,
    strength=0.92,
    use_refiner=True,
    model="default",
    loras={
        "crayon-style": 0.0,
        "paint-splash": 0.0
    }
)

# Generic helper funcs

# Run inference with the OctoAI SDK
def eg_octo_inference(input_payload, endpoint=endpoint, healthcheck=healthcheck):
    if client.health_check(healthcheck) == 200:
        
        # Run inference
        outputs = client.infer(endpoint_url=endpoint, inputs=input_payload)
        
        # Check if 'num_images' is specified in the input_payload
        num_images = input_payload.get("num_images", 1)
        
        # Initialize a list to store the output file names
        output_file_names = []
        
        # Loop through each image variant
        for i in range(num_images):
            # Get the image data for the current variant
            image_data = outputs["completion"]["image_" + str(i)]
            
            # Calculate payload_id with a numerical identifier
            payload_id = sha256(f"{input_payload}_{i}".encode()).hexdigest()
            
            # Generate the output file name with the numerical identifier
            output_file_name = str(IMAGES_PATH / f"{payload_id}_octo_{i}.png")
            #st.write("Saving image to", output_file_name)
            
            # Convert and save the base64 image with PIL
            Image.from_base64(image_data).to_file(output_file_name)
            
            # Append the output file name to the list
            output_file_names.append(output_file_name)
        
        return output_file_names

st.markdown("""
<style>
    /* Adjust the font size and padding to make the button larger */
    .stButton > button {
        font-size: 40px; /* Increase the font size */
        padding: 10px 20px; /* Increase the padding */
        background-color: #0077b6; /* Set the background color to marine blue */
        color: white; /* Set the text color to white */
    }
    /* Style the tabs */

	.stTabs [aria-selected="true"] {
  		background-color: #0077b6;
        padding: 10px 20px; /* Increase the padding */
        border-radius: 5px; /* Add rounded corners to the tabs */
        
	}
 
    /* Style the active tab */
    .stTabs [aria-selected="true"] {
        background-color: #005B8E; /* Set the background color for the active tab */
        border-radius: 5px; /* Add rounded corners to the active tab */
        font-size: 40px; /* Increase the font size */
    }
    
</style>
""", unsafe_allow_html=True)
# First curl command to test the service


# Streamlit inputs for each field in the Config model
def sd_inputs():
    col1, col2 = st.columns(2)
    
    with col1:

        config.prompt = st.text_input("Prompt", config.prompt)
        config.prompt_2 = st.text_input("Prompt 2", config.prompt_2)
        config.negative_prompt = st.text_input("Negative Prompt", config.negative_prompt)
        config.sampler = st.selectbox("Sampler",["DPM++2MKarras", "KLMS", "DDIM", "DDPM", "K_EULER", "K_EULER_ANCESTRAL", "DPMSolverMultistep", "PNDM", "DPMSingle", "HEUN", "DPM_2", "DPM2_ANCESTRAL"])
        config.cfg_scale = st.slider("CFG Scale",step=0.5,value=config.cfg_scale,max_value=30.0)
        config.height = st.number_input("Height", config.height)
        config.width = st.number_input("Width", config.width)
        
    with col2:
        config.seed = st.number_input("Seed", value=config.seed)
        config.steps = st.slider("Steps", value=config.steps,step=1,max_value=100)
        config.num_images = st.number_input("Number of Images", config.num_images)
        config.high_noise_frac = st.slider("High Noise Fraction", value=config.high_noise_frac,step=0.1,max_value=1.0)
        config.strength = st.number_input("Strength", config.strength)
        config.use_refiner = st.checkbox("Use Refiner", config.use_refiner)
        config.model = st.selectbox("Custom Checkpoints", ["default","copax-timeless", "crystal-clear", "duchaiten-aiart", "realcartoon", "samaritan"])

def sd_inputs_loras():
    config.loras["crayon-style"] = st.slider("Crayon Style", config.loras["crayon-style"],step=0.1)
    config.loras["paint-splash"] = st.slider("Paint Splash", config.loras["paint-splash"],step=0.1)


    #config.loras.crayon_style = st.number_input("Crayon Style", config.loras.crayon_style)
    #config.loras.paint_splash = st.number_input("Paint Splash", config.loras.paint_splash)
        
    # Display the updated config

# Wrapper func to update data configuration as changes made


def main():

    st.title('OctoAI Imagen & SDXL Evaluation | Typeface')
    # Global controls, config, and variables
    # Setup the sidebar
    st.sidebar.title("Quickstart")
    your_token=st.sidebar.text_input("Enter your OctoML SDXL token", value="your-token")
    endpoint_url=st.sidebar.text_input("Enter your OctoML SDXL endpoint", value="https://image.octoai.run")
    
    # If the user has entered a token and endpoint
    # Update token yaml configuration file
    if your_token != "your-token":
        CONF["token"] = your_token
        with open(ENV_PATH, "w") as f:
            yaml.dump(CONF, f)

    if endpoint_url != "https://image.octoai.run":
        CONF["endpoint"] = endpoint_url
        with open(ENV_PATH, "w") as f:
            yaml.dump(CONF, f)
    
    inference_button = st.sidebar.button("Run Inference")
    
    # Layout
    
    col1, col2 = st.columns([0.4, 0.6])
    # Container 1
    with col2:
        container1 = st.container()

        tab1,tab2 = container1.tabs(["Text2Image","Lora Configs"])
        with tab1:
            # Display config params
            sd_inputs()
            
        with tab2:
            # Display config params
            sd_inputs_loras()
            
    img_placeholder = container1.empty()
        
    if inference_button:

        # Run inference
        # Drop model key if equal 'default'
        payload = config.dict()
        if payload["model"] == "default":
            del payload["model"]
            del payload["loras"]
        #st.code(payload)
        img_res = eg_octo_inference(payload)
        
        # Update placeholder with image
        img_placeholder.image(img_res, width=300)
                
    container1.write(config.dict())
            
    # Sections
    # Section 1
    with col1:
        st.header("Quickstart")
        st.write(""" To get started, please see the sample scenarios below. As you adjust your SDXL parameters, the request payload will automatically update.
                 Press the _Run Inference_ button to generate an example images from.
        """)
        st.subheader("Endpoint Test")
        st.write(""" 
                Set your token and endpoint. You can paste your OctoAI token in the sidebar and press _eEnter_ to set it. This will update the 
                token in the `conf.yaml` file.
                
                Copy and paste the curl command below into your terminal to confirm your OctoAI SDXL
                endpoint is ready to accept resuts. 
                """)
        updated_config_params = json.dumps(config.dict(),indent=4)

        st.code(f"""
                curl -H 'Content-Type: application/json'\
                    -H 'Authorization: Bearer {OCTOAI_TOKEN}'\
                    -X POST 'https://image.octoai.run/predict'\
                    -d '{updated_config_params}'
                    """, language="bash")
        
        # Section 2 - Try another one
        st.subheader("A custom result")
        st.write(""" 
                Update the parameters to change the image. 
                * Try something like: ```'A cat in a fishbowl swimming with goldfish hyperrealism'```
                * Change the sampler (scheduler) to `K_EULER`.
                * Change the number of steps to `30`.
                """)
        
        # Section 3 - Multiple images
        st.subheader("Multiple images")
        st.write(""" 
                You can also generate multiple images at once. Try changing the number of images to `3`.
                """)
        
        # Seection 4 - Custom checkpoints
        st.subheader("Custom checkpoints")
        st.write(""" 
                You can generate images from custom checkpoints. Change the model setting to ```copax-timeless``` and click the _Run Inference_ button.
                """)
        
        # Section 5 - Loras
        st.subheader("Using LoRAs")
        st.write(""" 
               Apply a LoRA to guide the output image style from the `Lora Configs` tab. Try changing the ```crayon-style``` and ```paint-splash``` settings to `0.7` and `0.3` respectively.
                """)
        
        # Section 5 - Full API reference
        st.subheader("Full API reference")
        st.write(""" 
                Navigate to the full SDXL Image Gen API refernece from the sidebar.
                """)

    
            
if __name__ == "__main__":
    main()
