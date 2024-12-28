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

    return "dummy llm"

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
    return "I’m standing on a beach, but the water is a shimmering lavender color, and the sky above me is split into two halves—one a soft pastel pink, the other a vibrant electric blue. The sand under my feet feels warm like a summer afternoon, but a chilly breeze brushes past my shoulders. In the distance, I see floating lanterns bobbing along the lavender water, each one flickering with light that shifts from green to gold and back again.\n\nAs I walk along the shoreline, the sky’s colors melt together, creating ribbons of swirling light overhead. Suddenly, a grand wooden door appears right where the sand meets the waves. It stands upright with no walls around it. Curious, I push it open and step through—only to find myself in a cathedral made entirely of glass. Sunlight—though there is no sun—floods the interior, refracting into rainbows that dance across the polished floors.\n\nAt the far end of the cathedral, there’s a small pond surrounded by lilac vines. A silver fish leaps out of the water, and when it does, the entire scene ripples like a pebble dropped into a still lake. The walls quiver and the floor bends beneath my feet. My reflection on the glass wall smiles at me—but in slow motion, as if I’m floating underwater.\n\nI feel a strange mixture of awe and calmness, as if I’ve found a hidden place I’ve been searching for all my life. It’s silent, yet I sense a quiet melody humming in the background. I try to walk toward the pond to get a closer look at the fish, but as I move, I wake up—heart pounding, unsure whether I’m relieved or disappointed to return to reality."
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