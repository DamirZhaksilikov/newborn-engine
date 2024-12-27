from src.engine_backend.engine_generation import generate_dream_scenario, generate_interaction
import textwrap
import time

QUIT_STRING = "quit"

def print_newborn_description():
    title = "Welcome to the newborn game engine"
    line_break = "***********************************"
    description_p1 = "The newborn engine is a speculative game engine which supposes that neural decoding, in conjunction with generative technologies, could be adapted to produce a kind of technologically assisted lucid dreaming, allow us to interrogate dreams with the kind of lucidity that only grips us in the hours after we awake."
    description_p2 = "In its current form, newborn engine is trained on the descriptions of online users, who obsess over their dreams––sharing them online so as to achieve a similar lucidity through more analog means. In this version, the engine will ask you to provide a description of your most recent dream, its characters, images and other details that you can recount. From there, it will generate descriptions of this dream and a means to interact with text descriptions of their characters––allowing you to play them out in real time."

    print()
    print(title, "\n")
    print(line_break, "\n")
    print(textwrap.fill(description_p1, 100), "\n")
    print(textwrap.fill(description_p2, 100), "\n")
    print(line_break, "\n")

    return f"{title}\n\n{line_break}\n\n{description_p1}\n\n{description_p2}\n\n{line_break}"


def prompt_dream_description():
    prompt = "To begin, please provide a description of your most recent dream in as much detail as you can conjure, including any characters, scenery or interactions. If you would like to close the game engine, please type \"quit\":"
    dream_description = input(textwrap.fill(prompt, 100) + "\n\n")
    print()
    
    return f"{prompt}\n\n{dream_description}\n\n"

def prompt_user_interaction():
    prompt = "Please type your response below:"
    user_response = input(f"{prompt}\n\n")
    print()

    return f"{prompt}\n\n{user_response}\n\n"

def has_user_exited(user_response):
    lines = user_response.split("\n\n")
    return len(lines) > 1 and lines[len(lines) - 2].strip().lower() == QUIT_STRING

def save_game(context):
    file_name = f"gamelog_{time.strftime("%Y%m%d-%H%M%S")}"
    output_file_path = f"../../output/{file_name}"

    line_break = "***********************************"
    quit_text = "Thank you for playing!"
    readout_info = f"A readout of this gameplay has been saved to: {output_file_path}"

    termination_chunk = f"{line_break}\n\n{quit_text}\n\n{readout_info}\n"
    context = context + termination_chunk

    print(termination_chunk)
    
    with open(output_file_path, "w") as file:
        file.write(context)

if __name__ == "__main__":
    context = ""

    while(True):
        prompt = ""
        is_new_game = len(context) == 0

        if(is_new_game):
            context = print_newborn_description()
            prompt = prompt_dream_description()
        else:
            prompt = prompt_user_interaction()
        
        
        if(has_user_exited(prompt)):
            context = context + prompt + "\n"
            break

        else:
            if(is_new_game):
                generated_content = generate_dream_scenario(prompt, context)
            else:
                generated_content = generate_interaction(prompt, context)
            
            context = f"{context}\n{prompt}\n{generated_content}\n"
            print()

    save_game(context)