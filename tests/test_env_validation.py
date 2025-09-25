from pathlib import Path
import textwrap

from halai_config.env_validation import (
    ALLOW_EMPTY_KEYS,
    BOOLEAN_KEYS,
    REQUIRED_KEYS,
    EnvValidationError,
    load_env_file,
    parse_env_lines,
    strip_comments,
    validate_env,
    validate_env_file,
)


def build_valid_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for key in REQUIRED_KEYS:
        if key in BOOLEAN_KEYS:
            env[key] = "true"
        elif key in ALLOW_EMPTY_KEYS:
            env[key] = ""
        elif key == "N8N_PROTOCOL":
            env[key] = "https"
        elif key == "TRAEFIK_LOG_LEVEL":
            env[key] = "INFO"
        elif key == "N8N_PORT":
            env[key] = "5678"
        elif key == "QUEUE_BULL_REDIS_PORT":
            env[key] = "6379"
        elif key == "QUEUE_BULL_REDIS_DB":
            env[key] = "0"
        else:
            env[key] = "value"
    return env


def test_strip_comments_removes_inline_annotations():
    assert strip_comments("KEY=value # comment") == "KEY=value"
    assert strip_comments("# full line comment") == ""
    assert strip_comments("  KEY=value  ") == "KEY=value"


def test_parse_env_lines_handles_quotes_and_spacing():
    content = textwrap.dedent(
        """
        # comment
        KEY=value
        QUOTED="quoted=value"
        SPACED = spaced value
        EMPTY=
        """
    ).strip().splitlines()

    parsed = parse_env_lines(content)

    assert parsed["KEY"] == "value"
    assert parsed["QUOTED"] == "quoted=value"
    assert parsed["SPACED"] == "spaced value"
    assert parsed["EMPTY"] == ""


def test_validate_env_detects_missing_required_key():
    base_env = build_valid_env()

    missing_key = "TRAEFIK_ACME_EMAIL"
    base_env.pop(missing_key)

    errors = validate_env(base_env)

    assert EnvValidationError(key=missing_key, message="variabile mancante") in errors


def test_validate_env_allows_optional_empty_values():
    env = build_valid_env()
    for key in ALLOW_EMPTY_KEYS:
        env[key] = ""

    errors = validate_env(env)

    assert errors == []


def test_validate_env_file_matches_repository_example():
    path = Path(__file__).resolve().parent.parent / ".env.example"
    errors = validate_env_file(path)
    assert errors == []


def test_load_env_file_round_trip(tmp_path: Path):
    env_file = tmp_path / ".env"
    env_file.write_text("KEY=value\nBOOL=true\n", encoding="utf-8")

    env = load_env_file(env_file)

    assert env["KEY"] == "value"
    assert env["BOOL"] == "true"
