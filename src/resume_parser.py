# src/resume_parser.py

import re
from pathlib import Path
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path):
    """
    Extract complete text from a PDF resume.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(
            "Only PDF files are supported."
        )

    reader = PdfReader(
        str(pdf_path)
    )

    pages = []

    for page in reader.pages:

        try:

            text = page.extract_text()

            if text:
                pages.append(text)

        except Exception:
            continue

    final_text = "\n".join(pages)

    return final_text.strip()


def clean_text(text):
    """
    Clean extracted resume text.
    """

    if not text:
        return ""

    text = text.replace(
        "\x00",
        " "
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def extract_resume_sections(text):
    """
    Detect common resume sections.

    Returns:
        Dictionary containing sections.
    """

    text = clean_text(text)

    sections = {
        "summary": "",
        "skills": "",
        "experience": "",
        "projects": "",
        "education": "",
        "certifications": "",
        "internships": ""
    }

    if not text:
        return sections

    lines = text.splitlines()

    section_aliases = {

        "summary": [
            "summary",
            "professional summary",
            "profile",
            "objective",
            "career objective"
        ],

        "skills": [
            "skills",
            "technical skills",
            "skills & technologies",
            "technical skills and tools"
        ],

        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment history"
        ],

        "projects": [
            "projects",
            "academic projects",
            "personal projects",
            "key projects"
        ],

        "education": [
            "education",
            "academic background",
            "educational qualification"
        ],

        "certifications": [
            "certifications",
            "certificates",
            "licenses"
        ],

        "internships": [
            "internship",
            "internships",
            "training"
        ]
    }

    current_section = None

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        normalized_line = re.sub(
            r"[^a-zA-Z &]",
            "",
            clean_line.lower()
        ).strip()

        detected_section = None

        for section_name, aliases in section_aliases.items():

            if normalized_line in aliases:

                detected_section = section_name

                break

        if detected_section:

            current_section = detected_section

            continue

        if current_section:

            sections[current_section] += (
                clean_line + "\n"
            )

    return {
        key: value.strip()
        for key, value in sections.items()
    }