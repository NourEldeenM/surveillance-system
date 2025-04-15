from fastapi import FastAPI
from app.routers.user import router as users_router
from app.routers.auth import router as auth_router
from app.routers.branch import router as branch_router
from app.routers.region import router as region_router
from app.utils.register_exception_handlers import register_exception_handlers
from app.routers.face import router as face_router
# from app.routers.analytics import router as analytics_router
from app.routers.tracking import router as tracking_router
from app.routers.integration import router as integration_router

app = FastAPI()

register_exception_handlers(app)

# routes
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="", tags=["Auth"])
app.include_router(region_router, prefix="/regions", tags=["Regions"])
app.include_router(branch_router, prefix="/branches", tags=["Branches"])
app.include_router(face_router, prefix="/models/face", tags=["Models"])
# app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(tracking_router, prefix="/models/tracking", tags=["Models"])
app.include_router(integration_router, prefix="/models/integration", tags=["Models"])
