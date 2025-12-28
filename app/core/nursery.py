import asyncio
import typing


class Nursery(typing.Protocol):
    def __call__[**P, T](
        self,
        func: typing.Callable[P, typing.Coroutine[typing.Any, typing.Any, T]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> asyncio.Task[T]:
        raise NotImplementedError
