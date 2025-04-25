from pyflutterflow.logs import get_logger
from app.settings import get_settings

settings = get_settings()
logger = get_logger(__name__)


async def sample_service() -> None:
    """
    Services help separate your view layer from your business logic layer.
    These service functions are usually responsible for error handling,
    interacting with the database layer and models, and other business logic.
    """

    # add some business logic here

    return
