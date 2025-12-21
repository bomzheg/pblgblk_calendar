from aiogram.types import User

from app.core import users
from app.models import db

ID = 666
FIRST_NAME = "Harry"
LAST_NAME = "Potter"
USERNAME = "voldemort_killer"
DB_ID: users.UserId = 13


def create_tg_user(
    id_: int = ID,
    username: str = USERNAME,
    first_name: str = FIRST_NAME,
    last_name: str = LAST_NAME,
) -> User:
    return User(
        id=id_,
        username=username,
        first_name=first_name,
        last_name=last_name,
        is_bot=False,
    )


def create_dto_user() -> users.User:
    return users.User(
        tg_id=ID,
        db_id=DB_ID,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        username=USERNAME,
        is_bot=False,
    )


def create_create_user_dto() -> users.CreateUserData:
    return users.CreateUserData(
        tg_id=ID,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        username=USERNAME,
        is_bot=False,
    )


def create_db_user() -> db.User:
    return db.User(
        db_id=DB_ID,
        tg_id=ID,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        username=USERNAME,
        is_bot=False,
    )
