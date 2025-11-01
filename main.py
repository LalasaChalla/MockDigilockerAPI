from fastapi import FastAPI

app = FastAPI(title="Mock DigiLocker API")

# Mock Aadhaar Data
mock_aadhaar_data = {
    "123456789012": {
        "name": "Lalasa",
        "dob": "2000-05-21",
        "gender": "Female",
        "address": "Vijayawada, Andhra Pradesh",
    }
}

@app.get("/")
def home():
    return {"message": "Welcome to the Mock DigiLocker API"}

@app.get("/api/status")
def status():
    return {"status": "Mock DigiLocker API is running"}

@app.get("/api/user/aadhaar/{aadhaar_number}")
def get_aadhaar_details(aadhaar_number: str):
    user = mock_aadhaar_data.get(aadhaar_number)
    if user:
        return {"aadhaar_number": aadhaar_number, **user}
    return {"error": "User not found"}

# Mock PAN Data
mock_pan_data = {
    "ABCDE1234F": {
        "name": "Lalasa",
        "dob": "2000-05-21",
        "father_name": "Ramesh Kumar",
    }
}

@app.get("/api/user/pan/{pan_number}")
def get_pan_details(pan_number: str):
    user = mock_pan_data.get(pan_number.upper())
    if user:
        return {"pan_number": pan_number.upper(), **user}
    return {"error": "PAN not found"}

from fastapi.responses import FileResponse
import os

# Mock DigiLocker documents
mock_documents = {
    "123456789012": [  # Aadhaar number as key
        {
            "doc_id": "DOC001",
            "name": "Integrated Certificate",
            "type": "PDF",
            "issue_date": "2024-06-01",
            "issuer": "Revenue Department, Govt. of AP",
            "file_path": "sample_docs/integrated_certificate.pdf"
        },
        {
            "doc_id": "DOC002",
            "name": "PAN Card",
            "type": "PDF",
            "issue_date": "2023-09-15",
            "issuer": "Income Tax Department",
            "file_path": "sample_docs/pan_card.pdf"
        }
    ]
}

@app.get("/api/user/documents/{aadhaar_number}")
def list_user_documents(aadhaar_number: str):
    docs = mock_documents.get(aadhaar_number)
    if docs:
        return {"aadhaar_number": aadhaar_number, "documents": docs}
    return {"error": "No documents found for this user"}

@app.get("/api/document/download/{doc_id}")
def download_document(doc_id: str):
    # Search document by ID
    for docs in mock_documents.values():
        for doc in docs:
            if doc["doc_id"] == doc_id:
                path = doc["file_path"]
                if os.path.exists(path):
                    return FileResponse(path, media_type="application/pdf", filename=doc["name"] + ".pdf")
                return {"message": f"Mock file for {doc['name']} not found"}
    return {"error": "Invalid document ID"}


