# import spacy
# from typing import List, Dict

# # Load spaCy model
# try:
#     nlp = spacy.load("en_core_web_sm")
# except OSError:
#     print("Please run: python -m spacy download en_core_web_sm")
#     exit(1)

# # Technical skills patterns - expanded list
# TECHNICAL_SKILLS = [
#     # Programming languages
#     ["Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin", "Scala"],
#     # Frontend
#     ["React", "Angular", "Vue", "Vue.js", "Next.js", "Svelte", "HTML", "CSS", "Bootstrap", "Tailwind"],
#     # Backend
#     ["Node.js", "Express", "FastAPI", "Django", "Flask", "Spring Boot", "Rails", "Laravel", "ASP.NET"],
#     # Database
#     ["PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Oracle", "NoSQL", "Firebase"],
#     # DevOps/Cloud
#     ["Docker", "Kubernetes", "AWS", "Azure", "GCP", "Google Cloud", "Heroku", "Vercel", "Netlify"],
#     # Tools
#     ["Git", "Jenkins", "CI/CD", "GitHub", "GitLab", "Bitbucket", "Jira", "Terraform"],
#     # Methodologies
#     ["Agile", "Scrum", "Kanban", "TDD", "BDD", "DevOps"],
#     # ML/AI
#     ["Machine Learning", "TensorFlow", "PyTorch", "NLP", "BERT", "GPT"],
# ]

# def create_skill_matcher(nlp):
#     """Create PhraseMatcher for skills"""
#     from spacy.matcher import PhraseMatcher
#     matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
#     patterns = []
#     for skill_list in TECHNICAL_SKILLS:
#         for skill in skill_list:
#             patterns.append(nlp.make_doc(skill.lower()))
    
#     matcher.add("TECHNICAL_SKILLS", patterns)
#     return matcher

# # Create matcher globally
# matcher = create_skill_matcher(nlp)

# def extract_skills(text: str) -> Dict:
#     """Extract skills using spaCy NER + PhraseMatcher"""
#     doc = nlp(text)
    
#     # Extract with PhraseMatcher
#     matches = matcher(doc)
#     skills = list(set([doc[start:end].text for match_id, start, end in matches]))
    
#     # NER entities (ORG, PRODUCT might catch frameworks)
#     ner_skills = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT"]]
#     all_skills = list(set(skills + ner_skills))
    
#     # Categorize skills
#     categories = {
#         "programming": [],
#         "frontend": [],
#         "backend": [],
#         "devops": [],
#         "databases": [],
#         "methodologies": []
#     }
    
#     for skill in all_skills:
#         for i, skill_list in enumerate(TECHNICAL_SKILLS):
#             if skill in skill_list:
#                 if i == 0:
#                     categories["programming"].append(skill)
#                 elif i == 1:
#                     categories["frontend"].append(skill)
#                 elif i == 2:
#                     categories["backend"].append(skill)
#                 elif i == 3:
#                     categories["databases"].append(skill)
#                 elif i == 4:
#                     categories["devops"].append(skill)
#                 elif i >= 5:
#                     categories["methodologies"].append(skill)
    
#     # Common skills (most in-demand)
#     common_skills = ["Python", "JavaScript", "React", "Docker", "AWS", "Git", "SQL"]
#     rare_skills = [s for s in all_skills if s not in common_skills]
    
#     return {
#         "extracted_skills": all_skills,
#         "skill_categories": {k: v for k, v in categories.items() if v},
#         "common_skills": common_skills,
#         "rare_skills": rare_skills
#     }

# def recommend_jobs(skills):

#     skills_lower = [
#         skill.lower()
#         for skill in skills
#     ]

#     roles = []

#     if "python" in skills_lower:
#         roles.append("Python Developer")

#     if (
#         "machine learning" in skills_lower
#         or
#         "tensorflow" in skills_lower
#         or
#         "pytorch" in skills_lower
#     ):
#         roles.append("Machine Learning Engineer")

#     if (
#         "nlp" in skills_lower
#         or
#         "bert" in skills_lower
#         or
#         "llm" in skills_lower
#     ):
#         roles.append("AI Engineer")

#     if (
#         "sql" in skills_lower
#         or
#         "power bi" in skills_lower
#         or
#         "tableau" in skills_lower
#     ):
#         roles.append("Data Analyst")

#     if (
#         "machine learning" in skills_lower
#         and
#         "python" in skills_lower
#     ):
#         roles.append("Data Scientist")

#     if (
#         "fastapi" in skills_lower
#         or
#         "django" in skills_lower
#         or
#         "flask" in skills_lower
#     ):
#         roles.append("Backend Developer")

#     if (
#         "react" in skills_lower
#         or
#         "javascript" in skills_lower
#     ):
#         roles.append("Frontend Developer")

#     if (
#         "docker" in skills_lower
#         or
#         "kubernetes" in skills_lower
#         or
#         "aws" in skills_lower
#     ):
#         roles.append("DevOps Engineer")

#     return list(set(roles))


import spacy
from typing import Dict

# try:
#     nlp = spacy.load("en_core_web_sm")
# except OSError:
#     print("Run: python -m spacy download en_core_web_sm")
#     exit(1)

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError(
        "SpaCy model 'en_core_web_sm' is not installed."
    )
from spacy.matcher import PhraseMatcher

