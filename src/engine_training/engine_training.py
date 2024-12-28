from datasets import Dataset, load_dataset
from src.engine_constants.engine_constants import DREAM_DATASET_PATH, BASE_MODEL_ID, PEFT_MODEL_ID
from src.engine_training.llm_training_helpers import load_tokenizer, load_llm, trian_llm

def create_training_row(documents, input, output):
    instructions = get_model_behavior_instruction()

    if(documents != None):
       instructions = f"{instructions}\n\n{create_document_instructions(documents)}"

    text_row = f"""[INST] <<SYS>> {instructions}<</SYS>>\n\nBelow is the game context, generate a dream scenario based on it:\n\n{input} [/INST] \n {output} </s>"""
    return text_row

def create_training_data(dataset, output_file_path):
    with open(output_file_path, "w") as output_file:
        for item in dataset:
            training_line = {
                "text": create_training_row(item["Documents"], item["User"] ,item["Assistant"]),
                "documents": item["Documents"],
                "input": item["User"],
                "output": item["Assistant"]
            }
            output_file.write(json.dumps(training_line) + "\n")

if __name__ == "__main__":
    dataset = load_dataset(DREAM_DATASET_PATH, split="train", token=HF_TOKEN)
    train_data_path = "../../datasets/reddit-dream-descriptions.jsonl"
    create_training_data(dataset, train_data_path)
    train_dataset = load_dataset('json', data_files=train_data_path , split='train')

    tokenizer = load_tokenizer(BASE_MODEL_ID)
    llm = load_llm(BASE_MODEL_ID)
    train_llm(llm, train_dataset, PEFT_MODEL_ID, '../../models')