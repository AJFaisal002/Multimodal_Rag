from src.vectorstore import vectorstore


def get_retriever(k: int = 4):
    """
    Returns a retriever instance from the vectorstore.
    k = number of documents to retrieve.
    """
    return vectorstore.as_retriever(search_kwargs={"k": k})