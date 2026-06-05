# from pydantic import BaseModel
# from typing import List, Dict, Any
# from datetime import datetime

# class SkillsData(BaseModel):
#     extracted_skills: List[str]
#     skill_categories: Dict[str, List[str]]
#     common_skills: List[str]
#     rare_skills: List[str]

# class ATSResult(BaseModel):
#     ats_score: float
#     skill_match: float
#     semantic_match: float
#     experience_years: float
#     has_degree: bool
#     certifications: int
#     projects_count: int
#     missing_skills: List[str]
#     improvement_suggestions: List[str]
#     component_scores: Dict[str, float]

from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class JobDescription(BaseModel):
    job_title: str
    description: str
    required_skills: List[str]

class SkillsData(BaseModel):
    extracted_skills: List[str]
    skill_categories: Dict[str, List[str]]
    common_skills: List[str]
    rare_skills: List[str]

class ATSResult(BaseModel):
    ats_score: float
    skill_match: float
    semantic_match: float
    experience_years: float
    has_degree: bool
    certifications: int
    projects_count: int
    missing_skills: List[str]
    improvement_suggestions: List[str]
    component_scores: Dict[str, float]


