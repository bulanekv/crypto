from fastapi import APIRouter

from .endpoints import currencies

router = APIRouter()
router.include_router(currencies.router, prefix="/currencies", tags=["Currencies"])
