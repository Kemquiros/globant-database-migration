from fastapi import FastAPI
from routers.department import department_router
from routers.employee import employee_router
from routers.job import job_router
from config.database import engine, Base

app = FastAPI()

app.title = "Database Migration API"
app.version = "1.0.0"

app.include_router(department_router)
app.include_router(employee_router)
app.include_router(job_router)

# Generates the schema from metadata
Base.metadata.create_all(bind=engine)
