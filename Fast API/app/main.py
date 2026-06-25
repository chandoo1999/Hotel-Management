from fastapi import FastAPI

from app.core.database import Base
from app.core.database import engine

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router

from app.models.role import Role
from app.models.user import User

from app.routers.orders import router as orders_router
from app.routers.tables import router as tables_router
from app.routers.categories import router as categories_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Hotel Management API",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(tables_router)
app.include_router(categories_router)

@app.get("/")
def home():

    return {
        "message": "Hotel Management API Running"
    }