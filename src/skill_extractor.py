# src/skill_extractor.py

import json
import re
from pathlib import Path


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(text):

    if not text:
        return ""

    text = str(
        text
    ).lower()

    text = text.replace(
        "&",
        " and "
    )

    text = text.replace(
        "-",
        " "
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# LOAD SKILLS
# ============================================================

def load_skills(skills_path):

    skills_path = Path(
        skills_path
    )

    if not skills_path.exists():

        raise FileNotFoundError(
            f"Skills file not found: {skills_path}"
        )

    with open(
        skills_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# CREATE SEARCH PATTERN
# ============================================================

def create_pattern(skill):

    skill = normalize_text(
        skill
    )

    escaped = re.escape(
        skill
    )

    escaped = escaped.replace(
        r"\ ",
        r"\s+"
    )

    return (
        r"(?<![a-zA-Z0-9])"
        + escaped
        + r"(?![a-zA-Z0-9])"
    )


# ============================================================
# CHECK SKILL
# ============================================================

def skill_exists(
    text,
    skill
):

    if not text or not skill:
        return False

    normalized_text = normalize_text(
        text
    )

    pattern = create_pattern(
        skill
    )

    return bool(
        re.search(
            pattern,
            normalized_text,
            re.IGNORECASE
        )
    )


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(
    resume_text,
    skills_database,
    sections=None
):

    detected_skills = {}

    if not resume_text:
        return detected_skills

    # Use full resume if sections are unavailable
    if sections is None:

        sections = {
            "full_resume": resume_text
        }

    # --------------------------------------------------------
    # Combine text with section priority
    # --------------------------------------------------------

    section_text = " ".join(
        sections.values()
    )

    for category, skills in skills_database.items():

        category_matches = []

        # ====================================================
        # LIST FORMAT
        # ====================================================

        if isinstance(
            skills,
            list
        ):

            for skill in skills:

                if not isinstance(
                    skill,
                    str
                ):
                    continue

                if skill_exists(
                    section_text,
                    skill
                ):

                    category_matches.append(
                        skill
                    )

        # ====================================================
        # DICTIONARY FORMAT
        # ====================================================

        elif isinstance(
            skills,
            dict
        ):

            for main_skill, aliases in skills.items():

                found = False

                # Check main skill
                if skill_exists(
                    section_text,
                    main_skill
                ):

                    found = True

                # Check aliases
                if isinstance(
                    aliases,
                    list
                ):

                    for alias in aliases:

                        if skill_exists(
                            section_text,
                            alias
                        ):

                            found = True

                            break

                if found:

                    category_matches.append(
                        main_skill
                    )

        if category_matches:

            detected_skills[
                category
            ] = sorted(
                set(
                    category_matches
                )
            )

    return detected_skills


# ============================================================
# FLATTEN SKILLS
# ============================================================

def flatten_skills(
    detected_skills
):

    skills = []

    for category_skills in detected_skills.values():

        for skill in category_skills:

            if skill not in skills:

                skills.append(
                    skill
                )

    return skills


# ============================================================
# NORMALIZED SKILL MATCH
# ============================================================

def match_skills(
    resume_skills,
    required_skills
):

    resume_normalized = {

        normalize_text(
            skill
        )

        for skill in resume_skills

    }

    matched = []

    missing = []

    for required in required_skills:

        normalized_required = normalize_text(
            required
        )

        if normalized_required in resume_normalized:

            matched.append(
                required
            )

        else:

            missing.append(
                required
            )

    return (
        matched,
        missing
    )