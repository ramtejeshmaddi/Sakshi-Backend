from sqlalchemy.orm import Session
from app import models, schemas

def create_group(db: Session, group: schemas.GroupCreate):
    new_group = models.Group(name=group.name, created_by=group.created_by)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

def get_groups(db: Session):
    return db.query(models.Group).all()

def create_quiz(db: Session, quiz: schemas.QuizCreate):
    db_quiz = models.Quiz(
        title=quiz.title,
        description=quiz.description,
        group_id=quiz.group_id,
        created_by=quiz.created_by
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)

    for q in quiz.questions:
        db_question = models.Question(text=q.text, quiz_id=db_quiz.id)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        for a in q.answers:
            db_answer = models.Answer(
                text=a.text,
                is_correct=int(a.is_correct),
                question_id=db_question.id
            )
            db.add(db_answer)

    db.commit()
    return db_quiz

def get_quizzes_by_group(db: Session, group_id: int):
    return db.query(models.Quiz).filter(models.Quiz.group_id == group_id).all()

def submit_quiz(db: Session, submission_data: schemas.SubmissionCreate):
    correct_answers = 0
    total_questions = 0

    new_submission = models.Submission(
        user_id=submission_data.user_id,
        quiz_id=submission_data.quiz_id,
        score=0  # update later
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    for ans in submission_data.answers:
        total_questions += 1
        correct = db.query(models.Answer).filter_by(
            id=ans.selected_answer_id,
            question_id=ans.question_id,
            is_correct=1
        ).first()

        if correct:
            correct_answers += 1

        submitted = models.SubmittedAnswer(
            submission_id=new_submission.id,
            question_id=ans.question_id,
            selected_answer_id=ans.selected_answer_id
        )
        db.add(submitted)

    score = int((correct_answers / total_questions) * 100)
    new_submission.score = score
    db.commit()
    return new_submission

