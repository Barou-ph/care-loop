"""Build a clean CARE LOOP V3 source ZIP while preserving package paths."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT.parent / "CARE_LOOP_V3_FINAL.zip"

EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".idea", ".vscode", "node_modules", "runs", "data",
    "dist", "build", "sample_videos",
}
EXCLUDED_NAMES = {".DS_Store", "Thumbs.db"}
EXCLUDED_SUFFIXES = {
    ".pyc", ".pyo", ".part", ".db", ".sqlite", ".sqlite3",
    ".mp4", ".avi", ".mkv", ".mov", ".exe", ".dll", ".log",
}

with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED_DIRS for part in relative.parts):
            continue
        if path.name in EXCLUDED_NAMES or path.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        if path.name == ".env" or (path.name.startswith(".env.") and path.name != ".env.example"):
            continue
        archive.write(path, Path("CARE_LOOP_V3") / relative)

print(f"Created: {OUTPUT}")
print(f"Size: {OUTPUT.stat().st_size:,} bytes")
