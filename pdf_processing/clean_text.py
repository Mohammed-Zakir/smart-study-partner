import re


class TextCleaner:
    """
    Clean and preprocess extracted PDF text
    """

    def __init__(self):
        pass

    def remove_extra_spaces(self, text):
        """
        Remove multiple spaces and line breaks
        """
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def remove_special_characters(self, text):
        """
        Remove only truly unwanted characters, keep punctuation and numbers
        """
        # Keep letters, digits, common punctuation, brackets, quotes
        text = re.sub(r'[^\w\s.,!?;:()\[\]\'\"\-/%]', ' ', text)
        return text

    def remove_urls(self, text):
        """
        Remove URLs from text
        """
        text = re.sub(r'http\S+|www\S+', '', text)
        return text

    def remove_emails(self, text):
        """
        Remove email addresses
        """
        text = re.sub(r'\S+@\S+', '', text)
        return text

    def clean_text(self, text):
        """
        Full text cleaning pipeline
        """
        text = self.remove_urls(text)
        text = self.remove_emails(text)
        text = self.remove_special_characters(text)
        text = self.remove_extra_spaces(text)

        return text