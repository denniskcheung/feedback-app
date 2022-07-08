from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from fastapi import HTTPException


class Feedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rating: int = Field(ge=1, le=10, description="The rating must be 1..10")
    text: str


sqlite_url = f"sqlite://"


connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args, poolclass=StaticPool)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Feedback(rating=8, text="Pre-populated Feedback Item 1"))
        session.add(Feedback(rating=9, text="Pre-populated Feedback Item 2"))
        session.add(Feedback(rating=10, text="Pre-populated Feedback Item 3"))
        session.commit()


def get_all():
    with Session(engine) as session:
        feedbacks = session.exec(select(Feedback).order_by(Feedback.id.desc())).all()
        return feedbacks


def add_feedback(item: Feedback):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


def update_feedback(feedback_id: int, item: Feedback):
    with Session(engine) as session:
        statement = select(Feedback).where(Feedback.id == feedback_id)
        results = session.exec(statement)
        feedback = results.one()  # validates that the item is in the db, else raises error
        feedback.rating = item.rating
        feedback.text = item.text
        session.add(feedback)
        session.commit()
        session.refresh(feedback)
        return feedback


def del_feedback(feedback_id: int):
    with Session(engine) as session:
        statement = select(Feedback).where(Feedback.id == feedback_id)
        results = session.exec(statement)
        if not results:
            raise HTTPException(status_code=404, detail="Feedback not found")
        else:
            feedback = results.one()
            session.delete(feedback)
            session.commit()


if __name__ == "__main__":
    create_db_and_tables()