"""
This module provides a class for performing semantic search on arXiv papers using a sentence transformer model.
"""
import xml.etree.ElementTree as et

import requests
from sklearn.metrics.pairwise import cosine_similarity

from arxiv_query_data_model import ArxivQuery, Paper


class ArXivSemanticSearch:
    """
    Class for performing semantic search on arXiv papers using a sentence transformer model.
    """
    def __init__(self, embedding_model, max_papers=1000):
        """
        Initialize the ArXiv Semantic Search with a sentence transformer model.
        :param embedding_model: model to use for embeddings
        :param max_papers: Maximum number of papers to retrieve from arXiv
        """
        self.model = embedding_model
        self.max_papers = max_papers

    def search_arxiv(self, query: ArxivQuery) -> tuple[list[Paper], str]:
        """
        Search arXiv.org for papers and retrieve metadata
        :param query: Search query string
        :return: List of paper dictionaries
        """
        base_url = 'http://export.arxiv.org/api/query?'

        # Build query string from ArxivQuery object
        query_parts = []
        if query.title:
            query_parts.append(f'ti:"{query.title}"')
        if query.abstract:
            query_parts.append(f'abs:"{query.abstract}"')
        if query.author:
            query_parts.append(f'au:"{query.author}"')
        if query.category:
            query_parts.append(f'cat:{query.category}')
        if query.date_range:
            query_parts.append(f'submittedDate:{query.date_range}')

        # Join query parts with AND
        search_query = ' AND '.join(query_parts) if query_parts else 'all:*'
        url = f"{base_url}search_query={search_query}&start=0&max_results={self.max_papers}"

        response = requests.get(url)
        root = et.fromstring(response.content)

        papers = []
        namespace = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

        for entry in root.findall('atom:entry', namespace):
            paper = Paper(
                title=entry.find('atom:title', namespace).text.strip(),
                summary=entry.find('atom:summary', namespace).text.strip(),
                semantic_score=0,
                link=entry.find('atom:link[@title="pdf"]', namespace).get('href'),
                authors=[
                    author.find('atom:name', namespace).text
                    for author in entry.findall('atom:author', namespace)
                ]
            )
            papers.append(paper)

        return papers, search_query

    def generate_embeddings(self, papers) -> list:
        """
        Generate embeddings for paper titles and summaries
        :param papers: List of paper dictionaries
        :return: List of embeddings
        """
        texts = [f"{paper.title} {paper.summary}" for paper in papers]
        return self.model.embed_documents(texts)

    def semantic_search(self, query: ArxivQuery, max_results: int = 5, similarity_threshold: float = 0.5) -> list:
        """
        Perform semantic search on arXiv papers

        :param query: Search query string
        :param max_results: Maximum number of results to retrieve
        :param similarity_threshold: Minimum cosine similarity to return results
        :return: List of relevant papers sorted by semantic similarity
        """
        # Search arXiv for papers
        papers, query_string = self.search_arxiv(query)[0], self.search_arxiv(query)[1]

        # Generate embeddings
        paper_embeddings = self.generate_embeddings(papers)
        query_embedding = self.model.embed_documents([query_string])[0]

        # Calculate cosine similarities
        similarities = cosine_similarity([query_embedding], paper_embeddings)[0]

        # Filter and sort results
        relevant_papers = []
        for i, similarity in enumerate(similarities):
            if similarity >= similarity_threshold:
                papers[i].semantic_score = similarity
                relevant_papers.append(papers[i])

        # Sort by semantic similarity in descending order
        return sorted(relevant_papers, key=lambda x: x.semantic_score, reverse=True)[:max_results]
