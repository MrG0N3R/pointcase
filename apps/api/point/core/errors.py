from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException


def error_response(request: Request, status: int, code: str, message: str, details: dict | None = None):
    return JSONResponse(status_code=status, content={"error": {
        "code": code, "message": message, "details": details or {},
        "request_id": getattr(request.state, "request_id", ""),
    }})


async def http_error(request: Request, exc: HTTPException):
    messages = {404: ("NOT_FOUND", "El recurso no está disponible."), 405: ("METHOD_NOT_ALLOWED", "Esta acción no está disponible.")}
    code, message = messages.get(exc.status_code, ("HTTP_ERROR", "No se pudo completar la solicitud."))
    return error_response(request, exc.status_code, code, message)


async def validation_error(request: Request, exc: RequestValidationError):
    fields = [{"field": ".".join(str(part) for part in error["loc"]), "type": error["type"]} for error in exc.errors()]
    return error_response(request, 422, "VALIDATION_ERROR", "Revisa los campos de la solicitud.", {"fields": fields})
