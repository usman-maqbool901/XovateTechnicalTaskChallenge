from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .validator import validate_csv
from .schemas import ValidationResponse

app = FastAPI(title="Xovate Data Validation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/validate", response_model=ValidationResponse)
async def validate_endpoint(file: UploadFile = File(...)):
    content = await file.read()
    return validate_csv(content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
