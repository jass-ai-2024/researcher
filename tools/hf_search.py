import os
import re

import openai
import requests
import tiktoken
from bs4 import BeautifulSoup

class HuggingFaceSearch:
    def __init__(self, hf_url = "https://huggingface.co"):
        """
        Initialize HuggingFaceSearch class.
        :param hf_url: HuggingFace URL.
        """
        self.hf_url = hf_url

    def huggingface_info_by_context(self, info_type: str, query: str, total_pages:int = 1) -> list:
        """
        Returns results from available models on huggingface.co
        :param info_type: Type of search, possible values - 'model', 'dataset', 'space'
        :param query: The search query that will be used, keywords or sentence
        :param total_pages: The total number of pages to return results (20 items per page)
        :return: List of dictionaries for models and datasets
        Example:
        [{'item_name': '/hilmansw/resnet18-catdog-classifier',
        'item_link': 'https://huggingface.co/hilmansw/resnet18-catdog-classifier',
        'item_read_me': 'https://huggingface.co/hilmansw/resnet18-catdog-classifier/blob/main/README.md?code=true',
        'item_matches': '2 matches'}]
        """

        query = re.sub(r'\s+', '+', query)
        page = 0
        base_url = f"{self.hf_url}/search/full-text?q={query}&type={info_type}"

        try:
            while total_pages > 0:
                response = requests.get(base_url + f'&p={page}')
                soup = BeautifulSoup(response.content.decode('utf8'), features="html.parser")
                for item in soup.find_all('div', class_='transform'):
                    item_name = item.find('h4').find_all('a')[1].attrs['href']
                    item_link = f"{self.hf_url}{item_name}"
                    item_read_me = f"{self.hf_url}{item.find_all('h4')[1].find('a').attrs['href']}"
                    item_matches = item.find('header').find_all('div')[-1].text.replace('\n', ' ').replace('\t',
                                                                                                           ' ').strip()

                    yield {"item_name": item_name, "item_link": item_link, "item_read_me": item_read_me,
                           "item_matches": item_matches}
                total_pages -= 1
                page += 1
        except Exception as e:
            print(e)

    def get_possible_tasks_for_models(self) -> list:
        """
        Returns the list of possible tasks for models available on huggingface.co
        :return: List of tasks
        """
        url = f"{self.hf_url}/models"

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content.decode('utf8'))

            possible_tasks = []

            for item in soup.find('section').find_all('a', href=True):
                possible_tasks.append(item.attrs['href'].split('=')[1])
            return possible_tasks
        except Exception as e:
            print(e)

    @staticmethod
    def get_possible_sorting_options() -> list:
        return ['trending', 'likes', 'downloads', 'created', 'modified']

    def list_models_by_tasks(self, task: str, sort_by: str, search: str = None) -> list:
        """Returns first page of results from available models on huggingface.co
        :param task: Filter by possible tasks in machine learning. Can be received from get_possible_tasks_for_models
        :param sort_by: Sorting of the search results, possible values - 'trending', 'likes', 'downloads', 'created', 'modified'
        :param search: Search qwery that will be used, mostly look on model names
        :return: List of information about relevant models
        Example:
        [{'model_name': 'openai/whisper-large-v2',
        'last_updated': '2024-02-29T10:57:50',
        'liked': '1.66k'}]
        """
        url = f"{self.hf_url}/models?pipeline_tag={task}&sort={sort_by}"

        if search:
            url += f"&search={search}"

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content.decode('utf8'))

            for model in soup.find_all('article'):
                liked = model.find_all("svg")[-1].find_next_sibling(string=True).strip()

                model_name = model.find('a').attrs['href'][1:]
                timestamp = model.find('time').attrs['datetime']
                yield {"model_name": model_name, "last_updated": timestamp, "liked": liked}
        except Exception as e:
            print(e)

    @staticmethod
    def summarize_one_chunk(chunk: str) -> str:
        """
        Summarize one portion of text from the long page.
        :param chunk: Text portion that will be summarized
        :return: Summary of the chunk
        """
        try:
            client = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
            messages_for_model = [
                {"role": "system",
                 "content": "You're a researcher who analyse the files and gives a summary with most relevant info"},
                {"role": "user", "content": f"Give short summary the following README content:\n\n{chunk}"}]

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_for_model,
                temperature=0.5,
            )
            return response.choices[0].message.content
        except requests.exceptions.RequestException as e:
            print(f"Error fetching README: {e}")
            return None

    @staticmethod
    def split_text_by_tokens(long_text: str, chunk_size: int = 150000) -> list:
        """
        Splits a long text into portions with a maximum number of tokens.
        :param long_text: Long text to split
        :param chunk_size: Number of tokens in each portion.
        Returns:A list of text portions.
        """

        tokenizer = tiktoken.encoding_for_model("gpt-4o-mini")
        tokens = tokenizer.encode(long_text)

        chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]
        decoded_chunks = [tokenizer.decode(chunk) for chunk in chunks]

        return decoded_chunks

    def summarize_page(self, page_url: str) -> str:
        """
        Summarize a page of text, originally developed for README files on huggingface.co
        :param page_url: Link to the page that needs to be summarized
        :return: Full summary of the page
        """
        try:
            response = requests.get(page_url)
            response.raise_for_status()  # Raise an exception for bad status codes
            soup = BeautifulSoup(response.content.decode('utf8'))
            readme_content = soup.get_text(separator='\n').replace('\n', ' ').replace('\t', ' ').strip()
            readme_content = ' '.join(readme_content.split())

            tokenizer = tiktoken.encoding_for_model("gpt-4o-mini")
            tokens = tokenizer.encode(readme_content)

            if len(tokens) > 128000:
                readme_content = self.split_text_by_tokens(readme_content)
                summaries = [self.summarize_one_chunk(chunk) for chunk in readme_content]
                return ' '.join(summaries)

            return self.summarize_one_chunk(readme_content)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching README: {e}")
            return None
