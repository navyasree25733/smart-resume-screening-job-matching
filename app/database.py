# # from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Float
# # from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy.orm import sessionmaker
# # from datetime import datetime
# # import os

# # # Database configuration
# # DATABASE_URL = "sqlite:///./resume_screening.db"

# # engine = create_engine(
# #     DATABASE_URL,
# #     connect_args={"check_same_thread": False}
# # )

# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base = declarative_base()

# # class User(Base):
# #     __tablename__ = "users"
    
# #     id = Column(Integer, primary_key=True, index=True)
# #     email = Column(String, unique=True, index=True, nullable=False)
# #     username = Column(String, unique=True, index=True, nullable=False)
# #     hashed_password = Column(String, nullable=False)

# #     full_name = Column(String, nullable=True)
# #     phone = Column(String, nullable=True) 
# #     profile_photo = Column(String, nullable=True)
# #     is_active = Column(Boolean, default=True)
# #     is_employer = Column(Boolean, default=False)  # False = candidate, True = employer
# #     created_at = Column(DateTime, default=datetime.utcnow)

# # class ResumeHistory(Base):
# #     __tablename__ = "resume_history"

# #     id = Column(
# #         Integer,
# #         primary_key=True,
# #         index=True
# #     )

# #     user_id = Column(
# #         Integer,
# #         ForeignKey("users.id"),
# #         nullable=False
# #     )

# #     job_title = Column(String)

# #     file_name = Column(String)

# #     file_path = Column(String)

# #     ats_score = Column(Float)

# #     semantic_score = Column(Float)

# #     recommendation = Column(String)

# #     created_at = Column(
# #         DateTime,
# #         default=datetime.utcnow
# #     )

# # # Create tables
# # Base.metadata.create_all(bind=engine)

# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()

# # def get_user_by_email(db, email: str):
# #     return db.query(User).filter(User.email == email).first()

# # def get_user_by_username(db, username: str):
# #     return db.query(User).filter(User.username == username).first()

# # def create_user(db, email: str, username: str, password: str, full_name: str = None, is_employer: bool = False):
# #     from passlib.context import CryptContext
# #     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# #     hashed_password = pwd_context.hash(password)
    
# #     db_user = User(
# #         email=email,
# #         username=username,
# #         hashed_password=hashed_password,
# #         full_name=full_name,
# #         is_employer=is_employer
# #     )
# #     db.add(db_user)
# #     db.commit()
# #     db.refresh(db_user)
# #     return db_user

# # def verify_password(plain_password, hashed_password):
# #     from passlib.context import CryptContext
# #     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# #     return pwd_context.verify(plain_password, hashed_password)

# # def save_resume_history(
# #     db,
# #     user_id,
# #     job_title,
# #     file_name,
# #     file_path,
# #     ats_score,
# #     semantic_score,
# #     recommendation
# # ):

# #     history = ResumeHistory(
# #         user_id=user_id,
# #         job_title=job_title,
# #         file_name=file_name,
# #         file_path=file_path,
# #         ats_score=ats_score,
# #         semantic_score=semantic_score,
# #         recommendation=recommendation
# #     )

# #     db.add(history)
# #     db.commit()
# #     db.refresh(history)

# #     return history

# # def get_user_history(
# #     db,
# #     user_id
# # ):

# #     return (
# #         db.query(ResumeHistory)
# #         .filter(
# #             ResumeHistory.user_id == user_id
# #         )
# #         .order_by(
# #             ResumeHistory.created_at.desc()
# #         )
# #         .all()
# #     )

# # def get_recent_history(
# #     db,
# #     user_id,
# #     limit=3
# # ):

# #     return (
# #         db.query(ResumeHistory)
# #         .filter(
# #             ResumeHistory.user_id == user_id
# #         )
# #         .order_by(
# #             ResumeHistory.created_at.desc()
# #         )
# #         .limit(limit)
# #         .all()
# #     )

# # def get_dashboard_stats(
# #     db,
# #     user_id
# # ):

# #     history = (
# #         db.query(ResumeHistory)
# #         .filter(
# #             ResumeHistory.user_id == user_id
# #         )
# #         .all()
# #     )

# #     total_scans = len(history)

# #     avg_accuracy = (
# #         sum(
# #             h.semantic_score or 0
# #             for h in history
# #         ) / total_scans
# #         if total_scans > 0
# #         else 0
# #     )

