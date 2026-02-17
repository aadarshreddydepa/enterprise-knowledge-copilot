from app.core.embedding import embed_text
from app.core.vector import vector_client

def run_test():
    print("Generating embedding...")
    vec = embed_text("Hello Enterprise Copilot")

    print("Vector length:", len(vec))
    assert isinstance(vec, list)
    assert len(vec) > 0

    print("Storing vector...")
    vector_client.upsert([
        {
            "id": "doc-1",
            "values": vec,
            "metadata": {
                "roles": ["admin"],
                "text": "Hello Enterprise Copilot",
                "document_id": "doc-1",
                "version": 1,
            },
        }
    ])

    print("Searching vector...")
    results = vector_client.search(
        query_vector=vec,
        allowed_roles=["admin"],
        top_k=1,
    )

    print("Results:", results)
    assert len(results) == 1

    print("✅ SANITY CHECK PASSED")

if __name__ == "__main__":
    run_test()
