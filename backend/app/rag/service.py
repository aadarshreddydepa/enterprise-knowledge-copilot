from typing import List, Dict

SIMILARITY_THRESHOLD = 0.75
TOP_K = 5


async def retrieve_authorized_chunks(
    *,
    vector_client,
    query_embedding: list[float],
    allowed_roles: list[str],
) -> List[Dict]:
    """
    Retrieve chunks from vector DB and apply RBAC.
    """

    response = vector_client.query(
        vector=query_embedding,
        top_k=TOP_K,
        include_metadata=True,
    )

    authorized = []

    for match in response.get("matches", []):
        metadata = match.get("metadata", {})

        chunk_roles = metadata.get("roles", [])
        if not set(chunk_roles).intersection(set(allowed_roles)):
            continue

        authorized.append({
            "score": match["score"],
            "document_id": metadata["document_id"],
            "document_version": metadata.get("document_version", 1),
            "page": metadata.get("page"),
            "text": metadata["text"],
        })

    authorized.sort(key=lambda x: x["score"], reverse=True)
    return authorized


def similarity_gate(chunks: List[Dict]) -> None:
    """
    Hard guardrail against hallucinations.
    """
    if not chunks or chunks[0]["score"] < SIMILARITY_THRESHOLD:
        raise PermissionError("Low similarity – refusing to answer")


def build_context(chunks: List[Dict]) -> str:
    """
    Build safe LLM context.
    """
    return "\n\n".join(chunk["text"] for chunk in chunks)
