from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NovaQureSchema(BaseModel):
    """
    Base schema used by every DTO
    in the NovaQure backend.

    Enables ORM serialization and
    common configuration.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        validate_assignment=True,
    )


class TimestampSchema(NovaQureSchema):
    """
    Adds timestamp fields shared by
    most response objects.
    """

    created_at: datetime
    updated_at: datetime
