
from sqlalchemy.orm import Session
#------------------------------------
import crud, schemas
#from app import crud, schemas -> Use this when running locally
#------------------------------------
from database import Base, engine
#from app.database import Base, engine -> Use this when running locally
#------------------------------------
from schemas import GroupMembershipCreate
#from app.schemas import GroupMembershipCreate -> Use this when running locally
#------------------------------------
import models
#from app import models -> Use this when running locally
#------------------------------------
from database import get_db
#from app.database import get_db -> Use this when running locally
#------------------------------------
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import joinedload



router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/groups", response_model=schemas.GroupOut)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    return crud.create_group(db, group)

@router.get("/groups", response_model=list[schemas.GroupOut])
def read_groups(db: Session = Depends(get_db)):
    return crud.get_groups(db)

@router.post("/quizzes", response_model=schemas.QuizOut)
def create_quiz(quiz: schemas.QuizCreate, db: Session = Depends(get_db)):
    return crud.create_quiz(db, quiz)

@router.get("/groups/{group_id}/quizzes", response_model=list[schemas.QuizOut])
def get_quizzes(group_id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    return crud.get_quizzes_by_group(db, group_id)

@router.get("/quizzes/{quiz_id}", response_model=schemas.QuizOut)
def get_quiz_by_id(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz



@router.post("/quizzes/{quiz_id}/submit", response_model=schemas.SubmissionOut)
def submit_quiz(quiz_id: int, submission: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    return crud.submit_quiz(db, submission)


@router.post("/groups/join")
def join_group(membership: GroupMembershipCreate, db: Session = Depends(get_db)):
    existing = db.query(models.GroupMembership).filter_by(
        user_id=membership.user_id,
        group_id=membership.group_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already joined this group")

    db_membership = models.GroupMembership(**membership.dict())
    db.add(db_membership)
    db.commit()
    db.refresh(db_membership)
    return db_membership


@router.get("/groups/user/{user_id}")
def get_user_groups(user_id: str, db: Session = Depends(get_db)):
    memberships = (
        db.query(models.GroupMembership)
        .options(joinedload(models.GroupMembership.group))  # ✅ This loads the group
        .filter_by(user_id=user_id)
        .all()
    )

    return [
        {
            "group_id": m.group_id,
            "group_name": m.group.name if m.group else "Unknown"
        }
        for m in memberships
    ]

@router.delete("/groups/leave")
def leave_group(membership: GroupMembershipCreate, db: Session = Depends(get_db)):
    record = db.query(models.GroupMembership).filter_by(
        user_id=membership.user_id,
        group_id=membership.group_id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Membership not found")

    db.delete(record)
    db.commit()
    return {"message": "Left group successfully"}

@router.delete("/quizzes/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    db.delete(quiz)
    db.commit()
    return {"message": "Quiz deleted successfully"}

