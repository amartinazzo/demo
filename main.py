import logging
import sys
import time

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

import config

# pydantic model
class ModelInput(BaseModel):
    user_id: Optional[int]
    text: str

# ML model
tokenizer = AutoTokenizer.from_pretrained(config.PRETRAINED_MODEL)
model = AutoModelForCausalLM.from_pretrained(config.MODEL_PATH)
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer)

# API
app = FastAPI(
    title="MyModelApp",
    version="0.0.1",
    description="""
This is my model API!

## What it does

It generates text in Portuguese.
"""
)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@app.get("/", tags=["home"])
async def home():
    """
    my docstring
    """
    return {"message": "This is my model API."}

@app.post("/model", tags=["model"])
async def generate_text(inpt: ModelInput):
    """
    my other docstring
    """
    t0 = time.perf_counter()
    response = pipe(inpt.text)[0]
    time_elapsed = time.perf_counter() - t0
    logging.info("Model input: " + inpt.text)
    logging.info("Model output: " + response["generated_text"])
    logging.info("Time elapsed: " + str(round(time_elapsed, 4)) + " s")
    return response