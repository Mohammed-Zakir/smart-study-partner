import os
import numpy as np
import pickle
from models.model_loader import model_loader


class EmbeddingGenerator:
    """
    Generate and store embeddings for document chunks
    """

    def __init__(self):
        self.embedding_model = model_loader.get_embedding_model()

    def generate_embeddings(self, chunks):
        """
        Generate embeddings for list of text chunks
        """
        try:
            embeddings = self.embedding_model.generate_embeddings(chunks)
            return embeddings
        except Exception as e:
            print("Error generating embeddings:", e)
            return None

    def save_embeddings(self, embeddings, chunks, file_path):
        """
        Save embeddings and corresponding chunks
        """
        try:
            data = {
                "embeddings": embeddings,
                "chunks": chunks
            }

            with open(file_path, "wb") as f:
                pickle.dump(data, f)

            print("Embeddings saved to:", file_path)

        except Exception as e:
            print("Error saving embeddings:", e)

    def load_embeddings(self, file_path):
        """
        Load embeddings from file
        """
        try:
            with open(file_path, "rb") as f:
                data = pickle.load(f)

            return data["embeddings"], data["chunks"]

        except Exception as e:
            print("Error loading embeddings:", e)
            return None, None