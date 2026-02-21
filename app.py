from src.parser import parse_pdf
from src.summarizer import summarize_text, summarize_image
from src.vectorstore import add_documents
from src.rag_chain import ask_question


def main():
    texts, images = parse_pdf()

    print("Summarizing texts...")
    text_summaries = [summarize_text(t["text"]) for t in texts]

    print("Summarizing images...")
    image_summaries = [summarize_image(img["image_base64"]) for img in images]

    add_documents(text_summaries, image_summaries, texts, images)

    while True:
        query = input("\nAsk a question (or type 'exit'): ").strip()
        if query.lower() == "exit":
            break

        result = ask_question(query)

        print("\n=== ANSWER ===")
        print(result["answer"])

        print("\n=== TEXT SOURCES ===")
        for i, src in enumerate(result["text_sources"], 1):
            print(f"[{i}] Page {src['page_number']}")
            print(src["text_preview"])
            print("-" * 60)

        print("\n=== IMAGE SOURCES ===")
        if not result["image_sources"]:
            print("No image sources retrieved.")
        else:
            for i, src in enumerate(result["image_sources"], 1):
                print(f"[{i}] Page {src['page_number']} (image retrieved)")


if __name__ == "__main__":
    main()