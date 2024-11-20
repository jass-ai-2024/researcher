"""
This module contains a class to download
"""
import io
import re
from typing import Dict, List, Union

import PyPDF2
import requests


class PDFParser:
    """
    Class to download and extract text from PDF files.
    """

    def __init__(self, pdf_url: str):
        self.pdf_url = pdf_url

    def download_pdf(self) -> bytes:
        """Download PDF content from URL."""
        response = requests.get(self.pdf_url)
        response.raise_for_status()
        return response.content

    def extract_text_from_pdf(self) -> str:
        """Extract text from PDF content."""
        pdf_file = io.BytesIO(self.download_pdf())
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    @staticmethod
    def extract_git_links(text: str) -> List[str]:
        """Extract GitHub and GitLab links from text."""
        # Pattern for GitHub and GitLab repositories
        git_pattern = r'https?://(?:www\.)?(github\.com|gitlab\.com)/[\w\-\./]+'

        matches = re.finditer(git_pattern, text)
        links = []

        for match in matches:
            # Get the full matched URL
            full_url = match.group(0)

            # Clean up any trailing punctuation or unwanted characters
            full_url = re.sub(r'[.,;\)]$', '', full_url)

            links.append(full_url)

        # Remove duplicates while preserving order
        unique_links = list(dict.fromkeys(links))

        return unique_links

    def process_pdf_url(self) -> Dict[str, Union[str, List[str]]]:
        """Process PDF URL and return text and Git links."""
        try:
            # Extract text
            text = self.extract_text_from_pdf()

            # Extract Git links
            links = self.extract_git_links(text)

            # Create result dictionary
            result = {
                "text": text,
                "links": links
            }

            return result

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error downloading PDF: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
