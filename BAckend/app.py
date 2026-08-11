import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()

def initialize_medical_bot():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing. Check your .env file.")

    # Initialize the Groq Chat model via LangChain
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.2,  # Low temperature for deterministic, reliable output
        groq_api_key=api_key
    )

    # System prompt to set safe guardrails for a medical assistant
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are an AI Medical Assistant helper. Provide general medical information, "
         "explain health concepts, and outline potential steps clearly. "
         "Always include a disclaimer that you are an AI and not a licensed medical professional."),
        ("human", "{user_query}")
    ])

    # Combine into a LangChain Expression Language (LCEL) chain
    chain = prompt | llm | StrOutputParser()
    return chain

if __name__ == "__main__":
    bot_chain = initialize_medical_bot()
    
    # Test question
    sample_query = "What are the common symptoms of mild hypertension?"
    print(f"User Question: {sample_query}\n" + "-"*50)
    
    response = bot_chain.invoke({"user_query": sample_query})
    print(response)