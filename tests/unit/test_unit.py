from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.exc import IntegrityError

from pizza_crm.api import dependencies
from pizza_crm.db.models.catalog import Catalog
from pizza_crm.db.models.composition import Composition
from pizza_crm.db.models.ingredient import Ingredient
from pizza_crm.db.models.user import User
from pizza_crm.exceptions import exceptions
from pizza_crm.models.tokens import Tokens
from pizza_crm.schemas.catalog import (
    CatalogCreateSchema,
    CatalogResponseSchema,
    CompositionSchema,
    IngredientSchema,
)
from pizza_crm.schemas.user import (
    ChangePasswordOneRequest,
    ChangePasswordThreeRequest,
    ChangePasswordTwoRequest,
    LoginUserRequest,
    RegisterUserRequest,
)
from pizza_crm.services import auth_service, catalog_service, db_service, notifications_service, redis_service


# ---------- schemas / simple models ----------

def test_user_schemas_validation_and_boundaries():
    user = RegisterUserRequest(
        name="Ivan",
        surname="Petrov",
        patronymic="Ivanovich",
        age=20,
        email="ivan@example.com",
        password="12345678",
    )
    assert user.email == "ivan@example.com"

    login = LoginUserRequest(email="ivan@example.com", password="12345678")
    assert login.password == "12345678"

    assert ChangePasswordOneRequest(email="ivan@example.com").email
    assert ChangePasswordTwoRequest(email="ivan@example.com", otp="123456").otp == "123456"
    assert ChangePasswordThreeRequest(email="ivan@example.com", new_password="12345678").new_password == "12345678"

    with pytest.raises(Exception):
        LoginUserRequest(email="bad", password="12345678")
    with pytest.raises(Exception):
        LoginUserRequest(email="ivan@example.com", password="short")


def test_catalog_schema_and_models():
    item = CatalogCreateSchema(
        title="Pepperoni",
        description="Pizza",
        price=Decimal("499.90"),
        image_url="image.png",
        is_active=True,
        composition=[{"quantity": 100, "is_optional": False, "ingredient": {"id": 1}}],
    )
    assert item.composition[0].ingredient.id == 1

    ingredient = Ingredient(id=1, name="Cheese", cost_per_unit=Decimal("2.5"), is_allergen=False)
    composition = Composition(quantity=100, is_optional=False, ingredient=ingredient)
    dish = Catalog(id=1, title="Pizza", description="Pizza", price=Decimal("500"), image_url="x", is_active=True)
    assert composition.quantity == 100
    assert dish.title == "Pizza"


def test_tokens_and_user_models():
    tokens = Tokens("access", "refresh")
    assert tokens.AccessToken == "access"
    assert tokens.RefreshToken == "refresh"

    user = User(name="A", surname="B", patronymic="C", age=20, password="hash", mail="a@example.com")
    assert user.name == "A"


# ---------- auth service ----------

def make_user(user_id=1, role="customer", password=None):
    return SimpleNamespace(
        id=user_id,
        role=role,
        password=password or auth_service.hash_password("password123"),
        name="Ivan",
        surname="Petrov",
        patronymic="Ivanovich",
        age=20,
        mail="ivan@example.com",
    )


def test_password_hash_and_verify():
    hashed = auth_service.hash_password("password123")
    assert hashed != "password123"
    assert auth_service.verify_password("password123", hashed) is True
    assert auth_service.verify_password("wrong", hashed) is False


def test_create_and_verify_token_and_pair():
    token = auth_service.create_token(
        "42", "admin", __import__("datetime").timedelta(minutes=5),
        auth_service.config.JWT_ACCESS_SECRET_KEY,
    )
    payload = auth_service.verify_token(token, auth_service.config.JWT_ACCESS_SECRET_KEY)
    assert payload["sub"] == "42"
    assert payload["role"] == "admin"

    pair = auth_service.create_tokens_pair("42", "admin")
    assert isinstance(pair, Tokens)
    assert auth_service.verify_token(pair.AccessToken, auth_service.config.JWT_ACCESS_SECRET_KEY)["sub"] == "42"
    assert auth_service.verify_token(pair.RefreshToken, auth_service.config.JWT_REFRESH_SECRET_KEY)["sub"] == "42"


