from typing import Literal
from pydantic import BaseModel


class HealthChecks(BaseModel):
    database: bool
    migrations: bool


class Readiness(BaseModel):
    status: Literal["ok", "unavailable"]
    checks: HealthChecks


class DisplayDefaults(BaseModel):
    locale: str
    currency: str
    timezone: str


class PublicMetadata(BaseModel):
    name: str
    version: str
    phase: int
    defaults: DisplayDefaults
