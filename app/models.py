from tortoise.models import Model
from tortoise import fields
import uuid


class PresenceHistory(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    profile_id = fields.UUIDField()
    check_in = fields.DatetimeField(auto_now_add=True)
    check_out = fields.DatetimeField(null=True)
    status = fields.CharField(max_length=50)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "presence_history"


class PresenceDetails(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    presence_history = fields.ForeignKeyField(
        "models.PresenceHistory",
        related_name="presence_detail",
        on_delete=fields.CASCADE,
    )
    checkin_location = fields.CharField(max_length=255)
    checkout_location = fields.CharField(max_length=255, null=True)
    checkin_image = fields.CharField(max_length=255)
    checkout_image = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "presence_details"
