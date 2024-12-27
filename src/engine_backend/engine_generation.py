from src.engine_backend.llm_helpers import load_peft_llm

def load_engine_llm():
    print('Loading the newborn engine model, please wait...\n')

    model_id = "embodied-restoration-lab/lorde-language-model-7b-v0.1"
    base_model_id = "mistralai/Mistral-7B-Instruct-v0.1"
    engine_llm = load_peft_llm(model_id, base_model_id)

    print('Model loaded!\n')
    return engine_llm

def generate_dream_scenario(llm, prompt, context):
    dream_scenario = "[GENERATED DREAM SCENARIO]"
    print(dream_scenario)
    return dream_scenario

def generate_interaction(llm, prompt, context):
    interaction = "[GENERATED NEXT INTERACTION]"
    print(interaction)
    return interaction