TECHNICAL_SKILLS = {

    "programming": [
        "Python", "Java", "JavaScript", "TypeScript",
        "C++", "C#", "Go", "Rust", "PHP",
        "Ruby", "Swift", "Kotlin", "Scala"
    ],

    "frontend": [
        "React", "Angular", "Vue", "Vue.js",
        "Next.js", "Svelte", "HTML", "CSS",
        "Bootstrap", "Tailwind"
    ],

    "backend": [
        "Node.js", "Express", "FastAPI",
        "Django", "Flask", "Spring Boot",
        "Laravel", "ASP.NET"
    ],

    "databases": [
        "MySQL", "PostgreSQL", "MongoDB",
        "Redis", "SQLite", "Oracle",
        "Firebase", "NoSQL"
    ],

    "cloud_devops": [
        "AWS", "Azure", "GCP",
        "Docker", "Kubernetes",
        "Terraform", "Jenkins",
        "CI/CD"
    ],

    "data_science": [
        "Machine Learning",
        "Deep Learning",
        "Data Analysis",
        "Data Science",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Matplotlib",
        "Power BI",
        "Tableau"
    ],

    "ai_nlp": [
        "NLP",
        "BERT",
        "GPT",
        "LLM",
        "LangChain",
        "RAG",
        "Transformers",
        "Prompt Engineering"
    ],

    "testing": [
        "Selenium",
        "JUnit",
        "PyTest",
        "Postman",
        "Manual Testing",
        "Automation Testing"
    ],

    "cybersecurity": [
        "Penetration Testing",
        "Ethical Hacking",
        "Network Security",
        "Cyber Security"
    ],

    "mobile": [
        "Android",
        "Flutter",
        "React Native",
        "iOS"
    ],

    "tools": [
        "Git",
        "GitHub",
        "GitLab",
        "Bitbucket",
        "Jira"
    ]
}


def create_skill_matcher():

    matcher = PhraseMatcher(
        nlp.vocab,
        attr="LOWER"
    )

    patterns = []

    for category in TECHNICAL_SKILLS.values():

        for skill in category:

            patterns.append(
                nlp.make_doc(skill)
            )

    matcher.add(
        "SKILLS",
        patterns
    )

    return matcher


matcher = create_skill_matcher()


def extract_skills(text: str) -> Dict:

    doc = nlp(text)

    matches = matcher(doc)

    extracted_skills = []

    for _, start, end in matches:

        skill = doc[start:end].text

        if skill not in extracted_skills:

            extracted_skills.append(skill)

    categorized = {}

    for category, skill_list in TECHNICAL_SKILLS.items():

        matched = []

        for skill in extracted_skills:

            if skill in skill_list:

                matched.append(skill)

        if matched:

            categorized[category] = matched

    common_skills = [
        "Python",
        "JavaScript",
        "React",
        "AWS",
        "Docker",
        "Git",
        "SQL"
    ]

    rare_skills = [

        skill

        for skill in extracted_skills

        if skill not in common_skills
    ]

    return {

        "extracted_skills":
        extracted_skills,

        "skill_categories":
        categorized,

        "common_skills":
        common_skills,

        "rare_skills":
        rare_skills
    }


def recommend_jobs(skills):

    skills_lower = {
        skill.lower()
        for skill in skills
    }

    roles = []

    # AI / ML

    if (
        "machine learning" in skills_lower
        or "tensorflow" in skills_lower
        or "pytorch" in skills_lower
    ):
        roles.append(
            "Machine Learning Engineer"
        )

    if (
        "nlp" in skills_lower
        or "bert" in skills_lower
        or "gpt" in skills_lower
        or "llm" in skills_lower
    ):
        roles.append(
            "AI Engineer"
        )

    if (
        "machine learning" in skills_lower
        and "python" in skills_lower
    ):
        roles.append(
            "Data Scientist"
        )

    # Data

    if (
        "sql" in skills_lower
        or "power bi" in skills_lower
        or "tableau" in skills_lower
    ):
        roles.append(
            "Data Analyst"
        )

    # Backend

    if (
        "python" in skills_lower
        and
        (
            "django" in skills_lower
            or "fastapi" in skills_lower
            or "flask" in skills_lower
        )
    ):
        roles.append(
            "Backend Developer"
        )

    # Frontend

    if (
        "react" in skills_lower
        or "javascript" in skills_lower
        or "angular" in skills_lower
    ):
        roles.append(
            "Frontend Developer"
        )

    # Full Stack

    if (
        "react" in skills_lower
        and
        (
            "node.js" in skills_lower
            or "fastapi" in skills_lower
            or "django" in skills_lower
        )
    ):
        roles.append(
            "Full Stack Developer"
        )

    # DevOps

    if (
        "docker" in skills_lower
        or "kubernetes" in skills_lower
        or "aws" in skills_lower
        or "azure" in skills_lower
    ):
        roles.append(
            "DevOps Engineer"
        )

    # Cloud

    if (
        "aws" in skills_lower
        or "azure" in skills_lower
        or "gcp" in skills_lower
    ):
        roles.append(
            "Cloud Engineer"
        )

    # Testing

    if (
        "selenium" in skills_lower
        or "manual testing" in skills_lower
        or "automation testing" in skills_lower
    ):
        roles.append(
            "QA Engineer"
        )

    # Mobile

    if (
        "flutter" in skills_lower
        or "android" in skills_lower
        or "react native" in skills_lower
    ):
        roles.append(
            "Mobile App Developer"
        )

    # Cyber Security

    if (
        "ethical hacking" in skills_lower
        or "cyber security" in skills_lower
    ):
        roles.append(
            "Cyber Security Analyst"
        )

    if not roles:

        roles.append(
            "Software Engineer"
        )

    return list(set(roles))