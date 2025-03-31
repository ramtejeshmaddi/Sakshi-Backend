from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    created_by = Column(String)  # store admin username or ID

    quizzes = relationship("Quiz", back_populates="group")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    group_id = Column(Integer, ForeignKey("groups.id"))
    created_by = Column(String)  # instructor name/ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    group = relationship("Group", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))

    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("Answer", back_populates="question")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    is_correct = Column(Integer)  # 0 = False, 1 = True
    question_id = Column(Integer, ForeignKey("questions.id"))

    question = relationship("Question", back_populates="answers")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    score = Column(Integer)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    quiz = relationship("Quiz")
    submitted_answers = relationship("SubmittedAnswer", back_populates="submission")


class SubmittedAnswer(Base):
    __tablename__ = "submitted_answers"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    selected_answer_id = Column(Integer, ForeignKey("answers.id"))

    submission = relationship("Submission", back_populates="submitted_answers")



class GroupMembership(Base):
    __tablename__ = "group_memberships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))

    group = relationship("Group")


