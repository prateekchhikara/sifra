import click
from rich import print, print_json
from rich.console import Console
from utils import horizontalLine, initialize_global_variables, get_bio
from pyfiglet import figlet_format

from langchain_openai.chat_models import ChatOpenAI

import warnings
warnings.filterwarnings("ignore")

from logger import logger




@click.command()
@click.option('--pinfo', 
              default = "person_info.txt", 
              required =True, 
              help = 'Path to the file containing the information of the person.',
              prompt = '🤖 > : Please enter the path to the file containing the information of the person. This will help me understand the person better. \nDefault file: ')
def cli(pinfo):
    """
        This function is the entry point for the AI Assistant. It is a Click command line interface that takes in the path to the file containing the information of the person as an argument. 
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
        # model= "gpt-4o", 
        model = "gpt-3.5-turbo-0125",
        streaming=True,
        temperature=0.0,
        max_tokens=200,
    )

    # Start the conversation --------------------------------------------------------
    # import pdb; pdb.set_trace()