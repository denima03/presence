from pydantic import BaseModel, UUID4
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator
from models import PresenceHistory


class PresenceHistoryCheckIn(BaseModel):
    profile_id: UUID4
    status: str
    checkin_location: str
    checkin_image: str


class PresenceHistoryUpdate(BaseModel):
    profile_id: UUID4
    status: str
    check_in: datetime
    check_out: datetime
    checkin_location: str
    checkout_location: str
    checkin_image: str
    checkout_image: str


class PresenceHistoryCheckOut(BaseModel):
    checkout_location: str
    checkout_image: str


class PresenceDetailsResponse(BaseModel):
    id: UUID4
    checkin_location: str
    checkout_location: str | None = None
    checkin_image: str
    checkout_image: str | None = None

    class Config:
        from_attributes = True


class PresenceHistoryResponse(pydantic_model_creator(PresenceHistory, exclude=["created_at", "updated_at"])):
    presence_detail: list[PresenceDetailsResponse]

    class Config:
        from_attributes = True
