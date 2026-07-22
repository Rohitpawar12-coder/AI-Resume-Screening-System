# src/scoring_engine.py


def calculate_skill_score(
    matched_skills,
    required_skills
):

    if not required_skills:

        return 100.0

    matched = {

        skill.lower().strip()

        for skill in matched_skills

    }

    required = {

        skill.lower().strip()

        for skill in required_skills

    }

    if not required:

        return 100.0

    score = (

        len(
            matched.intersection(
                required
            )
        )

        / len(required)

    ) * 100

    return round(
        score,
        2
    )


def calculate_tool_score(
    matched_tools,
    required_tools
):

    if not required_tools:

        return 100.0

    matched = {

        tool.lower().strip()

        for tool in matched_tools

    }

    required = {

        tool.lower().strip()

        for tool in required_tools

    }

    score = (

        len(
            matched.intersection(
                required
            )
        )

        / len(required)

    ) * 100

    return round(
        score,
        2
    )


def calculate_overall_score(
    semantic_score,
    skill_score,
    tool_score
):

    """
    Improved scoring model.

    Semantic Relevance = 30%
    Required Skills    = 45%
    Tools/Libraries    = 25%
    """

    semantic_score = max(
        0,
        min(
            100,
            semantic_score
        )
    )

    skill_score = max(
        0,
        min(
            100,
            skill_score
        )
    )

    tool_score = max(
        0,
        min(
            100,
            tool_score
        )
    )

    final_score = (

        semantic_score * 0.30

        +

        skill_score * 0.45

        +

        tool_score * 0.25

    )

    return round(
        final_score,
        2
    )


def get_recommendation(
    score
):

    if score >= 85:

        return (
            "Strong Match",
            "Candidate is highly aligned with the selected role."
        )

    elif score >= 70:

        return (
            "Good Match",
            "Candidate has good alignment with the selected role."
        )

    elif score >= 55:

        return (
            "Moderate Match",
            "Candidate has partial alignment. "
            "Some relevant skills or tools are missing."
        )

    else:

        return (
            "Low Match",
            "Candidate currently has limited alignment "
            "with the selected role."
        )