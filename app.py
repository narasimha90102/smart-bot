from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

context_store = {}

class ContextRequest(BaseModel):
    user_id: str
    merchant: Optional[str] = None
    category: Optional[str] = None

class TickRequest(BaseModel):
    user_id: str
    trigger: str

class ReplyRequest(BaseModel):
    user_id: str

@app.get("/")
def home():
    return {"message": "Bot is running"}

@app.post("/v1/context")
def set_context(data: ContextRequest):
    context_store[data.user_id] = {
        "merchant": data.merchant,
        "category": data.category
    }
    return {"status": "context stored"}

@app.post("/v1/tick")
def process_tick(data: TickRequest):
    ctx = context_store.get(data.user_id, {})
    merchant = ctx.get("merchant")
    category = ctx.get("category")

    if category == "food":
        decision = "offer"
    elif merchant:
        decision = "merchant"
    else:
        decision = "general"

    context_store[data.user_id]["decision"] = decision
    return {"decision": decision}

@app.post("/v1/reply")
def get_reply(data: ReplyRequest):
    ctx = context_store.get(data.user_id, {})
    decision = ctx.get("decision")

    if decision == "offer":
        return {"reply": "Get 20% OFF on food!"}
    elif decision == "merchant":
        return {"reply": f"Check offers at {ctx.get('merchant')}"}
    else:
        return {"reply": "Welcome! Explore offers near you."}

@app.get("/v1/healthz")
def health():
    return {"status": "ok"}

@app.get("/v1/metadata")
def metadata():
    return {"name": "Simple Bot", "version": "1.0"}