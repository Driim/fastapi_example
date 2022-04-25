from sqlalchemy import Column, DateTime, BigInteger, ForeignKey, func
from sqlalchemy.orm import relationship

from src.campaign.dal.base_model import CampaignBaseModel


class Activation(CampaignBaseModel):
    id = Column(BigInteger, primary_key=True)

    campaign_id = Column(BigInteger, ForeignKey("campaign.campaign.id"))
    campaign = relationship("Campaign", lazy="selectin")

    user_id = Column(BigInteger) # user ID is external, so no foreign key

    created = Column(DateTime, server_default=func.utcnow())