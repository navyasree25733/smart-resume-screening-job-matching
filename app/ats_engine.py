

from sentence_transformers import SentenceTransformer, util
import re
from typing import List, Dict
from .models import JobDescription

# Load Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')


def calculate_ats_score(resume_text: str, job_desc: JobDescription) -> Dict:
    """Calculate ATS score using weighted formula"""

    # 1. Skill Match (25%)
    skills_score = calculate_skill_match(
        resume_text,
        job_desc.required_skills
    )

    # 2. Semantic Match (40%)
    semantic_score = calculate_semantic_match(
        resume_text,
        job_desc.description
    )

    # 3. Experience (15%)
    exp_score = calculate_experience(
        resume_text
    )

    # 4. Degree (10%)
    degree_score = calculate_degree(
        resume_text
    )

    # 5. Certifications (5%)
    cert_score = calculate_certifications(
        resume_text
    )

    # 6. Projects (5%)
    projects_score = calculate_projects(
        resume_text
    )

    # ATS Formula
    ats_score = (
        0.10 * skills_score +
        0.60 * semantic_score +
        0.10 * exp_score +
        0.10 * degree_score +
        0.05 * cert_score +
        0.05 * projects_score
    )

    ats_score = min(
        100,
        max(
            0,
            ats_score * 100
        )
    )

    # Missing Skills
    missing_skills = [
        skill
        for skill in job_desc.required_skills
        if skill.lower() not in resume_text.lower()
    ]

    # Matched Skills
    matched_skills = [
        skill
        for skill in job_desc.required_skills
        if skill.lower() in resume_text.lower()
    ]

    suggestions = generate_improvement_suggestions(
        missing_skills,
        skills_score
    )

    return {
        "ats_score": round(
            ats_score,
            2
        ),

        "skill_match": round(
            skills_score,
            2
        ),

        "semantic_match": round(
            semantic_score,
            2
        ),

        "matched_skills":
        matched_skills,

        "experience_years":
        exp_score,

        "has_degree":
        bool(degree_score),

        "certifications":
        cert_score,

        "projects_count":
        projects_score,

        "missing_skills":
        missing_skills,

        "improvement_suggestions":
        suggestions,

        "component_scores": {
            "S": skills_score,
            "M": semantic_score,
            "E": exp_score,
            "D": degree_score,
            "C": cert_score,
            "P": projects_score
        }
    }


def calculate_skill_match(
    resume: str,
    required_skills: List[str]
) -> float:

    if not required_skills:
        return 0.5

    matched = 0

    resume_lower = resume.lower()

    # Encode resume once
    resume_embedding = model.encode(
        resume[:1000]
    )

    for skill in required_skills:

        # Exact Match
        if skill.lower() in resume_lower:
            matched += 1
            continue

        # Semantic Skill Match
        skill_embedding = model.encode(
            skill
        )

        similarity = util.cos_sim(
            skill_embedding,
            resume_embedding
        )[0][0].item()

        if similarity > 0.50:
            matched += 1

    return matched / len(required_skills)


def calculate_semantic_match(
    resume: str,
    job_desc: str
) -> float:
    """Semantic similarity using Sentence Transformers"""

    resume_batch = (
        resume[:1000]
        if len(resume) > 1000
        else resume
    )

    job_batch = (
        job_desc[:1000]
        if len(job_desc) > 1000
        else job_desc
    )

    resume_embedding = model.encode(
        resume_batch
    )

    job_embedding = model.encode(
        job_batch
    )

    similarity = util.cos_sim(
        resume_embedding,
        job_embedding
    )[0][0].item()

    # Convert [-1,1] → [0,1]
    similarity = (
        similarity + 1
    ) / 2

    return min(
        max(
            similarity,
            0
        ),
        1
    )


