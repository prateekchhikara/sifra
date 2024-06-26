from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate
    )

from prompts import initialize_memory_prompt, memory_update_prompt
from logger import logger


import json
import logging
from typing import Any, Dict
from memory.memory_structure import Personality, PersonalityUpdate, Action

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, llm: Any):
        """
        Initializes the MemoryManager with a language model (llm).

        Args:
            llm (Any): The language model to be used for generating and modifying memory.
        """
        self.llm = llm

    def generate_initial_memory(self, data: str) -> None:
        """
        Generates the initial memory based on provided data.

        Args:
            data (str): Information to be used for generating initial memory.

        Returns:
            None
        """
        parser = PydanticOutputParser(pydantic_object=Personality)
        prompt = self._prepare_initial_memory_prompt(data)
        request = self._format_request(prompt, parser)

        logger.info("Generating Initial Memory")
        logger.info(f"Request: {request[0].content}")

        results = self.llm(request, temperature=0)
        results_values = parser.parse(results.content)

        logger.info(f"Results: {str(results_values)}")

        memory_dict = self._extract_memory_dict(results_values)
        self._save_memory(memory_dict)

    def modify_memory(self, user_response: str) -> Dict[str, Any]:
        """
        Modifies the memory based on the user response.

        Args:
            user_response (str): The response provided by the user for modifying memory.

        Returns:
            dict: Updated memory dictionary.
        """
        memory = self._load_memory()

        logger.info("Updating Memory")
        parser = PydanticOutputParser(pydantic_object=PersonalityUpdate)
        prompt = self._prepare_memory_update_prompt(user_response, memory)
        request = self._format_request(prompt, parser)

        logger.info(f"Request: {request[0].content}")

        results = self.llm(request, temperature=0)
        results_values = parser.parse(results.content)

        logger.info(f"Results: {str(results_values)}")

        memory_dict = self._extract_memory_dict(results_values)
        self._save_memory(memory_dict)

        self._log_action(results_values.action)
        return memory_dict

    def _prepare_initial_memory_prompt(self, data: str) -> str:
        """
        Prepares the initial memory prompt.

        Args:
            data (str): Information to be used for generating initial memory.

        Returns:
            str: The prepared prompt.
        """

        return initialize_memory_prompt.replace("{person_information}", data)

    def _prepare_memory_update_prompt(self, user_response: str, memory: dict) -> str:
        """
        Prepares the memory update prompt.

        Args:
            user_response (str): The response provided by the user for modifying memory.
            memory (dict): The current memory.

        Returns:
            str: The prepared prompt.
        """
        prompt = memory_update_prompt.replace("{input_prompt}", user_response)
        return prompt.replace("{memories}", json.dumps(memory, indent=4))

    def _format_request(self, prompt: str, parser: Any) -> Any:
        """
        Formats the request using the given prompt and parser.

        Args:
            prompt (str): The prompt to be formatted.
            parser (Any): The parser to format the request.

        Returns:
            Any: The formatted request.
        """
        human_prompt = HumanMessagePromptTemplate.from_template("{request}\n{format_instructions}")
        chat_prompt = ChatPromptTemplate.from_messages([human_prompt])

        return chat_prompt.format_prompt(
            request=prompt,
            format_instructions=parser.get_format_instructions()
        ).to_messages()

    def _extract_memory_dict(self, results_values: Any) -> Dict[str, Any]:
        """
        Extracts the memory dictionary from the parsed results.

        Args:
            results_values (Any): The parsed results containing memory values.

        Returns:
            dict: The extracted memory dictionary.
        """
        personality_traits = Personality.schema()['properties'].keys()
        return {key: results_values.dict()[key] for key in personality_traits}

    def _save_memory(self, memory_dict: Dict[str, Any]) -> None:
        """
        Saves the memory dictionary to a file.

        Args:
            memory_dict (dict): The memory dictionary to be saved.

        Returns:
            None
        """
        with open("memory.json", "w") as file:
            json.dump(memory_dict, file, indent=4)

    def _load_memory(self) -> Dict[str, Any]:
        """
        Loads the memory dictionary from a file.

        Returns:
            dict: The loaded memory dictionary.
        """
        with open("memory.json", "r") as file:
            return json.load(file)

    def _log_action(self, action: Any) -> None:
        """
        Logs the action taken during memory modification.

        Args:
            action (Any): The action taken.

        Returns:
            None
        """
        if action == Action.Nothing:
            logger.info("No action to be performed")
        else:
            logger.info(f"Memory Updated Successfully by action: {action}")
            print("Memory Updated Successfully:", action.value)



