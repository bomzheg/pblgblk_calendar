import asyncio
import typing
from asyncio import TaskGroup
from inspect import Parameter
from typing import Any, Callable, Coroutine

from dishka import AsyncContainer
from dishka.integrations.base import wrap_injection

from app.core.nursery import Nursery


def inject_task[T: Coroutine](func: Callable[..., T]) -> Callable[..., T]:
    return wrap_injection(
        func=func,
        manage_scope=True,
        additional_params=[
            Parameter(
                name="dishka_container__",
                kind=Parameter.KEYWORD_ONLY,
                annotation=AsyncContainer,
            ),
        ],
        is_async=True,
        container_getter=lambda _, kwargs: kwargs["dishka_container__"],
    )


class NurseryImpl(Nursery):
    def __init__(self, container: AsyncContainer) -> None:
        self._container = container
        self._group = TaskGroup()

    def __call__[**P, T](
        self,
        func: Callable[P, Coroutine[Any, Any, T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> asyncio.Task[T]:
        return self._group.create_task(func(*args, **kwargs, dishka_container__=self._container))  # type: ignore[arg-type]

    async def __aenter__(self) -> "NurseryImpl":
        await self._group.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):  # noqa: ANN001, ANN204
        await self._group.__aexit__(exc_type, exc_val, exc_tb)


AppNursery = typing.NewType("AppNursery", NurseryImpl)
RequestNursery = typing.NewType("RequestNursery", NurseryImpl)
