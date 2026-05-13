from models.model_loader import model_loader

# SAFE LIMIT FOR DISTILBERT
MAX_CONTEXT_WORDS = 450


class AnswerExtractor:
    """
    Smart Answer Extractor

    Improvements:
    - Better context handling
    - Better confidence filtering
    - Better research-paper support
    - Cleaner answer extraction
    """

    def __init__(self):

        self.qa_model = model_loader.get_qa_model()

    # =========================
    # TRUNCATE LONG CONTEXT
    # =========================
    def _truncate_context(
        self,
        text,
        max_words=MAX_CONTEXT_WORDS
    ):

        words = text.split()

        return " ".join(words[:max_words])

    # =========================
    # CLEAN ANSWER
    # =========================
    def _clean_answer(self, answer):

        if not answer:
            return None

        answer = answer.strip()

        # remove tiny garbage answers
        if len(answer) < 3:
            return None

        # remove bad tokens
        bad_tokens = [
            "[CLS]",
            "[SEP]",
            "...",
            "..."
        ]

        for token in bad_tokens:

            if token in answer:
                return None

        return answer

    # =========================
    # MAIN ANSWER EXTRACTION
    # =========================
    def extract_answer(
        self,
        question,
        contexts
    ):

        if not contexts:

            return (
                "No relevant information "
                "found in the document."
            )

        best_answer = None

        best_score = 0.0

        # =========================
        # STRATEGY 1
        # COMBINED CONTEXT
        # =========================

        combined = " ".join(contexts)

        combined = self._truncate_context(
            combined
        )

        try:

            result = self.qa_model.get_answer(
                question,
                combined
            )

            if isinstance(result, dict):

                answer = self._clean_answer(
                    result.get("answer")
                )

                score = result.get(
                    "score",
                    0
                )

                if answer and score > best_score:

                    best_answer = answer

                    best_score = score

        except Exception as e:

            print(
                "Combined context error:",
                e
            )

        # =========================
        # STRATEGY 2
        # INDIVIDUAL CHUNKS
        # =========================

        for ctx in contexts:

            ctx = self._truncate_context(
                ctx
            )

            try:

                result = self.qa_model.get_answer(
                    question,
                    ctx
                )

                if isinstance(result, dict):

                    answer = self._clean_answer(
                        result.get("answer")
                    )

                    score = result.get(
                        "score",
                        0
                    )

                    if answer and score > best_score:

                        best_answer = answer

                        best_score = score

            except Exception as e:

                print(
                    "Chunk QA error:",
                    e
                )

                # =========================
        # LOW CONFIDENCE HANDLING
        # =========================

        if not best_answer:

            if contexts and len(contexts) > 0:

                return contexts[0][:500]

            return (
                "No relevant information found "
                "inside the uploaded PDF."
            )

        # =========================
        # FINAL CLEANUP
        # =========================

        best_answer = best_answer.strip()

        return best_answer