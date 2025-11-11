import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Company, Service, ProcessStep, ContactMessage

app = FastAPI(title="MILDSHIFT PRoject API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"name": "MILDSHIFT PRoject", "status": "ok"}

@app.get("/api/company", response_model=List[dict])
def get_company_profile():
    try:
        docs = get_documents("company", limit=1)
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/company")
def create_company_profile(payload: Company):
    try:
        inserted_id = create_document("company", payload)
        return {"inserted_id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/services", response_model=List[dict])
def list_services():
    try:
        return get_documents("service")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/services")
def create_service(payload: Service):
    try:
        inserted_id = create_document("service", payload)
        return {"inserted_id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/process", response_model=List[dict])
def list_process_steps():
    try:
        # Sort by order in client side; Mongo helper does basic find only.
        docs = get_documents("processstep")
        return sorted(docs, key=lambda d: d.get("order", 9999))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process")
def create_process_step(payload: ProcessStep):
    try:
        inserted_id = create_document("processstep", payload)
        return {"inserted_id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
def submit_contact(payload: ContactMessage):
    try:
        inserted_id = create_document("contactmessage", payload)
        return {"message": "Thanks for reaching out!", "ticket_id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
