from typing import AsyncGenerator, AsyncIterable, Iterable, Union

async def as_async_generator(it: Union[Iterable, AsyncIterable]) -> AsyncGenerator:
    """Wraps an iterable (sync or async) into an async generator."""
    pass