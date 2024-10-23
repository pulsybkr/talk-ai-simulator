from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import BaseModel
from typing import Optional, List

# SQLAlchemy models
class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    job_description = Column(Text)
    cv = Column(Text)
    cover_letter = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="interviews")
    messages = relationship("Message", back_populates="interview")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    role = Column(String)
    interview_id = Column(Integer, ForeignKey("interviews.id"))

    interview = relationship("Interview", back_populates="messages")

# Pydantic models
class InterviewBase(BaseModel):
    job_description: str
    cv: str
    cover_letter: Optional[str] = None

class InterviewCreate(InterviewBase):
    pass

class InterviewModel(InterviewBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    content: str
    role: str

class MessageCreate(MessageBase):
    pass

class MessageModel(MessageBase):
    id: int
    interview_id: int

    class Config:
        from_attributes = True

class InterviewWithMessages(InterviewModel):
    messages: List[MessageModel] = []
