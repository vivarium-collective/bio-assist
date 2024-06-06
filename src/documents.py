import requests
import tiktoken
from bs4 import BeautifulSoup, SoupStrainer
from langchain_core.documents.base import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


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


def fetch_web_document(url: str) -> Document:
    loader = WebBaseLoader(
        web_paths=(url),
        bs_kwargs=dict(
            parse_only=SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )
    return loader.load()


def split_document(document: Document, chunk_size=300, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap)
    return text_splitter.split_documents([document])


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

