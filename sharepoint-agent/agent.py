import os

from dotenv import load_dotenv
from google import genai

from document_loader import search_documents


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing from the .env file."
    )

client = genai.Client(
    api_key=GEMINI_API_KEY
)


MODEL_NAME = "gemini-3.6-flash"


def ask_agent(question):

    results = search_documents(question)

    if not results:
        return (
            "I couldn't find relevant information "
            "in the available documents."
        )

    context = "\n\n".join(
        [
            f"Document: {result['filename']}\n"
            f"{result['content']}"
            for result in results[:3]
        ]
    )

    prompt = f"""
You are a SharePoint AI Assistant.

Answer the user's question using ONLY the
information contained in the documents below.

If the answer is not available, say:

"I couldn't find that information in the available documents."

Do not invent information.

DOCUMENTS:

{context}

USER QUESTION:

{question}

Give a clear and concise answer.
"""

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=prompt
    )

    return interaction.output_text