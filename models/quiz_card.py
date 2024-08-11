from datetime import date
from pydantic import BaseModel, Field

class QuizCard(BaseModel):
    question: str = Field(description="A question whos answer is always a date")
    answer: date = Field(description="The answer to the question in the form of a date")

