from dishka import Provider, Scope, provide

from app.core.plaining.interactors import (
    BusyDaysReaderInteractor,
    CalendarPainterInteractor,
    FlipDayBusyInteractor,
)
from app.core.plaining.interfaces import CalendarPainter
from app.infrastructure.painter import CalendarPainterImpl


class PlanningProvider(Provider):
    scope = Scope.REQUEST

    reader_interactor = provide(BusyDaysReaderInteractor)
    flip_interactor = provide(FlipDayBusyInteractor)
    painter_interactor = provide(CalendarPainterInteractor)

    @provide
    def get_painter(self) -> CalendarPainter:
        return CalendarPainterImpl()
