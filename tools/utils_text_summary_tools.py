import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')

def summarize_text(client: OpenAI, text: str, model: str = "gpt-4o-mini") -> str:
    """
    Summarize the given text using OpenAI API.

    Args:
        client (OpenAI): The OpenAI client.
        text (str): The text to be summarized.
        model (str): The model to use for summarization. Default is "gpt-4o-mini".

    Returns:
        str: The summary of the given text.
    """
    prompt = f"Please provide a concise summary of the following text:\n\n{text}"
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
        n=1,
    )
    return response.choices[0].message.content.strip()

def analyze_code(client: OpenAI, text: str, model: str = "gpt-4o-mini") -> str:
    """
    Analyze the given code and provide a step-by-step explanation using OpenAI API.

    Args:
        text (str): The code to be analyzed.
        model (str): The model to use for analysis. Default is "gpt-4o-mini".
        client (OpenAI): The OpenAI client.

    Returns:
        str: The step-by-step explanation of the code.
    """
    prompt = f"Please provide a step-by-step explanation of what the following code does:\n\n{text}"
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
        n=1,
    )
    return response.choices[0].message.content.strip()