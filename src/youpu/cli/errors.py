from __future__ import annotations

from dataclasses import dataclass


EXIT_OK = 0
EXIT_VALIDATION_FAILED = 1
EXIT_USAGE_ERROR = 2
EXIT_RUNTIME_ERROR = 3


@dataclass(frozen=True)
class CliError(Exception):
    message: str
    exit_code: int = EXIT_RUNTIME_ERROR

    def __str__(self) -> str:
        return self.message


class UsageError(CliError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, exit_code=EXIT_USAGE_ERROR)


class RuntimeCliError(CliError):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, exit_code=EXIT_RUNTIME_ERROR)
