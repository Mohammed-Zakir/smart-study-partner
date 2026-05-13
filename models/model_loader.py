from models.qa_model import QAModel
from models.embedding_model import EmbeddingModel


class ModelLoader:
    """
    Centralized model loader for SmartDocQA
    """

    def __init__(self):
        self.qa_model = None
        self.embedding_model = None

    def load_models(self):
        """
        Load all required models
        """
        try:
            print("Loading QA Model...")
            self.qa_model = QAModel()

            print("Loading Embedding Model...")
            self.embedding_model = EmbeddingModel()

            print("All models loaded successfully.")

        except Exception as e:
            print("Error loading models:", e)

    def get_qa_model(self):
        """
        Return QA model
        """
        if self.qa_model is None:
            self.qa_model = QAModel()

        return self.qa_model

    def get_embedding_model(self):
        """
        Return Embedding model
        """
        if self.embedding_model is None:
            self.embedding_model = EmbeddingModel()

        return self.embedding_model


# Global model loader instance
model_loader = ModelLoader()

# Load models when file is imported
model_loader.load_models()