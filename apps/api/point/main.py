import time
from contextlib import asynccontextmanager
from uuid import UUID, uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from point import __version__
from point.core.config import Settings
from point.core.errors import error_response, http_error, validation_error
from point.core.logging import configure_logging
from point.db.connection import build_engine
from point.modules.system.router import router


def create_app(settings: Settings | None = None, engine=None) -> FastAPI:
    config = settings or Settings()
    database = engine if engine is not None else build_engine(config)
    logger = configure_logging(config.log_level)

    @asynccontextmanager
    async def lifespan(app):
        yield
        if engine is None:
            database.dispose()

    app = FastAPI(
        title=config.app_name, version=__version__, lifespan=lifespan,
        docs_url="/api/docs" if config.environment != "production" else None,
        redoc_url=None, openapi_url="/api/v1/openapi.json" if config.environment != "production" else None,
    )
    app.state.settings = config
    app.state.engine = database
    app.add_middleware(CORSMiddleware, allow_origins=config.cors_origins, allow_methods=["GET"],
                       allow_headers=["Content-Type", "X-Request-ID"], expose_headers=["X-Request-ID"])

    @app.middleware("http")
    async def request_context(request: Request, call_next):
        try:
            request_id = str(UUID(request.headers.get("X-Request-ID", "")))
        except ValueError:
            request_id = str(uuid4())
        request.state.request_id = request_id
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception as exc:
            logger.error("request_failed", extra={"event": "request_failed", "request_id": request_id, "error_type": type(exc).__name__})
            response = error_response(request, 500, "INTERNAL_ERROR", "Ocurrió un error. Usa el identificador de la solicitud para pedir ayuda.")
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        route = request.scope.get("route")
        logger.info("http_request", extra={"event": "http_request", "request_id": request_id, "method": request.method,
                                          "path": getattr(route, "path", "unmatched"), "status": response.status_code,
                                          "duration_ms": round((time.perf_counter() - start) * 1000, 2)})
        return response

    app.add_exception_handler(HTTPException, http_error)
    app.add_exception_handler(RequestValidationError, validation_error)
    app.include_router(router)
    return app
