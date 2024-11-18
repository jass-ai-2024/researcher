"""
This module provides a class for performing semantic search on arXiv papers using a sentence transformer model.
"""
import xml.etree.ElementTree as et

import requests
from sklearn.metrics.pairwise import cosine_similarity


class ArXivSemanticSearch:
    def __init__(self, embedding_model, max_papers=1000):
        """
        Initialize the ArXiv Semantic Search with a sentence transformer model.
        :param embedding_model: model to use for embeddings
        :param max_papers: Maximum number of papers to retrieve from arXiv
        """
        self.model = embedding_model
        self.max_papers = max_papers

    def search_arxiv(self, query) -> list:
        """
        Search arXiv.org for papers and retrieve metadata
        :param query: Search query string
        :return: List of paper dictionaries
        """
        base_url = 'http://export.arxiv.org/api/query?'
        search_query = f'search_query=all:{query}&start=0&max_results={self.max_papers}'

        response = requests.get(base_url + search_query)
        root = et.fromstring(response.content)

        papers = []
        namespace = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

        for entry in root.findall('atom:entry', namespace):
            paper = {
                'title': entry.find('atom:title', namespace).text.strip(),
                'summary': entry.find('atom:summary', namespace).text.strip(),
                'link': entry.find('atom:link[@title="pdf"]', namespace).get('href'),
                'authors': [author.find('atom:name', namespace).text
                            for author in entry.findall('atom:author', namespace)]
            }
            papers.append(paper)

        return papers

    def generate_embeddings(self, papers) -> list:
        """
        Generate embeddings for paper titles and summaries
        :param papers: List of paper dictionaries
        :return: List of embeddings
        """
        texts = [f"{paper['title']} {paper['summary']}" for paper in papers]
        return self.model.encode(texts)

    def semantic_search(self, query: str, max_results: int = 5, similarity_threshold: float = 0.5) -> list:
        """
        Perform semantic search on arXiv papers

        :param query: Search query string
        :param max_results: Maximum number of results to retrieve
        :param similarity_threshold: Minimum cosine similarity to return results
        :return: List of relevant papers sorted by semantic similarity
        """
        # Search arXiv for papers
        papers = self.search_arxiv(query)

        # Generate embeddings
        paper_embeddings = self.generate_embeddings(papers)
        query_embedding = self.model.encode([query])[0]

        # Calculate cosine similarities
        similarities = cosine_similarity([query_embedding], paper_embeddings)[0]

        # Filter and sort results
        relevant_papers = []
        for i, similarity in enumerate(similarities):
            if similarity >= similarity_threshold:
                papers[i]['semantic_score'] = similarity
                relevant_papers.append(papers[i])

        # Sort by semantic similarity in descending order
        return sorted(relevant_papers, key=lambda x: x['semantic_score'], reverse=True)[:max_results]
