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


from scoring_engine import (
    calculate_skill_match,
    calculate_final_score,
    get_recommendation
)


# ============================================================
# Test Skill Matching
# ============================================================

def test_skill_match_all_skills():

    resume_skills = [
        "Python",
        "Machine Learning",
        "TensorFlow"
    ]

    jd_skills = [
        "Python",
        "Machine Learning",
        "TensorFlow"
    ]

    score, matched, missing = (
        calculate_skill_match(
            resume_skills,
            jd_skills
        )
    )

    assert score == 100.0

    assert set(matched) == {
        "python",
        "machine learning",
        "tensorflow"
    }

    assert missing == []


# ============================================================
# Test Partial Skill Matching
# ============================================================

def test_skill_match_partial():

    resume_skills = [
        "Python",
        "Machine Learning"
    ]

    jd_skills = [
        "Python",
        "Machine Learning",
        "TensorFlow",
        "Docker"
    ]

    score, matched, missing = (
        calculate_skill_match(
            resume_skills,
            jd_skills
        )
    )

    assert score == 50.0

    assert set(matched) == {
        "python",
        "machine learning"
    }

    assert set(missing) == {
        "tensorflow",
        "docker"
    }


# ============================================================
# Test No Matching Skills
# ============================================================

def test_skill_match_no_skills():

    resume_skills = [
        "Python"
    ]

    jd_skills = [
        "Docker",
        "AWS"
    ]

    score, matched, missing = (
        calculate_skill_match(
            resume_skills,
            jd_skills
        )
    )

    assert score == 0.0

    assert matched == []

    assert set(missing) == {
        "docker",
        "aws"
    }


# ============================================================
# Test Empty JD Skills
# ============================================================

def test_empty_jd_skills():

    resume_skills = [
        "Python",
        "Machine Learning"
    ]

    jd_skills = []

    score, matched, missing = (
        calculate_skill_match(
            resume_skills,
            jd_skills
        )
    )

    assert score == 0

    assert matched == []

    assert missing == []


# ============================================================
# Test Final Score
# ============================================================

def test_final_score():

    semantic_score = 80

    skill_score = 90

    final_score = calculate_final_score(
        semantic_score,
        skill_score
    )

    # 80 * 0.60 + 90 * 0.40
    # = 48 + 36
    # = 84

    assert final_score == 84.0


# ============================================================
# Test Strong Candidate
# ============================================================

def test_strong_candidate():

    recommendation, message = (
        get_recommendation(85)
    )

    assert recommendation == (
        "Strong Candidate"
    )

    assert (
        "strong alignment"
        in message.lower()
    )


# ============================================================
# Test Good Candidate
# ============================================================

def test_good_candidate():

    recommendation, message = (
        get_recommendation(70)
    )

    assert recommendation == (
        "Good Candidate"
    )


# ============================================================
# Test Weak Candidate
# ============================================================

def test_needs_improvement():

    recommendation, message = (
        get_recommendation(40)
    )

    assert recommendation == (
        "Needs Improvement"
    )