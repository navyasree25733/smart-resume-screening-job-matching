from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .extraction import extract_resume_text
from .skills import extract_skills
from .llm_skills import extract_skills_llm
from .ats_engine import calculate_ats_score
from .models import JobDescription
from fastapi.responses import FileResponse
# from .llm_skills import recommend_jobs_llm
from .skills import recommend_jobs
# from .auth import router as auth_router
import uvicorn
import os
import shutil
from fastapi import Depends
from sqlalchemy.orm import Session
# from app.ats_engine import recommend_jobs
from .database import (
    User,
    Candidate,
    get_db,
    create_user,
    get_user_by_email,
    get_user_by_username,
    verify_password,
    ResumeHistory,
    save_resume_history,
    save_candidate,
    get_recent_history,
    get_dashboard_stats
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from fastapi.responses import FileResponse

from openpyxl import Workbook


app = FastAPI(title="AI Resume Screening Platform")
UPLOAD_DIR = "app/uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

PROFILE_DIR = "app/static/profile_photos"

app.mount(
    "/profile_photos",
    StaticFiles(
        directory="app/static/profile_photos"
    ),
    name="profile_photos"
)

os.makedirs(
    PROFILE_DIR,
    exist_ok=True
)

from .database import Base, engine

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

class SignupRequest(BaseModel):
    email: str
    username: str
    password: str
    full_name: str | None = None
    is_employer: bool = False

class LoginRequest(BaseModel):
    email: str
    password: str


@app.get("/health")
async def health():
    return {"status": "healthy"}

#-----------------------------------
# Home 
#-----------------------------------
@app.get("/")
def home():
    return FileResponse("app/static/home.html")

#-----------------------------------
# Signup
#-----------------------------------
@app.get("/signup")
def signup_page():
    return FileResponse("app/static/signup.html")
@app.post("/api/signup")
def signup(
    user: SignupRequest,
    db: Session = Depends(get_db)
):

    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = create_user(
        db=db,
        email=user.email,
        username=user.username,
        password=user.password,
        full_name=user.full_name,
        is_employer=user.is_employer
    )

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }

#-----------------------------------
# Login
#-----------------------------------
@app.get("/login")
def login_page():
    return FileResponse("app/static/login.html")
