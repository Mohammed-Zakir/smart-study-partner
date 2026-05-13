from transformers import pipeline


class QAModel:

    def __init__(self):
        """
        Initialize QA model
        """

        try:

            self.qa_pipeline = pipeline(
                "text2text-generation",
                model="google/flan-t5-base"
            )

            print("QA Model loaded successfully.")

        except Exception as e:

            print("Error loading QA model:", e)

            self.qa_pipeline = None

    # =========================
    # GET ANSWER
    # =========================
    def get_answer(self, question, context):

        if not self.qa_pipeline:

            return {
                "answer": "QA model not loaded.",
                "score": 0
            }

        try:

            prompt = f"""
            Answer the question using the context below.

            Context:
            {context}

            Question:
            {question}

            Give a short and accurate answer.
            """

            result = self.qa_pipeline(
                prompt,
                max_new_tokens=80
            )

            answer = result[0]["generated_text"].strip()

            # fallback
            if not answer:
                answer = "No answer could be generated."

            return {
                "answer": answer,
                "score": 1.0
            }

        except Exception as e:

            print("QA Extraction Error:", e)

            return {
                "answer": "Error extracting answer.",
                "error": str(e),
                "score": 0
            }