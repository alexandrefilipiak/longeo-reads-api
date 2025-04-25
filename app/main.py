"""
main.py is the entry point of the API. It sets up the FastAPI app,
mounts the PyFlutterflow dashboard, initializes the Firebase Admin SDK,
mounts the middleware and includes the user and admin routes.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pyflutterflow import PyFlutterflow
from pyflutterflow.logs import get_logger
from pyflutterflow import routes as pyff_routes
from pyflutterflow.middleware import handle_uncaught_exceptions, handle_validation_error
from app.settings import get_settings
from app.models import initialize_firebase_admin
from app.routers.admin import sample_admin_routes
from app.routers.user import sample_user_routes

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI): # pylint: disable=unused-argument
    await initialize_firebase_admin()
    logger.info("Emails are %s", "enabled" if not settings.disable_email else "disabled")
    yield


app = FastAPI(title=settings.app_title, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, 'http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Pyflutterflow setup
pyflutterflow = PyFlutterflow(settings=settings)
app.mount(*pyflutterflow.dashboard_path())
app.include_router(pyff_routes.router)

# Middleware for exception catching
app.middleware("http")(handle_uncaught_exceptions)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await handle_validation_error(request, exc)


# User routes
app.include_router(sample_user_routes.router)

# Admin routes
app.include_router(sample_admin_routes.router)
