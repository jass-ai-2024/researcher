import requests
from typing import List, Dict, Any

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

def search_github_repos(key_words: List[str], paper_name: str, top_k: int = 5, min_stars: int = 10) -> List[Dict[str, Any]]:
    """
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
    # Form the search query
    query = '+'.join(key_words) + '+' + paper_name
    url = f'https://api.github.com/search/repositories?q={query}'

    # Perform the request to GitHub API
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Process the response
    data = response.json()
    repos = data['items']

    # Filter and sort repositories by stars
    filtered_repos = [repo for repo in repos if repo['stargazers_count'] >= min_stars]
    sorted_repos = sorted(filtered_repos, key=lambda x: x['stargazers_count'], reverse=True)

    # Select top_k repositories
    top_repos = sorted_repos[:top_k]

    # Extract relevant information and README content
    repo_info = []
    for repo in top_repos:
        owner = repo['owner']['login']
        repo_name = repo['name']
        readme = get_repo_readme(owner, repo_name)
        repo_info.append({
            'name': repo_name,
            'url': repo['html_url'],
            'stars': repo['stargazers_count'],
            'size': repo['size'],
            'language': repo['language'],
            'readme': readme
        })

    return repo_info


# Example usage
if __name__ == "__main__":
    key_words = ["transformer", "attention"]
    paper_name = "Attention is All You Need"
    repos = search_github_repos(key_words, paper_name)
    for repo in repos:
        print(repo)