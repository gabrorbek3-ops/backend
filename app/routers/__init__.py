from fastapi import APIRouter

from .health import router as health_router
from .auth import router as auth_router
from .phone_numbers import router as phone_numbers_router


router = APIRouter()

router.include_router(health_router)
router.include_router(auth_router)
router.include_router(phone_numbers_router)