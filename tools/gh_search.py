import requests
import time
from typing import List, Dict, Any
from tools.utils_text_summary_tools import summarize_text, analyze_code
from openai import OpenAI

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

def search_github_repos(key_words: List[str], paper_name: str, top_k: int = 5, min_stars: int = 10, min_paper_repos: int = 3) -> List[Dict[str, Any]]:
    """
    Searches for GitHub repositories based on provided keywords and paper name, and returns the top repositories
    filtered by the minimum number of stars.

    Args:
        key_words (List[str]): A list of keywords to include in the search.
        paper_name (str): The name of the paper to include in the search.
        top_k (int): The number of top repositories to return. Default is 5.
        min_stars (int): The minimum number of stars a repository must have to be included. Default is 10.
        min_paper_repos (int): The minimum number of repositories to return based on the paper name. Default is 3.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing information about the top repositories.
    """
    all_repos = []

    # Perform search for the paper name if it is not None or empty
    paper_repos = []
    if paper_name and paper_name.strip():
        paper_query = f'"{paper_name}"'
        paper_url = f'https://api.github.com/search/repositories?q={paper_query}'
        paper_response = requests.get(paper_url)
        paper_response.raise_for_status()
        paper_data = paper_response.json()
        paper_repos = paper_data['items'][:min_paper_repos]
        # print(f"repos names for papers: {[repo['full_name'] for repo in paper_repos]}")

    # Perform separate searches for each keyword
    keyword_repos = []
    for term in key_words:
        query = f'"{term}"'
        url = f'https://api.github.com/search/repositories?q={query}'
        time.sleep(0.5)  # Rate limiting
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        keyword_repos.extend(data['items'][:1])  # Take at least one repo for each keyword

    # Remove duplicates by repository full name (owner/repo)
    unique_repos = {repo['full_name']: repo for repo in all_repos + keyword_repos}.values()

    # Filter and sort repositories by stars
    filtered_repos = [repo for repo in unique_repos if repo['stargazers_count'] >= min_stars]
    sorted_repos = sorted(filtered_repos, key=lambda x: x['stargazers_count'], reverse=True)

    # Select top_k repositories
    top_repos = sorted_repos[:top_k - len(paper_repos)]
    top_repos.extend(paper_repos)

    # Extract relevant information and README content
    repo_info = []
    for repo in top_repos:
        owner = repo['owner']['login']
        repo_name = repo['name']
        readme = get_repo_readme(owner, repo_name)
        repo_info.append({
            'owner': owner,
            'name': repo_name,
            'url': repo['html_url'],
            'stars': repo['stargazers_count'],
            'size': repo['size'],
            'language': repo['language'],
            'readme': readme
        })

    return repo_info

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
    if readme == "README not available":
        return {'readme_summary': "README not available"}
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


def search_and_summary_gh_repos(key_words: List[str], paper_name: str, top_k: int = 5, min_stars: int = 10, min_paper_repos: int = 3) -> Dict[str, Any]:
    """
    Searches for GitHub repositories based on provided keywords and paper name, and returns summaries of the top repositories.

    Args:
        key_words (List[str]): A list of keywords to include in the search.
        paper_name (str): The name of the paper to include in the search.
        top_k (int): The number of top repositories to return. Default is 5.
        min_stars (int): The minimum number of stars a repository must have to be included. Default is 10.
        min_paper_repos (int): The minimum number of repositories to return based on the paper name. Default is 3.

    Returns:
        Dict[str, Any]: A dictionary containing summaries of the top repositories.
    """
    repos = search_github_repos(key_words, paper_name, top_k, min_stars, min_paper_repos)
    summaries = []
    for repo in repos:
        owner = repo['owner']
        repo_name = repo['name']
        summary = summarize_repository(owner, repo_name, include_files=False)
        summaries.append({
            'repository': repo,
            'summary': summary
        })
    return {'repositories': summaries}


# Example usage
if __name__ == "__main__":
    params = {
        'key_words': ['image classification', 'cats and dogs', 'pre-trained model'], 
        # 'paper_name': 'Image Classification of Cats and Dogs', 
        'paper_name': '', 
        'top_k': 5,
        'min_stars': 10,
        'min_paper_repos': 3
    }
    result = search_and_summary_gh_repos(**params)
    for repo_summary in result['repositories']:
        repo = repo_summary['repository']
        summary = repo_summary['summary']
        print(f"Repository: {repo['name']}, Stars: {repo['stars']}, Size: {repo['size']}, Language: {repo['language']}")
        print("README Summary:", summary['readme_summary'])
        if 'code_summaries' in summary:
            for file_name, code_summary in summary['code_summaries'].items():
                print(f"Code Summary for {file_name}:", code_summary)
        print("\n")

