from src.campaign.application import initialize_application
from src.campaign.configuration import Configuration


config = Configuration()
app = initialize_application(config)
