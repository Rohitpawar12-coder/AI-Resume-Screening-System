# src/matcher.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMatcher:
    """
    Calculates semantic similarity between
    a resume and a target job description.
    """

    def __init__(
        self,
        model_name="all-MiniLM-L6-v2"
    ):
        self.model_name = model_name

        self.model = SentenceTransformer(
            self.model_name
        )

    def calculate_similarity(
        self,
        resume_text,
        job_description
    ):
        """
        Returns semantic similarity
        between 0 and 1.
        """

        if not resume_text:
            return 0.0

        if not job_description:
            return 0.0

        resume_text = str(
            resume_text
        ).strip()

        job_description = str(
            job_description
        ).strip()

        if not resume_text:
            return 0.0

        if not job_description:
            return 0.0

        resume_embedding = self.model.encode(
            [resume_text],
            convert_to_numpy=True
        )

        job_embedding = self.model.encode(
            [job_description],
            convert_to_numpy=True
        )

        similarity = cosine_similarity(
            resume_embedding,
            job_embedding
        )

        score = float(
            similarity[0][0]
        )

        score = max(
            0.0,
            min(
                1.0,
                score
            )
        )

        return score