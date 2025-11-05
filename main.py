import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import db, create_document, get_documents
from schemas import Candidate

app = FastAPI(title="HR Onboarding Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "HR Onboarding Backend Running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, "name", "✅ Connected")
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

@app.post("/start_onboarding")
def start_onboarding(candidate: Candidate):
    """
    Create a new candidate record and set initial status to "Offer Sent".
    """
    try:
        data = candidate.model_dump()
        data["status"] = "Offer Sent"
        inserted_id = create_document("candidate", data)
        return {"success": True, "id": inserted_id, "message": "Onboarding started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/candidates")
def list_candidates() -> List[dict]:
    try:
        docs = get_documents("candidate", {}, None)
        # normalize ObjectId and datetime fields to strings
        normalized = []
        for d in docs:
            d["id"] = str(d.pop("_id", ""))
            for key in ["created_at", "updated_at", "joining_date"]:
                if key in d and isinstance(d[key], datetime):
                    d[key] = d[key].isoformat()
            normalized.append(d)
        # sort by updated_at desc if available
        normalized.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return normalized
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
