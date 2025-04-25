"""
Test_crud.py is a generic test module for saving time on writing CRUD tests for each resource.
While always remembering that the whole point of testing to to ensure consistency and functionality
of logic well beyond CRUD, it's also reassuring to know that your RLS policies are working as they
should be for each and every table.

Remember, this module is not here to replace proper testing, and you should have test modules covering
each and every endpoint. However, this module can save you from writing the exact same test for different
tables over and over.

Simply follow the convention of the example in the TEST_CONFIG dictionary, providing the table name as
the dictionary key and adding sample data where appropriate.
"""
import pytest
from app.tests.fixtures.sample_data import sample_notification
from app.tests.fixtures.sample_users import rocket

TEST_CONFIG = {
    "notifications": {
        "sample_data": sample_notification,
        "sample_field": "is_read",
        "update_sample_field_to": True
    }
}


@pytest.fixture(scope="function")
async def create_resource(resource_name, async_client, login_as_rocket):
    response = await async_client.post(
        f"/supabase/rest/v1/{resource_name}",
        json={"user_id": rocket.uid, **TEST_CONFIG[resource_name]['sample_data']},
        headers={"Prefer": "return=representation", "Accept": "application/vnd.pgrst.object+json"}
    )
    assert response.status_code == 201
    return response.json()


@pytest.mark.parametrize("resource_name", TEST_CONFIG.keys())
async def test_user_can_see_their_resource_list(async_client, resource_name, create_resource, login_as_rocket):
    response = await async_client.get(f"/supabase/rest/v1/{resource_name}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == create_resource


@pytest.mark.parametrize("resource_name", TEST_CONFIG.keys())
async def test_user_can_create_a_resource(async_client, resource_name, create_resource, login_as_rocket):
    sample_field = TEST_CONFIG[resource_name]['sample_field']
    assert create_resource[sample_field] == TEST_CONFIG[resource_name]['sample_data'][sample_field]


@pytest.mark.parametrize("resource_name", TEST_CONFIG.keys())
async def test_user_cannot_see_another_users_resources_list(async_client, resource_name, create_resource, login_as_quill):
    response = await async_client.get(f"/supabase/rest/v1/{resource_name}")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize("resource_name", TEST_CONFIG.keys())
async def test_user_can_get_their_resource(async_client, resource_name, create_resource, login_as_rocket):
    response = await async_client.get(
        f"/supabase/rest/v1/{resource_name}?id=eq.{create_resource['id']}",
        headers={"Prefer": "return=representation", "Accept": "application/vnd.pgrst.object+json"}
    )
    assert response.status_code == 200
    assert response.json() == create_resource


@pytest.mark.parametrize("resource_name", TEST_CONFIG.keys())
async def test_user_cannot_get_another_users_resource(async_client, resource_name, create_resource, login_as_quill):
    response = await async_client.get(
        f"/supabase/rest/v1/{resource_name}?id=eq.{create_resource['id']}",
        headers={"Prefer": "return=representation", "Accept": "application/vnd.pgrst.object+json"}
    )
    assert response.status_code == 406


@pytest.mark.parametrize("resource_name", TEST_CONFIG.keys())
async def test_user_can_update_their_resource(async_client, resource_name, create_resource, login_as_rocket):
    sample_field = TEST_CONFIG[resource_name]['sample_field']
    update_sample_field_to = TEST_CONFIG[resource_name]['update_sample_field_to']
    response = await async_client.patch(
        f"/supabase/rest/v1/{resource_name}?id=eq.{create_resource['id']}",
        json={sample_field: update_sample_field_to},
        headers={"Prefer": "return=representation", "Accept": "application/vnd.pgrst.object+json"}
    )
    assert response.status_code == 200
    assert response.json()[sample_field] ==  update_sample_field_to


@pytest.mark.parametrize("resource_name", TEST_CONFIG.keys())
async def test_user_cannot_update_another_users_resource(async_client, resource_name, create_resource, login_as_quill):
    sample_field = TEST_CONFIG[resource_name]['sample_field']
    update_sample_field_to = TEST_CONFIG[resource_name]['update_sample_field_to']
    response = await async_client.patch(
        f"/supabase/rest/v1/{resource_name}?id=eq.{create_resource['id']}",
        json={sample_field: update_sample_field_to},
        headers={"Prefer": "return=representation", "Accept": "application/vnd.pgrst.object+json"}
    )
    assert response.status_code == 406


@pytest.mark.parametrize("resource_name", TEST_CONFIG.keys())
async def test_user_can_delete_their_resource(async_client, resource_name, create_resource, login_as_rocket):
    response = await async_client.delete(
        f"/supabase/rest/v1/{resource_name}?id=eq.{create_resource['id']}",
        headers={"Prefer": "return=representation", "Prefer": "return=minimal", "Accept": "application/vnd.pgrst.object+json"}
    )
    assert response.status_code == 204


@pytest.mark.parametrize("resource_name", TEST_CONFIG.keys())
async def test_user_cannot_delete_another_users_resource(async_client, resource_name, create_resource, login_as_quill):
    response = await async_client.delete(
        f"/supabase/rest/v1/{resource_name}?id=eq.{create_resource['id']}",
        headers={"Prefer": "return=representation", "Prefer": "return=minimal", "Accept": "application/vnd.pgrst.object+json"}
    )
    assert response.status_code == 406
