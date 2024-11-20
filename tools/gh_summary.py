import requests
import openai
from openai import OpenAI
from typing import List, Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')

def get_repo_readme(owner: str, repo: str) -> str:
    """
    Fetches the README file content for a given repository.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.

    Returns:
        str: The content of the README file.
    """
    url = f'https://api.github.com/repos/{owner}/{repo}/readme'
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return "README not available"

def get_repo_files(owner: str, repo: str) -> List[Dict[str, Any]]:
    """
    Fetches the list of files in the repository.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing file information.
    """
    url = f'https://api.github.com/repos/{owner}/{repo}/contents'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_file_content(owner: str, repo: str, path: str) -> str:
    """
    Fetches the content of a file in the repository.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        path (str): The path to the file.

    Returns:
        str: The content of the file.
    """
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

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

def summarize_repository(owner: str, repo: str, include_files: bool = True) -> Dict[str, Any]:
    """
    Summarize the given repository, including README and optionally code analysis.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        include_files (bool): Whether to include code analysis. Default is True.

    Returns:
        Dict[str, Any]: A dictionary containing the summaries of the README and optionally code analysis.
    """
    # Get README content
    client = OpenAI()
    readme = get_repo_readme(owner, repo)
    readme_summary = summarize_text(client, readme)

    result = {
        'readme_summary': readme_summary,
    }

    if include_files:
        # Get repository files
        files = get_repo_files(owner, repo)
        code_summaries = {}
        for file in files:
            if file['type'] == 'file' and file['name'].endswith('.py'):  # Assuming Python files for code analysis
                file_content = get_file_content(owner, repo, file['path'])
                code_summary = analyze_code(client, file_content)
                code_summaries[file['name']] = code_summary
        result['code_summaries'] = code_summaries

    return result

# Example usage
if __name__ == "__main__":
    owner = "lsdefine"
    repo = "attention-is-all-you-need-keras"
    summary = summarize_repository(owner, repo, include_files=False)
    print("README Summary:", summary['readme_summary'])
    if 'code_summaries' in summary:
        for file_name, code_summary in summary['code_summaries'].items():
            print(f"Code Summary for {file_name}:", code_summary)