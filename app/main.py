from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from routers.user import router as users_router
from routers.auth import router as auth_router
from routers.branch import router as branch_router
from routers.region import router as region_router
from utils.register_exception_handlers import register_exception_handlers
from routers.face import router as face_router
# from routers.analytics import router as analytics_router
from routers.tracking import router as tracking_router
from routers.integration import router as integration_router

app = FastAPI()

# app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount(
#     "/static/outputs",
#     StaticFiles(directory="static/outputs"),
#     name="outputs"
# )

templates = Jinja2Templates(directory="templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", response_class=HTMLResponse)
async def integration_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/results", response_class=HTMLResponse)
async def integration_results(request: Request):
    return templates.TemplateResponse("results.html", {"request": request})

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    # Save the uploaded file to a specific location
    with open(f"static/uploads/{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())
    return {"message": "File uploaded successfully", "filename": file.filename}

@app.get("/face", response_class=HTMLResponse)
async def face_page(request: Request):
    return templates.TemplateResponse("face.html", {"request": request})

@app.get("/tracking", response_class=HTMLResponse)
async def tracking_page(request: Request):
    return templates.TemplateResponse("tracking.html", {"request": request})

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