def calculate_experience(
    resume: str
) -> float:

    patterns = [
        r'(\d+)\s*years?\s*(?:of\s+)?experience',
        r'(\d+)\s*years?',
        r'experience[:\-]?\s*(\d+)'
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            resume,
            re.IGNORECASE
        )

        if match:

            years = float(
                match.group(1)
            )

            return min(
                20,
                years
            ) / 20

    return 0.3


def calculate_degree(
    resume: str
) -> float:

    degree_keywords = [
        'bachelor',
        'master',
        'phd',
        'bs',
        'ms',
        'ba',
        'ma',
        'degree'
    ]

    return (
        1.0
        if any(
            keyword in resume.lower()
            for keyword in degree_keywords
        )
        else 0.0
    )


def calculate_certifications(
    resume: str
) -> float:

    cert_keywords = [
        'certified',
        'certification',
        'aws certified',
        'azure',
        'google cloud',
        'pmp',
        'scrum'
    ]

    certs = sum(
        1
        for keyword in cert_keywords
        if keyword in resume.lower()
    )

    return min(
        certs,
        5
    ) / 5


def calculate_projects(
    resume: str
) -> float:

    projects = resume.lower().count(
        'project'
    )

    return min(
        projects,
        5
    ) / 5


def generate_improvement_suggestions(
    missing_skills: List[str],
    skill_score: float
) -> List[str]:

    suggestions = []

    if skill_score < 0.6:
        suggestions.append(
            "Add missing skills to your resume with specific examples"
        )

    if missing_skills:
        suggestions.append(
            f"Include these key skills: {', '.join(missing_skills[:3])}"
        )

    suggestions.extend([
        "Quantify achievements with numbers (e.g., increased efficiency by 30%)",
        "Use standard section headers: Experience, Education, Skills",
        "Tailor keywords from the job description",
        "Add GitHub or portfolio links for technical roles"
    ])

    return suggestions[:4]

















# from sentence_transformers import SentenceTransformer, util
# import numpy as np
# import re
# from typing import List, Dict
# from .models import JobDescription

# # Use a lightweight model
# model = SentenceTransformer('all-MiniLM-L6-v2')

# def calculate_ats_score(resume_text: str, job_desc: JobDescription) -> Dict:
#     """Calculate ATS score using weighted formula"""
    
#     # 1. Skill Match (35%)
#     skills_score = calculate_skill_match(resume_text, job_desc.required_skills)
    
#     # 2. Semantic Match (30%) - BERT Cosine Similarity
#     semantic_score = calculate_semantic_match(resume_text, job_desc.description)
    
#     # 3. Experience (15%)
#     exp_score = calculate_experience(resume_text)
    
#     # 4. Degree (10%)
#     degree_score = calculate_degree(resume_text)
    
#     # 5. Certifications (5%)
#     cert_score = calculate_certifications(resume_text)
    
#     # 6. Projects (5%)
#     projects_score = calculate_projects(resume_text)
    
#     # ATS Formula: 0.35S + 0.30M + 0.15E + 0.10D + 0.05C + 0.05P
#     ats_score = (
#         0.35 * skills_score +
#         0.30 * semantic_score +
#         0.15 * exp_score +
#         0.10 * degree_score +
#         0.05 * cert_score +
#         0.05 * projects_score
#     )
    
    
#     # Normalize to 0-100
#     ats_score = min(100, max(0, ats_score * 100))
    
#     missing_skills = [skill for skill in job_desc.required_skills 
#                      if skill.lower() not in resume_text.lower()]
#     matched_skills = [

#     skill

#     for skill in job_desc.required_skills

#     if skill.lower()
#     in resume_text.lower()
# ]
#     suggestions = generate_improvement_suggestions(missing_skills, skills_score)
    
#     return {
#         "ats_score": round(ats_score, 2),
#         "skill_match": round(skills_score, 2),
#         "semantic_match": round(semantic_score, 2),
#         "matched_skills": matched_skills,
#         "experience_years": exp_score,
#         "has_degree": bool(degree_score),
#         "certifications": cert_score,
#         "projects_count": projects_score,
#         "missing_skills": missing_skills,
#         "improvement_suggestions": suggestions,
#         "component_scores": {
#             "S": skills_score,
#             "M": semantic_score,
#             "E": exp_score,
#             "D": degree_score,
#             "C": cert_score,
#             "P": projects_score
#         }
#     }

