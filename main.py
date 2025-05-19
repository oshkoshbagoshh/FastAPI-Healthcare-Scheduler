from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database.database import get_db, init_db
from database.seed import seed_database
from api import patients, resources, medical, scheduling

# Initialize FastAPI app
app = FastAPI(
    title="Healthcare Scheduling API",
    description="An AI-powered healthcare scheduling system for outpatient procedures",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(patients.router)
app.include_router(resources.router)
app.include_router(medical.router)
app.include_router(scheduling.router)


@app.get("/")
async def root():
    return {
        "message": "Healthcare Scheduling API",
        "description": "An AI-powered healthcare scheduling system for outpatient procedures",
        "documentation": "/docs",
    }


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/seed-database")
async def seed_db(
    patient_count: int = 50,
    resource_count: int = 10,
    days_ahead: int = 30,
    db: Session = Depends(get_db)
):
    """
    Seed the database with fake data.

    This endpoint is for development and testing purposes only.
    """
    # Initialize database
    init_db()

    # Seed database
    result = seed_database(db, patient_count, resource_count, days_ahead)

    return {
        "message": "Database seeded successfully",
        "data": result
    }


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
