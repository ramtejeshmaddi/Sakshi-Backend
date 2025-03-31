from pydantic import BaseModel
from typing import List, Optional

class AnswerCreate(BaseModel):
    text: str
    is_correct: bool

class QuestionCreate(BaseModel):
    text: str
    answers: List[AnswerCreate]

class QuizCreate(BaseModel):
    title: str
    description: Optional[str] = None
    group_id: int
    created_by: str
    questions: List[QuestionCreate]

class GroupCreate(BaseModel):
    name: str
    created_by: str


# Response models

class AnswerOut(AnswerCreate):
    id: int
    class Config:
        orm_mode = True

class QuestionOut(BaseModel):
    id: int
    text: str
    answers: List[AnswerOut]
    class Config:
        orm_mode = True

class QuizOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    group_id: int
    created_by: str
    questions: List[QuestionOut]

    class Config:
        orm_mode = True

class GroupOut(BaseModel):
    id: int
    name: str
    created_by: str
    class Config:
        orm_mode = True
class SubmittedAnswerCreate(BaseModel):
    question_id: int
    selected_answer_id: int

class SubmissionCreate(BaseModel):
    user_id: str
    quiz_id: int
    answers: List[SubmittedAnswerCreate]

class SubmissionOut(BaseModel):
    id: int
    user_id: str
    quiz_id: int
    score: int

    class Config:
        orm_mode = True


class GroupMembershipCreate(BaseModel):
    user_id: str
    group_id: int

