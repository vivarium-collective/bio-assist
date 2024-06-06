from langchain_openai import OpenAIEmbeddings
from langchain_core.documents.base import Document
from langchain_community.vectorstores import Chroma


def retrieve_prediction(document_splits: list, invocation_question: str, k: int = 1, embedding=None) -> list[Document]:
    vectorstore = Chroma.from_documents(documents=document_splits, embedding=embedding or OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever.invoke(invocation_question)