# #     latest_recommendation = (
# #         history[-1].recommendation
# #         if history
# #         else "No recommendations available"
# #     )

# #     return {
# #         "total_scans": total_scans,
# #         "accuracy": round(avg_accuracy, 2),
# #         "recommendation":
# #             latest_recommendation
# #     }


# from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Float
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from datetime import datetime
# import os

# # Database configuration
# DATABASE_URL = "sqlite:///./resume_screening.db"

# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     username = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)

#     full_name = Column(String, nullable=True)
#     phone = Column(String, nullable=True) 
#     profile_photo = Column(String, nullable=True)
#     is_active = Column(Boolean, default=True)
#     is_employer = Column(Boolean, default=False)  # False = candidate, True = employer
#     created_at = Column(DateTime, default=datetime.utcnow)

# class ResumeHistory(Base):
#     __tablename__ = "resume_history"

#     id = Column(
#         Integer,
#         primary_key=True,
#         index=True
#     )

#     user_id = Column(
#         Integer,
#         ForeignKey("users.id"),
#         nullable=False
#     )

#     job_title = Column(String)

#     file_name = Column(String)

#     file_path = Column(String)

#     ats_score = Column(Float)

#     semantic_score = Column(Float)

#     recommendation = Column(String)

#     created_at = Column(
#         DateTime,
#         default=datetime.utcnow
#     )

# class Candidate(Base):
#     __tablename__ = "candidates"

#     id = Column(
#         Integer,
#         primary_key=True,
#         index=True
#     )

#     hr_id = Column(
#         Integer,
#         ForeignKey("users.id")
#     )

#     candidate_name = Column(String)

#     resume_file = Column(String)

#     job_title = Column(String)

#     ats_score = Column(Float)

#     semantic_score = Column(Float)

#     recommendation = Column(String)

#     created_at = Column(
#         DateTime,
#         default=datetime.utcnow
#     )

    
# # Create tables
# Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def get_user_by_email(db, email: str):
#     return db.query(User).filter(User.email == email).first()

# def get_user_by_username(db, username: str):
#     return db.query(User).filter(User.username == username).first()

# def create_user(db, email: str, username: str, password: str, full_name: str = None, is_employer: bool = False):
#     from passlib.context import CryptContext
#     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#     hashed_password = pwd_context.hash(password)
    
#     db_user = User(
#         email=email,
#         username=username,
#         hashed_password=hashed_password,
#         full_name=full_name,
#         is_employer=is_employer
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def verify_password(plain_password, hashed_password):
#     from passlib.context import CryptContext
#     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#     return pwd_context.verify(plain_password, hashed_password)

# def save_resume_history(
#     db,
#     user_id,
#     job_title,
#     file_name,
#     file_path,
#     ats_score,
#     semantic_score,
#     recommendation
# ):

#     history = ResumeHistory(
#         user_id=user_id,
#         job_title=job_title,
#         file_name=file_name,
#         file_path=file_path,
#         ats_score=ats_score,
#         semantic_score=semantic_score,
#         recommendation=recommendation
#     )

#     db.add(history)
#     db.commit()
#     db.refresh(history)

#     return history

# def get_user_history(
#     db,
#     user_id
# ):

#     return (
#         db.query(ResumeHistory)
#         .filter(
#             ResumeHistory.user_id == user_id
#         )
#         .order_by(
#             ResumeHistory.created_at.desc()
#         )
#         .all()
#     )

# def get_recent_history(
#     db,
#     user_id,
#     limit=3
# ):

#     return (
#         db.query(ResumeHistory)
#         .filter(
#             ResumeHistory.user_id == user_id
#         )
#         .order_by(
#             ResumeHistory.created_at.desc()
#         )
#         .limit(limit)
#         .all()
#     )

# def get_dashboard_stats(
#     db,
#     user_id
# ):

#     history = (
#         db.query(ResumeHistory)
#         .filter(
#             ResumeHistory.user_id == user_id
#         )
#         .all()
#     )

#     total_scans = len(history)

#     avg_accuracy = (
#         sum(
#             h.semantic_score or 0
#             for h in history
#         ) / total_scans
#         if total_scans > 0
#         else 0
#     )

