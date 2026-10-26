from typing import Iterable

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.pool import StaticPool

from wapang.main import app
from wapang.app.users.models import User
from wapang.database.common import Base
from wapang.database.settings import DB_SETTINGS
from wapang.database.connection import get_db_session
from wapang.settings import ENV
 
# 하위 테스트 모듈에서 공통으로 사용할 플러그인/픽스처 로드
pytest_plugins = [
    "tests.stores.conftest",
    "tests.items.conftest",
]


@pytest.fixture(autouse=True, scope="session")
def set_test_env():
    ENV = "test"


@pytest.fixture(scope="function")
def db_engine(set_test_env) -> Iterable[sqlalchemy.Engine]:
    url = "sqlite:///:memory:"
    engine = sqlalchemy.create_engine(
        url,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)

    try:
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine: sqlalchemy.Engine) -> Iterable[orm.Session]:
    connection = db_engine.connect()
    transaction = connection.begin_nested()

    session_maker = orm.sessionmaker(
        connection,
        expire_on_commit=True,
    )

    session = session_maker()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session: orm.Session) -> Iterable[TestClient]:

    def override_get_db_session():
        return db_session

    app.dependency_overrides[get_db_session] = override_get_db_session
    client = TestClient(app)
    try:
        yield client
    finally:
        app.dependency_overrides.pop(get_db_session, None)
        client.close()

@pytest.fixture
def user(
    client: TestClient
) -> User:
    req = {
        "email": "test1234@snu.ac.kr",
        "password": "password123"
    }
    
    res = client.post("/api/users", json=req)
    res_json = res.json()
    
    return User(
        id=res_json["id"],
        email=res_json["email"],
        nickname=res_json.get("nickname"),
        address=res_json.get("address"),
        phone_number=res_json.get("phone_number")
    )
    
@pytest.fixture
def token(
    client: TestClient,
    user: User
) -> dict:
    req = {
        "email": "test1234@snu.ac.kr",
        "password": "password123"
    }
    res = client.post("/api/auth/tokens", json=req)
    res_json = res.json()
    
    return {
        "access_token": res_json["access_token"],
        "refresh_token": res_json["refresh_token"]
    }

@pytest.fixture
def access_token(
    token: dict
) -> str:
    return token["access_token"]

@pytest.fixture
def another_user_access_token(
    client: TestClient
) -> str:
    signup_req = {
        "email": "another_user@snu.ac.kr",
        "password": "password1234"
    }
    client.post("/api/users", json=signup_req)

    signin_req = signup_req
    res = client.post("/api/auth/tokens", json=signin_req)
    res_json = res.json()

    return res_json["access_token"]
