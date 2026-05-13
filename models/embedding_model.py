from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingModel:

    def __init__(self):
        """
        Load the sentence transformer model
        """
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("Embedding model loaded successfully.")
        except Exception as e:
            print("Error loading embedding model:", e)
            self.model = None


    def generate_embedding(self, text):
        """
        Generate embedding for a single text
        """
        if not self.model:
            return None

        try:
            embedding = self.model.encode(text)
            return embedding
        except Exception as e:
            print("Error generating embedding:", e)
            return None


    def generate_embeddings(self, texts):
        """
        Generate embeddings for multiple text chunks
        """
        if not self.model:
            return None

        try:
            embeddings = self.model.encode(texts)
            return np.array(embeddings)
        except Exception as e:
            print("Error generating embeddings:", e)
            return None


    def compute_similarity(self, query_embedding, document_embeddings):
        """
        Compute cosine similarity between query and document embeddings
        """
        if query_embedding is None or document_embeddings is None:
            return None

        similarities = []

        for doc_embedding in document_embeddings:
            sim = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            similarities.append(sim)

        return similarities