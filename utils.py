import shutil, json, os
from dotenv import load_dotenv

def horizontalLine():
    terminal_width = shutil.get_terminal_size().columns
    print('-' * terminal_width)


def initialize_global_variables():
    load_dotenv()

    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    os.environ["LANGCHAIN_PROJECT"] = "Sifra"

def get_bio(pinfo):
    with open(pinfo, 'r') as file:
        data = file.read()

    data = data.replace("\n", " ")
    data = data.replace("  ", " ")

    return data