def test_verify_token_invalid():
    with pytest.raises(exceptions.InvalidTokenError):
        auth_service.verify_token("not-a-token", auth_service.config.JWT_ACCESS_SECRET_KEY)


@pytest.mark.asyncio
async def test_register_success_and_duplicate():
    db = MagicMock()
    auth_service.db_service.find_user_by_email = AsyncMock(side_effect=[None, make_user()])
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    data = RegisterUserRequest(
        name="A", surname="B", patronymic="C", age=20,
        email="a@example.com", password="password123",
    )
    result = await auth_service.register_auth_service(db, data)
    assert result.mail == "a@example.com"
    db.add.assert_called_once()
    db.commit.assert_called_once()

    with pytest.raises(ValueError, match="exists"):
        await auth_service.register_auth_service(db, data)


@pytest.mark.asyncio
async def test_register_integrity_error():
    db = MagicMock()
    auth_service.db_service.find_user_by_email = AsyncMock(return_value=None)
    db.commit.side_effect = IntegrityError("insert", {}, Exception())

    data = RegisterUserRequest(
        name="A", surname="B", patronymic="C", age=20,
        email="a@example.com", password="password123",
    )
    with pytest.raises(ValueError, match="already exists"):
        await auth_service.register_auth_service(db, data)
    db.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_login_success_and_wrong_credentials():
    db = MagicMock()
    user = make_user()
    auth_service.db_service.find_user_by_email = AsyncMock(return_value=user)

    data = LoginUserRequest(email="ivan@example.com", password="password123")
    result_user, tokens = await auth_service.login_auth_service(db, data)
    assert result_user is user
    assert isinstance(tokens, Tokens)

    with pytest.raises(ValueError, match="Incorrect"):
        await auth_service.login_auth_service(
            db, LoginUserRequest(email="ivan@example.com", password="wrongpass")
        )

    auth_service.db_service.find_user_by_email = AsyncMock(return_value=None)
    with pytest.raises(ValueError, match="Incorrect"):
        await auth_service.login_auth_service(db, data)


@pytest.mark.asyncio
async def test_refresh_and_userdata_and_delete():
    db = MagicMock()
    user = make_user(user_id=7, role="admin")
    auth_service.db_service.find_user_by_id = AsyncMock(return_value=user)

    refresh = auth_service.create_tokens_pair("7", "admin").RefreshToken
    tokens, user_id = await auth_service.refresh_token_auth_service(db, refresh)
    assert isinstance(tokens, Tokens)
    assert user_id == 7

    access = tokens.AccessToken
    found = await auth_service.get_userdata_auth_service(db, access)
    assert found is user

    auth_service.db_service.delete_user = AsyncMock()
    await auth_service.delete_user_profile_auth_service(db, access)
    auth_service.db_service.delete_user.assert_awaited_once_with(db, 7)


@pytest.mark.asyncio
async def test_get_userdata_invalid_payload_and_delete():
    db = MagicMock()
    auth_service.db_service.find_user_by_id = AsyncMock(return_value=make_user())

    # token without sub
    import jwt
    token = jwt.encode({"role": "customer"}, auth_service.config.JWT_ACCESS_SECRET_KEY, algorithm="HS256")
    with pytest.raises(exceptions.InvalidTokenPayload):
        await auth_service.get_userdata_auth_service(db, token)

    auth_service.db_service.delete_user = AsyncMock()
    with pytest.raises(exceptions.InvalidTokenPayload):
        await auth_service.delete_user_profile_auth_service(db, token)

    valid = auth_service.create_tokens_pair("1", "customer").AccessToken
    await auth_service.delete_user_profile_auth_service(db, valid)
    auth_service.db_service.delete_user.assert_awaited_once_with(db, 1)


