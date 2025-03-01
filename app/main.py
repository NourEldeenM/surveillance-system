from fastapi import FastAPI
from app.routers.user import router as users_router
from app.routers.auth import router as auth_router
from app.routers.branch import router as branch_router
from app.utils.register_exception_handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)

# routes
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="", tags=["Auth"])
app.include_router(branch_router, prefix="/branches", tags=["Branches"])
