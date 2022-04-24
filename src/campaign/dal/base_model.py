from sqlalchemy.ext.declarative import as_declarative

from src.common.database import BaseModel


@as_declarative()
class CampaignBaseModel(BaseModel):
    # Each microservice has own declarative base to run migrations separately
    # Note: models should be in __init__ for alembic
    __table_args__ = {"schema": "campaign"}
