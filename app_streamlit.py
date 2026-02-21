import streamlit as st
import tempfile
import os

from src.parser import parse_pdf
from src.summarizer import summarize_text, summarize_image
from src.vectorstore import add_documents
from src.rag_chain import ask_question


# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(
    page_title="Multimodal RAG",
    layout="wide",
)

st.title("📄 Multimodal RAG — Chat with PDF")


# ----------------------------------
# Session State Initialization
# ----------------------------------

if "indexed" not in st.session_state:
    st.session_state.indexed = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_uploaded_name" not in st.session_state:
    st.session_state.last_uploaded_name = None


# ----------------------------------
# Sidebar Controls
# ----------------------------------

with st.sidebar:
    st.header("Controls")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if st.button("Reset Vectorstore"):
        st.session_state.indexed = False
        st.session_state.chat_history = []
        st.session_state.last_uploaded_name = None

        st.warning(
            "Stop the app and manually delete the 'vectorstore' folder before re-indexing."
        )


# ----------------------------------
# PDF Indexing Logic
# ----------------------------------

if uploaded_file:

    # Detect new file upload
    if st.session_state.last_uploaded_name != uploaded_file.name:
        st.session_state.indexed = False
        st.session_state.chat_history = []
        st.session_state.last_uploaded_name = uploaded_file.name

    if not st.session_state.indexed:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        with st.spinner("Parsing PDF..."):
            texts, images = parse_pdf(temp_path)

        with st.spinner("Summarizing text..."):
            text_summaries = [
                summarize_text(t["text"]) for t in texts
            ]

        with st.spinner("Summarizing images..."):
            image_summaries = [
                summarize_image(img["image_base64"]) for img in images
            ]

        with st.spinner("Indexing into vectorstore..."):
            add_documents(
                text_summaries,
                image_summaries,
                texts,
                images,
            )

        st.session_state.indexed = True
        st.success("PDF Indexed Successfully!")


# ----------------------------------
# Chat Interface
# ----------------------------------

if st.session_state.indexed:

    query = st.chat_input("Ask a question about the document")

    if query:
        result = ask_question(query)

        st.session_state.chat_history.append(
            {
                "question": query,
                "answer": result["answer"],
                "text_sources": result["text_sources"],
                "image_sources": result["image_sources"],
            }
        )

    # Display chat (latest first)
    for chat in reversed(st.session_state.chat_history):

        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):
            st.write(chat["answer"])

            # Text sources
            if chat["text_sources"]:
                with st.expander("Text Sources"):
                    for src in chat["text_sources"]:
                        st.markdown(f"**Page {src['page_number']}**")
                        st.write(src["text_preview"])
                        st.divider()

            # Image sources
            if chat["image_sources"]:
                with st.expander("Image Sources"):
                    for src in chat["image_sources"]:
                        st.markdown(f"**Page {src['page_number']}**")
                        st.image(
                            f"data:image/jpeg;base64,{src['image_base64']}",
                            use_column_width=True,
                        )


# ----------------------------------
# Footer
# ----------------------------------

st.markdown(
    """
    <hr style="margin-top:50px;">
    <div style='text-align: center; font-size: 14px; color: gray;'>
        © 2025 Adnan Faisal & Shiti Chowdhury — Multimodal RAG Project
    </div>
    """,
    unsafe_allow_html=True,
)


