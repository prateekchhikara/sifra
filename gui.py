from dataclasses import dataclass
from typing import Literal
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from langchain import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory
import streamlit.components.v1 as components
from dotenv import load_dotenv
load_dotenv()
from memory.memory import MemoryManager
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import json
from langchain import PromptTemplate
# Local imports
from utils import (
    horizontalLine, managerMessageList, get_memory, initialize_global_variables, 
    get_bio, check_exit, show_memory, show_messages
    )
from prompts import intro_prompt
from memory.memory import MemoryManager
from langchain_core.runnables import RunnableSequence

# Initialize the LLM model -------------------------------------------------------
llmMain = ChatOpenAI(
    model= "gpt-4", 
    # model = "gpt-3.5-turbo-0125",
    streaming=True,
    temperature=0.0,
    max_tokens=200,
)

mem = MemoryManager(llmMain)

@dataclass
class Message:
    """Class for keeping track of a chat message."""
    origin: Literal["human", "ai"]
    message: str

def load_css():
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

def initialize_session_state(data):

    
    mem.generate_initial_memory(data)

    # Generate the prompt for the AI to introduce itself --------------------------------
    prompt_template = PromptTemplate(
        input_variables=["person_information"],
        template=intro_prompt,
    )
    sequence = RunnableSequence(prompt_template | llmMain)
    response = sequence.invoke({"person_information" : data}).content

    # Collecting all messages -------------------------------------------------------
    memory = get_memory()
    # messages = [
    #     SystemMessage("You are Sifra, an AI assistant. You are very amiable and helpful. You love assisting people and help them in the conversation. Start with a greeting and then ask the person how they are doing. You can pick one of the points from the information so that it seems like you know the person well."),
    #     SystemMessage(f"About me: {json.dumps(memory)}"),
    #     AIMessage(response)
    # ]


    if "history" not in st.session_state:
        st.session_state.history = []
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0
    if "conversation" not in st.session_state:
        llm = ChatOpenAI(
            # model= "gpt-4", 
            model = "gpt-3.5-turbo-0125",
            streaming=True,
            temperature=0.0,
            max_tokens=200,
        )
        st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=ConversationSummaryMemory(llm=llm),
        )

    if "memory" not in st.session_state:
        st.session_state.memory = memory

    if "messages" not in st.session_state:
        st.session_state.messages = [
        SystemMessage("You are Sifra, an AI assistant. You are very amiable and helpful. You love assisting people and help them in the conversation. Start with a greeting and then ask the person how they are doing. You can pick one of the points from the information so that it seems like you know the person well."),
        SystemMessage(f"About me: {json.dumps(memory)}"),
        AIMessage(response)
    ]

def on_click_callback():
    with get_openai_callback() as cb:
        human_prompt = st.session_state.human_prompt
        llm_response = st.session_state.conversation.run(
            human_prompt
        )

        st.session_state.history.append(
            Message("human", human_prompt)
        )
        st.session_state.history.append(
            Message("ai", llm_response)
        )
        st.session_state.token_count += cb.total_tokens

        st.session_state.memory = show_memory()

        st.session_state.messages.append(HumanMessage(human_prompt))
        st.session_state.messages.append(AIMessage(llm_response))

        st.session_state.messages = managerMessageList(st.session_state.messages, k = 5)

        memory = mem.modify_memory(human_prompt)
        st.session_state.messages[1] = SystemMessage(f"About me: {json.dumps(memory)}")



# Create a file uploader in the sidebar
uploaded_file = st.sidebar.file_uploader("Choose a text file", type="txt")

load_css()
initialize_session_state(uploaded_file)

st.title("Welcome, I am SIFRA 🤖")
st.markdown("(Super Intelligent and Friendly Responsive Agent)")

chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")
# display_memory = st.empty()





with chat_placeholder:
    for chat in st.session_state.history:
        div = f"""
<div class="chat-row 
    {'' if chat.origin == 'ai' else 'row-reverse'}">
    <img class="chat-icon" src="app/static/{
        'ai-avatar.png' if chat.origin == 'ai' 
                      else 'human-avatar.png'}"
         width=32 height=32>
    <div class="chat-bubble
    {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
        &#8203;{chat.message}
    </div>
</div>
        """
        st.markdown(div, unsafe_allow_html=True)
    
    for _ in range(3):
        st.markdown("")

with prompt_placeholder:
    st.markdown("**Chat**")
    cols = st.columns((6, 1))
    cols[0].text_input(
        "Chat",
        value="Hello bot",
        label_visibility="collapsed",
        key="human_prompt",
    )
    cols[1].form_submit_button(
        "Submit", 
        type="primary", 
        on_click=on_click_callback, 
    )


st.markdown("---")
st.markdown("Memory 🧠")
st.json(st.session_state.memory)




components.html("""
<script>
const streamlitDoc = window.parent.document;

const buttons = Array.from(
    streamlitDoc.querySelectorAll('.stButton > button')
);
const submitButton = buttons.find(
    el => el.innerText === 'Submit'
);

streamlitDoc.addEventListener('keydown', function(e) {
    switch (e.key) {
        case 'Enter':
            submitButton.click();
            break;
    }
});
</script>
""", 
    height=0,
    width=0,
)





# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the content of the file
    data = uploaded_file.read().decode("utf-8")
    
    # Display the content of the file in the sidebar without horizontal scroll
    st.sidebar.write("File content:")
    st.sidebar.markdown(data)

else:
    st.sidebar.write("Please upload a text file.")