from engine_backend.engine_generation import generate_dream_scenario, generate_interaction

QUIT_STRING = "quit"

def print_newborn_description():
        print("""
Welcome to the newborn game engine
    
***********************************

The newborn engine is a speculative game engine which supposes
that neural decoding, in conjunction with generative technologies,
could be adapted to produce a kind of technologically assisted lucid 
dreaming, allow us to interrogate them with the kind of lucidity that 
only grips us in the hours after we awake.

In its current form, newborn engine is trained on the descriptions of
online users, who obsess over their dreams––sharing them online so as
to achieve a similar lucidity through more analog means. In this version,
the engine will ask you to provide a description of your most recent dream,
its characters, images and other details that you can recount. From there,
it will generate descriptions of this dream and a means to interact with
text descriptions of their characters––allowing you to play them out in real
time.

***********************************

""")


def prompt_dream_description():
    return input("""To begin, please provide a description of your most recent dream in as much 
detail as you can conjure, including any characters, scenery or interactions.
If you would like to close the game engine, please type "quit":\n\n""")

def prompt_user_interaction():
    return ""

def save_game(context):
        print("""***********************************
Thank you for playing!

A readout of this gameplay has been saved to: {output_file_path}""")

if __name__ == "__main__":
    context = ""
    has_user_exited = False

    while(not has_user_exited):
        new_context = ""
        is_new_game = len(context) == 0

        if(is_new_game):
            print_newborn_description()
            new_context = prompt_dream_description()
        else:
            new_context = prompt_user_interaction()
        
        context = context + new_context + "\n"
        
        if(new_context.strip().lower() == QUIT_STRING):
            has_user_exited = True
            save_game(context)
        elif(is_new_game):
            generate_dream_scenario(context)
        else:
            generate_interaction(context)