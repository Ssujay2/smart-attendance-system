from document_loader import load_documents, search_documents


print("Loading documents...")

documents = load_documents()

print(f"Documents found: {len(documents)}")

for document in documents:
    print(f"- {document['filename']}")


print("\nSearching for: leave policy")

results = search_documents("leave policy")

print(f"Results found: {len(results)}")

for result in results:

    print(
        f"\nFile: {result['filename']}"
    )

    print(
        f"Score: {result['score']}"
    )

    print(
        result["content"]
    )