# # def calculate_skill_match(resume: str, required_skills: List[str]) -> float:
# #     """Calculate skill match percentage"""
# #     resume_lower = resume.lower()
# #     if not required_skills:
# #         return 0.5
# #     matches = sum(1 for skill in required_skills if skill.lower() in resume_lower)
# #     return min(1.0, matches / max(len(required_skills), 1))

# def calculate_skill_match(resume: str, required_skills: List[str]) -> float:

#     if not required_skills:
#         return 0.5

#     matched = 0

#     resume_lower = resume.lower()

#     for skill in required_skills:

#         # Exact Match
#         if skill.lower() in resume_lower:
#             matched += 1
#             continue

#         # Semantic Match
#         skill_embedding = model.encode(skill)
#         resume_embedding = model.encode(resume[:1000])

#         similarity = util.cos_sim(
#             skill_embedding,
#             resume_embedding
#         )[0][0].item()

#         if similarity > 0.50:
#             matched += 1

#     return matched / len(required_skills)

# # def calculate_semantic_match(resume: str, job_desc: str) -> float:
# #     """BERT-based semantic similarity"""
# #     # Truncate long texts for efficiency
# #     resume_batch = resume[:1000] if len(resume) > 1000 else resume
# #     job_batch = job_desc[:1000] if len(job_desc) > 1000 else job_desc
    
# #     resume_embedding = model.encode(resume_batch)
# #     job_embedding = model.encode(job_batch)
# #     similarity = util.cos_sim(resume_embedding, job_embedding)[0][0].item()
# #     return float(similarity)

# def calculate_semantic_match(resume: str, job_desc: str) -> float:
#     """BERT-based semantic similarity normalized to 0-1"""

#     resume_batch = resume[:1000] if len(resume) > 1000 else resume
#     job_batch = job_desc[:1000] if len(job_desc) > 1000 else job_desc

#     resume_embedding = model.encode(resume_batch)
#     job_embedding = model.encode(job_batch)

#     similarity = util.cos_sim(
#         resume_embedding,
#         job_embedding
#     )[0][0].item()

#     # Convert from [-1,1] to [0,1]
#     similarity = (similarity + 1) / 2

#     return min(max(similarity, 0), 1)

# def calculate_experience(resume: str) -> float:
#     """Extract years of experience"""
#     patterns = [
#         r'(\d+)\s*years?\s*(?:of\s+)?experience',
#         r'(\d+)\s*years?',
#         r'experience[:\-]?\s*(\d+)'
#     ]
#     for pattern in patterns:
#         match = re.search(pattern, resume, re.IGNORECASE)
#         if match:
#             return min(20, float(match.group(1))) / 20  # Normalize 0-20 years
    
#     return 0.3  # Default assumption

# def calculate_degree(resume: str) -> float:
#     """Check for degree keywords"""
#     degree_keywords = ['bachelor', 'master', 'phd', 'bs', 'ms', 'ba', 'ma', 'degree']
#     return 1.0 if any(keyword in resume.lower() for keyword in degree_keywords) else 0.0

# def calculate_certifications(resume: str) -> int:
#     """Count certifications"""
#     cert_keywords = ['certified', 'certification', 'aws certified', 'azure', 'google cloud', 'pmp', 'scrum']
#     certs = sum(1 for keyword in cert_keywords if keyword in resume.lower())
#     return min(certs, 5) / 5

# def calculate_projects(resume: str) -> int:
#     """Count projects"""
#     projects = resume.lower().count('project')
#     return min(projects, 5) / 5

