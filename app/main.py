from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, clients, cases, documents, hearings, imports

app = FastAPI()

# CORS (production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://psr-lawfirm-app.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(clients.router, prefix="/clients", tags=["Clients"])
app.include_router(cases.router, prefix="/cases", tags=["Cases"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(hearings.router, prefix="/hearings", tags=["Hearings"])
app.include_router(imports.router, prefix="/imports", tags=["Imports"])

@app.get("/")
def root():
    return {"status": "PSR API running", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"health": "ok"}
