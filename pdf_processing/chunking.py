class TextChunker:
    """
    Split text into smaller chunks for embedding and QA processing
    """

    def __init__(self, chunk_size=150, overlap=20):
        """
        chunk_size: number of words per chunk
        overlap: number of words overlapping between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap


    def split_text(self, text):
        """
        Split text into overlapping chunks
        """
        words = text.split()
        chunks = []

        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunk = words[start:end]
            chunks.append(" ".join(chunk))

            start += self.chunk_size - self.overlap

        return chunks


    def split_text_from_file(self, file_path):
        """
        Read text file and split into chunks
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = self.split_text(text)
            return chunks

        except Exception as e:
            print("Error reading file:", e)
            return []