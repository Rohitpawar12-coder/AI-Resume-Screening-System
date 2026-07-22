import sys
import os

import pytest


# Add src directory to Python path
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SRC_DIR = os.path.join(
    BASE_DIR,
    "src"
)

sys.path.insert(
    0,
    SRC_DIR
)


from resume_parser import extract_text


def test_extract_text_file_not_found():

    with pytest.raises(FileNotFoundError):

        extract_text(
            "non_existing_resume.pdf"
        )


def test_extract_text_returns_string(
    tmp_path
):

    # Create a fake PDF file path
    pdf_file = tmp_path / "test.pdf"

    pdf_file.write_bytes(
        b"%PDF-1.4"
    )

    # This should raise an error because
    # this is not a valid PDF.
    with pytest.raises(RuntimeError):

        extract_text(
            str(pdf_file)
        )