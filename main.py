import logging
import sys
import time

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# pydantic model
class ModelInput(BaseModel):
    user_id: Optional[int]
    text: str

# ML model
tokenizer = AutoTokenizer.from_pretrained("pierreguillou/gpt2-small-portuguese")
model = AutoModelForCausalLM.from_pretrained("model")
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer)

# API
app = FastAPI(title="MyModelApp", version="0.0.1")
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@app.get("/")
async def root():
    return {"message": "This is my model API."}

@app.post("/mymodel")
async def generate_text(inpt: ModelInput):
    t0 = time.perf_counter()
    response = pipe(inpt.text)
    time_elapsed = time.perf_counter() - t0
    logging.info("Model input: " + inpt.text)
    logging.info("Model output: " + response[0]["generated_text"])
    logging.info("Time elapsed: " + str(round(time_elapsed, 4)) + " s")
    return response