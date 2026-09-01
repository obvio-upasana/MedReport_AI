from langchain_core.tools import tool

from rag import search_report


@tool
def search_uploaded_report(question: str) -> str:
    """
    Search the currently uploaded medical report for information
    relevant to the user's question.

    Use this tool whenever the user asks about something that may
    be contained in their uploaded report.
    """

    return search_report(
        question=question,
        k=4
    )


@tool
def medical_term_explainer(term: str) -> str:
    """
    Explain common medical laboratory terms in simple educational language.
    """

    glossary = {

        "hemoglobin":
            "Hemoglobin is a protein in red blood cells that carries oxygen.",

        "platelets":
            "Platelets are blood components that help the body form blood clots.",

        "white blood cells":
            "White blood cells are cells involved in the body's immune response.",

        "wbc":
            "WBC means white blood cell count.",

        "rbc":
            "RBC means red blood cell count.",

        "hematocrit":
            "Hematocrit describes the proportion of blood made up of red blood cells.",

        "glucose":
            "Glucose is a type of sugar used by the body as an important source of energy.",

        "cholesterol":
            "Cholesterol is a waxy substance involved in several normal body functions.",

        "creatinine":
            "Creatinine is a waste product commonly measured when evaluating kidney function."
    }

    cleaned_term = term.lower().strip()

    return glossary.get(
        cleaned_term,
        "I do not have a specific explanation for that term in my basic glossary."
    )