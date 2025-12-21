from datetime import date

from sqlalchemy import BigInteger, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.plaining import entity
from app.models import dto
from app.models.db.base import Base


class BusyDay(Base):
    __tablename__ = "busy_date"
    __mapper_args__ = {"eager_defaults": True}  # noqa: RUF012
    __table_args__ = (UniqueConstraint("user_id", "date_", name="busy_date_uc"),)
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    busy: Mapped[bool] = mapped_column(default=False, nullable=False)
    user_id: Mapped[dto.UserId] = mapped_column(ForeignKey("users.id"), nullable=False)
    date_: Mapped[date] = mapped_column(Date, nullable=False)

    def __repr__(self) -> str:
        return f"<BusyDay ID={self.id} date={self.date_} {self.user_id}>"

    def to_dto(self) -> entity.BusyDay:
        return entity.BusyDay(
            id=self.id,
            _date=self.date_,
            is_busy=self.busy,
        )