@app.post("/api/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):

    db_user = get_user_by_email(
        db,
        user.email
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    return {
    "id": db_user.id,
    "email": db_user.email,
    "username": db_user.username,
    "full_name": db_user.full_name,
    "is_employer": db_user.is_employer,
    "dashboard": (
        "/hr-dashboard"
        if db_user.is_employer
        else "/candidate-dashboard"
    )
}


#-----------------------------------
# Consumer Dashboard
#-----------------------------------
@app.get("/candidate-dashboard")
def candidate_dashboard():
    return FileResponse(
        "app/static/consumer/C-D.html"
    )

@app.get("/candidate-results")
def candidate_results():
    return FileResponse(
        "app/static/consumer/C-R.html"
    )

@app.get("/api/user-dashboard/{user_id}")
def user_dashboard(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    stats = get_dashboard_stats(
        db,
        user_id
    )

    recent = get_recent_history(
        db,
        user_id
    )

    return {

        "id": user.id,
        "name": user.full_name,
        "email": user.email,

        "total_scans":
            stats["total_scans"],

        "accuracy":
            stats["accuracy"],

        "recommendation":
            stats["recommendation"],

        "recent_scans": [

            {
                "job_title":
                    r.job_title,

                "ats_score":
                    r.ats_score,

                "semantic_score":
                    r.semantic_score,

                "date":
                    r.created_at.strftime(
                        "%d-%m-%Y"
                    )
            }

            for r in recent
        ]
    }

#-----------------------------------
# Hr Dashboard
#-----------------------------------
@app.get("/hr-dashboard")
def hr_dashboard_page():
    return FileResponse(
        "app/static/hr/H-D.html"
    )

@app.get("/dashboard")
def dashboard_redirect():
    return {
        "message":
        "Redirect handled after login"
    }
# @app.get("/api/hr-dashboard/{user_id}")
# def hr_dashboard(
#     user_id: int,
#     db: Session = Depends(get_db)
# ):

#     history = (
#         db.query(ResumeHistory)
#         .order_by(
#             ResumeHistory.created_at.desc()
#         )
#         .all()
#     )

#     total_candidates = len(history)

#     avg_accuracy = (
#         sum(
#             h.semantic_score or 0
#             for h in history
#         ) / total_candidates
#         if total_candidates > 0
#         else 0
#     )

#     shortlisted = len([
#         h for h in history
#         if (h.ats_score or 0) >= 80
#     ])
#     print("Total Records:", total_candidates)

#     return {

#         "total_candidates":
#             total_candidates,

#         "avg_accuracy":
#             round(avg_accuracy, 2),

#         "shortlisted":
#             shortlisted,

#         "candidates": [

#             {
#                 "name":
#                     h.file_name,

#                 "role":
#                     h.job_title,

#                 "ats_score":
#                     h.ats_score,

#                 "match":
#                     h.semantic_score
#             }

#             for h in history[:3]
#         ]
#     }

@app.get("/api/hr-dashboard/{user_id}")
def hr_dashboard(
    user_id: int,
    db: Session = Depends(get_db)
):

    # Only fetch candidates screened by this HR
    candidates = (
        db.query(Candidate)
        .filter(
            Candidate.hr_id == user_id
        )
        .order_by(
            Candidate.created_at.desc()
        )
        .all()
    )

    total_candidates = len(candidates)

    avg_accuracy = (
        sum(
            c.semantic_score or 0
            for c in candidates
        ) / total_candidates
        if total_candidates > 0
        else 0
    )

    shortlisted = len([
        c for c in candidates
        if (c.ats_score or 0) >= 80
    ])

    return {

        "total_candidates":
            total_candidates,

        "avg_accuracy":
            round(avg_accuracy, 2),

        "shortlisted":
            shortlisted,

        "candidates": [

            {
                "id":
                    c.id,

                "name":
                    c.candidate_name,

                "role":
                    c.job_title,

                "ats_score":
                    c.ats_score,

                "match":
                    c.semantic_score,

                "recommendation":
                    c.recommendation,

                "date":
                    c.created_at.strftime(
                        "%d-%m-%Y"
                    )
            }

            for c in candidates[:10]
        ]
    }

@app.get("/api/hr-history/{user_id}")
def hr_history(
    user_id: int,
    db: Session = Depends(get_db)
):

    candidates = (
        db.query(Candidate)
        .filter(
            Candidate.hr_id == user_id
        )
        .order_by(
            Candidate.created_at.desc()
        )
        .all()
    )

    return [

        {
            "id": c.id,
            "candidate_name": c.candidate_name,
            "job_title": c.job_title,
            "ats_score": c.ats_score,
            "semantic_score": c.semantic_score,
            "recommendation": c.recommendation,
            "date": c.created_at.strftime(
                "%d-%m-%Y"
            )
        }

        for c in candidates

    ]

#-----------------------------------
# Consumer Resume Screening(Job seeker)
#-----------------------------------
# @app.post("/api/screen-resume")
# async def screen_resume(
#     resume: UploadFile = File(...),
#     job_title: str = Form(...),
#     job_description: str = Form(...),
#     user_id: int = Form(...),
#     db: Session = Depends(get_db)
# ):

#     if not resume.filename.endswith((".pdf", ".docx")):
#         raise HTTPException(
#             status_code=400,
#             detail="Only PDF and DOCX files allowed"
#         )

#     print("Processing:", resume.filename)

#     # STEP 1: Extract text FIRST
#     resume_text = await extract_resume_text(resume)

#     print("Extracted Length:", len(resume_text))

#     if not resume_text or len(resume_text.strip()) < 20:
#         raise HTTPException(
#             status_code=400,
#             detail="Could not extract text from resume"
#         )

#     # STEP 2: Reset file pointer
#     await resume.seek(0)

#     # STEP 3: Save uploaded file
#     file_path = os.path.join(
#         UPLOAD_DIR,
#         resume.filename
#     )

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(
#             resume.file,
#             buffer
#         )

#     # STEP 4: Extract skills
#     skills_data = extract_skills(resume_text)
#     llm_data = extract_skills_llm(resume_text)

#     skills_data["llm_analysis"] = llm_data
#     skills_data["all_skills"] = list(set(skills_data.get("extracted_skills",[])+llm_data.get("technical_skills",[])+llm_data.get("tools",[])+llm_data.get("frameworks",[])))


#     # STEP 5: Create Job Description
#     job_desc = JobDescription(
#         job_title=job_title,
#         description=job_description,
#         required_skills=skills_data.get(
#             "all_skills",
#             []
#         )
#     )

#     # STEP 6: Calculate ATS Score
#     ats_result = calculate_ats_score(
#         resume_text,
#         job_desc
#     )
    

#     # STEP 7: Save History
#     save_resume_history(
#         db=db,
#         user_id=user_id,
#         job_title=job_title,
#         file_name=resume.filename,
#         file_path=file_path,

#         ats_score=ats_result.get(
#             "ats_score",
#             0
#         ),
#         semantic_score=ats_result.get(
#             "semantic_match",
#             0
#         ),
#         recommendation=str(
#             ats_result.get(
#                 "recommendation",
#                 "Resume looks good"
#             )
#         )
#     )

#     # STEP 8: Return Result
#     return {
#         "resume_text": (
#             resume_text[:500] + "..."
#             if len(resume_text) > 500
#             else resume_text
#         ),
#         "skills": skills_data,
#         **ats_result
#     }

@app.post("/api/screen-resume")
async def screen_resume(
    resume: UploadFile = File(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):

    # ==========================
    # FILE VALIDATION
    # ==========================

    if not resume.filename.endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files allowed"
        )

    print("Processing:", resume.filename)

    # ==========================
    # EXTRACT RESUME TEXT
    # ==========================

    resume_text = await extract_resume_text(
        resume
    )

    print(
        "Extracted Length:",
        len(resume_text)
    )

    if (
        not resume_text
        or
        len(resume_text.strip()) < 20
    ):
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from resume"
        )

    # ==========================
    # RESET FILE POINTER
    # ==========================

    await resume.seek(0)

    # ==========================
    # SAVE FILE
    # ==========================

    file_path = os.path.join(
        UPLOAD_DIR,
        resume.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            resume.file,
            buffer
        )

    # ==========================
    # SKILL EXTRACTION
    # ==========================

    skills_data = extract_skills(
        resume_text
    )

    llm_data = extract_skills_llm(
        resume_text
    )

    skills_data["llm_analysis"] = llm_data

    skills_data["all_skills"] = list(
        set(
            skills_data.get(
                "extracted_skills",
                []
            )
            +
            llm_data.get(
                "technical_skills",
                []
            )
            +
            llm_data.get(
                "tools",
                []
            )
            +
            llm_data.get(
                "frameworks",
                []
            )
        )
    )

    # ==========================
    # JOB RECOMMENDATIONS
    # ==========================

    recommended_jobs = recommend_jobs(
        skills_data["all_skills"]
    )

    # ==========================
    # JOB DESCRIPTION
    # ==========================

    job_required_skills = extract_skills(
        job_description
    )

    job_desc = JobDescription(
        job_title=job_title,
        description=job_description,
        required_skills=
        job_required_skills.get(
            "extracted_skills",
            []
        )
    )

    # ==========================
    # ATS SCORE
    # ==========================

    ats_result = calculate_ats_score(
        resume_text,
        job_desc
    )

    # ==========================
    # SAVE HISTORY
    # ==========================

    # save_resume_history(
    #     db=db,
    #     user_id=user_id,
    #     job_title=job_title,
    #     file_name=resume.filename,
    #     file_path=file_path,
    #     ats_score=float(
    #         ats_result.get(
    #             "ats_score",
    #             0
    #         )
    #     ),
    #     semantic_score=float(
    #         ats_result.get(
    #             "semantic_match",
    #             0
    #         )
    #     ),
    #     recommendation=str(
    #         ats_result.get(
    #             "recommendation",
    #             "Resume looks good"
    #         )
    #     )
    # )
    # 
    save_resume_history(

    db=db,

    user_id=user_id,

    job_title=job_title,

    file_name=resume.filename,

    file_path=file_path,

    ats_score=float(
        ats_result.get(
            "ats_score",
            0
        )
    ),

    semantic_score=float(
        ats_result.get(
            "semantic_match",
            0
        )
    ),

    recommendation=str(
        ats_result.get(
            "recommendation",
            "Resume looks good"
        )
    ),

    report_data=json.dumps({

        "skills": skills_data,

        "ats_result": ats_result,

        "recommended_jobs": recommended_jobs

    })

)

    # ==========================
    # RETURN RESPONSE
    # ==========================

    return {

        "resume_text":
        (
            resume_text[:500] + "..."
            if len(resume_text) > 500
            else resume_text
        ),

        "skills":
        skills_data,

        "recommended_jobs":
        recommended_jobs,

        "ats_score":
        float(
            ats_result.get(
                "ats_score",
                0
            )
        ),
        "skill_match":
        float(
            ats_result.get(
                "skill_match",
                0
            )
        ),

        "semantic_match":
        float(
            ats_result.get(
                "semantic_match",
                0
            )
        ),

        "matched_skills":
        ats_result.get(
            "matched_skills",
            []
        ),

        "missing_skills":
        ats_result.get(
            "missing_skills",
            []
        ),
        "improvement_suggestions":
    ats_result.get(
        "improvement_suggestions",
        []
    ),

    "component_scores":
    ats_result.get(
        "component_scores",
        {}
    ),

        "recommendation":
        str(
            ats_result.get(
                "recommendation",
                ""
            )
        )
    }












#-----------------------------------
# HR Resume Screening
#-----------------------------------
# @app.post("/api/bulk-screen")
# async def bulk_screen_resumes(

#     resumes: list[UploadFile] = File(...),

#     job_title: str = Form(
#         "Software Engineer"
#     ),

#     job_description: str = Form(
#         "Looking for Python, JavaScript, React developers"
#     ),

#     user_id: int = Form(...),

#     db: Session = Depends(get_db)

# ):

#     # ==========================
#     # LIMIT CHECK
#     # ==========================

#     if len(resumes) > 50:

#         raise HTTPException(

#             status_code=400,

#             detail=
#             "Maximum 50 resumes allowed"
#         )

#     results = []

#     # ==========================
#     # REQUIRED SKILLS
#     # ==========================

#     required_skills = []

#     tech_keywords = [

#         "python",
#         "javascript",
#         "java",
#         "react",
#         "angular",
#         "vue",
#         "node",
#         "docker",
#         "aws",
#         "azure",
#         "gcp",
#         "sql",
#         "mongodb",
#         "postgresql",
#         "mysql",
#         "redis",
#         "golang",
#         "rust",
#         "typescript",
#         "kubernetes"
#     ]

#     job_lower = job_description.lower()

#     for keyword in tech_keywords:

#         if keyword in job_lower:

#             required_skills.append(
#                 keyword.capitalize()
#             )

#     job_desc = JobDescription(

#         job_title=job_title,

#         description=job_description,

#         required_skills=
#         required_skills
#         if required_skills
#         else [
#             "Python",
#             "JavaScript"
#         ]
#     )

#     # ==========================
#     # PROCESS RESUMES
#     # ==========================

#     for resume in resumes:

#         try:

#             print(
#                 "Processing:",
#                 resume.filename
#             )

#             # ----------------------
#             # FILE TYPE VALIDATION
#             # ----------------------

#             if not resume.filename.lower().endswith(
#                 (".pdf", ".docx")
#             ):
#                 continue

#             # ----------------------
#             # EXTRACT TEXT
#             # ----------------------

#             resume_text = (
#                 await extract_resume_text(
#                     resume
#                 )
#             )

#             if (

#                 not resume_text

#                 or

#                 len(
#                     resume_text.strip()
#                 ) < 20

#             ):
#                 print(
#                     f"Skipping "
#                     f"{resume.filename}"
#                 )

#                 continue

#             # ----------------------
#             # RESET POINTER
#             # ----------------------

#             await resume.seek(0)

#             # ----------------------
#             # SAVE FILE
#             # ----------------------

#             file_path = os.path.join(

#                 UPLOAD_DIR,

#                 resume.filename

#             )

#             with open(
#                 file_path,
#                 "wb"
#             ) as buffer:

#                 shutil.copyfileobj(

#                     resume.file,

#                     buffer

#                 )

#             # ----------------------
#             # EXTRACT SKILLS
#             # ----------------------

#             skills_data = extract_skills(resume_text)
#             llm_data = extract_skills_llm(resume_text)
#             skills_data["llm_analysis"] = llm_data
#             skills_data["all_skills"] = list(set(skills_data.get("extracted_skills",[])+llm_data.get("technical_skills",[])+llm_data.get("tools",[])+llm_data.get("frameworks",[])))

#             # ----------------------
#             # ATS SCORE
#             # ----------------------

#             ats_result = (
#                 calculate_ats_score(

#                     resume_text,

#                     job_desc
#                 )
#             )

#             # ----------------------
#             # SAVE HISTORY
#             # ----------------------

#             save_resume_history(

#                 db=db,

#                 user_id=user_id,

#                 job_title=job_title,

#                 file_name=
#                 resume.filename,

#                 file_path=
#                 file_path,

#                 ats_score=
#                 ats_result.get(
#                     "ats_score",
#                     0
#                 ),

#                 semantic_score=
#                 ats_result.get(
#                     "semantic_match",
#                     0
#                 ),

#                 recommendation=
#                 "Bulk Screening"
#             )

#             # ----------------------
#             # SAVE CANDIDATE
#             # ----------------------

#             save_candidate(

#                 db=db,

#                 hr_id=user_id,

#                 candidate_name=

#                 resume.filename

#                 .replace(
#                     ".pdf",
#                     ""
#                 )

#                 .replace(
#                     ".docx",
#                     ""
#                 ),

#                 resume_file=
#                 file_path,

#                 job_title=
#                 job_title,

#                 ats_score=

#                 ats_result.get(
#                     "ats_score",
#                     0
#                 ),

#                 semantic_score=

#                 ats_result.get(
#                     "semantic_match",
#                     0
#                 ),

#                 recommendation=

#                 ats_result.get(
#                     "recommendation",
#                     "Review Candidate"
#                 )
#             )

#             # ----------------------
#             # RESPONSE LIST
#             # ----------------------

#             results.append({

#                 "filename":
#                 resume.filename,

#                 "skills":
#                 skills_data,

#                 **ats_result

#             })

#         except Exception as e:

#             print(

#                 f"Error processing "

#                 f"{resume.filename}: "

#                 f"{e}"

#             )

#             continue

#     # ==========================
#     # SORT BY ATS
#     # ==========================

#     results.sort(

#         key=lambda x:

#         x.get(
#             "ats_score",
#             0
#         ),

#         reverse=True
#     )

#     # ==========================
#     # RETURN
#     # ==========================

#     return {

#         "total_uploaded":
#         len(results),

#         "job_title":
#         job_title,

#         "candidates":
#         results
#     }


@app.post("/api/bulk-screen")
async def bulk_screen_resumes(
    resumes: list[UploadFile] = File(...),
    job_title: str = Form("Software Engineer"),
    job_description: str = Form(
        "Looking for Python, JavaScript, React developers"
    ),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):

    if len(resumes) > 50:
        raise HTTPException(
            status_code=400,
            detail="Maximum 50 resumes allowed"
        )

    results = []

    # ------------------------
    # Extract required skills
    # ------------------------

    required_skills = []

    tech_keywords = [
        "python",
        "javascript",
        "java",
        "react",
        "angular",
        "vue",
        "node",
        "docker",
        "aws",
        "azure",
        "gcp",
        "sql",
        "mongodb",
        "postgresql",
        "mysql",
        "redis",
        "golang",
        "rust",
        "typescript",
        "kubernetes"
    ]

    job_lower = job_description.lower()

    for keyword in tech_keywords:
        if keyword in job_lower:
            required_skills.append(
                keyword.capitalize()
            )

    job_desc = JobDescription(
        job_title=job_title,
        description=job_description,
        required_skills=required_skills
        if required_skills
        else ["Python", "JavaScript"]
    )

    # ------------------------
    # Process Resumes
    # ------------------------

    for resume in resumes:

        try:

            print(
                f"Processing {resume.filename}"
            )

            if not resume.filename.lower().endswith(
                (".pdf", ".docx")
            ):
                print(
                    f"Skipping unsupported file: {resume.filename}"
                )
                continue

            # --------------------
            # Extract Resume Text
            # --------------------

            resume_text = await extract_resume_text(
                resume
            )

            if (
                not resume_text
                or len(
                    resume_text.strip()
                ) < 20
            ):
                print(
                    f"Empty Resume: {resume.filename}"
                )
                continue

            await resume.seek(0)

            # --------------------
            # Save File
            # --------------------

            file_path = os.path.join(
                UPLOAD_DIR,
                resume.filename
            )

            with open(
                file_path,
                "wb"
            ) as buffer:

                shutil.copyfileobj(
                    resume.file,
                    buffer
                )

            # --------------------
            # Skill Extraction
            # --------------------

            skills_data = extract_skills(
                resume_text
            )

            skills_data["all_skills"] = (
                skills_data.get(
                    "extracted_skills",
                    []
                )
            )

            # --------------------
            # ATS Scoring
            # --------------------

            ats_result = calculate_ats_score(
                resume_text,
                job_desc
            )

            candidate_data = {
                "filename": resume.filename,
                "resume_text": resume_text,
                "skills": skills_data,
                **ats_result
            }

            results.append(
                candidate_data
            )

            # --------------------
            # Save History
            # --------------------

            save_resume_history(
                db=db,
                user_id=user_id,
                job_title=job_title,
                file_name=resume.filename,
                file_path=file_path,
                ats_score=ats_result.get(
                    "ats_score",
                    0
                ),
                semantic_score=ats_result.get(
                    "semantic_match",
                    0
                ),
                recommendation="Bulk Screening"
            )

            # --------------------
            # Save Candidate
            # --------------------

            save_candidate(
                db=db,
                hr_id=user_id,
                candidate_name=os.path.splitext(
                    resume.filename
                )[0],
                resume_file=file_path,
                job_title=job_title,
                ats_score=ats_result.get(
                    "ats_score",
                    0
                ),
                semantic_score=ats_result.get(
                    "semantic_match",
                    0
                ),
                recommendation=ats_result.get(
                    "recommendation",
                    "Review Candidate"
                )
            )

        except Exception as e:

            print(
                f"Error processing "
                f"{resume.filename}: {e}"
            )

            continue

    # ------------------------
    # Sort Candidates
    # ------------------------

    results.sort(
        key=lambda x: x.get(
            "ats_score",
            0
        ),
        reverse=True
    )

    # ------------------------
    # LLM Analysis
    # ------------------------

    TOP_N = 5

    top_candidates = results[
        :min(
            TOP_N,
            len(results)
        )
    ]

    for candidate in top_candidates:

        try:

            llm_data = extract_skills_llm(
                candidate["resume_text"]
            )

            candidate[
                "llm_analysis"
            ] = llm_data

        except Exception as e:

            print(
                "LLM Error:",
                e
            )

            candidate[
                "llm_analysis"
            ] = {}

    # ------------------------
    # Cleanup
    # ------------------------

    for candidate in results:

        candidate.pop(
            "resume_text",
            None
        )

    return {
        "success": True,
        "job_title": job_title,
        "total_uploaded": len(resumes),
        "total_processed": len(results),
        "top_candidates": top_candidates,
        "candidates": results
    }



@app.get("/H-C")
def hr_candidates_page():

    return FileResponse(
        "app/static/hr/H-C.html"
    )

@app.get("/api/candidates/{hr_id}")
def get_candidates(
    hr_id: int,
    db: Session = Depends(get_db)
):

    candidates = (
        db.query(Candidate)
        .filter(
            Candidate.hr_id == hr_id
        )
        .order_by(
            Candidate.created_at.desc()
        )
        .all()
    )

    return [

        {
            "id": c.id,
            "name": c.candidate_name,
            "role": c.job_title,
            "ats_score": c.ats_score,
            "semantic_score": c.semantic_score,
            "recommendation": c.recommendation,
            "date": c.created_at.strftime("%d-%m-%Y")
        }

        for c in candidates

    ]





#-----------------------------------
# HR Profile
#-----------------------------------
@app.get("/H-P")
def hr_profile_page():
    return FileResponse(
        "app/static/hr/H-P.html"
    )


@app.get("/api/hr-profile/{user_id}")
def get_hr_profile(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {

        "id": user.id,

        "username": user.username,

        "full_name": user.full_name,

        "email": user.email,

        "phone": user.phone,

        "profile_photo": user.profile_photo
    }


from pydantic import BaseModel

class HRProfileUpdate(BaseModel):

    full_name: str

    email: str

    phone: str


@app.put("/api/hr-profile/{user_id}")
def update_hr_profile(
    user_id: int,
    data: HRProfileUpdate,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.full_name = data.full_name

    user.email = data.email

    user.phone = data.phone

    db.commit()

    return {
        "message":
        "Profile Updated"
    }

@app.post(
    "/api/hr-profile-photo/{user_id}"
)
async def upload_hr_photo(

    user_id: int,

    photo: UploadFile = File(...),

    db: Session = Depends(get_db)

):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    filename = (
        f"{user_id}_{photo.filename}"
    )

    file_path = os.path.join(
        PROFILE_DIR,
        filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            photo.file,
            buffer
        )

    user.profile_photo = (
    f"/profile_photos/{filename}"
)

    db.commit()

    return {
        "message":
        "Photo Uploaded"
    }


#-----------------------------------
# History of Consumer
#-----------------------------------

@app.get("/api/history/{user_id}")
def get_history(
    user_id: int,
    db: Session = Depends(get_db)
):

    history = (
        db.query(ResumeHistory)
        .filter(
            ResumeHistory.user_id == user_id
        )
        .order_by(
            ResumeHistory.created_at.desc()
        )
        .limit(10)
        .all()
    )

    return [
        {
            "id": item.id,
            "role": item.job_title,
            "file_name": item.file_name,
            "ats_score": item.ats_score,
            "semantic_score": item.semantic_score,
            "recommendation": item.recommendation,
            "scan_date": item.created_at.strftime("%d-%m-%Y")
        }
        for item in history
    ]

#-----------------------------------
# consumer dashboard
#-----------------------------------

@app.get("/C-D")
async def consumer_dashboard():
    return FileResponse(
        "app/static/consumer/C-D.html"
    )

@app.get("/C-H")
async def consumer_history():
    return FileResponse(
        "app/static/consumer/C-H.html"
    )

#-----------------------------------
# consumer dashboard Profile
#-----------------------------------
@app.get("/C-P")
async def consumer_profile():
    return FileResponse(
        "app/static/consumer/C-P.html"
    )

@app.post("/api/update-profile")
async def update_profile(
    user_id: int = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    photo: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.full_name = full_name
    user.email = email
    user.phone = phone

    if photo:

        filename = (
            f"user_{user.id}_{photo.filename}"
        )

        file_path = os.path.join(
            PROFILE_DIR,
            filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                photo.file,
                buffer
            )

        user.profile_photo = (
            f"/static/profile_photos/{filename}"
        )

    db.commit()
    db.refresh(user)

    return {
        "message": "Profile Updated",
        "user": {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "profile_photo": user.profile_photo
        }
    }

#-----------------------------------
# consumer dashboard exports
#-----------------------------------
# @app.get("/export-report/{history_id}")
# def export_report(
#     history_id: int,
#     db: Session = Depends(get_db)
# ):

#     history = (
#         db.query(ResumeHistory)
#         .filter(
#             ResumeHistory.id == history_id
#         )
#         .first()
#     )

#     if not history:

#         raise HTTPException(
#             status_code=404,
#             detail="Report not found"
#         )

#     pdf_path = (
#         f"ATS_Report_{history.id}.pdf"
#     )

#     doc = SimpleDocTemplate(
#         pdf_path
#     )

#     styles = (
#         getSampleStyleSheet()
#     )

#     content = [

#         Paragraph(
#             "ATS Resume Analysis Report",
#             styles["Title"]
#         ),

#         Spacer(1, 20),

#         Paragraph(
#             f"<b>Resume File:</b> {history.file_name}",
#             styles["Normal"]
#         ),

#         Paragraph(
#             f"<b>Job Role:</b> {history.job_title}",
#             styles["Normal"]
#         ),

#         Paragraph(
#             f"<b>ATS Score:</b> {history.ats_score:.2f}%",
#             styles["Normal"]
#         ),

#         Paragraph(
#             f"<b>Semantic Match:</b> {history.semantic_score:.2f}%",
#             styles["Normal"]
#         ),

#         Paragraph(
#             f"<b>Recommendation:</b> {history.recommendation}",
#             styles["Normal"]
#         ),

#         Paragraph(
#             f"<b>Scan Date:</b> {history.created_at.strftime('%d-%m-%Y %H:%M')}",
#             styles["Normal"]
#         ),

#         Spacer(1, 20),

#         Paragraph(
#             "Generated by JobAI Resume Intelligence Platform",
#             styles["Italic"]
#         )
#     ]

#     doc.build(content)

#     return FileResponse(
#         pdf_path,
#         filename=pdf_path,
#         media_type="application/pdf"
#     )

# @app.get("/export-excel/{history_id}")
# def export_excel(
#     history_id: int,
#     db: Session = Depends(get_db)
# ):

#     history = (
#         db.query(ResumeHistory)
#         .filter(
#             ResumeHistory.id == history_id
#         )
#         .first()
#     )

#     if not history:

#         raise HTTPException(
#             status_code=404,
#             detail="Report not found"
#         )

#     wb = Workbook()
#     ws = wb.active

#     ws.title = "ATS Report"

#     ws.append(["Field", "Value"])

#     ws.append(["Resume File", history.file_name])
#     ws.append(["Job Role", history.job_title])
#     ws.append(["ATS Score", history.ats_score])
#     ws.append(["Semantic Match", history.semantic_score])
#     ws.append(["Recommendation", history.recommendation])
#     ws.append([
#         "Scan Date",
#         history.created_at.strftime(
#             "%d-%m-%Y %H:%M"
#         )
#     ])

#     file_path = (
#         f"ATS_Report_{history.id}.xlsx"
#     )

#     wb.save(file_path)

#     return FileResponse(
#         file_path,
#         filename=file_path,
#         media_type=
#         "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )


@app.get("/api/export-report/{report_id}")
def export_report(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = (
        db.query(ResumeHistory)
        .filter(
            ResumeHistory.id == report_id
        )
        .first()
    )

    if not report:

        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    data = json.loads(
        report.report_data
    )

    ats = data.get(
        "ats_result",
        {}
    )

    skills = data.get(
        "skills",
        {}
    )

    jobs = data.get(
        "recommended_jobs",
        []
    )

    filename = (
        f"ATS_Report_{report_id}.txt"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
f"""
==================================================
          ATS RESUME SCREENING REPORT
==================================================

Resume File:
{report.file_name}

Job Role:
{report.job_title}

Generated On:
{report.created_at}

==================================================
OVERALL SCORES
==================================================

ATS Score:
{ats.get('ats_score',0)}%

Skill Match:
{round(ats.get('skill_match',0)*100)}%

Semantic Match:
{round(ats.get('semantic_match',0)*100)}%

==================================================
MATCHED SKILLS
==================================================

{chr(10).join(ats.get('matched_skills',[]))}

==================================================
MISSING SKILLS
==================================================

{chr(10).join(ats.get('missing_skills',[]))}

==================================================
EXTRACTED SKILLS
==================================================

{chr(10).join(skills.get('extracted_skills',[]))}

==================================================
RECOMMENDED JOBS
==================================================

{chr(10).join(jobs)}

==================================================
IMPROVEMENT SUGGESTIONS
==================================================

{chr(10).join(ats.get('improvement_suggestions',[]))}

==================================================
END OF REPORT
==================================================
"""
        )

    return FileResponse(
        filename,
        filename=filename,
        media_type="text/plain"
    )


import json

@app.get("/api/report/{history_id}")
def get_report(
    history_id: int,
    db: Session = Depends(get_db)
):

    report = (
        db.query(ResumeHistory)
        .filter(
            ResumeHistory.id == history_id
        )
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    if not report.report_data:
        raise HTTPException(
            status_code=404,
            detail="No report data stored"
        )
    
    print(report.report_data)

    return json.loads(
        report.report_data
    )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

























