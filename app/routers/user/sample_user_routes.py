from fastapi import APIRouter, Depends, status
from pyflutterflow.logs import get_logger
from app.settings import get_settings
from app.services.sample_service import sample_service

logger = get_logger(__name__)
settings = get_settings()

router = APIRouter(
    prefix='/sample',
    tags=['Sample User Routes'],
)


@router.get('', status_code=status.HTTP_200_OK, response_model=dict)
async def get_items(items: dict = Depends(sample_service)):
    """
    User routes are for authenticated users, and are entry points
    for any business logic you want to perform. You can use the
    Depends keyword to inject service functions from the services
    directory, this keeping your view layer and service layers tidy.
    """
    return items
