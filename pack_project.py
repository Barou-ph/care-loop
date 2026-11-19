import os
import zipfile

PROJECT_DIR = "care-loop"
OUTPUT_ZIP = "care-loop-source.zip"

EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
    "node_modules",
    "runs",
}

EXCLUDE_FILES = {
    ".DS_Store",
}

with zipfile.ZipFile(
    OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED
) as archive:

    for root, dirs, files in os.walk(PROJECT_DIR):
        dirs[:] = [
            d for d in dirs if d not in EXCLUDE_DIRS
        ]

        for filename in files:
            if filename in EXCLUDE_FILES:
                continue

            filepath = os.path.join(root, filename)
            archive.write(filepath, filepath)

print(f"Created: {OUTPUT_ZIP}")
