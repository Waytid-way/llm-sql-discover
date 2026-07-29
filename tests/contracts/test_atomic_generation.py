from pathlib import Path

import pytest

from sqltrace.contracts.registry import write_atomic


def test_invalid_generation_preserves_previous_output(tmp_path: Path) -> None:
    target = tmp_path / "registry.json"
    target.write_text("previous", encoding="utf-8")
    with pytest.raises(ValueError):
        write_atomic(target, lambda: (_ for _ in ()).throw(ValueError("invalid")))
    assert target.read_text(encoding="utf-8") == "previous"


def test_cancelled_generation_does_not_publish_partial_output(tmp_path: Path) -> None:
    target = tmp_path / "registry.json"
    with pytest.raises(KeyboardInterrupt):
        write_atomic(target, lambda: (_ for _ in ()).throw(KeyboardInterrupt()))
    assert not target.exists()