# def generate_improvement_suggestions(missing_skills: List[str], skill_score: float) -> List[str]:
#     """Generate AI-powered suggestions"""
#     suggestions = []
#     if skill_score < 0.6:
#         suggestions.append("Add missing skills to your resume with specific examples")
#     if missing_skills:
#         suggestions.append(f"Include these key skills: {', '.join(missing_skills[:3])}")
#     suggestions.extend([
#         "Quantify achievements with numbers (e.g., 'increased revenue by 30%')",
#         "Use standard section headers: Experience, Education, Skills",
#         "Tailor keywords from the job description",
#         "Add GitHub/portfolio links for technical roles"
#     ])
#     return suggestions[:4]




# # from sentence_transformers import SentenceTransformer, util
# # import numpy as np
# # import re
# # from typing import List, Dict
# # from .models import JobDescription

# # model = SentenceTransformer('all-MiniLM-L6-v2')

# # def calculate_ats_score(resume_text: str, job_desc: JobDescription) -> Dict:
# #     """Calculate ATS score using weighted formula"""
    
# #     # 1. Skill Match (35%)
# #     skills_score = calculate_skill_match(resume_text, job_desc.required_skills)
    
# #     # 2. Semantic Match (30%) - BERT Cosine Similarity
# #     semantic_score = calculate_semantic_match(resume_text, job_desc.description)
    
# #     # 3. Experience (15%)
# #     exp_score = calculate_experience(resume_text)
    
# #     # 4. Degree (10%)
# #     degree_score = calculate_degree(resume_text)
    
# #     # 5. Certifications (5%)
# #     cert_score = calculate_certifications(resume_text)
    
# #     # 6. Projects (5%)
# #     projects_score = calculate_projects(resume_text)
    
# #     # ATS Formula: 0.35S + 0.30M + 0.15E + 0.10D + 0.05C + 0.05P
# #     ats_score = (
# #         0.35 * skills_score +
# #         0.30 * semantic_score +
# #         0.15 * exp_score +
# #         0.10 * degree_score +
# #         0.05 * cert_score +
# #         0.05 * projects_score
# #     )
    
# #     # Normalize to 0-100
# #     ats_score = min(100, max(0, ats_score * 100))
    
# #     missing_skills = [skill for skill in job_desc.required_skills 
# #                      if skill.lower() not in resume_text.lower()]
    
# #     suggestions = generate_improvement_suggestions(missing_skills, skills_score)
    
# #     return {
# #         "ats_score": round(ats_score, 2),
# #         "skill_match": round(skills_score, 2),
# #         "semantic_match": round(semantic_score, 2),
# #         "experience_years": exp_score,
# #         "has_degree": bool(degree_score),
# #         "certifications": cert_score,
# #         "projects_count": projects_score,
# #         "missing_skills": missing_skills,
# #         "improvement_suggestions": suggestions,
# #         "component_scores": {
# #             "S": skills_score, "M": semantic_score, "E": exp_score,
# #             "D": degree_score, "C": cert_score, "P": projects_score
# #         }
# #     }

# # def calculate_skill_match(resume: str, required_skills: List[str]) -> float:
# #     """Calculate skill match percentage"""
# #     resume_lower = resume.lower()
# #     matches = sum(1 for skill in required_skills if skill.lower() in resume_lower)
# #     return min(1.0, matches / max(len(required_skills), 1))

# # def calculate_semantic_match(resume: str, job_desc: str) -> float:
# #     """BERT-based semantic similarity"""
# #     resume_embedding = model.encode(resume)
# #     job_embedding = model.encode(job_desc)
# #     similarity = util.cos_sim(resume_embedding, job_embedding)[0][0].item()
# #     return float(similarity)

# # def calculate_experience(resume: str) -> float:
# #     """Extract years of experience"""
# #     patterns = [
# #         r'(\d+)\s*years??\s*(?:of\s+)?experience',
# #         r'(\d+)\s*years?',
# #         r'experience[:\-]?\s*(\d+)'
# #     ]
# #     for pattern in patterns:
# #         match = re.search(pattern, resume, re.IGNORECASE)
# #         if match:
# #             return min(20, float(match.group(1))) / 20  # Normalize 0-20 years
    
