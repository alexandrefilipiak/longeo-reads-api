from firebase_admin import credentials as firebase_credentials, initialize_app as init_firebase, get_app as get_firebase_app
from pyflutterflow.logs import get_logger
from app.settings import get_settings

logger = get_logger(__name__)
settings = get_settings()


async def initialize_firebase_admin():
    """
    Initialize the Firebase Admin SDK if it hasn't been initialized already. This will
    work automatically in GCP environments or local environments that have set up gcloud.

    You can also set the FIREBASE_CONFIG environment variable.
    """
    try:
        get_firebase_app()
    except ValueError:
        if not settings.firebase_config:
            init_firebase()
        else:
            init_firebase(firebase_credentials.Certificate(settings.firebase_config))
