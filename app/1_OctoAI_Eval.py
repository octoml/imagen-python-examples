import streamlit as st
from octoai.client import Client
import subprocess
from dotenv import load_dotenv
import os
from pathlib import Path
from pydantic import BaseModel
from typing import List
import json
from hashlib import sha256
import yaml
from octoai.types import Image

BASE_PATH = Path(__file__).parent
ENV_PATH = BASE_PATH / "conf.yaml"
CONF = yaml.safe_load(ENV_PATH.open())

IMAGES_PATH = BASE_PATH / "generated_images"

# Create a directory to store the images
IMAGES_PATH.mkdir(parents=True, exist_ok=False)

# Load token from yaml file
OCTOAI_TOKEN = CONF["token"]
OCTOAI_ENDPOINT = CONF["endpoint"]
client = Client(token=OCTOAI_TOKEN)
endpoint = OCTOAI_ENDPOINT + "/predict"
healthcheck = OCTOAI_ENDPOINT + "/healthcheck"

# Pydantic schema for the request body
class LorasConfig(BaseModel):
    crayon_style: float
    paint_splash: float
    
class Config(BaseModel):
    prompt: str
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
    # loras: LorasConfig # coming soon
    
# Create an instance of the Config Pydantic model with default values
config = Config(
    prompt="a cat in a fishbowl hyperrealistic painting",
    negative_prompt="ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, blurry, bad anatomy, blurred, watermark, grainy, signature, cut off, draft",
    sampler="DPM++2MKarras",
    cfg_scale=7.5,
    height=1024,
    width=1024,
    seed=0,
    steps=20,
    num_images=1,
    high_noise_frac=0.92,
    strength=0.92,
    use_refiner=True,
    model=""
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
            st.write("Saving image to", output_file_name)
            
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
        config.negative_prompt = st.text_input("Negative Prompt", config.negative_prompt)
        config.sampler = st.selectbox("Sampler",["PNDM", "KLMS", "DDIM", "DDPM", "K_EULER", "K_EULER_ANCESTRAL", "DPMSolverMultistep", "DPM++2MKarras", "DPMSingle", "HEUN", "DPM_2", "DPM2_ANCESTRAL"])
        config.cfg_scale = st.number_input("CFG Scale", config.cfg_scale,step=0.5)
        config.height = st.number_input("Height", config.height)
        config.width = st.number_input("Width", config.width)
        
    with col2:
        config.seed = st.number_input("Seed", config.seed)
        config.steps = st.number_input("Steps", config.steps)
        config.num_images = st.number_input("Number of Images", config.num_images)
        config.high_noise_frac = st.number_input("High Noise Fraction", config.high_noise_frac)
        config.strength = st.number_input("Strength", config.strength)
        config.use_refiner = st.checkbox("Use Refiner", config.use_refiner)
        #config.model = st.text_input("Model", config.model)


def sd_inputs_loras():
    return

    #config.loras.crayon_style = st.number_input("Crayon Style", config.loras.crayon_style)
    #config.loras.paint_splash = st.number_input("Paint Splash", config.loras.paint_splash)
        
    # Display the updated config
    
      
def config_payload():
    # Assuming you already have the `config` Pydantic model instance
    json_payload = config.dict()

    # Convert the Python dictionary to a JSON string
    json_payload_str = json.dumps(json_payload, indent=4)
    return json_payload_str
        
    


# Image styling section
def section_three(inference_button):
    
    
    if inference_button:
        updated_config_params = config.dict()
        st.write(updated_config_params)
        img_res = eg_octo_inference(config.dict())
        # Display the image
        st.image(img_res, width=400)

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

    tab1,tab2 = st.tabs(["Text2Image","ControlNet - Coming Soon"])
    with tab1:
        # Display config params
        sd_inputs()
        
        if inference_button:
            updated_config_params = config.dict()
            st.write(updated_config_params)
            img_res = eg_octo_inference(config.dict())
            # Display the image
            st.image(img_res, width=400,use_column_width="auto")
            # Show tab2 by default
    
    # Sections
    # Section 1
    st.header("Quickstart")
    st.write(""" Let's run a few basic queries against the OctoML SDXL 
    endpoint you were provided to make sure it's working correclty. 
    I've provided some sample code with SDXL queries below. You can press:
    'run code' to see the code go.""")
    st.subheader("1. Endpoint Test")
    st.write(""" 
             To get started, ensure you've set your token and endpoint. You can paste your
             token in the sidebar and press 'enter.'
             
             Copy and paste the curl command below into your terminal to confirm your OctoAI SDXL
             endpoint is ready to accept resuts. 
             """)
    new_payload = json.dumps(config.dict(),indent=4)

    st.code(f"""
            curl -H 'Content-Type: application/json'\
                 -H 'Authorization: Bearer {OCTOAI_TOKEN}'\
                 -X POST 'https://image.octoai.run/predict'\
                 -d '{new_payload}'
                 """, language="bash")
    
    # Section 2
    
    st.subheader("2. The OctoML SDK")
    st.markdown(""" Use the OctoML SDK run inferences against SDXL endpoint in a more
             repeatable, programmable, and CI/CD friendly way.
             If you haven't already, install the OctoML SDK with:""")
    st.code("pip install octoai", language="bash")
    # Run inference with the OctoAI SDK
    new_payload = json.dumps(config.dict(),indent=4)
    
    # Section 3 - Try another one
    st.subheader("3. A different result")
    st.write(""" 
             Update the parameters to change the image. Try something like: 'A cat in a fishbowl'
                and see what happens. You can also change the sampler to 'DPM++2MKarras' to get a different results
             """)
    
    # Section 4 - Multiple images
    st.subheader("4. Multiple images")
    st.write(""" 
             You can also generate multiple images at once. Try changing the number of images to 3.
             """)
    
    
    with tab2:
        sd_inputs()

        st.write("Coming soon")
            
if __name__ == "__main__":
    main()