#     latest_recommendation = (
#         history[-1].recommendation
#         if history
#         else "No recommendations available"
#     )

#     return {
#         "total_scans": total_scans,
#         "accuracy": round(avg_accuracy, 2),
#         "recommendation":
#             latest_recommendation
#     }

# def save_candidate(
#     db,
#     hr_id,
#     candidate_name,
#     resume_file,
#     job_title,
#     ats_score,
#     semantic_score,
#     recommendation
# ):

#     candidate = Candidate(

#         hr_id=hr_id,

#         candidate_name=candidate_name,

#         resume_file=resume_file,

#         job_title=job_title,

#         ats_score=ats_score,

#         semantic_score=semantic_score,

#         recommendation=recommendation
#     )

#     db.add(candidate)

#     db.commit()

#     db.refresh(candidate)

#     return candidate

# from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Float
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from datetime import datetime
# import os

# # Database configuration
# DATABASE_URL = "sqlite:///./resume_screening.db"

# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     username = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)

#     full_name = Column(String, nullable=True)
#     phone = Column(String, nullable=True) 
#     profile_photo = Column(String, nullable=True)
#     is_active = Column(Boolean, default=True)
#     is_employer = Column(Boolean, default=False)  # False = candidate, True = employer
#     created_at = Column(DateTime, default=datetime.utcnow)

# class ResumeHistory(Base):
#     __tablename__ = "resume_history"

#     id = Column(
#         Integer,
#         primary_key=True,
#         index=True
#     )

#     user_id = Column(
#         Integer,
#         ForeignKey("users.id"),
#         nullable=False
#     )

#     job_title = Column(String)

#     file_name = Column(String)

#     file_path = Column(String)

#     ats_score = Column(Float)

#     semantic_score = Column(Float)

#     recommendation = Column(String)

#     created_at = Column(
#         DateTime,
#         default=datetime.utcnow
#     )

# # Create tables
# Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def get_user_by_email(db, email: str):
#     return db.query(User).filter(User.email == email).first()

# def get_user_by_username(db, username: str):
#     return db.query(User).filter(User.username == username).first()

# def create_user(db, email: str, username: str, password: str, full_name: str = None, is_employer: bool = False):
#     from passlib.context import CryptContext
#     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#     hashed_password = pwd_context.hash(password)
    
#     db_user = User(
#         email=email,
#         username=username,
#         hashed_password=hashed_password,
#         full_name=full_name,
#         is_employer=is_employer
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def verify_password(plain_password, hashed_password):
#     from passlib.context import CryptContext
#     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#     return pwd_context.verify(plain_password, hashed_password)

# def save_resume_history(
#     db,
#     user_id,
#     job_title,
#     file_name,
#     file_path,
#     ats_score,
#     semantic_score,
#     recommendation
# ):

#     history = ResumeHistory(
#         user_id=user_id,
#         job_title=job_title,
#         file_name=file_name,
#         file_path=file_path,
#         ats_score=ats_score,
#         semantic_score=semantic_score,
#         recommendation=recommendation
#     )

#     db.add(history)
#     db.commit()
#     db.refresh(history)

#     return history

# def get_user_history(
#     db,
#     user_id
# ):

#     return (
#         db.query(ResumeHistory)
#         .filter(
#             ResumeHistory.user_id == user_id
#         )
#         .order_by(
#             ResumeHistory.created_at.desc()
#         )
#         .all()
#     )

# def get_recent_history(
#     db,
#     user_id,
#     limit=3
# ):

#     return (
#         db.query(ResumeHistory)
#         .filter(
#             ResumeHistory.user_id == user_id
#         )
#         .order_by(
#             ResumeHistory.created_at.desc()
#         )
#         .limit(limit)
#         .all()
#     )

# def get_dashboard_stats(
#     db,
#     user_id
# ):

#     history = (
#         db.query(ResumeHistory)
#         .filter(
#             ResumeHistory.user_id == user_id
#         )
#         .all()
#     )

#     total_scans = len(history)

#     avg_accuracy = (
#         sum(
#             h.semantic_score or 0
#             for h in history
#         ) / total_scans
#         if total_scans > 0
#         else 0
#     )

#     latest_recommendation = (
#         history[-1].recommendation
#         if history
#         else "No recommendations available"
#     )

