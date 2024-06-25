import json
import streamlit as st
from rich.console import Console
from pyfiglet import figlet_format

# Langchain imports
from langchain_core.runnables import RunnableSequence
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain import PromptTemplate

# Local imports (Ensure these modules are accessible in your environment)
from utils import (
    horizontalLine, managerMessageList, get_memory, initialize_global_variables, 
    get_bio, check_exit, show_memory, show_messages
)
from prompts import intro_prompt
from memory.memory import MemoryManager

import warnings
warnings.filterwarnings("ignore")

def main():
    st.title("Sifra AI Assistant")
    
    initialize_global_variables()


    
    st.title("Welcome to SIFRA")
    st.subheader("Super Intelligent and Friendly Responsive Agent 🤖")
    # st.markdown(f"<pre>{figlet_format('S I F R A', font='standard', width=100, justify='center')}</pre>", unsafe_allow_html=True)


    chat_placeholder = st.container()
    prompt_placeholder = st.container()

   

    exit()

    with st.sidebar:
        st.sidebar.title("Select Bio File")

        st.sidebar.markdown("Please upload the file containing the information of the person.")
        uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt"])


    col1, col2 = st.columns([2, 1])

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    with col1:
        st.writ
            




if __name__ == '__main__':
    main()
