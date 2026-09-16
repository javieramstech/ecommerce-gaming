from fastapi.testclient import TestClient


def test_signup_success(client: TestClient):
    payload = {
        "email": "user@example.com",
        "full_name": "Test User",
        "password": "secretpassword123"
    }
    response = client.post("/api/v1/auth/signup", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "hashed_password" not in data


def test_signup_duplicate_email(client: TestClient):
    payload = {
        "email": "duplicate@example.com",
        "full_name": "User One",
        "password": "password123"
    }
    res1 = client.post("/api/v1/auth/signup", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/api/v1/auth/signup", json=payload)
    assert res2.status_code == 400
    assert "ya se encuentra registrado" in res2.json()["detail"]


def test_login_success(client: TestClient):
    # Registrar usuario
    client.post("/api/v1/auth/signup", json={
        "email": "loginuser@example.com",
        "full_name": "Login User",
        "password": "password123"
    })

    # Log in
    login_payload = {
        "email": "loginuser@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client: TestClient):
    client.post("/api/v1/auth/signup", json={
        "email": "wrongpwd@example.com",
        "full_name": "Wrong Password",
        "password": "correctpassword"
    })

    response = client.post("/api/v1/auth/login", json={
        "email": "wrongpwd@example.com",
        "password": "incorrectpassword"
    })
    assert response.status_code == 401


def test_get_me_endpoint(client: TestClient):
    # Register and login to get token
    client.post("/api/v1/auth/signup", json={
        "email": "me@example.com",
        "full_name": "Me User",
        "password": "password123"
    })
    token_res = client.post("/api/v1/auth/login", json={
        "email": "me@example.com",
        "password": "password123"
    })
    token = token_res.json()["access_token"]

    # Request /me with Bearer token
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "me@example.com"
