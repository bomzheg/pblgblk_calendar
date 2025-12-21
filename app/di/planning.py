from dishka import Provider, Scope, provide

from app.core.plaining.interactors import BusyDaysReaderInteractor, FlipDayBusyInteractor


class PlanningProvider(Provider):
    scope = Scope.REQUEST

    reader_interactor = provide(BusyDaysReaderInteractor)
    flip_interactor = provide(FlipDayBusyInteractor)