#     return {
#         "total_scans": total_scans,
#         "accuracy": round(avg_accuracy, 2),
#         "recommendation":
#             latest_recommendation
#     }


from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database configuration
DATABASE_URL = "sqlite:///./resume_screening.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    full_name = Column(String, nullable=True)
    phone = Column(String, nullable=True) 
    profile_photo = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_employer = Column(Boolean, default=False)  # False = candidate, True = employer
    created_at = Column(DateTime, default=datetime.utcnow)

# class ResumeHistory(Base):
#     __tablename__ = "resume_history"

#     id = Column(
#         Integer,
#         primary_key=True,
#         index=True
#     )

#     user_id = Column(
#         Integer,
#         ForeignKey("users.id"),
#         nullable=False
#     )

#     job_title = Column(String)

#     file_name = Column(String)

#     file_path = Column(String)

#     ats_score = Column(Float)

#     semantic_score = Column(Float)

#     recommendation = Column(String)

#     created_at = Column(
#         DateTime,
#         default=datetime.utcnow
#     )


class ResumeHistory(Base):
    __tablename__ = "resume_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    job_title = Column(String)

    file_name = Column(String)

    file_path = Column(String)

    ats_score = Column(Float)

    semantic_score = Column(Float)

    recommendation = Column(String)

    report_data = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    hr_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    candidate_name = Column(String)

    resume_file = Column(String)

    job_title = Column(String)

    ats_score = Column(Float)

    semantic_score = Column(Float)

    recommendation = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    
# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_email(db, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db, email: str, username: str, password: str, full_name: str = None, is_employer: bool = False):
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)
    
    db_user = User(
        email=email,
        username=username,
        hashed_password=hashed_password,
        full_name=full_name,
        is_employer=is_employer
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

# def save_resume_history(
#     db,
#     user_id,
#     job_title,
#     file_name,
#     file_path,
#     ats_score,
#     semantic_score,
#     recommendation
# ):

def save_resume_history(
    db,
    user_id,
    job_title,
    file_name,
    file_path,
    ats_score,
    semantic_score,
    recommendation,
    report_data=None
):
    
    # history = ResumeHistory(
    #     user_id=user_id,
    #     job_title=job_title,
    #     file_name=file_name,
    #     file_path=file_path,
    #     ats_score=ats_score,
    #     semantic_score=semantic_score,
    #     recommendation=recommendation
    # )
    
    history = ResumeHistory(
    user_id=user_id,
    job_title=job_title,
    file_name=file_name,
    file_path=file_path,
    ats_score=ats_score,
    semantic_score=semantic_score,
    recommendation=recommendation,
    report_data=report_data
)

    db.add(history)
    db.commit()
    db.refresh(history)

    return history

def get_user_history(
    db,
    user_id
):

    return (
        db.query(ResumeHistory)
        .filter(
            ResumeHistory.user_id == user_id
        )
        .order_by(
            ResumeHistory.created_at.desc()
        )
        .all()
    )

def get_recent_history(
    db,
    user_id,
    limit=3
):

    return (
        db.query(ResumeHistory)
        .filter(
            ResumeHistory.user_id == user_id
        )
        .order_by(
            ResumeHistory.created_at.desc()
        )
        .limit(limit)
        .all()
    )

def get_dashboard_stats(
    db,
    user_id
):

    history = (
        db.query(ResumeHistory)
        .filter(
            ResumeHistory.user_id == user_id
        )
        .all()
    )

    total_scans = len(history)

    avg_accuracy = (
        sum(
            h.semantic_score or 0
            for h in history
        ) / total_scans
        if total_scans > 0
        else 0
    )

    latest_recommendation = (
        history[-1].recommendation
        if history
        else "No recommendations available"
    )

    return {
        "total_scans": total_scans,
        "accuracy": round(avg_accuracy, 2),
        "recommendation":
            latest_recommendation
    }

def save_candidate(
    db,
    hr_id,
    candidate_name,
    resume_file,
    job_title,
    ats_score,
    semantic_score,
    recommendation
):

    candidate = Candidate(

        hr_id=hr_id,

        candidate_name=candidate_name,

        resume_file=resume_file,

        job_title=job_title,

        ats_score=ats_score,

        semantic_score=semantic_score,

        recommendation=recommendation
    )

    db.add(candidate)

    db.commit()

    db.refresh(candidate)

    return candidate

