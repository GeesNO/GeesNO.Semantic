"""Privacy-safe offline hygiene checks for public distribution files."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

RAW_FIXTURES = frozenset(
    {
        "conformance/invalid/raw-bom.raw",
        "conformance/invalid/raw-comment.raw",
        "conformance/invalid/raw-duplicate-extension-payload.raw",
        "conformance/invalid/raw-duplicate-nested-core.raw",
        "conformance/invalid/raw-duplicate-root.raw",
        "conformance/invalid/raw-invalid-utf8.raw",
        "conformance/invalid/raw-lone-surrogate.raw",
        "conformance/invalid/raw-non-object-root.raw",
        "conformance/invalid/raw-resource-refusal.raw",
        "conformance/invalid/raw-trailing-comma.raw",
    }
)

JUNK_PATH = re.compile(
    r"(?i)(?:\.bak|\.tmp|\.swp|\.orig|~|\.pyc)$|"
    r"(?:^|/)(?:\.DS_Store|Thumbs\.db|desktop\.ini|\.coverage)$|"
    r"(?:^|/)(?:__pycache__|\.pytest_cache|\.mypy_cache|htmlcov|dist|build|"
    r"\.venv|venv)(?:/|$)|\.egg-info(?:/|$)|(?:^|/)\.env(?:\.|$)|\.local$"
)
ARCHIVE_OR_BINARY = re.compile(
    r"(?i)\.(?:zip|tar|gz|tgz|7z|pdf|png|jpe?g|gif|webp|exe|dll|so|dylib|"
    r"db|sqlite|docx?|xlsx?|pptx?)$"
)
WINDOWS_RESERVED = re.compile(r"(?i)^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)")

# Keep pattern fragments separate so this checker does not flag its own source.
MACHINE_LOCAL = re.compile(
    r"(?i)(?:^|[^A-Za-z0-9])(?:[A-Za-z]:"
    + r"[\\/](?:Users|home|Genaro)[\\/]|/(?:Users|home)/[A-Za-z0-9._-]+/)"
)
SECRET_PATTERNS = (
    re.compile("-----BEGIN " + r"(?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(r"\bgh" + r"[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bA" + r"(?:KIA|SIA)[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    re.compile(
        r"(?i)\b(?:password|passwd|api[_-]?key|client[_-]?secret|"
        r"access[_-]?token|bearer)\s*[:=]\s*[A-Za-z0-9_./+=-]{8,}"
    ),
)


@dataclass(frozen=True)
class HygieneReport:
    tracked_paths: tuple[str, ...]
    machine_local_files: tuple[str, ...]
    secret_candidate_files: tuple[str, ...]
    junk_paths: tuple[str, ...]
    case_collisions: tuple[tuple[str, ...], ...]
    unsafe_paths: tuple[str, ...]
    symlink_paths: tuple[str, ...]
    submodule_paths: tuple[str, ...]
    lfs_required: bool
    raw_fixture_paths: tuple[str, ...]
    unexpected_binary_or_archive_paths: tuple[str, ...]

    @property
    def errors(self) -> tuple[str, ...]:
        errors: list[str] = []
        if self.machine_local_files:
            errors.append("machine-local content appears in tracked files")
        if self.secret_candidate_files:
            errors.append("high-confidence credential material appears in tracked files")
        if self.junk_paths:
            errors.append("generated, editor or local-only paths are tracked")
        if self.case_collisions:
            errors.append("case-insensitive tracked-path collisions exist")
        if self.unsafe_paths:
            errors.append("non-portable tracked path names exist")
        if self.symlink_paths:
            errors.append("tracked symlinks require explicit publication review")
        if self.submodule_paths:
            errors.append("tracked submodules require explicit publication review")
        if self.lfs_required:
            errors.append("Git LFS is required by tracked attributes")
        if set(self.raw_fixture_paths) != RAW_FIXTURES:
            errors.append("the intentional raw conformance fixture inventory changed")
        if self.unexpected_binary_or_archive_paths:
            errors.append("unexpected binary or archive files are tracked")
        return tuple(errors)


def tracked_paths() -> tuple[str, ...]:
    """Enumerate distributed files without requiring a Git checkout."""
    return tuple(sorted(
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(ROOT).parts
        and "__pycache__" not in path.relative_to(ROOT).parts
    ))


def tracked_modes() -> dict[str, str]:
    return {relative: "120000" if (ROOT / relative).is_symlink() else "100644"
            for relative in tracked_paths()}


def _text(path: Path) -> str | None:
    data = path.read_bytes()
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _unsafe_path(path: str) -> bool:
    for part in path.split("/"):
        if WINDOWS_RESERVED.match(part) or part.endswith((".", " ")):
            return True
        if any(ord(character) < 32 for character in part):
            return True
    return False


def audit_current_tree() -> HygieneReport:
    paths = tracked_paths()
    modes = tracked_modes()
    local_files: list[str] = []
    secret_files: list[str] = []

    for relative in paths:
        text = _text(ROOT / relative)
        if text is None:
            continue
        if MACHINE_LOCAL.search(text):
            local_files.append(relative)
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            secret_files.append(relative)

    folded: dict[str, list[str]] = {}
    for path in paths:
        folded.setdefault(path.casefold(), []).append(path)

    attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8")
    raw_paths = tuple(path for path in paths if path.endswith(".raw"))
    unexpected_binary = tuple(path for path in paths if ARCHIVE_OR_BINARY.search(path))

    return HygieneReport(
        tracked_paths=paths,
        machine_local_files=tuple(local_files),
        secret_candidate_files=tuple(secret_files),
        junk_paths=tuple(path for path in paths if JUNK_PATH.search(path)),
        case_collisions=tuple(
            tuple(group) for group in folded.values() if len(group) > 1
        ),
        unsafe_paths=tuple(path for path in paths if _unsafe_path(path)),
        symlink_paths=tuple(path for path, mode in modes.items() if mode == "120000"),
        submodule_paths=tuple(path for path, mode in modes.items() if mode == "160000"),
        lfs_required="filter=lfs" in attributes.replace(" ", "").casefold(),
        raw_fixture_paths=raw_paths,
        unexpected_binary_or_archive_paths=unexpected_binary,
    )


def main() -> int:
    report = audit_current_tree()
    if report.errors:
        for error in report.errors:
            print(f"ERROR: {error}")
        print("Sensitive candidate values are intentionally redacted.")
        return 1
    print(
        "Public distribution hygiene PASS: "
        f"{len(report.tracked_paths)} distribution files; "
        "0 machine-local leaks; 0 high-confidence credential candidates; "
        f"{len(report.raw_fixture_paths)} intentional raw fixtures; "
        "0 case collisions; 0 unsafe paths; 0 symlinks; 0 submodules; "
        "Git LFS not required."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
