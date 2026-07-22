import sys
import os


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


from matcher import SemanticMatcher


def test_semantic_matcher():

    matcher = SemanticMatcher()

    resume_text = """
    Python developer with experience
    in Machine Learning and Data Science.
    """

    job_description = """
    Looking for a Python developer
    with Machine Learning experience.
    """

    score = matcher.calculate_similarity(
        resume_text,
        job_description
    )

    assert isinstance(
        score,
        float
    )

    assert 0 <= score <= 100