def load_engine_llm():
    model_id = "embodied-restoration-lab/lorde-language-model-7b-v0.1"
    embedding_model_id = "intfloat/multilingual-e5-large"
    return load_peft_llm(model_id, base_model_id, hf_token)

def generate_dream_scenario(llm, prompt, context):
    print("""[GENERATED DREAM SCENARIO]""")

def generate_interaction(llm, prompt, context):
    print("""[GENERATED NEXT INTERACTION]""")