# #     return 0.3  # Default assumption

# # def calculate_degree(resume: str) -> float:
# #     """Check for degree keywords"""
# #     degree_keywords = ['bachelor', 'master', 'phd', 'bs', 'ms', 'ba', 'ma']
# #     return 1.0 if any(keyword in resume.lower() for keyword in degree_keywords) else 0.0

# # def calculate_certifications(resume: str) -> int:
# #     """Count certifications"""
# #     cert_keywords = ['certified', 'certification', 'aws', 'azure', 'google cloud']
# #     return sum(1 for keyword in cert_keywords if keyword in resume.lower())

# # def calculate_projects(resume: str) -> int:
# #     """Count projects"""
# #     return max(0, resume.lower().count('project') + resume.lower().count('portfolio'))

# # def generate_improvement_suggestions(missing_skills: List[str], skill_score: float) -> List[str]:
# #     """Generate AI-powered suggestions"""
# #     suggestions = []
# #     if skill_score < 0.6:
# #         suggestions.append("Add missing skills to your resume with specific examples")
# #     if missing_skills:
# #         suggestions.append(f"Include these key skills: {', '.join(missing_skills[:3])}")
# #     suggestions.extend([
# #         "Quantify achievements with numbers (e.g., 'increased revenue by 30%')",
# #         "Use standard section headers: Experience, Education, Skills",
# #         "Tailor keywords from the job description",
# #         "Add GitHub/portfolio links for technical roles"
# #     ])
# #     return suggestions[:4]

# # from sentence_transformers import SentenceTransformer, util
# # import numpy as np
# # import re
# # from typing import List, Dict
# # from .models import JobDescription

# # # Use a lightweight model
# # model = SentenceTransformer('all-MiniLM-L6-v2')
# from sentence_transformers import SentenceTransformer, util
# import numpy as np
# import re
# from typing import List, Dict
# from .models import JobDescription

# # Lazy Loading Model (Render Memory Friendly)
# _model = None

# def get_model():
#     global _model

#     if _model is None:
#         _model = SentenceTransformer(
#             "all-MiniLM-L6-v2"
#         )

#     return _model

# def calculate_ats_score(resume_text: str, job_desc: JobDescription) -> Dict:
#     """Calculate ATS score using weighted formula"""
    
#     # 1. Skill Match (35%)
#     skills_score = calculate_skill_match(resume_text, job_desc.required_skills)
    
#     # 2. Semantic Match (30%) - BERT Cosine Similarity
#     semantic_score = calculate_semantic_match(resume_text, job_desc.description)
    
#     # 3. Experience (15%)
#     exp_score = calculate_experience(resume_text)
    
#     # 4. Degree (10%)
#     degree_score = calculate_degree(resume_text)
    
#     # 5. Certifications (5%)
#     cert_score = calculate_certifications(resume_text)
    
#     # 6. Projects (5%)
#     projects_score = calculate_projects(resume_text)
    
#     # ATS Formula: 0.35S + 0.30M + 0.15E + 0.10D + 0.05C + 0.05P
#     ats_score = (
#         0.35 * skills_score +
#         0.30 * semantic_score +
#         0.15 * exp_score +
#         0.10 * degree_score +
#         0.05 * cert_score +
#         0.05 * projects_score
#     )
    
#     # Normalize to 0-100
#     ats_score = min(100, max(0, ats_score * 100))
    
#     missing_skills = [skill for skill in job_desc.required_skills 
#                      if skill.lower() not in resume_text.lower()]
#     matched_skills = [

#     skill

#     for skill in job_desc.required_skills

#     if skill.lower()
#     in resume_text.lower()
# ]
#     suggestions = generate_improvement_suggestions(missing_skills, skills_score)
    
