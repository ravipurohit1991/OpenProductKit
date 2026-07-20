from __future__ import annotations

from typing import Protocol

from .domain import GenerationRequest, ProviderResult


class AIProvider(Protocol):
    """An async-capable provider. A submission may also complete immediately."""

    name: str

    def submit(self, request: GenerationRequest) -> ProviderResult: ...

    def poll(self, request_id: str) -> ProviderResult: ...
