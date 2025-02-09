import os
import sys
from pathlib import Path

import yaml

from helpers.utils import get_model_type_from_input

HERE = Path(__file__).parent
CONF_PATH: Path = HERE / "conf.yaml"


if CONF_PATH.is_file():
    with open(CONF_PATH, "r") as f:
        config = yaml.safe_load(f)

    try:

        # LLM Api
        model_name = config["llm_api"]["model_name"]
        client_type = get_model_type_from_input(model_name)

        if client_type.model_family == "MISTRAL":
            os.environ["MISTRAL_API_KEY"] = config["llm_api"]["key"]

        key = os.environ["MISTRAL_API_KEY"]

        # Frontend
        video_path = config["frontend"]["video_path"]
        manim_code_path = config["frontend"]["manim_code_path"]

    except KeyError as e:
        sys.exit(f"The parameter '{e}' was not found. Please check {CONF_PATH}.")
