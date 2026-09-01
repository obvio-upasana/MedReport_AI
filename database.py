"""
MedReport AI does not use a persistent database.

No user reports, conversations, medical information,
or personal data are stored for later use.

ChromaDB is also configured as an in-memory vector store
in rag.py.

Restarting the backend clears the data.
Uploading a new report replaces the previous report.

This is a placeholder for further expansion
"""


def database_status():

    return {
        "database": False,
        "persistent_storage": False,
        "message": "MedReport AI uses no persistent database."
    }