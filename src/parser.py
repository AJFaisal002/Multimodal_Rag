import fitz  # PyMuPDF
import base64


def parse_pdf(pdf_path: str):
    """
    Parse a PDF file and extract:
    - Text chunks (with page numbers)
    - Images (base64 encoded, with page numbers)
    """

    texts = []
    images = []

    doc = fitz.open(pdf_path)

    try:
        for page_index in range(len(doc)):
            page = doc[page_index]
            page_number = page_index + 1

            # -------------------------
            # Extract Text
            # -------------------------
            raw_text = page.get_text("text")

            if raw_text:
                text = raw_text.strip()

                if text:
                    chunk_size = 2000
                    for i in range(0, len(text), chunk_size):
                        chunk_text = text[i:i + chunk_size]

                        texts.append({
                            "text": chunk_text,
                            "page_number": page_number
                        })

            # -------------------------
            # Extract Images
            # -------------------------
            image_list = page.get_images(full=True)

            for img in image_list:
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]

                    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

                    images.append({
                        "image_base64": image_b64,
                        "page_number": page_number
                    })

                except Exception:
                    # Skip corrupted or unsupported images
                    continue

    finally:
        doc.close()

    print(f"Text chunks: {len(texts)}")
    print(f"Images found: {len(images)}")

    return texts, images