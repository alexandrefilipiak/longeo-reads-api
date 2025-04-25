from fastapi import APIRouter, Depends, status
from pyflutterflow.logs import get_logger
from pyflutterflow.auth import get_admin_user
from app.settings import get_settings
from app.services.sample_service import sample_service


logger = get_logger(__name__)
settings = get_settings()

router = APIRouter(
    prefix='/admin',
    tags=['Admin'],
    dependencies=[Depends(get_admin_user)]
)


@router.get('', status_code=status.HTTP_201_CREATED, response_model=dict)
async def get_all_items(items = Depends(sample_service)):
    """
    Admin routes are for admin users, which are defined as users who
    have the role 'admin' custom claims in the Firebase token. You can create
    admins using the create_admin.py script in the scripts/ directory.
    """
    return items
