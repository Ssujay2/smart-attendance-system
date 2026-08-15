import os


DOCUMENTS_FOLDER = "documents"


def load_documents():
    """
    Load all text documents from the documents folder.
    """

    documents = []

    if not os.path.exists(DOCUMENTS_FOLDER):
        return documents

    for filename in os.listdir(DOCUMENTS_FOLDER):

        if filename.endswith(".txt"):

            filepath = os.path.join(
                DOCUMENTS_FOLDER,
                filename
            )

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

            documents.append(
                {
                    "filename": filename,
                    "content": content
                }
            )

    return documents


def search_documents(query):
    """
    Simple keyword-based document search.
    """

    documents = load_documents()

    query_words = query.lower().split()

    results = []

    for document in documents:

        content = document["content"].lower()

        score = 0

        for word in query_words:

            if word in content:
                score += 1

        if score > 0:

            results.append(
                {
                    "filename": document["filename"],
                    "content": document["content"],
                    "score": score
                }
            )

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results