
from sqlalchemy import Column, DateTime, BigInteger, String

from src.campaign.dal.base_model import CampaignBaseModel

NAME_LENGTH = 255


class Campaign(CampaignBaseModel):
    id = Column(BigInteger, primary_key=True)
    name = Column(String(NAME_LENGTH), nullable=False)

    starts = Column(DateTime(timezone=True), nullable=True)
    ends = Column(DateTime(timezone=True), nullable=True)

    activations_count = Column(BigInteger, nullable=True)
    per_user_activations = Column(BigInteger, nullable=True)