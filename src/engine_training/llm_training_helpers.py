from transformers import AutoTokenizer
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from trl import SFTTrainer
from peft import LoraConfig
from transformers import TrainingArguments


def load_tokenizer(model_id):
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=HF_TOKEN)

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    if tokenizer.model_max_length > 100_000:
        tokenizer.model_max_length = 2048
    
    return tokenizer

def load_llm(model_id):
    compute_dtype = getattr(torch, "float16")

    quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=compute_dtype
    )
    device_map = {"": torch.cuda.current_device()} if torch.cuda.is_available() else None

    model_kwargs = dict(
        attn_implementation="flash_attention_2",
        torch_dtype="auto",
        use_cache=False,
        device_map=device_map,
        quantization_config=quantization_config,
    )

    return AutoModelForCausalLM.from_pretrained(model_id, **model_kwargs)

def train_llm(base_model, train_dataset, output_model_id, output_dir):
    version_number = 0.1
    output_dir = f"data/{output_model_id}"

    training_args = TrainingArguments(
        fp16=True,
        do_eval=False,
        gradient_accumulation_steps=128,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        learning_rate=2.0e-04,
        log_level="info",
        logging_steps=5,
        logging_strategy="steps",
        lr_scheduler_type="cosine",
        max_steps=-1,
        num_train_epochs=1,
        output_dir=output_dir,
        overwrite_output_dir=True,
        per_device_train_batch_size=1,
        push_to_hub=True,
        hub_model_id=output_model_id,
        hub_strategy="every_save",
        report_to="tensorboard",
        save_strategy="no",
        save_total_limit=None,
        seed=42,
    )

    peft_config = LoraConfig(
            r=64,
            lora_alpha=16,
            lora_dropout=0.1,
            bias="none",
            task_type="CAUSAL_LM",
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )

    trainer = SFTTrainer(
            model=base_model,
            args=training_args,
            train_dataset=train_dataset,
            dataset_text_field="text",
            tokenizer=tokenizer,
            packing=True,
            peft_config=peft_config,
            max_seq_length=tokenizer.model_max_length,
        )
    
    train_result = trainer.train()
    trainer.push_to_hub()