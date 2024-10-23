from sqlalchemy.orm import Session
from app.models.interview import Interview, InterviewCreate, Message

def create_interview(db: Session, interview: InterviewCreate):
    db_interview = Interview(
        job_description=interview.job_description,
        cv=interview.cv,
        cover_letter=interview.cover_letter
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview

def get_interview(db: Session, interview_id: int):
    return db.query(Interview).filter(Interview.id == interview_id).first()

def save_messages(db: Session, interview_id: int, messages: list):
    for msg in messages:
        db_message = Message(content=msg["content"], role=msg["role"], interview_id=interview_id)
        db.add(db_message)
    db.commit()

def get_interview_context(db: Session, interview: Interview):
    context = {
        "job_description": interview.job_description,
        "cv": interview.cv,
        "cover_letter": interview.cover_letter
    }
    return context

def get_interview_messages(db: Session, interview: Interview):
    """
    Récupère tous les messages associés à un entretien spécifique.
    """
    return db.query(Message).filter(Message.interview_id == interview.id).order_by(Message.id).all()
