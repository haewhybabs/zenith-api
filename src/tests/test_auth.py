import pytest

@pytest.mark.asyncio
async def test_signup_and_login(client):
    #1. Test signup
    signup_data = {
        "username":"testuser",
        "email":"test@example.com",
        "password":"strongpassword123"
    }
    response = await client.post("/users/signup", json=signup_data)
    assert response.status_code ==201
    assert response.json()["email"] == "test@example.com"

    #2. Test Login
    login_data = {
        "username":"test@example.com",
        "password":"strongpassword123"
    }
    login_response = await client.post("/login", data=login_data)
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert login_response.json()["token_type"] == "bearer"