"""Load first-party product APIs without coupling them to the template.

Set ``APP_PRODUCT_ROUTERS`` to comma-separated import targets. Each target may
be a FastAPI ``APIRouter``, a ``FastAPI`` app, or a zero-argument factory that
returns either. This is the low-friction seam for bringing an existing backend
or wrapping an existing core; plugins remain the right seam for optional
third-party extensions.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any

from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute


class ProductRouterError(RuntimeError):
    """A configured product router could not be imported or validated."""


@dataclass(frozen=True, slots=True)
class LoadedProductRouter:
    target: str
    router: APIRouter


def parse_product_router_targets(value: str) -> list[str]:
    """Parse a comma-separated setting, preserving order and removing duplicates."""
    return list(dict.fromkeys(target.strip() for target in value.split(",") if target.strip()))


def _resolve_target(target: str) -> Any:
    module_name, separator, attribute_path = target.partition(":")
    if not separator or not module_name.strip() or not attribute_path.strip():
        raise ProductRouterError(
            f"Invalid product router '{target}'. Expected 'python.module:attribute'."
        )
    try:
        value: Any = import_module(module_name.strip())
    except (ImportError, ModuleNotFoundError) as exc:
        raise ProductRouterError(
            f"Could not import module '{module_name.strip()}' for product router "
            f"'{target}': {exc}"
        ) from exc
    try:
        for part in attribute_path.strip().split("."):
            value = getattr(value, part)
    except AttributeError as exc:
        raise ProductRouterError(
            f"Product router '{target}' has no attribute '{attribute_path.strip()}'."
        ) from exc
    return value


def _as_router(target: str, value: Any, *, call_factory: bool = True) -> APIRouter:
    if isinstance(value, APIRouter):
        return value
    if isinstance(value, FastAPI):
        # Import only API endpoints. The host keeps ownership of lifespan,
        # middleware, docs and static files; those cannot be safely merged.
        router = APIRouter()
        router.routes.extend(route for route in value.routes if isinstance(route, APIRoute))
        return router
    if call_factory and callable(value):
        try:
            built = value()
        except Exception as exc:
            raise ProductRouterError(
                f"Product router factory '{target}' failed: {exc}"
            ) from exc
        return _as_router(target, built, call_factory=False)
    raise ProductRouterError(
        f"Product router '{target}' must be an APIRouter, FastAPI app, or "
        "zero-argument factory returning one."
    )


def load_product_routers(value: str) -> list[LoadedProductRouter]:
    """Import and validate every router configured in ``APP_PRODUCT_ROUTERS``."""
    return [
        LoadedProductRouter(target=target, router=_as_router(target, _resolve_target(target)))
        for target in parse_product_router_targets(value)
    ]


def mount_product_routers(app: FastAPI, value: str) -> list[LoadedProductRouter]:
    """Include configured product APIs and return their validated descriptors."""
    loaded = load_product_routers(value)
    for item in loaded:
        app.include_router(item.router)
    return loaded