@pytest.mark.asyncio
async def test_save_refresh_token():
    db = MagicMock()
    await auth_service.save_refresh_token_to_db(db, 1, "refresh", "pytest")
    db.add.assert_called_once()
    db.commit.assert_called_once()
    token = db.add.call_args.args[0]
    assert token.user_id == 1
    assert token.refresh_token == "refresh"
    assert token.user_agent == "pytest"


@pytest.mark.asyncio
async def test_password_reset_service_flow(monkeypatch):
    db = MagicMock()
    user = make_user(user_id=5)
    monkeypatch.setattr(auth_service.db_service, "find_user_by_email", AsyncMock(return_value=user))
    monkeypatch.setattr(auth_service.redis_service, "gen_otp", AsyncMock(return_value="123456"))
    monkeypatch.setattr(auth_service.notifications_service, "send_letter_to_email", AsyncMock(return_value={"message": "ok"}))

    assert await auth_service.gen_otp_send_email(db, user.mail) is True
    auth_service.notifications_service.send_letter_to_email.assert_awaited_once()

    monkeypatch.setattr(auth_service.redis_service, "verify_otp_gen_reset_token", AsyncMock(return_value="reset"))
    assert await auth_service.verify_otp_gen_reset_token_auth_service(db, user.mail, "123456") == "reset"

    monkeypatch.setattr(auth_service.redis_service, "verify_reset_token", AsyncMock(return_value=True))
    monkeypatch.setattr(auth_service.db_service, "update_user_password", AsyncMock())
    await auth_service.verify_reset_token_change_password_auth_service(db, user.mail, "reset", "newpassword")
    auth_service.db_service.update_user_password.assert_awaited_once()


@pytest.mark.asyncio
async def test_password_reset_missing_user():
    db = MagicMock()
    auth_service.db_service.find_user_by_email = AsyncMock(return_value=None)

    with pytest.raises(exceptions.UserNotFoundError):
        await auth_service.gen_otp_send_email(db, "missing@example.com")
    with pytest.raises(exceptions.UserNotFoundError):
        await auth_service.verify_otp_gen_reset_token_auth_service(db, "missing@example.com", "123456")
    with pytest.raises(exceptions.UserNotFoundError):
        await auth_service.verify_reset_token_change_password_auth_service(db, "missing@example.com", "reset", "new")


# ---------- redis service ----------

class FakeRedis:
    def __init__(self):
        self.data = {}
        self.calls = []

    async def get(self, key):
        return self.data.get(key)

    async def set(self, key, value, ex=None):
        self.calls.append(("set", key, value, ex))
        self.data[key] = value
        return True

    async def delete(self, key):
        self.calls.append(("delete", key))
        self.data.pop(key, None)
        return 1


@pytest.mark.asyncio
async def test_redis_otp_and_reset_flow(monkeypatch):
    fake = FakeRedis()
    monkeypatch.setattr(redis_service, "redis_client", fake)
    monkeypatch.setattr(redis_service.secrets, "randbelow", lambda _: 0)

    assert redis_service.secrets.randbelow(10) == 0
    otp = await redis_service.gen_otp(1, exp=60)
    assert otp == "100000"
    assert fake.data["pwd_reset_otp:1"] == "100000"

    with pytest.raises(exceptions.OTPExists):
        await redis_service.gen_otp(1)

    with pytest.raises(exceptions.OTPNotMatch):
        await redis_service.verify_otp_gen_reset_token(1, "wrong")

    reset = await redis_service.verify_otp_gen_reset_token(1, "100000", exp=60)
    assert reset
    assert "pwd_reset_otp:1" not in fake.data

    fake.data["pwd_reset_otp:1"] = "100000"
    fake.data["reset_token:1"] = "existing"
    with pytest.raises(exceptions.ReetTokenExists):
        await redis_service.verify_otp_gen_reset_token(1, "100000")

    fake.data["reset_token:1"] = reset
    assert await redis_service.verify_reset_token(1, reset) is True
    with pytest.raises(exceptions.ResetTokenNotFound):
        await redis_service.verify_reset_token(1, reset)


