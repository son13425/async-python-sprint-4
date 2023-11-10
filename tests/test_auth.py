from conftest import client


def test_register_user():
    """Проверка успешной регистрации юзера"""
    response = client.post("/auth/register", json={
        "email": "user@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False
    })
    assert response.status_code == 201
