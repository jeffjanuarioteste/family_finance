from httpx import AsyncClient


async def test_saude_ok(api: AsyncClient) -> None:
    response = await api.get("/api/v1/saude")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "banco": "ok"}


async def test_openapi_valido(api: AsyncClient) -> None:
    response = await api.get("/openapi.json")
    assert response.status_code == 200
    assert "/api/v1/saude" in response.json()["paths"]
