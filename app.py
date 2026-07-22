import json
import re
from pathlib import Path

import streamlit as st
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume Screening & Job Matching System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

JOB_ROLES_PATH = DATA_DIR / "job_roles.json"

SKILLS_PATH = DATA_DIR / "skills.json"


# ============================================================
# LOAD JSON FILE
# ============================================================

@st.cache_data
def load_json_file(file_path):

    if not file_path.exists():

        st.error(
            f"File not found: {file_path}"
        )

        st.stop()

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except json.JSONDecodeError as e:

        st.error(
            f"Invalid JSON file: {file_path}\n\n{e}"
        )

        st.stop()


# ============================================================
# LOAD JOB ROLES
# ============================================================

job_roles = load_json_file(
    JOB_ROLES_PATH
)


# ============================================================
# LOAD SKILLS
# ============================================================

skills_database = load_json_file(
    SKILLS_PATH
)


# ============================================================
# LOAD SEMANTIC MODEL
# ============================================================

@st.cache_resource
def load_semantic_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


# ============================================================
# PDF RESUME PARSER
# ============================================================

def extract_text_from_pdf(
    pdf_file
):

    try:

        reader = PdfReader(
            pdf_file
        )

        pages_text = []

        for page in reader.pages:

            text = page.extract_text()

            if text:

                pages_text.append(
                    text
                )

        final_text = "\n".join(
            pages_text
        )

        return final_text.strip()

    except Exception as e:

        raise Exception(
            f"Could not read PDF: {e}"
        )


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(
    text
):

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
# SKILL MATCHING
# ============================================================

def skill_exists_in_resume(
    resume_text,
    skill
):

    resume_text = normalize_text(
        resume_text
    )

    skill = normalize_text(
        skill
    )

    if not skill:

        return False

    # Exact phrase matching
    pattern = (
        r"(?<![a-zA-Z0-9])"
        + re.escape(skill)
        + r"(?![a-zA-Z0-9])"
    )

    if re.search(
        pattern,
        resume_text,
        flags=re.IGNORECASE
    ):

        return True

    return False


# ============================================================
# EXTRACT SKILLS FROM RESUME
# ============================================================

def extract_resume_skills(
    resume_text,
    skills_database
):

    detected_skills = {}

    for category, skills in skills_database.items():

        matched_skills = []

        # ----------------------------------------------------
        # LIST FORMAT
        # ----------------------------------------------------

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

                if skill_exists_in_resume(
                    resume_text,
                    skill
                ):

                    if skill not in matched_skills:

                        matched_skills.append(
                            skill
                        )


        # ----------------------------------------------------
        # DICTIONARY FORMAT WITH ALIASES
        # ----------------------------------------------------

        elif isinstance(
            skills,
            dict
        ):

            for main_skill, aliases in skills.items():

                found = False

                # Check main skill
                if skill_exists_in_resume(
                    resume_text,
                    main_skill
                ):

                    found = True


                # Check aliases
                if isinstance(
                    aliases,
                    list
                ):

                    for alias in aliases:

                        if skill_exists_in_resume(
                            resume_text,
                            alias
                        ):

                            found = True

                            break


                if found:

                    if main_skill not in matched_skills:

                        matched_skills.append(
                            main_skill
                        )


        if matched_skills:

            detected_skills[
                category
            ] = matched_skills


    return detected_skills


# ============================================================
# FLATTEN SKILLS
# ============================================================

def flatten_detected_skills(
    detected_skills
):

    all_skills = []

    for category, skills in detected_skills.items():

        for skill in skills:

            if skill not in all_skills:

                all_skills.append(
                    skill
                )

    return all_skills


# ============================================================
# CALCULATE SEMANTIC SIMILARITY
# ============================================================

def calculate_semantic_similarity(
    resume_text,
    job_description
):

    model = load_semantic_model()

    resume_embedding = model.encode(
        [
            resume_text
        ],
        convert_to_numpy=True
    )

    job_embedding = model.encode(
        [
            job_description
        ],
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

    return score * 100


# ============================================================
# CALCULATE SKILL MATCH
# ============================================================

def calculate_skill_match(
    resume_skills,
    required_skills
):

    if not required_skills:

        return 0.0


    resume_skills_normalized = {

        normalize_text(
            skill
        )

        for skill in resume_skills

    }


    matched_skills = []

    missing_skills = []


    for skill in required_skills:

        normalized_skill = normalize_text(
            skill
        )

        if normalized_skill in resume_skills_normalized:

            matched_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )


    score = (

        len(matched_skills)

        / len(required_skills)

    ) * 100


    return (
        score,
        matched_skills,
        missing_skills
    )


