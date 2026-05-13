from retrieval.embedding_generator import EmbeddingGenerator
from retrieval.similarity_search import SimilaritySearch
from models.model_loader import model_loader


class DocumentRetriever:
    """
    Smart semantic document retriever with improved
    context ranking and answer extraction.
    """

    def __init__(self, embedding_file):

        self.embedding_file = embedding_file

        self.embedding_generator = EmbeddingGenerator()

        self.similarity_search = SimilaritySearch()

        self.qa_model = model_loader.get_qa_model()

        self.embeddings, self.chunks = (
            self.embedding_generator.load_embeddings(
                self.embedding_file
            )
        )

    def retrieve_relevant_chunks(self, query, top_k=8):

        """
        Retrieve semantically relevant chunks.
        Lower threshold improves research-paper retrieval.
        """

        results = self.similarity_search.get_top_k_chunks(
    query,
    self.embeddings,
    self.chunks,
    top_k,
    0.15
)

        # SORT AGAIN FOR SAFETY
        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        return results

    def get_answer(self, query, top_k=8):

        """
        Retrieve relevant chunks and extract best answer.
        """

        try:

            results = self.retrieve_relevant_chunks(
                query,
                top_k
            )

            contexts = [
                r["chunk"]
                for r in results
            ]

            scores = [
                round(r["score"], 4)
                for r in results
            ]

            # FALLBACK IF NOTHING FOUND
            if not contexts:

                return {

                    "query": query,

                    "answer":
                    (
                        "No relevant information found "
                        "inside the uploaded PDF."
                    ),

                    "contexts": [],

                    "scores": []
                }

            from qa_engine.answer_extractor import (
                AnswerExtractor
            )

            extractor = AnswerExtractor()

            answer = extractor.extract_answer(
                query,
                contexts
            )

            # EXTRA CLEANUP
            if not answer or len(answer.strip()) < 3:

                answer = (
                    "Relevant context was found, "
                    "but a confident answer "
                    "could not be extracted."
                )

            return {

                "query": query,

                "answer": answer,

                "contexts": contexts,

                "scores": scores
            }

        except Exception as e:

            print("Error retrieving answer:", e)

            return {

                "query": query,

                "answer":
                (
                    "An error occurred while "
                    "retrieving the answer."
                ),

                "contexts": [],

                "scores": []
            }