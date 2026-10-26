import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def add_to_cart(client: TestClient, access_token: str):
	"""Helper to add or update a cart line for the logged-in user."""

	def _add(item_id: str, quantity: int):
		return client.patch(
			"/api/carts",
			json={"item_id": item_id, "quantity": quantity},
			headers={"Authorization": f"Bearer {access_token}"},
		)

	return _add


@pytest.fixture
def get_cart(client: TestClient, access_token: str):
	"""Helper to fetch the current cart for the logged-in user."""

	def _get():
		return client.get(
			"/api/carts",
			headers={"Authorization": f"Bearer {access_token}"},
		)

	return _get


@pytest.fixture
def clear_cart(client: TestClient, access_token: str):
	"""Helper to clear the cart for the logged-in user."""

	def _clear():
		return client.delete(
			"/api/carts",
			headers={"Authorization": f"Bearer {access_token}"},
		)

	return _clear


@pytest.fixture
def checkout_cart(client: TestClient, access_token: str):
	"""Helper to checkout the cart for the logged-in user."""

	def _checkout():
		return client.post(
			"/api/carts/checkout",
			headers={"Authorization": f"Bearer {access_token}"},
		)

	return _checkout

