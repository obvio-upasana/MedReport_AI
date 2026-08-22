from langchain_community.document_loaders import PyPDFLoader


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF using LangChain's PyPDFLoader.
    """

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    text = "\n".join(document.page_content for document in documents)

    return text