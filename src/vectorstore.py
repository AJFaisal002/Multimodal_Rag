from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from config import VECTORSTORE_PATH

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = Chroma(
    collection_name="multimodal_rag",
    embedding_function=embeddings,
    persist_directory=VECTORSTORE_PATH,
)


def reset_vectorstore():
    # Optional utility if you want a clean rebuild each run
    # (Chroma may keep old docs otherwise)
    pass


def add_documents(text_summaries, image_summaries, texts, images):
    docs = []

    # Text docs
    for i, summary in enumerate(text_summaries):
        docs.append(
            Document(
                page_content=summary,
                metadata={
                    "type": "text",
                    "original_text": texts[i]["text"],
                    "page_number": texts[i]["page_number"],
                },
            )
        )

    # Image docs
    for i, summary in enumerate(image_summaries):
        docs.append(
            Document(
                page_content=summary,
                metadata={
                    "type": "image",
                    "original_image": images[i]["image_base64"],
                    "page_number": images[i]["page_number"],
                },
            )
        )

    vectorstore.add_documents(docs)
    print(f"Documents added to vectorstore: {len(docs)}")