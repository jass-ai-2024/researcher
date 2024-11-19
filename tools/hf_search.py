import re

import requests
from bs4 import BeautifulSoup

class HuggingFaceSearch:
    def __init__(self, hf_url = "https://huggingface.co"):
        """
        Initialize HuggingFaceSearch class.
        :param hf_url: HuggingFace URL.
        """
        self.hf_url = hf_url

    def huggingface_info_by_context(self, info_type, query, total_pages=1) -> list:
        """
        Returns results from available models on huggingface.co
        :param info_type: Type of search, possible values - 'model', 'dataset', 'space'
        :param query: The search query that will be used
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

    def get_possible_tasks_for_models(self):
        """
        Returns the list of possible tasks for models available on huggingface.co
        :return: List of tasks
        """
        url = f"{self.hf_url}/models"
        response = requests.get(url)
        soup = BeautifulSoup(response.content.decode('utf8'))

        possible_tasks = []

        for item in soup.find('section').find_all('a', href=True):
            possible_tasks.append(item.attrs['href'].split('=')[1])
        return possible_tasks

    @staticmethod
    def get_possible_sorting_options():
        return ['trending', 'likes', 'downloads', 'created', 'modified']

    def list_models_by_tasks(self, task, sort_by, search=None):
        """Returns first page of results from available models on huggingface.co
        :param task: Filter by possible tasks in machine learning
        :param sort_by: Sorting of the search results, possible values - 'trending', 'likes', 'downloads', 'created', 'modified'
        :param search: Search qwery that will be used, mostly look on model names
        :return: List of information about relevant models
        Example:
        [{'model_name': 'openai/whisper-large-v2',
        'last_updated': '2024-02-29T10:57:50',
        'liked': '1.66k'}
        """
        url = f"{self.hf_url}/models?pipeline_tag={task}&sort={sort_by}"

        if search:
            url += f"&search={search}"

        response = requests.get(url)
        soup = BeautifulSoup(response.content.decode('utf8'))

        for model in soup.find_all('article'):
            liked = model.find_all("svg")[-1].find_next_sibling(string=True).strip()

            model_name = model.find('a').attrs['href'][1:]
            timestamp = model.find('time').attrs['datetime']
            yield {"model_name": model_name, "last_updated": timestamp, "liked": liked}


