import openai
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

class Summarizer:
    """
    A class to summarize text using OpenAI API.
    """
    def __init__(self, type_task: str = 'text'):
        """
        Initialize the Summarizer with the type of task.
        :param type_task: text or code
        """
        self.model = "gpt-4o-mini"
        self.temperature = 0.3
        self.n = 1
        self.type_task = type_task
        self.client = ChatOpenAI(model=self.model, temperature=self.temperature, n=self.n)

    def prompt_generation(self) -> str:
        """
        Generate a prompt based on the type of task.
        :return:
        """
        if self.type_task == 'text':
            return "Please provide a concise summary of the following text:"
        elif self.type_task == 'code':
            return "Please provide a step-by-step explanation of what the following code does:"

    def summarize_text(self, text: str) -> str:
        """
        Summarize the given text using OpenAI API.

        Args:
            text (str): The text to be summarized.
        Returns:
            str: The summary of the given text.
        """

        messages = [{"role": "user", "content": self.prompt_generation() + text}]
        response = self.client.invoke(messages)
        return response.content.strip()
