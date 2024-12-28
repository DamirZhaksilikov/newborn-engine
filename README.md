Note, that given that this project runs a 7 billion parameter it cannot be run on most machines. Please refer to the documentation here to understand further: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1

To run, install the following dependencies

```
pip install 'transformers[torch]'
pip install 'bitsandbytes' 'peft'
pip install 'pinecone-client' 'pinecone-notebooks'
pip install python-dotenv
pip install flash-attn --no-build-isolation
```

Then to use the program, navigate to the CLI directory and run

```
cd src/engine_cli/
python engine_cli.py
```