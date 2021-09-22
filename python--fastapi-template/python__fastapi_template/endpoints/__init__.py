from dataclasses import dataclass, field
from fastapi import APIRouter

@dataclass(frozen=True)
class Endpoint:
    prefix: str
    router: APIRouter = field(default_factory=APIRouter)