# ============================================================
# CALCULATE OVERALL SCORE
# ============================================================

def calculate_overall_score(
    semantic_score,
    skill_score
):

    overall_score = (

        semantic_score * 0.60

    ) + (

        skill_score * 0.40

    )

    return max(
        0.0,
        min(
            100.0,
            overall_score
        )
    )


# ============================================================
# GET RECOMMENDATION
# ============================================================

def get_recommendation(
    score
):

    if score >= 80:

        return (
            "Excellent Match",
            "Your resume is highly aligned with the selected target role."
        )

    elif score >= 65:

        return (
            "Good Match",
            "Your resume has good alignment with the selected target role. "
            "Improve the missing skills to increase your match."
        )

    elif score >= 50:

        return (
            "Moderate Match",
            "Your resume partially matches the selected target role. "
            "Focus on developing the missing skills."
        )

    else:

        return (
            "Low Match",
            "Your resume currently has limited alignment with the selected "
            "target role. Consider building the required skills."
        )


# ============================================================
# HEADER
# ============================================================

st.title(
    "📄 AI Resume Screening & Job Matching System"
)

st.markdown(
    """
    Upload your resume and select your target IT career.
    The system analyzes your resume using semantic similarity
    and skill matching.
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "🎯 Career Target"
    )

    st.write(
        "Choose your career field and target role."
    )


    # --------------------------------------------------------
    # CAREER FIELD
    # --------------------------------------------------------

    career_fields = list(
        job_roles.keys()
    )


    selected_career_field = st.selectbox(
        "Select Career Field",
        career_fields
    )


    # --------------------------------------------------------
    # TARGET ROLE
    # --------------------------------------------------------

    roles_data = job_roles[
        selected_career_field
    ]


    target_roles = list(
        roles_data.keys()
    )


    selected_target_role = st.selectbox(
        "Select Target Role",
        target_roles
    )


    # --------------------------------------------------------
    # SELECT ROLE
    # --------------------------------------------------------

    selected_role = roles_data[
        selected_target_role
    ]


    st.divider()


    # --------------------------------------------------------
    # ROLE REQUIREMENTS
    # --------------------------------------------------------

    st.subheader(
        "📋 Role Requirements"
    )


    with st.expander(
        "Required Skills"
    ):

        required_skills = selected_role.get(
            "required_skills",
            []
        )

        for skill in required_skills:

            st.write(
                f"• {skill}"
            )


    with st.expander(
        "Tools & Libraries"
    ):

        tools_and_libraries = selected_role.get(
            "tools_and_libraries",
            []
        )

        for tool in tools_and_libraries:

            st.write(
                f"• {tool}"
            )


    with st.expander(
        "Recommended Skills"
    ):

        recommended_skills = selected_role.get(
            "recommended_skills",
            []
        )

        for skill in recommended_skills:

            st.write(
                f"• {skill}"
            )


    st.divider()


    # --------------------------------------------------------
    # SCORING MODEL
    # --------------------------------------------------------

    st.subheader(
        "📊 Scoring Model"
    )

    st.write(
        "Semantic Similarity"
    )

    st.progress(
        60
    )

    st.caption(
        "Weight: 60%"
    )


    st.write(
        "Skill Match"
    )

    st.progress(
        40
    )

    st.caption(
        "Weight: 40%"
    )


# ============================================================
# MAIN UPLOAD SECTION
# ============================================================

st.subheader(
    "📤 Upload Resume"
)


uploaded_file = st.file_uploader(
    "Upload your resume in PDF format",
    type=[
        "pdf"
    ]
)


# ============================================================
# TARGET INFORMATION
# ============================================================

st.info(
    f"""
    🎯 **Career Field:** {selected_career_field}

    💼 **Target Role:** {selected_target_role}
    """
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_button = st.button(
    "🚀 Analyze Resume",
    type="primary",
    use_container_width=True
)


# ============================================================
# PROCESS RESUME
# ============================================================

if analyze_button:

    if uploaded_file is None:

        st.warning(
            "⚠️ Please upload your resume first."
        )

        st.stop()


    try:

        # ----------------------------------------------------
        # EXTRACT PDF TEXT
        # ----------------------------------------------------

        with st.spinner(
            "📄 Reading resume..."
        ):

            resume_text = extract_text_from_pdf(
                uploaded_file
            )


        if not resume_text:

            st.error(
                "❌ No readable text found in this PDF."
            )

            st.stop()


        # ----------------------------------------------------
        # GET ROLE INFORMATION
        # ----------------------------------------------------

        job_description = selected_role.get(
            "description",
            ""
        )


        required_skills = selected_role.get(
            "required_skills",
            []
        )


        tools_and_libraries = selected_role.get(
            "tools_and_libraries",
            []
        )


        recommended_skills = selected_role.get(
            "recommended_skills",
            []
        )


        # ----------------------------------------------------
        # CREATE COMPLETE JOB PROFILE
        # ----------------------------------------------------

        complete_job_profile = f"""

        Target Career Field:

        {selected_career_field}


        Target Job Role:

        {selected_target_role}


        Job Description:

        {job_description}


        Required Skills:

        {", ".join(required_skills)}


        Tools and Libraries:

        {", ".join(tools_and_libraries)}


        Recommended Skills:

        {", ".join(recommended_skills)}

        """


        # ----------------------------------------------------
        # DETECT RESUME SKILLS
        # ----------------------------------------------------

        with st.spinner(
            "🔍 Detecting skills and technologies..."
        ):

            detected_skills = extract_resume_skills(
                resume_text,
                skills_database
            )


        resume_skills = flatten_detected_skills(
            detected_skills
        )


        # ----------------------------------------------------
        # SEMANTIC SCORE
        # ----------------------------------------------------

        with st.spinner(
            "🤖 Calculating semantic similarity..."
        ):

            semantic_score = calculate_semantic_similarity(
                resume_text,
                complete_job_profile
            )


        # ----------------------------------------------------
        # SKILL SCORE
        # ----------------------------------------------------

        skill_result = calculate_skill_match(
            resume_skills,
            required_skills
        )


        skill_score = skill_result[
            0
        ]

        matched_skills = skill_result[
            1
        ]

        missing_skills = skill_result[
            2
        ]


        # ----------------------------------------------------
        # MATCH TOOLS
        # ----------------------------------------------------

        resume_skills_normalized = {

            normalize_text(
                skill
            )

            for skill in resume_skills

        }


        matched_tools = []


        for tool in tools_and_libraries:

            if normalize_text(
                tool
            ) in resume_skills_normalized:

                matched_tools.append(
                    tool
                )


        # ----------------------------------------------------
        # OVERALL SCORE
        # ----------------------------------------------------

        overall_score = calculate_overall_score(
            semantic_score,
            skill_score
        )


        # ----------------------------------------------------
        # RECOMMENDATION
        # ----------------------------------------------------

        recommendation, recommendation_message = (
            get_recommendation(
                overall_score
            )
        )


        # ====================================================
        # DISPLAY RESULTS
        # ====================================================

        st.success(
            "✅ Resume analysis completed successfully!"
        )


        st.divider()


        st.header(
            "📊 Resume Analysis Results"
        )


        # ----------------------------------------------------
        # TARGET
        # ----------------------------------------------------

        col1, col2 = st.columns(
            2
        )


        with col1:

            st.metric(
                "Career Field",
                selected_career_field
            )


        with col2:

            st.metric(
                "Target Role",
                selected_target_role
            )


        st.divider()


        # ----------------------------------------------------
        # SCORE CARDS
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(
            3
        )


        with col1:

            st.metric(
                "🏆 Overall Match",
                f"{overall_score:.1f}%"
            )


        with col2:

            st.metric(
                "🧠 Semantic Similarity",
                f"{semantic_score:.1f}%"
            )


        with col3:

            st.metric(
                "🛠️ Skill Match",
                f"{skill_score:.1f}%"
            )


        st.divider()


        # ----------------------------------------------------
        # RECOMMENDATION
        # ----------------------------------------------------

        st.subheader(
            "🤖 AI Recommendation"
        )


        if overall_score >= 80:

            st.success(
                f"### {recommendation}\n\n"
                f"{recommendation_message}"
            )

        elif overall_score >= 65:

            st.info(
                f"### {recommendation}\n\n"
                f"{recommendation_message}"
            )

        elif overall_score >= 50:

            st.warning(
                f"### {recommendation}\n\n"
                f"{recommendation_message}"
            )

        else:

            st.error(
                f"### {recommendation}\n\n"
                f"{recommendation_message}"
            )


        st.divider()


        # ----------------------------------------------------
        # SKILL ANALYSIS
        # ----------------------------------------------------

        st.subheader(
            "🛠️ Required Skill Analysis"
        )


        col1, col2 = st.columns(
            2
        )


        with col1:

            st.markdown(
                "### ✅ Matched Skills"
            )


            if matched_skills:

                for skill in matched_skills:

                    st.success(
                        f"✓ {skill}"
                    )

            else:

                st.info(
                    "No required skills matched."
                )


        with col2:

            st.markdown(
                "### ❌ Missing Skills"
            )


            if missing_skills:

                for skill in missing_skills:

                    st.error(
                        f"✗ {skill}"
                    )

            else:

                st.success(
                    "🎉 All required skills matched!"
                )


        st.divider()


        # ----------------------------------------------------
        # TOOLS AND LIBRARIES
        # ----------------------------------------------------

        st.subheader(
            "🔧 Tools & Libraries"
        )


        if matched_tools:

            st.success(
                "Tools and libraries detected in your resume:"
            )


            tool_columns = st.columns(
                min(
                    4,
                    len(
                        matched_tools
                    )
                )
            )


            for index, tool in enumerate(
                matched_tools
            ):

                with tool_columns[
                    index % len(
                        tool_columns
                    )
                ]:

                    st.info(
                        f"✓ {tool}"
                    )

        else:

            st.warning(
                "No target-specific tools or libraries detected."
            )


        st.divider()


        # ----------------------------------------------------
        # DETECTED SKILLS
        # ----------------------------------------------------

        st.subheader(
            "🧠 Skills Detected From Resume"
        )


        if detected_skills:

            for category, skills in detected_skills.items():

                with st.expander(
                    f"📌 {category}",
                    expanded=False
                ):

                    st.write(
                        ", ".join(
                            skills
                        )
                    )

        else:

            st.warning(
                "No skills were detected."
            )


        st.divider()


        # ----------------------------------------------------
        # IMPROVEMENT SUGGESTIONS
        # ----------------------------------------------------

        st.subheader(
            "💡 Career Improvement Suggestions"
        )


        if missing_skills:

            st.write(
                f"""
                To improve your resume for the
                **{selected_target_role}** role,
                consider learning or gaining project
                experience in the following skills:
                """
            )


            for skill in missing_skills:

                st.warning(
                    f"📚 {skill}"
                )

        else:

            st.success(
                "Your resume covers all required skills!"
            )


        # ----------------------------------------------------
        # TOOLS SUGGESTIONS
        # ----------------------------------------------------

        missing_tools = [

            tool

            for tool in tools_and_libraries

            if tool not in matched_tools

        ]


        if missing_tools:

            st.write(
                "### 🔧 Recommended Tools & Libraries"
            )


            for tool in missing_tools:

                st.info(
                    f"Learn or gain experience with: {tool}"
                )


        st.divider()


        # ----------------------------------------------------
        # FINAL ASSESSMENT
        # ----------------------------------------------------

        st.subheader(
            "📌 Final Assessment"
        )


        st.markdown(
            f"""
            **Target Career:** {selected_career_field}

            **Target Role:** {selected_target_role}

            **Overall Match Score:** {overall_score:.1f}%

            **Semantic Similarity:** {semantic_score:.1f}%

            **Required Skill Match:** {skill_score:.1f}%

            **Recommendation:** {recommendation}
            """
        )


    except Exception as e:

        st.error(
            "❌ An error occurred while analyzing the resume."
        )

        st.exception(
            e
        )