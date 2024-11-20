import os

import openai
import requests
import tiktoken
from bs4 import BeautifulSoup


class GoogleSearch:
    def __init__(self, google_url = "https://www.google.com"):
        """
        Initialize GoogleSearch class.
        :param google_url: Google URL.
        """
        self.google_url = google_url

    def google_search(self, query: str) -> list:
        """
        Allow to search information in Google by qwery.
        :param query: Search qwery, can be any string.
        :return: List of dicts with search results. Dict include title and a link to the page
        Example:
        [{'title': 'База данных: что такое БД, их типы, свойства, структура',
        'link': 'https://practicum.yandex.ru/blog/chto-takoe-bazy-dannyh/'}]
        """
        try:
            url = f'{self.google_url}/search?q={query}'

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            result_links = []

            for g in soup.find_all('div', class_='tF2Cxc'):
                title = g.find('h3').text
                link = g.find('a')['href']
                result_links.append(
                    {
                        "title": title,
                        "link": link
                    }
                )
            return result_links
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
                {"role": "user", "content": f"Give short summary the following content:\n\n{chunk}"}]

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
            print(f"Error fetching page: {e}")
            return None