#     return {
#         "ats_score": round(ats_score, 2),
#         "skill_match": round(skills_score, 2),
#         "semantic_match": round(semantic_score, 2),
#         "matched_skills": matched_skills,
#         "experience_years": exp_score,
#         "has_degree": bool(degree_score),
#         "certifications": cert_score,
#         "projects_count": projects_score,
#         "missing_skills": missing_skills,
#         "improvement_suggestions": suggestions,
#         "component_scores": {
#             "S": skills_score,
#             "M": semantic_score,
#             "E": exp_score,
#             "D": degree_score,
#             "C": cert_score,
#             "P": projects_score
#         }
#     }

# def calculate_skill_match(resume: str, required_skills: List[str]) -> float:
#     """Calculate skill match percentage"""
#     resume_lower = resume.lower()
#     if not required_skills:
#         return 0.5
#     matches = sum(1 for skill in required_skills if skill.lower() in resume_lower)
#     return min(1.0, matches / max(len(required_skills), 1))

# # def calculate_semantic_match(resume: str, job_desc: str) -> float:
# #     """BERT-based semantic similarity"""
# #     # Truncate long texts for efficiency
# #     resume_batch = resume[:1000] if len(resume) > 1000 else resume
# #     job_batch = job_desc[:1000] if len(job_desc) > 1000 else job_desc
    
# #     resume_embedding = model.encode(resume_batch)
# #     job_embedding = model.encode(job_batch)
# #     similarity = util.cos_sim(resume_embedding, job_embedding)[0][0].item()
# #     return float(similarity)


# def calculate_semantic_match(resume: str, job_desc: str) -> float:
#     """BERT-based semantic similarity"""

#     model = get_model()

#     resume_batch = (
#         resume[:1000]
#         if len(resume) > 1000
#         else resume
#     )

#     job_batch = (
#         job_desc[:1000]
#         if len(job_desc) > 1000
#         else job_desc
#     )

#     resume_embedding = model.encode(
#         resume_batch
#     )

#     job_embedding = model.encode(
#         job_batch
#     )

#     similarity = util.cos_sim(
#         resume_embedding,
#         job_embedding
#     )[0][0].item()

#     return float(similarity)


# def calculate_experience(resume: str) -> float:
#     """Extract years of experience"""
#     patterns = [
#         r'(\d+)\s*years?\s*(?:of\s+)?experience',
#         r'(\d+)\s*years?',
#         r'experience[:\-]?\s*(\d+)'
#     ]
#     for pattern in patterns:
#         match = re.search(pattern, resume, re.IGNORECASE)
#         if match:
#             return min(20, float(match.group(1))) / 20  # Normalize 0-20 years
    
#     return 0.3  # Default assumption

# def calculate_degree(resume: str) -> float:
#     """Check for degree keywords"""
#     degree_keywords = ['bachelor', 'master', 'phd', 'bs', 'ms', 'ba', 'ma', 'degree']
#     return 1.0 if any(keyword in resume.lower() for keyword in degree_keywords) else 0.0

# def calculate_certifications(resume: str) -> int:
#     """Count certifications"""
#     cert_keywords = ['certified', 'certification', 'aws certified', 'azure', 'google cloud', 'pmp', 'scrum']
#     return sum(1 for keyword in cert_keywords if keyword in resume.lower())

# def calculate_projects(resume: str) -> int:
#     """Count projects"""
#     return max(0, resume.lower().count('project'))

# def generate_improvement_suggestions(missing_skills: List[str], skill_score: float) -> List[str]:
#     """Generate AI-powered suggestions"""
#     suggestions = []
#     if skill_score < 0.6:
#         suggestions.append("Add missing skills to your resume with specific examples")
#     if missing_skills:
#         suggestions.append(f"Include these key skills: {', '.join(missing_skills[:3])}")
#     suggestions.extend([
#         "Quantify achievements with numbers (e.g., 'increased revenue by 30%')",
#         "Use standard section headers: Experience, Education, Skills",
#         "Tailor keywords from the job description",
#         "Add GitHub/portfolio links for technical roles"
#     ])
#     return suggestions[:4]
