from src.engine_backend.engine_generation import generate_dream_scenario, generate_interaction, load_engine_llm
import textwrap
import time
import os

QUIT_STRING = "quit"

def print_newborn_description():
    title = "Welcome to the newborn game engine"
    line_break = "***********************************"
    description_p1 = "The newborn engine is a speculative game engine which supposes that neural decoding, in conjunction with generative technologies, could be adapted to produce a kind of technologically assisted lucid dreaming, allow us to interrogate dreams with the kind of lucidity that only grips us in the hours after we awake."
    description_p2 = "In its current form, newborn engine is trained on the descriptions of online users, who obsess over their dreams––sharing them online so as to achieve a similar lucidity through more analog means. In this version, the engine will ask you to provide a description of your most recent dream, its characters, images and other details that you can recount. From there, it will generate descriptions of this dream and a means to interact with text descriptions of their characters––allowing you to play them out in real time."

    lines = [title, line_break, description_p1, description_p2, line_break]

    for l in lines:
        print(f'\033[94m{textwrap.fill(l, 100)}\033[0m\n')
        time.sleep(0)

    return f"{title}\n\n{line_break}\n\n{description_p1}\n\n{description_p2}\n\n{line_break}"


def prompt_dream_description():
    prompt = "To begin, please provide a description of your most recent dream in as much detail as you can conjure, including any characters, scenery or interactions. If you would like to close the game engine, please type \"quit\":"
    dream_description = input(f"\033[94m{textwrap.fill(prompt, 100)}\n\n\033[0m")
    print()
    
    return f"{prompt}\n\n{dream_description}"

def prompt_user_interaction():
    prompt = "Please type your response below:"
    user_response = input(f"\033[94m{prompt}\033[0m\n\n")
    print()

    return f"{prompt}\n\n{user_response}"

def has_user_exited(user_response):
    lines = user_response.split("\n\n")
    return len(lines) > 0 and lines[len(lines) - 1].strip().lower() == QUIT_STRING

def save_game(context):
    file_name = f"gamelog_{time.strftime("%Y%m%d-%H%M%S")}"
    output_file_path = f"../../output/{file_name}.txt"

    line_break = "***********************************"
    quit_text = "Thank you for playing!"
    readout_info = f"A readout of this gameplay has been saved to: {output_file_path}"

    termination_chunk = f"{line_break}\n\n{quit_text}\n\n{readout_info}"
    context = context + termination_chunk

    print(f"\033[94m{termination_chunk}\033[0m")
    
    with open(output_file_path, "w") as file:
        file.write(context)

if __name__ == "__main__":
    context = print_newborn_description()
    [ engine_llm, engine_tokenizer ] = load_engine_llm()
    is_new_game = True

    while(True):
        prompt = ""

        if(is_new_game):
            prompt = prompt_dream_description()
        else:
            prompt = prompt_user_interaction()
        
        
        if(has_user_exited(prompt)):
            context = context + "\n\n" + prompt + "\n\n"
            break

        else:
            if(is_new_game):
                generated_content = generate_dream_scenario(engine_llm, engine_tokenizer, prompt, context)
                is_new_game = False
            else:
                generated_content = generate_interaction(engine_llm, engine_tokenizer, prompt, context)
            
            context = f"{context}\n\n{prompt}\n\n{generated_content}"
            print()

    save_game(context)