import uvicorn
from models.database import engine
from models import models_db

# Create the database tables
models_db.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(
        "application.rest:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
