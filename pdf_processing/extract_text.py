import pdfplumber
import os


class PDFTextExtractor:
    """
    Extract text from PDF files
    """

    def __init__(self):
        pass

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from a single PDF
        """
        extracted_text = ""

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"

        except Exception as e:
            print("Error extracting PDF text:", e)

        return extracted_text


    def extract_text_and_save(self, pdf_path, output_folder):
        """
        Extract text and save to file
        """
        try:
            text = self.extract_text_from_pdf(pdf_path)

            if not text:
                print("No text extracted from PDF.")
                return None

            # Create output folder if not exists
            os.makedirs(output_folder, exist_ok=True)

            filename = os.path.basename(pdf_path).replace(".pdf", ".txt")
            output_path = os.path.join(output_folder, filename)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

            print("Text saved to:", output_path)

            return output_path

        except Exception as e:
            print("Error saving extracted text:", e)
            return None