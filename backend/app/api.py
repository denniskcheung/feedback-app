from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Feedbacks
from sqlalchemy import exc


app = FastAPI()




origins = [
    "http://localhost:3000/",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def on_startup():
    Feedbacks.create_db_and_tables()


@app.get("/", tags=["root"])
async def get_root() -> dict:
    return {"message": "Welcome to our feedback list."}


@app.get("/feedback", tags=["feedbacks"])
async def get_feedback() -> dict:
    return Feedbacks.get_all()


@app.delete("/feedback/{feedback_id}", tags=["feedbacks"])
async def delete_feedback(feedback_id: int):
    try:
        Feedbacks.del_feedback(feedback_id)
        return {
            "data": f"Feedback with id {feedback_id} has been removed."
        }
    except exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")


@app.post("/feedback", tags=["feedbacks"], status_code=status.HTTP_201_CREATED, response_model=Feedbacks.Feedback)
async def post_feedback(feedback: Feedbacks.Feedback):
    return Feedbacks.add_feedback(feedback)


@app.put("/feedback/{feedback_id}", tags=["feedbacks"], response_model=Feedbacks.Feedback)
async def update_feedback(feedback_id: int, feedback: Feedbacks.Feedback):
    return Feedbacks.update_feedback(feedback_id, feedback)




