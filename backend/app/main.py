from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.api.rag import answer_query
from app.api.tax_calc import calc_taxes
from app.api.parser_updates import trigger_update
import os

app = FastAPI(title="AI Accountant (RUS)")


class QuestionPayload(BaseModel):
    question: str
    user_id: str | None = None


class TaxPayload(BaseModel):
    kind: str
    revenue: float | None = None
    expenses: float | None = None
    amount: float | None = None
    salary_total: float | None = None
    scheme: str | None = "6"


@app.post("/api/question")
async def question(payload: QuestionPayload):
    return await answer_query(payload.question, payload.user_id)


@app.post("/api/tax/calc")
def tax_calc(payload: TaxPayload):
    return calc_taxes(payload.dict())


@app.post("/api/admin/update-knowledge")
async def admin_update(secret: str):
    if secret != os.getenv("ADMIN_SECRET"):
        raise HTTPException(status_code=403, detail="forbidden")
    return await trigger_update()


@app.get("/health")
def health():
    return {"status": "ok"}
