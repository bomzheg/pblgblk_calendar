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

    @property
    def fullname(self) -> str:
        if self.first_name is None:
            return ""
        if self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @property
    def name_mention(self) -> str:
        return self.fullname or self.username or str(self.tg_id) or str(self.db_id) or "unknown"

