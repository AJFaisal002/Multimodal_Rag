from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from src.retriever import get_retriever

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def ask_question(question, k: int = 4):

    retriever = get_retriever(k)
    docs = retriever.invoke(question)

    context_text = ""
    image_payloads = []

    text_sources = []
    image_sources = []

    seen_pages = set()

    for doc in docs:
        dtype = doc.metadata.get("type")
        page_number = doc.metadata.get("page_number")

        if dtype == "text":
            if page_number not in seen_pages:
                seen_pages.add(page_number)
                original_text = doc.metadata.get("original_text", "")
                context_text += original_text + "\n\n"

                text_sources.append({
                    "page_number": page_number,
                    "text_preview": original_text[:500]
                })

        elif dtype == "image":
            img_b64 = doc.metadata.get("original_image")
            if img_b64:
                image_payloads.append(img_b64)
                image_sources.append({
                    "page_number": page_number,
                    "image_base64": img_b64
                })

    prompt_content = [
        {
            "type": "text",
            "text": f"""
Answer the question using only the provided context.

Text Context:
{context_text}

Question: {question}

If the answer is not clearly supported by the context, say so.
"""
        }
    ]

    for img in image_payloads:
        prompt_content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img}"},
            }
        )

    response = llm.invoke([HumanMessage(content=prompt_content)])

    return {
        "answer": response.content,
        "text_sources": text_sources,
        "image_sources": image_sources,
    }