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


