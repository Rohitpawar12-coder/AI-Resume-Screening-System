import PyPDF2


def extract_text(pdf_file):
    """
    Extract text from a PDF resume.

    Parameters:
        pdf_file (str): Path to the PDF file.

    Returns:
        str: Extracted resume text.
    """

    text = []

    try:
        with open(pdf_file, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            if len(reader.pages) == 0:
                raise ValueError("The PDF contains no pages.")

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text.append(page_text)

        extracted_text = "\n".join(text).strip()

        if not extracted_text:
            raise ValueError(
                "Could not extract text from the PDF. "
                "The resume may be scanned or image-based."
            )

        return extracted_text

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Resume file not found: {pdf_file}"
        )

    except Exception as e:
        raise RuntimeError(
            f"Error while extracting resume text: {str(e)}"
        )