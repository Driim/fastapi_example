from sqlalchemy.ext.declarative import declared_attr
from pydantic import BaseModel as PydanticModel


class BaseModel:

    # eager_defaults is required in order to access columns
    # with server defaults or SQL expression defaults,
    # subsequent to a flush without triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

    @declared_attr
    def __tablename__(cls):  # noqa
        return f"{cls.__name__.lower()}s"

    def update(self, data: PydanticModel):
        for key, value in data.dict(exclude_unset=True).items():
            if not hasattr(self, key):
                raise KeyError()

            setattr(self, key, value)
