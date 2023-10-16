from fastapi import APIRouter
from ..controller import address as address_controller

router = APIRouter()

router.include_router(address_controller.router, tags=["addresses"])
