from app.tgbot.utils.mappers import user_tg_to_dto
from tests.fixtures.user_constants import create_create_user_dto, create_tg_user


def test_from_aiogram_to_dto() -> None:
    source = create_tg_user()
    expected = create_create_user_dto()
    actual = user_tg_to_dto(source)
    assert expected == actual
