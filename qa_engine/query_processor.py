from retrieval.retriever import DocumentRetriever
from qa_engine.answer_extractor import AnswerExtractor


class QueryProcessor:
    """
    Process user queries and return answers from documents
    """

    def __init__(self, embedding_file):
        self.retriever = DocumentRetriever(embedding_file)
        self.answer_extractor = AnswerExtractor()

    def process_query(self, query, top_k=3):
        """
        Main function to process a user query
        """
        try:
            # Retrieve relevant chunks
            results = self.retriever.retrieve_relevant_chunks(query, top_k)

            contexts = []
            scores = []

            for r in results:
                contexts.append(r["chunk"])
                scores.append(r["score"])

            # Extract answer from retrieved contexts
            answer = self.answer_extractor.extract_answer(query, contexts)

            return {
                "query": query,
                "answer": answer,
                "contexts": contexts,
                "scores": scores
            }

        except Exception as e:
            print("Error processing query:", e)

            return {
                "query": query,
                "answer": "Error processing query.",
                "contexts": [],
                "scores": []
            }