import os

import requests
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings

from tools.gh_search import summarize_repository
from tools.hf_search import HuggingFaceSearch
from tools.arxiv_search import ArXivSemanticSearch, ArxivQuery
from tools.utils_text_summary_tools import Summarizer


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
    Useful to retrieve information about pretrained models or datasets from huggingface
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
def hf_summary_tool(page_url: str) -> str:
    """
            Summarize a page from HuggingFace by link
            :param page_url: Link to the page that needs to be summarized
            :return: Full summary of the page
    """
    hf = HuggingFaceSearch()
    return f"HF Summary: {hf.summarize_page(page_url)}"


@tool
def github_summary_tool(github_link: str):
    """
               Summarize a page from Github by link
               :param github_link: Link to the page that needs to be summarized
               :return: Full summary of the page
    """
    summary = summarize_repository(*github_link.split("/")[-2:])
    return "Git summary: {}".format(summary)


@tool
def arxiv_summary_tool(arxiv_link: str):
    """
        Summarize a page from arXiv by link
        :param arxiv_link: Link to the page that needs to be summarized
        :return: Full summary of the page
    """
    summer = Summarizer()
    result = summer.summarize_text_pipeline(arxiv_link)
    return "ArXiv Summary: {}".format(result)

@tool
def arxic_fetch_tool(query: ArxivQuery):
    """
    Useful to retrieve information about arxiv papers that could be helpful for research.
    Use it find SOTA implementations and analytical information
    Perform semantic search on arXiv papers
    :param query: Search query string
    :param max_results: Maximum number of results to retrieve
    :param similarity_threshold: Minimum cosine similarity to return results
    :return: List of relevant papers sorted by semantic similarity
    """
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002",  # This is the default and most cost-effective model
        chunk_size=1000  # Number of texts to embed in each batch
    )
    arxic_search = ArXivSemanticSearch(embeddings)
    try:
        result = arxic_search.semantic_search(query, max_results=5,
                                              similarity_threshold=0.3)
    except ValueError as exc:
        print(exc)
        return "None Papers Found"

    return "ArXiv fetching results {}".format(result)


@tool
def google_search_tool(search_query: str):
    """Useful to find information in internet for arXiv papers and Github repos"""
    API_KEY = os.getenv("GOOGLE_API_KEY")
    CX = os.getenv("GOOGLE_CX")

    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": search_query,
    }

    response = requests.get(url, params=params)

    result = []
    if response.status_code == 200:
        data = response.json()
        for item in data.get("items", []):
            result.append({"title": item['title'], "link": item['link']})
        return f"Result from google: {result}"
    else:
        return "Can't find anything"
