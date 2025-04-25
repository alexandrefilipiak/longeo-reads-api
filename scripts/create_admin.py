import asyncio
from firebase_admin import auth
from firebase_admin import initialize_app
from pyflutterflow import constants
from pyflutterflow.logs import get_logger
from pyflutterflow.auth import set_admin_flag
from pyflutterflow import PyFlutterflow
from app.settings import get_settings

logger = get_logger(__name__)
settings = get_settings()


async def create_admin():
    PyFlutterflow(settings=settings).get_settings()
    initialize_app()

    user_uid = input("Enter the UID of the user you want to make an admin: ")
    try:
        auth.set_custom_user_claims(user_uid, {'role': constants.ADMIN_ROLE})
        await set_admin_flag(user_uid, is_admin=True)
        logger.info("User role %s was set for user %s", constants.ADMIN_ROLE, user_uid)
    except Exception as e:
        logger.error("Error encountered setting userrole: %s", e)



if __name__ == "__main__":
    asyncio.run(create_admin())
