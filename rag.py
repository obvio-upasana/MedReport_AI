from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


# --------------------------------------------------
# Embedding model
# Runs locally.
# No embedding API required.
# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# In-memory ChromaDB
# --------------------------------------------------

vectorstore = Chroma(
    collection_name="medical_report",
    embedding_function=embeddings
)


# --------------------------------------------------
# Text splitter
# --------------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)


# --------------------------------------------------
# Add report to ChromaDB
# --------------------------------------------------

def add_report(text: str) -> int:

    chunks = text_splitter.split_text(text)

    if not chunks:
        return 0

    vectorstore.add_texts(
        texts=chunks
    )

    return len(chunks)


# --------------------------------------------------
# Clear current report
# --------------------------------------------------

def clear_report():

    global vectorstore

    try:
        vectorstore.delete_collection()
    except Exception:
        pass

    vectorstore = Chroma(
        collection_name="medical_report",
        embedding_function=embeddings
    )


# --------------------------------------------------
# Search report
# --------------------------------------------------

def search_report(
    question: str,
    k: int = 4
) -> str:

    results = vectorstore.similarity_search(
        question,
        k=k
    )

    if not results:
        return "No relevant information was found in the uploaded report."

    context = []

    for i, document in enumerate(results):

        context.append(
            f"[Report section {i + 1}]\n"
            f"{document.page_content}"
        )

    return "\n\n".join(context)


# --------------------------------------------------
# Check whether report exists
# --------------------------------------------------

def has_report() -> bool:

    try:

        result = vectorstore.get()

        return len(result.get("ids", [])) > 0

    except Exception:

        return False