from fastapi import HTTPException
from fastapi_pagination.ext.tortoise import paginate
from models import PresenceHistory, PresenceDetails
import schemas
from datetime import datetime
from tortoise.expressions import Q


class PresenceHistoryRepository:
    async def get(self) -> PresenceHistory:
        presence_history = PresenceHistory.all().prefetch_related("presence_detail")
        paginated_presence_history = await paginate(presence_history)
        return paginated_presence_history

    async def get_by_id(self, presence_history_id) -> PresenceHistory:
        presence_history = await PresenceHistory.get(
            id=presence_history_id
        ).prefetch_related("presence_detail")
        return presence_history

    async def update(
        self, id: str, presence_history_data: schemas.PresenceHistoryUpdate
    ) -> PresenceHistory:
        presence_history = {
            "profile_id": presence_history_data.profile_id,
            "check_in": presence_history_data.check_in,
            "check_out": presence_history_data.check_out,
            "status": presence_history_data.status,
        }
        presence_detail = {
            "checkin_location": presence_history_data.checkin_location,
            "checkout_location": presence_history_data.checkout_location,
            "checkin_image": presence_history_data.checkin_image,
            "checkout_image": presence_history_data.checkout_image,
        }
        await PresenceHistory.get(id=id).update(**presence_history)
        await PresenceDetails.get(presence_history_id=id).update(**presence_detail)

        presence_history_response = await PresenceHistory.get(id=id).prefetch_related(
            "presence_detail"
        )
        return schemas.PresenceHistoryResponse.from_orm(presence_history_response)

    async def checkin(
        self, presence_history_data: schemas.PresenceHistoryCheckIn
    ) -> PresenceHistory:
        presence_history = await PresenceHistory.create(**presence_history_data.__dict__)
        presence_detail = {
            "presence_history_id": presence_history.id,
            "checkin_location": presence_history_data.checkin_location,
            "checkin_image": presence_history_data.checkin_image,
        }
        await PresenceDetails.create(**presence_detail)
        await presence_history.fetch_related("presence_detail")
        return schemas.PresenceHistoryResponse.from_orm(presence_history)

    async def checkout(
        self, id: str, presence_history_data: schemas.PresenceHistoryCheckOut
    ) -> PresenceHistory:
        updated_presence_history = (
            await PresenceHistory.filter(Q(id=id) & Q(check_out=None))
            .first()
            .update(check_out=datetime.now())
        )

        if not updated_presence_history:
            raise HTTPException(400, "Anda belum checkin")

        update_history_detail = {
            "checkout_location": presence_history_data.checkout_location,
            "checkout_image": presence_history_data.checkout_image,
        }
        await PresenceDetails.filter(
            Q(presence_history_id=id)
            & Q(checkout_location=None)
            & Q(checkout_image=None)
        ).first().update(**update_history_detail)

        presence_history = await PresenceHistory.get(id=id).prefetch_related(
            "presence_detail"
        )
        return schemas.PresenceHistoryResponse.from_orm(presence_history)

    async def delete(self, presence_history_id: str) -> PresenceHistory:
        await PresenceHistory.filter(id=presence_history_id).delete()
        return "Ok"
