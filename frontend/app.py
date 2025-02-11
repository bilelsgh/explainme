import json
import os
import sys

sys.path.append("../explainme")

import streamlit as st

from clients.llmclient import AVAILABLE_MODELS
from config.config import key, video_path
from frontend.utils import generate_video
from helpers.utils import get_llm_client, get_model_type_from_input

st.title("Explain me!")

# Model choice
client_choice = st.selectbox("Chose your model", list(AVAILABLE_MODELS.keys()))
client_choice = client_choice
model_type = get_model_type_from_input(client_choice)

# Init the client
if "client" not in st.session_state or st.session_state.client_choice != client_choice:
    prompt_instr = """
            The user will provide you with three pieces of information: a topic, a concept, and its description.
            Your task is to generate a Python script using the Manim library to visually illustrate the concept without any texts except annotations or formulas.
            Follow these strict rules to ensure clarity and readability:

            1. Clarity & Spacing
            No Overlapping: Very important! Objects and text must never overlap. I don't want any object to be on a text
            No Off-Screen Elements: Ensure that all text and objects remain within the video frame
            Proper Spacing: Distribute elements evenly and avoid clustering too many elements at the same time.
            Efficient Object Management: Clean regularly. If an object is no longer needed, remove it from the scene instead of keeping unnecessary elements that may clutter the visualization.

            2. Text Handling
            Limit Text Size: Use concise text and avoid large paragraphs.
            Position Carefully: Use .next_to() or .move_to() with spacing constraints to keep text readable.
            If too much text → Prioritize animations that reveal content progressively instead of showing everything at once.

            3. Object Management
            Remove unnecessary objects once they are no longer needed.
            Animate text appearance sequentially rather than displaying everything at once.
            Use smooth transitions (e.g., .fade_out(), .shift(), .transform()) instead of abrupt changes.

            4. Code Structure
            Name the scene class DynamicScene.
            Ensure the code is self-contained and executable as-is.
            Use comments to structure the script logically.
            Output format: Return only the Python code. No explanations or extra text.

            Here is the history of the conversation:
            {chat_history}

            User: {input}
            Assistant:
            """

    try:
        st.session_state.client = get_llm_client(
            model=model_type, key=key, prompt_instruction=prompt_instr
        )
        st.session_state.client_choice = client_choice
        st.session_state.request_ongoing = False
        st.info(f"Model `{client_choice}` selected.")
    except Exception as e:
        st.error(f"Error while creating the client: {e}")

# Start the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inputs
topic = st.selectbox(
    "What is the topic of the concept you want me to explain ?",
    ["Math", "Computer Science", "Physics", "Chemistry", "Other"],
)
concept_name = st.text_input(
    "What is this concept? Go straight to the point",
)
description = st.text_area(
    "Tell me a bit more about this concept and how you want me to explain it."
)

user_input = {"topic": topic, "concept_name": concept_name, "description": description}

if st.button(
    "Explain me!",
    disabled=not (topic and concept_name and description)
    or st.session_state.request_ongoing,
):
    manim_code = st.session_state.client.ask(json.dumps(user_input))
    st.session_state.request_ongoing = True
    with st.spinner("Let me cook a clear video to illustrate the concept. 👨🏻‍🍳"):
        generate_video(manim_code)

    st.session_state.request_ongoing = False
    video = os.listdir(video_path)
    st.video(f"{video_path}/videos/1080p60/DynamicScene.mp4", autoplay=True)
