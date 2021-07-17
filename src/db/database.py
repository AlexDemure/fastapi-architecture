from tortoise import Tortoise

from core.config import settings

MODELS_LIST = ["apps.accounts.models",]


async def sqlite_db_init():
    await Tortoise.init(
        db_url=settings.SQLITE_URI,
        modules={'models': MODELS_LIST}
    )
    # Generate the schema
    await Tortoise.generate_schemas()
