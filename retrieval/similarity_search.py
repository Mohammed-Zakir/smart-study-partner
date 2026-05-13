import numpy as np
from models.model_loader import model_loader


class SimilaritySearch:
    """
    Perform semantic similarity search
    between query and document embeddings.
    """

    def __init__(self):

        self.embedding_model = (
            model_loader.get_embedding_model()
        )

    # =========================
    # COSINE SIMILARITY
    # =========================
    def cosine_similarity(
        self,
        query_embedding,
        document_embeddings
    ):

        similarities = []

        for doc_embedding in document_embeddings:

            norm = (
                np.linalg.norm(query_embedding)
                *
                np.linalg.norm(doc_embedding)
            )

            if norm > 0:

                sim = float(

                    np.dot(
                        query_embedding,
                        doc_embedding
                    ) / norm
                )

            else:

                sim = 0.0

            similarities.append(sim)

        return similarities

    # =========================
    # GET TOP K CHUNKS
    # =========================
    def get_top_k_chunks(
        self,
        query,
        embeddings,
        chunks,
        top_k=5,
        threshold=0.3
    ):
        """
        Return top-k chunks with cosine similarity.
        """

        try:

            # 🔥 Generate query embedding
            query_embedding = (
                self.embedding_model.generate_embedding(
                    query
                )
            )

            # 🔥 Compute similarity
            similarities = self.cosine_similarity(
                query_embedding,
                embeddings
            )

            # 🔥 Rank best chunks
            ranked_indices = (
                np.argsort(similarities)[::-1]
            )

            top_chunks = []

            for idx in ranked_indices[:top_k]:

                score = similarities[idx]

                if score >= threshold:

                    top_chunks.append({

                        "chunk": chunks[idx],

                        "score": score
                    })

            # 🔥 fallback best chunk
            if (
                not top_chunks
                and len(ranked_indices) > 0
            ):

                best = ranked_indices[0]

                top_chunks.append({

                    "chunk": chunks[best],

                    "score": similarities[best]
                })

            return top_chunks

        except Exception as e:

            print(
                "Error in similarity search:",
                e
            )

            return []