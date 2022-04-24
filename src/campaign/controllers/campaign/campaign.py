import logging
from typing import Optional
from fastapi import APIRouter, Depends, FastAPI
from fastapi_restful.cbv import cbv
from src.common.auth.auth import UserRole, get_user_id, get_user_role

from src.common.validators.path import PathIdParam

logger = logging.getLogger(__name__)

# FIXME: cbv have issue with empty paths, so we can not use prefix
router = APIRouter(
    tags=["Campaign"],
)


@cbv(router)
class CampaignController:
    # TODO: response dto depends on role
    user_role: UserRole = Depends(get_user_role)
    user_id: Optional[int] = Depends(get_user_id)

    @router.get("/campaign/{id}")
    async def get_info_about_campaign(self, id: int = PathIdParam):
        pass

    @router.post("/campaign")
    async def create_campaign(self):
        pass

    @router.delete("/campaign/{id}")
    async def deactivate_campaign(self, id: int = PathIdParam):
        pass

    @router.post("/campaign/{id}/activate")
    async def user_activation(self, id: int = PathIdParam):
        pass

    @router.get("/campaign/{id}/status")
    async def user_status(self, id: int = PathIdParam):
        pass


def register_campaign_router(application: FastAPI, version: str) -> None:
    logger.debug("Registering market campaign router")
    router.tags.append(version)
    application.include_router(router, prefix=version)
