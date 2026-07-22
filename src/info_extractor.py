import re


def extract_name(text):
    """
    Extract candidate name from resume text.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    ignored_words = {
        "resume",
        "curriculum vitae",
        "cv",
        "profile",
        "contact",
        "about me",
    }

    for line in lines[:10]:

        clean_line = line.lower().strip()

        if clean_line in ignored_words:
            continue

        # Skip lines containing contact information
        if "@" in line:
            continue

        if re.search(r"\d{7,}", line):
            continue

        # Skip URLs
        if "http://" in clean_line or "https://" in clean_line:
            continue

        # Candidate name usually contains 2-4 alphabetic words
        if re.fullmatch(
            r"[A-Za-z]+(?:\s+[A-Za-z]+){1,3}",
            line
        ):
            return line.title()

    return "Not Found"


def extract_email(text):
    """
    Extract email address.
    """

    pattern = (
        r"[a-zA-Z0-9._%+-]+"
        r"@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    )

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return "Not Found"


def extract_phone(text):
    """
    Extract Indian phone number.
    """

    patterns = [
        r"\+91[-\s]?[6-9]\d{9}",
        r"\b[6-9]\d{9}\b",
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return match.group(0)

    return "Not Found"


def extract_linkedin(text):
    """
    Extract LinkedIn profile URL.
    """

    pattern = (
        r"https?://(?:www\.)?"
        r"linkedin\.com/in/[^\s]+"
    )

    match = re.search(pattern, text)

    if match:
        return match.group(0).rstrip(".,)")

    return "Not Found"


def extract_github(text):
    """
    Extract GitHub profile URL.
    """

    pattern = (
        r"https?://(?:www\.)?"
        r"github\.com/[^\s]+"
    )

    match = re.search(pattern, text)

    if match:
        return match.group(0).rstrip(".,)")

    return "Not Found"


def extract_candidate_info(text):
    """
    Extract all important candidate information.
    """

    return {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "LinkedIn": extract_linkedin(text),
        "GitHub": extract_github(text),
    }