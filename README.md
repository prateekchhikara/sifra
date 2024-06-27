![](images/cover.png)

# 🤖 SIFRA 

SIFRA (Super Intelligent & Friendly Responsive Agent) is a personalized AI agent designed to revolutionize the way users interact with technology. By leveraging generative AI techniques, this AI agent can understand and remember user details and preferences from unstructured data sources, providing a highly tailored and engaging conversational experience. Whether it is remembering your favorite hobbies or deducing preferences from blog posts, Sifra ensures that every interaction feels personal and intuitive.

SIFRA has the following capabilitites:

1. **Unstructured Data Handling:** Seamlessly input various unstructured data sources, such as blog post content, personal bios, and more, into the AI Assistant.
2. **Automatic Profiling:** Automatically deduce relevant user details and preferences from the ingested data. Moreover, it  builds and updates personalized user profiles based on continuous data input.
3. **Personalized Interactions:** Recall and leverage user profile information to provide responses that are contextualized and highly personalized.
4. **Adaptive Learning:** Continuously learn and adapt to user preferences to enhance the conversational experience over time.

## 🔎 Framework Overview

SIFRA's framework is majorly divided into two phases: (1) Initiation Phase and (2) Episode Phase. 

### Phase-1 (Initiation)
![](images/fig1.png)

In the initiation phase, the user uploads an unstructured text, such as a Wikipedia page or a personal bio of a person. After the file is uploaded, Sifra processes the data and then sends it to OpenAI to get the output in a structured format. To ensure the data is systematically organized, the Pydantic library in Python is used. Once the structured information is received from OpenAI, Sifra creates a memory.

Next, a message queue is created with a restricted size (k=6) to ensure Sifra does not remember all historical chats but can deduce information from the memory to answer future messages. The queue consists of three sections:

1. **System Instructions:** This read-only part helps Sifra behave in a certain way and consists of generic prompts defining Sifra's role in the conversation.
2. **Memory:** This read-write part is used by Sifra to answer future queries. Sifra can update this section with new inputs via functions.
3. **FIFO Queue:** This section supports both reading and writing and is managed by a queue manager. The size of this queue is limited to 4, so only the latest 4 messages are stored here.

Using Pydantic, I extracted several key fields from the OpenAI output to comprehensively capture various aspects of a person's profile. These fields include the person's full name, a list of likes and dislikes, hobbies, personality traits, and core values. Additionally, the profile includes a detailed "About Me" narrative, descriptions of relationships, a to-do list, and reminders for important dates or commitments. This structured approach ensures a thorough and organized representation of an individual's attributes and preferences.

### Phase-2 (Episode)
![](images/fig2.png)

Phase 2, also known as the Episode phase, defines an interaction episode between the user and Sifra. Initially, Sifra greets the user based on the received inputs. Then, it appends the new input from the user to the Query Message area of the Message Queue and sends it to OpenAI. OpenAI returns the updated output in a structured key-value format, indicating whether any fields in the memory were updated, deleted, added, or unchanged. Sifra then uses this output to update the message queue. As discussed, during the initiation phase, Sifra creates a memory, and in this phase, it gets updated with the conversation. Finally, Sifra responds to the user.

## 📚 Features


High-Level Features of SIFRA
- Converts unstructured text to structured format using OpenAI and Pydantic.
- Manages memory creation and updates during Initiation Phase.
- Implements a message queue with sections for instructions, memory, and FIFO handling.
- Facilitates interactive user sessions in the Episode Phase.
- Ensures scalability and systematic data organization.

## ⚙️ Dependencies and Installation

Firstly, you need to clone this repository in order to access SIFRA. You can do so py running the following command in your terminal.

```
git clone https://github.com/prateekchhikara/ai-assistant
```

Then

```
cd ai-assistant
```

The required dependencies are present in the file ```requirements.txt```.

Before proceeding, you must need to add some API-keys in a ```.env``` file in the directory of sifra. There are 4 keys which are required to run SIFRA. You can find the example .env file in the directory.

```
LANGCHAIN_API_KEY = ""
OPENAI_API_KEY = ""
OPENAI_BASE_URL = "https://api.openai.com/v1"
```

```LANGCHAIN_API_KEY``` is used to log all queries on LangChain server. If you prefer not to log queries on a separate server, you can omit this step and modify the ```utils.py/initialize_global_variables``` function accordingly. Additionally, the repository includes a custom logging feature: logs will be stored in ```sifra.log``` once your experiments are underway.

