import warnings
warnings.filterwarnings("ignore")

from dataclasses import dataclass
from typing import Literal
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
import streamlit.components.v1 as components
from dotenv import load_dotenv
load_dotenv()
from memory.memory import MemoryManager
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import json, time
from langchain import PromptTemplate
# Local imports
from utils import (
    managerMessageList, get_memory, get_bio, show_memory
    )
from prompts import intro_prompt
from memory.memory import MemoryManager
from langchain_core.runnables import RunnableSequence
import constants

warnings.filterwarnings("ignore")



st.title("Welcome, I am SIFRA 🤖")
full_form = "Super Intelligent and Friendly Responsive Agent"
colored_full_form = " ".join([f"<span style='color: blue; font-size:20px; font-weight: bold;'> {word[0]}</span>{word[1:]}" for word in full_form.split() if word != "and"])
st.markdown(f"({colored_full_form} )", unsafe_allow_html=True)

# Check if memory exists in session state
if "memory" not in st.session_state:

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("static/ai-avatar.png", width=200)
    with col2:
        # List of 5 elements
        elements = [
            "Advanced Data Handling: Manages diverse unstructured data sources seamlessly.", 
            "Automatic Profiling: Deduces user details and preferences automatically.", 
            "Personalized Interaction: Tailors responses based on contextual user profiles.", 
            "Continuous Adaptation: Learns and adjusts to user preferences over time.", 
        ]
        # Iterate through elements and display them one by one
        for element in elements:
            time.sleep(0.5)
            title, description = element.split(": ", 1)
            st.markdown(f"- <span style='color: red;'><b>{title}:</b></span> {description}", unsafe_allow_html=True)
        
        time.sleep(0.5)
            

        st.markdown("---")  

    


# Initialize the LLM model -------------------------------------------------------
llmMain = ChatOpenAI(
    model = constants.model,
    streaming = True,
    temperature = 0.0,
    max_tokens = constants.max_tokens,
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

def initialize_session_state():
    data = None

    # File uploader in the sidebar
    uploaded_file = st.sidebar.file_uploader("Choose a text file", type="txt")
    if uploaded_file is not None:
        data = uploaded_file.read().decode("utf-8")
        st.sidebar.markdown("**Uploaded Text:**")
        st.sidebar.markdown(data)

    # Wait until file is uploaded and data is populated
    while data is None:
        st.sidebar.write("Please upload a text file.")
        st.stop()

    # data = get_bio("person_info.txt")
    

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


    if "update_type" not in st.session_state:
        st.session_state.update_type = "Nothing"

    if "history" not in st.session_state:
        st.session_state.history = [Message("ai", response)]
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0
    if "conversation" not in st.session_state:
        llm = ChatOpenAI(
            model = constants.model,
            streaming = True,
            temperature = 0.0,
            max_tokens = constants.max_tokens,
        )


    if "memory" not in st.session_state:
        st.session_state.memory = show_memory()

    if "messages" not in st.session_state:
        st.session_state.messages = [
        SystemMessage("You are Sifra, an AI assistant. You are very amiable and helpful. You love assisting people and help them in the conversation. Start with a greeting and then ask the person how they are doing. You can pick one of the points from the information so that it seems like you know the person well."),
        SystemMessage(f"About me: {json.dumps(memory)}"),
        AIMessage(response)
    ]

def on_click_callback():
    with get_openai_callback() as cb:
        human_prompt = st.session_state.human_prompt

        st.session_state.messages.append(HumanMessage(human_prompt))

        llm_response = llmMain(st.session_state.messages).content

        st.session_state.messages.append(AIMessage(llm_response))


        st.session_state.messages = managerMessageList(st.session_state.messages, k = 5)

        # add the messages to the history
        st.session_state.history.append(
            Message("human", human_prompt)
        )
        st.session_state.history.append(
            Message("ai", llm_response)
        )
        # st.session_state.token_count += cb.total_tokens
        st.session_state.memory, update_type = mem.modify_memory(human_prompt)
        st.session_state.messages[1] = SystemMessage(f"About me: {json.dumps(st.session_state.memory)}")

        st.session_state.memory = show_memory()

        st.session_state.update_type = update_type

        st.session_state.human_prompt = ""




chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")

load_css()

if "memory" not in st.session_state:
    initialize_session_state()



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
        value="",
        label_visibility="collapsed",
        key="human_prompt",
    )
    cols[1].form_submit_button(
        "Submit", 
        type="primary", 
        on_click=on_click_callback, 
    )

    st.write(f"Memory Status: {st.session_state.update_type}")




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