@pytest.mark.asyncio
async def test_redis_missing_otp():
    fake = FakeRedis()
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(redis_service, "redis_client", fake)
    try:
        with pytest.raises(exceptions.OTPNotFound):
            await redis_service.verify_otp_gen_reset_token(99, "123456")
    finally:
        monkeypatch.undo()


# ---------- catalog service ----------

def catalog_input():
    return CatalogCreateSchema(
        title="Test Pizza",
        description="Description",
        price=Decimal("500"),
        image_url="image",
        is_active=True,
        composition=[{"quantity": 100, "is_optional": False, "ingredient": {"id": 1}}],
    )


@pytest.mark.asyncio
async def test_catalog_service_get_delete():
    db = MagicMock()
    catalog_service.db_service.get_full_catalog = AsyncMock(return_value=["pizza"])
    assert await catalog_service.get_catalog_catalog_service(db) == ["pizza"]

    catalog_service.db_service.delete_catalog_item = AsyncMock()
    assert await catalog_service.delete_catalog_item_catalog_service(db, 1) is None
    catalog_service.db_service.delete_catalog_item.assert_awaited_once_with(db, 1)


@pytest.mark.asyncio
async def test_catalog_service_add_success_and_missing_ingredient():
    db = MagicMock()
    ingredient = SimpleNamespace(id=1)
    catalog_service.db_service.find_ingredient_by_id = AsyncMock(return_value=ingredient)

    item = await catalog_service.add_new_catalog_item_catalog_service(db, catalog_input())
    assert item.title == "Test Pizza"
    assert db.add.call_count == 2
    db.commit.assert_called_once()

    catalog_service.db_service.find_ingredient_by_id = AsyncMock(return_value=None)
    with pytest.raises(exceptions.ErrorCreatingDish):
        await catalog_service.add_new_catalog_item_catalog_service(db, catalog_input())
    db.rollback.assert_called()


@pytest.mark.asyncio
async def test_catalog_service_update_success_missing_and_error():
    db = MagicMock()
    existing = Catalog(id=10, title="Old", description="Old", price=100, image_url="old", is_active=True)
    catalog_service.db_service.find_catalog_item_by_id = AsyncMock(return_value=existing)
    catalog_service.db_service.delete_compositions = AsyncMock()
    catalog_service.db_service.find_ingredient_by_id = AsyncMock(return_value=SimpleNamespace(id=1))

    updated = await catalog_service.update_catalog_item_catalog_service(db, 10, catalog_input())
    assert updated.title == "Test Pizza"
    catalog_service.db_service.delete_compositions.assert_awaited_once_with(db, 10)

    catalog_service.db_service.find_catalog_item_by_id = AsyncMock(return_value=None)
    with pytest.raises(exceptions.ErrorCreatingDish):
        await catalog_service.update_catalog_item_catalog_service(db, 10, catalog_input())

    catalog_service.db_service.find_catalog_item_by_id = AsyncMock(return_value=existing)
    catalog_service.db_service.find_ingredient_by_id = AsyncMock(return_value=None)
    with pytest.raises(exceptions.ErrorCreatingDish):
        await catalog_service.update_catalog_item_catalog_service(db, 10, catalog_input())


# ---------- db service ----------

def query_result(value):
    q = MagicMock()
    q.filter.return_value = q
    q.options.return_value = q
    q.first.return_value = value
    q.delete.return_value = 1
    return q


