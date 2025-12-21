import typing
from dataclasses import dataclass

UserId: typing.TypeAlias = int


@dataclass
class CreateUserData:
    tg_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_bot: bool | None = None


@dataclass(kw_only=True)
class User:
    tg_id: int
    db_id: UserId
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_bot: bool
