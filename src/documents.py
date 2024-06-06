import requests
from bs4 import BeautifulSoup
from langchain_core.documents.base import Document


def fetch_pubmed_article(pubmed_id: str) -> Document:
    """Function to load PubMed article"""
    url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch the article: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find_all(class_=["abstract", "full-text", "heading-title"])
    article_text = "\n\n".join([c.get_text() for c in content])
    return Document(article_text)
