from fastapi import APIRouter, Request, Response
from point import __version__
from point.modules.system.schemas import PublicMetadata, Readiness
from point.modules.system.service import check_readiness

router = APIRouter(tags=["system"])


@router.get("/health/live")
def live():
    return {"status": "ok"}


@router.get("/health/ready", response_model=Readiness, responses={503: {"model": Readiness}})
@router.get("/api/v1/system/status", response_model=Readiness, responses={503: {"model": Readiness}})
def ready(request: Request, response: Response):
    result = check_readiness(request.app.state.engine)
    response.status_code = 200 if result.status == "ok" else 503
    return result


@router.get("/api/v1/meta", response_model=PublicMetadata)
def metadata(request: Request):
    config = request.app.state.settings
    return PublicMetadata(name=config.app_name, version=__version__, phase=2, defaults={
        "locale": config.default_locale, "currency": config.default_currency, "timezone": config.default_timezone,
    })
