from transformers import AutoModelForCausalLM
import config

model = AutoModelForCausalLM.from_pretrained(config.PRETRAINED_MODEL)
model.save_pretrained(config.MODEL_PATH)