You can select the type of OpenAI model and token length from ```constants.py```.

### There are two ways in which SIFRA can be accessed:

### 1. Command Line Interface (CLI) 🖵

A python package is created though which SIFRA-cli can be accessed. The user just needs to install the package using the following command. Running the command will install the required dependencies in your local.

```
pip install --editable .
```

After the installation has been completed. Run ```sifra``` in your terminal.



### 2. Graphic User Interface (GUI) 🖼️

For GUI, Streamlit is used which is a powerful framework for building interactive web applications. 

```
streamlit run gui.py
```

If you would like to run the streamlit using docker then you can build the docker by using the below command.

```
docker compose up --build
```

**Note:** Please make sure that all these commands are run from the ```ai-assistant``` folder.

## 🚀 Quick Demo Examples

The GUI features an interactive chat session with Sifra, allowing users to upload a text file containing unstructured data or a personal bio. Upon file selection, Sifra creates an initial memory, visible at the bottom of the page and printed in the terminal. This memory initially includes details such as likes, dislikes, personal traits, and hobbies of the person.

During the session, if the user mentions a change, such as no longer liking dancing, Sifra updates the memory by removing "dancing" from the hobbies attribute. Subsequently, if the user indicates new preferences, such as liking Ramen and disliking burgers, Sifra adds "Ramen" to the likes attribute and "burgers" to the dislikes attribute.

At one point, the user informs Sifra about upcoming date plans, prompting Sifra to accurately make a note of it. Finally, when the user inquires about their interests, Sifra responds based on the updated memory, despite the buffer queue only retaining the last four messages of the conversation.

This interaction demonstrates Sifra's ability to dynamically update and recall information from its memory based on user input, enhancing the personalized chat experience.

https://github.com/prateekchhikara/ai-assistant/assets/46902268/2bab90ee-f129-43fb-8716-0094d39d5d2d


In the CLI, users can specify the path to a text file containing unstructured text or a personal bio. If no path is mentioned and the user simply hits enter, Sifra defaults to picking information from the ```person_info.txt``` file. Upon hitting enter, Sifra initializes its memory based on this input.

Throughout the interaction, the user is presented with four options after each step: they can exit, view memory, debug (for testing purposes), or check the message buffer. This setup allows for seamless interaction with Sifra via the CLI.

During one session, the user mentions no longer liking swimming, prompting Sifra to remove it from the hobbies list. When the user states a newfound interest in cricket and hockey, Sifra adds these to the hobbies list. The message buffer, visible to the user, retains the last four conversations alongside system instructions and memory details.

Towards the end of the episode, the user asks Sifra about their interests, and Sifra accurately responds based on its updated memory. This demonstration underscores Sifra's ability to dynamically adjust its knowledge and provide relevant responses in a CLI environment.

https://github.com/prateekchhikara/ai-assistant/assets/46902268/898595f4-d5dd-4834-bb0e-90615f9d5a7d



## 🎓 References

```
@article{packer2023memgpt,
  title={Memgpt: Towards llms as operating systems},
  author={Packer, Charles and Fang, Vivian and Patil, Shishir G and Lin, Kevin and Wooders, Sarah and Gonzalez, Joseph E},
  journal={arXiv preprint arXiv:2310.08560},
  year={2023}
}

@article{lin2024swiftsage,
  title={Swiftsage: A generative agent with fast and slow thinking for complex interactive tasks},
  author={Lin, Bill Yuchen and Fu, Yicheng and Yang, Karina and Brahman, Faeze and Huang, Shiyu and Bhagavatula, Chandra and Ammanabrolu, Prithviraj and Choi, Yejin and Ren, Xiang},
  journal={Advances in Neural Information Processing Systems},
  volume={36},
  year={2024}
}

@article{majumder2023clin,
  title={Clin: A continually learning language agent for rapid task adaptation and generalization},
  author={Majumder, Bodhisattwa Prasad and Mishra, Bhavana Dalvi and Jansen, Peter and Tafjord, Oyvind and Tandon, Niket and Zhang, Li and Callison-Burch, Chris and Clark, Peter},
  journal={arXiv preprint arXiv:2310.10134},
  year={2023}
}


```