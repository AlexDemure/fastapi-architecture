from tortoise import Tortoise

from src.core.config import settings

MODELS_LIST = ["src.apps.accounts.models",]


async def sqlite_db_init():
    await Tortoise.init(
        db_url=settings.SQLITE_URI,
        modules={'models': MODELS_LIST}
    )
    # Generate the schema
    await Tortoise.generate_schemas()
