import typing
from typing import AsyncIterable

from dishka import AsyncContainer, Provider, Scope, provide

from app.infrastructure.nursery import AppNursery, NurseryImpl, RequestNursery


class NurseryProvider(Provider):
    @provide(scope=Scope.APP)
    async def app_nursery(self, dishka: AsyncContainer) -> AsyncIterable[AppNursery]:
        async with NurseryImpl(container=dishka) as nursery:
            yield typing.cast(AppNursery, nursery)

    @provide(scope=Scope.REQUEST)
    async def request_nursery(self, dishka: AsyncContainer) -> AsyncIterable[RequestNursery]:
        async with NurseryImpl(container=dishka) as nursery:
            yield typing.cast(RequestNursery, nursery)
