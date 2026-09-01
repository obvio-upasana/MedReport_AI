import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import create_agent

from tools import (
    search_uploaded_report,
    medical_term_explainer
)


# --------------------------------------------------
# Environment variables
# --------------------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)


if not GROQ_API_KEY:

    raise RuntimeError(
        "GROQ_API_KEY is missing. "
        "Add it to your .env file."
    )


# --------------------------------------------------
# Groq LLM
# --------------------------------------------------

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0.1
)


# --------------------------------------------------
# Medical safety instructions
# --------------------------------------------------

SYSTEM_PROMPT = """
You are MedReport AI, an educational medical report assistant.

Your job is to help users understand their uploaded medical reports
in simple, easy-to-understand language.

IMPORTANT SAFETY RULES:

1. You provide EDUCATIONAL information only.
2. Never diagnose a disease or medical condition.
3. Never claim that the user definitely has a condition.
4. Never prescribe medication.
5. Never recommend medication doses.
6. Never tell the user to stop or start medication.
7. Do not replace a qualified healthcare professional.
8. Clearly distinguish information found in the report from
   general medical information.
9. If the report does not contain enough information, say so.
10. Do not invent laboratory values.
11. If a result appears outside its reference range, explain that
    this can have multiple possible explanations and does not by
    itself establish a diagnosis.
12. Encourage the user to discuss concerning or unclear results
    with a qualified healthcare professional.

When appropriate, structure answers as:

- What the result means
- What the report shows
- General possible explanations
- Questions to ask a doctor

Always use cautious language such as:
"can be associated with",
"may have several explanations",
or "your healthcare professional can interpret this in context".

Use the uploaded-report search tool whenever the answer depends
on information contained in the user's report.
"""


# --------------------------------------------------
# Create LangChain Agent
# --------------------------------------------------

agent = create_agent(
    model=llm,
    tools=[
        search_uploaded_report,
        medical_term_explainer
    ],
    system_prompt=SYSTEM_PROMPT
)


# --------------------------------------------------
# Run Agent
# --------------------------------------------------

def ask_agent(question: str) -> str:

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    messages = result.get(
        "messages",
        []
    )

    if not messages:
        return "I could not generate an answer."

    final_message = messages[-1]

    content = final_message.content

    # Most normal LangChain responses are strings.
    if isinstance(content, str):
        return content

    # Handle structured content if returned by the model.
    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                if "text" in item:
                    text_parts.append(
                        item["text"]
                    )

            elif isinstance(item, str):

                text_parts.append(item)

        if text_parts:
            return "\n".join(text_parts)

    return str(content)