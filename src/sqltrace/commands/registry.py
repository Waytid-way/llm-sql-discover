"""Stable extension point for isolated CLI command modules."""

from __future__ import annotations

import importlib
import pkgutil


from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class CommandRegistry:
    def __init__(self) -> None:
        self._commands: dict[str, Callable[..., Any]] = {}
        self._app: Any | None = None

    def bind(self, app: Any) -> None:
        self._app = app
        for name, function in self.items():
            self._bind_one(name, function)

    def _bind_one(self, name: str, function: Callable[..., Any]) -> None:
        commands = getattr(self._app, "registered_commands", ()) if self._app is not None else ()
        if self._app is not None and not any(command.name == name for command in commands):
            self._app.command(name)(function)

    def command(self, name: str) -> Callable[[F], F]:
        if not name or name in self._commands:
            raise ValueError(f"duplicate command: {name}")

        def register(function: F) -> F:
            self._commands[name] = function
            self._bind_one(name, function)
            return function

        return register

    def get(self, name: str) -> Callable[..., Any]:
        return self._commands[name]

    def items(self) -> tuple[tuple[str, Callable[..., Any]], ...]:
        return tuple(sorted(self._commands.items()))

    def discover(self, package_name: str = "sqltrace.commands") -> tuple[str, ...]:
        package = importlib.import_module(package_name)
        names = sorted(
            module.name
            for module in pkgutil.iter_modules(package.__path__, f"{package_name}.")
            if module.name.rsplit(".", 1)[-1] not in {"registry", "__init__"}
        )
        for module_name in names:
            importlib.import_module(module_name)
        return tuple(names)


registry = CommandRegistry()

__all__ = ["CommandRegistry", "registry"]
