from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "presence_history" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "profile_id" UUID NOT NULL,
    "check_in" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "check_out" TIMESTAMPTZ,
    "status" VARCHAR(50) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "presence_details" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "checkin_location" VARCHAR(255) NOT NULL,
    "checkout_location" VARCHAR(255),
    "checkin_image" VARCHAR(255) NOT NULL,
    "checkout_image" VARCHAR(255),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "presence_history_id" UUID NOT NULL REFERENCES "presence_history" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
