from io import BytesIO

import pytest
from PIL import Image

from cryptoapp.infrastructure.persistence.gateways.user_mapper import (
    UserMapper,
)
from httpx import AsyncClient


global_data = {
    "username": "pc"
}

@pytest.mark.asyncio(loop_scope="session")
async def test_success_register(
    http_client: AsyncClient, email, scoped_container
):
    data = {"username": global_data["username"], "email": email, "password": "pc"}

    response = await http_client.post(url="auth/register", json=data)

    assert response.status_code == 201
    assert response.json() == {
        "message": "Registration was successful. Please check your email."
    }

    user_mapper = await scoped_container.get(UserMapper)

    user = await user_mapper.by_username(username=data["username"])

    user.activate()

    await user_mapper._session.commit()


@pytest.mark.asyncio(loop_scope="session")
async def test_login_success(http_client, container):
    username = "pc"
    password = "pc"

    response = await http_client.post(
        "auth/login", json={"username": username, "password": password}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "You have successfully logged in."}

def image_bytes():
    image = Image.new(
        "RGB", (1, 1), color=(255, 0, 0)
    )
    image_bytes_io = BytesIO()
    image.save(image_bytes_io, format="JPEG")
    image_bytes = image_bytes_io.getvalue()
    return image_bytes

@pytest.mark.asyncio(loop_scope="session")
async def test_create_portfolio(http_client, container):
    name = "Test Portfolio"
    file_content = image_bytes()
    file_name = "avatar.jpg"

    files = {"loaded_file": (file_name, BytesIO(file_content), "image/jpeg")}

    response = await http_client.post(
        "/portfolios/",
        data={"name": name},
        files=files,
    )

    assert response.status_code == 201
    response_data = response.json()

    assert response_data["name"] == name
    assert "portfolio_id" in response_data
    assert isinstance(
        response_data["avatar"], str
    )

    global_data.update(
        portfolio_id=response_data["portfolio_id"]
    )



