from typing import List
import requests
from langchain_core.tools import tool

from tools.gh_search import search_github_repos
from tools.hf_search import HuggingFaceSearch


@tool
def select_ml_service_node(arch: str):
    """
    Useful if you a get a service architecture of project description to extract ML service information
    """
    return (f"Extract only ML service and information about models and requirements"
            f" for them from provided service arch. Don't miss details: {arch}. ML_Service:")


@tool
def generate_tasks_node(ml_service_information: str):
    """Useful to convert ML_service to a list of tasks for comprehensive up-to date ML research"""
    return (f"Write a detailed and focused list of research tasks for implementing machine learning service."
            f" The tasks should be tailored to the described domain,"
            f" and aim to find the most up-to-date and effective solutions."
            f"Ml Service description: {ml_service_information}. Tasks:")

@tool
def hf_fetch_tool(info_type: str, query: str):
    """
    Useful to retrieve information about a specific model or dataset from huggingface
    Use only for tasks that require datasets or models!
        Returns results from available models on huggingface.co
        :param info_type: Type of search, possible values - 'model', 'dataset', 'space'
        :param query: The search query or keywords that will be used. Must be related to a research task
        :return: List of dictionaries for models and datasets
    """
    hf = HuggingFaceSearch()
    result = [r for r in hf.huggingface_info_by_context(info_type, query, total_pages=1)]
    return "Result of HF research: {}".format(result)

@tool
def github_fetch_tool(key_words: List[str], paper_name: str, top_k: int = 5, min_stars: int = 10):
    """
    Useful to retrieve information about a specific implementation that could help in research.
    Searches for GitHub repositories based on provided keywords and paper name, and returns the top repositories
    filtered by the minimum number of stars.

    Args:
        key_words (List[str]): A list of keywords to include in the search.
        paper_name (str): The name of the paper to include in the search.
        top_k (int): The number of top repositories to return. Default is 5.
        min_stars (int): The minimum number of stars a repository must have to be included. Default is 10.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing information about the top repositories.
    """
    result = search_github_repos(key_words, paper_name, top_k, min_stars)
    return "Github fetching results {}".format(result)


