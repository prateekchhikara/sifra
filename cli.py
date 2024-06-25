import click
import json
from logger import logger
from rich import print
from rich.console import Console
from pyfiglet import figlet_format

# Langchain imports
from langchain_core.runnables import RunnableSequence
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain import PromptTemplate

# Local imports
from utils import (
    horizontalLine, managerMessageList, get_memory, initialize_global_variables, 
    get_bio, check_exit, show_memory, show_messages
    )
from prompts import intro_prompt
from memory.memory import MemoryManager


import warnings
warnings.filterwarnings("ignore")




@click.command()
@click.option('--pinfo', 
              default = "person_info.txt", 
              required =True, 
              help = 'Path to the file containing the information of the person.',
              prompt = '🤖 > : Please enter the path to the file containing the information of the person. This will help me understand the person better. \nDefault file: ')
def cli(pinfo):
    """
        This function is the entry point for the AI Assistant. 
        It is a Click command line interface that takes in the path to the file containing the information of the person as an argument. 
    """


    # Initialize the global variables ------------------------------------------------
    initialize_global_variables()
    console = Console()

    console.print("Welcome, I am [bold]SIFRA[/] ([bold]S[/b]uper [bold]I[/]ntelligent and [bold]F[/]riendly [bold]R[/]esponsive [bold]A[/]gent) 🤖 ")
    console.print(figlet_format("S I F R A ", font = "standard", width = 100, justify = "center"), style = "bold bright_yellow")
    
    logger.info("-" * 50)
    logger.info("Starting the Sifra AI Assistant")
    
    horizontalLine()

    # Get the information of the person ---------------------------------------------
    data = get_bio(pinfo)

    console.print(data, style = "italic white")
    horizontalLine()

    # Initialize the LLM model -------------------------------------------------------
    llmMain = ChatOpenAI(
        model= "gpt-4", 
        # model = "gpt-3.5-turbo-0125",
        streaming=True,
        temperature=0.0,
        max_tokens=200,
    )

    # write initial memory to file -------------------------------------------
    mem = MemoryManager(llmMain)
    mem.generate_initial_memory(data)


    # Generate the prompt for the AI to introduce itself --------------------------------
    prompt_template = PromptTemplate(
        input_variables=["person_information"],
        template=intro_prompt,
    )
    sequence = RunnableSequence(prompt_template | llmMain)
    response = sequence.invoke({"person_information" : data}).content

    console.print(f" 🤖 > [bold]Sifra:[/] {response}", style = "green")

    # Collecting all messages -------------------------------------------------------
    memory = get_memory()
    messages = [
        SystemMessage("You are Sifra, an AI assistant. You are very amiable and helpful. You love assisting people and help them in the conversation. Start with a greeting and then ask the person how they are doing. You can pick one of the points from the information so that it seems like you know the person well."),
        SystemMessage(f"About me: {json.dumps(memory)}"),
        AIMessage(response)
    ]


    while True:
        print("Options: [1] Exit ❌ | [2] Show Memory 🧠 | [3] Debug 🛠️ | [4] Message Buffer 📋 \n")

        # Get the user input -----------------------------------------------------------
        keyboard = input(" 👤 > You: ")
        
        horizontalLine()

        # Check if the user wants to exit
        if check_exit(keyboard):
            break

        # Check if the user wants to show the memory
        if keyboard == "2":
            show_memory()
            continue

        # Check if the user wants to debug
        if keyboard == "3":
            import pdb; pdb.set_trace()
            # enter c to continue
            continue

        if keyboard == "4":
            show_messages(messages)
            continue

       
        # Add the user message to the list of messages ---------------------------------
        messages.append(HumanMessage(keyboard))

        # Get the response from the AI -------------------------------------------------
        ai_response = llmMain(messages).content

        # Add the AI response to the list of messages ----------------------------------
        messages.append(AIMessage(ai_response))

        # Print the AI response --------------------------------------------------------
        console.print(" 🤖 > [bold]Sifra:[/] ", ai_response, style = "green")

        # Manage the messages list -----------------------------------------------------
        messages = managerMessageList(messages, k = 5)

        # Modify the memory ------------------------------------------------------------
        memory = mem.modify_memory(keyboard)
        messages[1] = SystemMessage(f"About me: {json.dumps(memory)}")

        # import pdb; pdb.set_trace()


    

if __name__ == '__main__':
    cli()