from fastapi import APIRouter
from fastapi_pagination import Page
import schemas
from repositories.presence_history import PresenceHistoryRepository

router = APIRouter(tags=["Presence History"])
presence_history = PresenceHistoryRepository()


@router.get("/presence-history", response_model=Page[schemas.PresenceHistoryResponse])
async def route_get():
    return await presence_history.get()


@router.get("/presence-history/{id}", response_model=schemas.PresenceHistoryResponse)
async def route_get_by_id(id: str):
    return await presence_history.get_by_id(id)


@router.put("/presence-history/{id}", response_model=schemas.PresenceHistoryResponse)
async def route_update(
    id: str, request_presence_history: schemas.PresenceHistoryUpdate
):
    return await presence_history.update(id, request_presence_history)


@router.post("/presence-check-in")
async def route_checkin(request_presence_history: schemas.PresenceHistoryCheckIn):
    return await presence_history.checkin(request_presence_history)


@router.put("/presence-check-out/{id}", response_model=schemas.PresenceHistoryResponse)
async def route_checkout(
    id: str, request_presence_history: schemas.PresenceHistoryCheckOut
):
    return await presence_history.checkout(id, request_presence_history)


@router.delete("/presence-history/{id}")
async def route_delete(id: str):
    return await presence_history.delete(id)
