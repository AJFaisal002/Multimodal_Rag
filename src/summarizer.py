from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)


def summarize_text(text):
    prompt = f"""
Summarize the following content clearly and concisely.

Content:
{text}
"""
    response = llm.invoke(prompt)
    return response.content


def summarize_image(base64_image):
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Describe this image in detail. Include visible text, diagram structure, and key content."},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
            },
        ]
    )
    response = llm.invoke([message])
    return response.content