from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from routes import blog

app = FastAPI(
    title="50fin Blog",
    description="Full Stack Developer Hiring Task",
)

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def request_exception_handler(_, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": f"{exc}".replace("\n", " ").replace("   ", " ")},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(Exception)
async def exception_handler(_, exc):
    print(exc)
    return JSONResponse(status_code=500, content={"error": "internal server error"})


app.include_router(blog.router, tags=["Blog"], prefix="/api/posts")


@app.get("/api/health", description="health route")
def root():
    return {"status": "OK"}


@app.route("/{full_path:path}")
async def catch_all_handler(request: Request):
    return JSONResponse(
        status_code=404,
        content={
            "Docmentation": "https://five0fin.onrender.com/docs",
            "Preview": "https://50fin.ahampriyanshu.com",
            "Code": "https://github.com/ahampriyanshu/50fin-server",
        },
    )
