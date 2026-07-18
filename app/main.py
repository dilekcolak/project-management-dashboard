from fastapi import FastAPI

from app.api.routes.auth import router as auth_router

app = FastAPI(
    title="Project Management Dashboard API",
    description="Project and document management service",
    version="0.1.0",
)


app.include_router(auth_router)

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Project Management Dashboard API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}