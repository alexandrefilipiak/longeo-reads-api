import pytest
import pytest_asyncio
import asyncio
from app.main import app
from httpx import AsyncClient
from pyflutterflow.auth import get_current_user, get_admin_user, FirebaseUser
from app.tests.fixtures.sample_users import admin, quill, rocket
from pyflutterflow.database.supabase.supabase_client import SupabaseClient
from pyflutterflow.logs import get_logger
from app.settings import get_settings

settings = get_settings()
logger = get_logger(__name__)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def create_user(user: FirebaseUser):
    client = await SupabaseClient().get_client()
    await client.table(settings.users_table).upsert({
        "id": user.uid,
        "email": user.email
    }).execute()


@pytest_asyncio.fixture(loop_scope="function")
async def reset_db():
    if 'localhost' not in settings.supabase_url and '127.0.0.1' not in settings.supabase_url:
        pytest.exit("Refusing to reset the database: this doesn't seem to be a local connection. Are you connecting to the local test database?")
    client = await SupabaseClient().get_client()
    await client.table('users').delete().neq("id", "xxx").execute()
    await client.table('notifications').delete().gt("id", 0).execute()
    await create_user(quill)
    await create_user(rocket)
    await create_user(admin)


@pytest_asyncio.fixture(loop_scope="function")
async def async_client(reset_db):
    async with AsyncClient(app=app, base_url="http://localhost:8000") as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="function")
async def login_as_quill():
    app.dependency_overrides[get_current_user] = lambda: quill
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def login_as_rocket():
    app.dependency_overrides[get_current_user] = lambda: rocket
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def login_as_admin():
    app.dependency_overrides[get_current_user] = lambda: admin
    app.dependency_overrides[get_admin_user] = lambda: admin
    yield
    app.dependency_overrides.clear()
