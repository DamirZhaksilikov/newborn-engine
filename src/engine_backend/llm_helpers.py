import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
import os
from dotenv import load_dotenv

load_dotenv() 
HF_TOKEN = os.environ.get('HF_API_KEY')

def load_peft_llm(peft_model_id, base_model_id):
    compute_dtype = getattr(torch, "float16")

    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=compute_dtype
    )
    device_map = {"": torch.cuda.current_device()} if torch.cuda.is_available() else None

    model_kwargs = dict(
        torch_dtype="auto",
        use_cache=False,
        device_map=device_map,
        quantization_config=quantization_config,
    )

    #base_model = AutoModelForCausalLM.from_pretrained(base_model_id, **model_kwargs, token=HF_TOKEN)
    #config = PeftConfig.from_pretrained(peft_model_id)
    return None #PeftModel.from_pretrained(base_model, peft_model_id)