@pytest.mark.asyncio
async def test_db_service_user_operations():
    db = MagicMock()
    user = make_user()
    db.query.return_value = query_result(user)

    assert await db_service.find_user_by_email(db, "ivan@example.com") is user
    assert await db_service.find_user_by_id(db, 1) is user
    await db_service.delete_user(db, 1)
    db.delete.assert_called_once_with(user)
    db.commit.assert_called()

    db.query.return_value = query_result(None)
    with pytest.raises(exceptions.UserNotFoundError):
        await db_service.find_user_by_id(db, 99)
    with pytest.raises(exceptions.UserNotFoundError):
        await db_service.delete_user(db, 99)


@pytest.mark.asyncio
async def test_db_service_catalog_operations():
    db = MagicMock()
    item = SimpleNamespace(id=2)
    db.query.return_value = query_result(item)

    assert await db_service.find_ingredient_by_id(db, 1) is item
    assert await db_service.find_catalog_item_by_id(db, 2) is item
    await db_service.delete_catalog_item(db, 2)
    db.delete.assert_called_with(item)

    db.query.return_value = query_result(None)
    with pytest.raises(exceptions.DishNotFound):
        await db_service.delete_catalog_item(db, 404)

    catalog_query = query_result(["catalog"])
    db.query.return_value = catalog_query
    assert await db_service.get_full_catalog(db) is catalog_query

    db.query.return_value = query_result(None)
    await db_service.delete_compositions(db, 2)


@pytest.mark.asyncio
async def test_db_service_update_password():
    db = MagicMock()
    user = make_user()
    db.query.return_value = query_result(user)
    await db_service.update_user_password(db, 1, "newhash")
    assert user.password == "newhash"
    db.commit.assert_called()


# ---------- dependencies / notifications ----------

@pytest.mark.asyncio
async def test_dependencies_current_user_and_roles():
    token = auth_service.create_tokens_pair("12", "admin").AccessToken
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    context = await dependencies.get_current_user_context(credentials)
    assert context == {"user_id": 12, "user_role": "admin"}

    checker = dependencies.require_role(["admin"])
    assert await checker(context) == context

    with pytest.raises(exceptions.PermissionDenied):
        await dependencies.require_role(["kitchen"])(context)

    bad = HTTPAuthorizationCredentials(scheme="Bearer", credentials="bad")
    with pytest.raises(exceptions.InvalidTokenError):
        await dependencies.get_current_user_context(bad)


@pytest.mark.asyncio
async def test_dependencies_invalid_payload():
    import jwt
    token = jwt.encode({"sub": "12"}, auth_service.config.JWT_ACCESS_SECRET_KEY, algorithm="HS256")
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    with pytest.raises(exceptions.InvalidTokenPayload):
        await dependencies.get_current_user_context(credentials)


@pytest.mark.asyncio
async def test_notifications_success_and_failure(monkeypatch):
    class FakeFM:
        def __init__(self, config):
            pass

        async def send_message(self, message):
            return None

    monkeypatch.setattr(notifications_service, "FastMail", FakeFM)
    result = await notifications_service.send_letter_to_email("Subject", "Text", "a@example.com")
    assert result["message"].startswith("OTP")

    class BrokenFM(FakeFM):
        async def send_message(self, message):
            raise RuntimeError("smtp down")

    monkeypatch.setattr(notifications_service, "FastMail", BrokenFM)
    with pytest.raises(exceptions.OTPErrorSending):
        await notifications_service.send_letter_to_email("Subject", "Text", "a@example.com")


# ---------- database models ----------

def test_database_model_metadata():
    assert User.__tablename__ == "users"
    assert Catalog.__tablename__ == "catalog"
    assert Ingredient.__tablename__ == "ingredients"
    assert Composition.__tablename__ == "composition"
    assert "role" in User.__table__.columns
    assert "price" in Catalog.__table__.columns
    assert "cost_per_unit" in Ingredient.__table__.columns
