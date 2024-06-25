import shutil, os
from dotenv import load_dotenv
import json
from rich.console import Console
from rich.json import JSON

console = Console()

def horizontalLine():
    """
        Print a horizontal line across the terminal.
    """

    terminal_width = shutil.get_terminal_size().columns
    print('-' * terminal_width)


def initialize_global_variables():
    """
        Load environment variables from a .env file.
    """
    load_dotenv()

    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    os.environ["LANGCHAIN_PROJECT"] = "Sifra"

def get_bio(pinfo):
    """
    Retrieve the biography information from a specified file.

    Args:
        pinfo (str): The path to the file containing the person's information.

    Returns:
        str: A string containing the biography information, with unnecessary whitespace and newlines removed.
    """

    with open(pinfo, 'r') as file:
        data = file.read()

    data = data.replace("\n", " ")
    data = data.replace("  ", " ")

    return data

def managerMessageList(messages, k):
    """
    Manage a list of messages to ensure its length does not exceed a specified limit.

    This function keeps the first two messages and the last (k-2) messages if the total number of messages exceeds 'k'.
    It's designed to maintain a compact list of messages by preserving the start, a portion of the end, and trimming the middle.

    Args:
        messages (list): The list of messages to be managed.
        k (int): The maximum number of messages to keep in the list.

    Returns:
        list: The managed list of messages with a length not exceeding 'k'.
    """

    if len(messages) > k:
        messages = [messages[0], messages[1]] + messages[-(k-1):]

    return messages


def get_memory():
    """
    Retrieve the current state of memory from a persistent storage.

    This function is intended to load the memory state from a file or database (not implemented in the snippet provided).
    It should be modified to include the actual implementation details based on the storage mechanism used.

    Returns:
        dict: A dictionary representing the loaded memory state. The structure and content of this dictionary will depend on the implementation.
    """

    with open("memory.json", "r") as file:
        memory = json.load(file)

    return memory

def check_exit(keyboard):
    """
    Check if the user wants to exit the chat.

    Args:
        keyboard (str): The input string from the user.

    Returns:
        bool: True if the user wants to exit, False otherwise.
    """

    if keyboard in ["1", "exit", "quit", "bye", "goodbye"]:
        return True
    
    return False

def show_memory():
    """
    Display the contents of the memory.json file.

    This function reads the memory.json file and prints its contents. If the file is empty,
    it indicates that there is no memory yet.
    """

    with open("memory.json", "r") as file:
        memories = json.load(file)
        if not memories:
            console.print(" 🤖 > [bold]Sifra:[/] Oopsy!! Sorry, I don't have any memory yet.", style="yellow")
        else:
            console.print(" 🤖 > [bold]Sifra:[/] Here is the memory that I have 👇", style="green")
            # console.print(json.dumps(memories, indent=4), style="italic magenta1")

            # print only if there is a value corresponding to the key

            temp_memories = {}
            for key, value in memories.items():
                if value:
                    temp_memories[key] = value
                    console.print(f"{key}: {value}", style="magenta")

    return temp_memories

def show_messages(messages):
    """
    Show the messages in the message buffer.

    Args:
        messages (list): A list of message objects to be displayed. Each message object
                         should have a 'type' attribute indicating if it's an 'ai' or 'system'
                         message, and a 'content' attribute containing the message text.
    """

    for message in messages:
        if message.type == "ai":
            console.print(f" 🤖 > [bold]Sifra:[/] {message.content}", style="white")
        elif message.type == "system":
            console.print(f" 🖥️ > [bold]System:[/] {message.content}", style="white")
        else:
            console.print(f" 👤 > [bold]You:[/] {message.content}", style="white")
