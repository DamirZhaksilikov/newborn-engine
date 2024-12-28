import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
import os
from dotenv import load_dotenv
from transformers import AutoTokenizer

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

    base_model = AutoModelForCausalLM.from_pretrained(base_model_id, **model_kwargs, token=HF_TOKEN)
    config = PeftConfig.from_pretrained(peft_model_id)
    return PeftModel.from_pretrained(base_model, peft_model_id)

def load_tokenizer(model_id):
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=HF_TOKEN)

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    if tokenizer.model_max_length > 100_000:
        tokenizer.model_max_length = 2048
    
    return tokenizer

def llm_generate(llm, tokenizer, model_input):
    input_ids = tokenizer(model_input, return_tensors="pt", truncation=True).input_ids.cuda()

    outputs = llm.generate(
        input_ids=input_ids,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95
    )

    return tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0][len(full_prompt):]