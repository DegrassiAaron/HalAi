"""Helpers for validating `.env` files used by HalAi."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional

CommentStrippedLine = str


@dataclass(frozen=True)
class EnvValidationError:
    """Represents a single validation issue detected in an env file."""

    key: Optional[str]
    message: str

    def __str__(self) -> str:  # pragma: no cover - trivial
        if self.key is None:
            return self.message
        return f"{self.key}: {self.message}"


REQUIRED_KEYS: tuple[str, ...] = (
    "COMPOSE_PROJECT_NAME",
    "TZ",
    "TRAEFIK_ACME_EMAIL",
    "TRAEFIK_DOMAIN",
    "TRAEFIK_DASHBOARD_DOMAIN",
    "TRAEFIK_LOG_LEVEL",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
    "REDIS_PASSWORD",
    "N8N_HOST",
    "N8N_PORT",
    "N8N_PROTOCOL",
    "N8N_ENCRYPTION_KEY",
    "N8N_BASIC_AUTH_ACTIVE",
    "N8N_BASIC_AUTH_USER",
    "N8N_BASIC_AUTH_PASSWORD",
    "N8N_JWT_SECRET",
    "N8N_EDITOR_BASE_URL",
    "N8N_API_BASE_URL",
    "QUEUE_BULL_REDIS_HOST",
    "QUEUE_BULL_REDIS_PORT",
    "QUEUE_BULL_REDIS_DB",
    "OPEN_WEBUI_DOMAIN",
    "OLLAMA_GPU",
    "COMFYUI_DOMAIN",
    "COMFYUI_GIT_REF",
)

ALLOW_EMPTY_KEYS: frozenset[str] = frozenset({"REDIS_PASSWORD"})
BOOLEAN_KEYS: frozenset[str] = frozenset({"N8N_BASIC_AUTH_ACTIVE", "OLLAMA_GPU"})
LOG_LEVELS: frozenset[str] = frozenset({"DEBUG", "INFO", "WARN", "WARNING", "ERROR"})
PROTOCOLS: frozenset[str] = frozenset({"http", "https"})


def load_env_file(path: Path) -> Dict[str, str]:
    """Load an env file into a dictionary."""

    with path.open("r", encoding="utf-8") as file:
        lines = file.readlines()
    return parse_env_lines(lines)


def parse_env_lines(lines: Iterable[str]) -> Dict[str, str]:
    data: Dict[str, str] = {}
    for raw_line in lines:
        line = strip_comments(raw_line)
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        data[key] = _unquote(value)
    return data


def strip_comments(line: str) -> CommentStrippedLine:
    """Remove inline comments and whitespace from a line."""

    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return ""
    escaped = False
    result_chars: List[str] = []
    for char in stripped:
        if char == "\\" and not escaped:
            escaped = True
            result_chars.append(char)
            continue
        if char == "#" and not escaped:
            break
        escaped = False
        result_chars.append(char)
    return "".join(result_chars).strip()


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def validate_env(env: Mapping[str, str]) -> List[EnvValidationError]:
    errors: List[EnvValidationError] = []

    for key in REQUIRED_KEYS:
        if key not in env:
            errors.append(EnvValidationError(key=key, message="variabile mancante"))
            continue
        if key not in ALLOW_EMPTY_KEYS and env[key] == "":
            errors.append(EnvValidationError(key=key, message="valore obbligatorio mancante"))

    for key in BOOLEAN_KEYS:
        if key in env and env[key].lower() not in {"true", "false"}:
            errors.append(
                EnvValidationError(
                    key=key,
                    message="valore booleano non valido (usa 'true' o 'false')",
                )
            )

    protocol = env.get("N8N_PROTOCOL")
    if protocol and protocol.lower() not in PROTOCOLS:
        errors.append(
            EnvValidationError(
                key="N8N_PROTOCOL", message="protocollo non valido (http/https)"
            )
        )

    log_level = env.get("TRAEFIK_LOG_LEVEL")
    if log_level and log_level.upper() not in LOG_LEVELS:
        errors.append(
            EnvValidationError(
                key="TRAEFIK_LOG_LEVEL",
                message="livello log non valido",
            )
        )

    for numeric_key in ("N8N_PORT", "QUEUE_BULL_REDIS_PORT", "QUEUE_BULL_REDIS_DB"):
        value = env.get(numeric_key)
        if value and not value.isdigit():
            errors.append(
                EnvValidationError(
                    key=numeric_key,
                    message="deve essere un numero intero positivo",
                )
            )

    return errors


def validate_env_file(path: Path) -> List[EnvValidationError]:
    env = load_env_file(path)
    return validate_env(env)


__all__ = [
    "EnvValidationError",
    "load_env_file",
    "parse_env_lines",
    "strip_comments",
    "validate_env",
    "validate_env_file",
]
