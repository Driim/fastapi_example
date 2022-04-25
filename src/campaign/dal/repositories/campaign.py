from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.campaign.dal.models.campaign import Campaign

from src.common.database import get_session

class CampaignRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self._session = session

    async def find(self, filters, pagination) -> PaginatedResult[Campaign]:
        pass

    async def get(self, id: int, locked: bool = False) -> Campaign:
        pass

    @handle_alchemy_exception("Unable to save model")
    async def save(self, entity: Campaign) -> Campaign:
        pass

    @handle_alchemy_exception("Unable to delete model")
    async def delete(self, entity: Campaign) -> None:
        pass


    async def create(self, data: CampaignCreateDto) -> Campaign:
        pass