"""
Q-Guard: Hackathon Submission Packaging Script.

Packages project source code, configuration, tests, documentation, and evidence
into a validated ZIP archive adhering to submission rules.
"""

from pathlib import Path
import sys
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent.parent
ZIP_PATH = ROOT.parent / "Q-Guard_Submission.zip"

EXCLUDED_DIRS = {
    ".venv", ".venv-1", "venv", "__pycache__", ".git",
    ".pytest_cache", ".mypy_cache", "node_modules", ".idea", ".vscode"
}

EXCLUDED_FILES = {
    ".env", ".env.local", "secrets.json", ".DS_Store"
}

REQUIRED_ITEMS = [
    "main.py",
    "README.md",
    "requirements.txt",
    "SUBMISSION_NOTES.md",
    "config/processors.json",
    "qguard",
    "tests",
    "scripts",
    "docs/REQUIREMENTS_AUDIT.md",
    "docs/IMPLEMENTATION_STATUS.md",
    "docs/METHODOLOGY.md",
    "docs/LIMITATIONS.md",
    "outputs/experiment_results.csv",
    "outputs/final_report.md",
    "outputs/fidelity_comparison.png",
]


def is_excluded(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return True
    if path.name in EXCLUDED_FILES or path.suffix == ".pyc":
        return True
    if path.resolve() == ZIP_PATH.resolve():
        return True
    return False


def build_submission_zip():
    print("=" * 70)
    print("Q-Guard: Building Hackathon Submission Package")
    print(f"Target Archive: {ZIP_PATH}")
    print("=" * 70)

    # Verify presence of essential components
    missing = [item for item in REQUIRED_ITEMS if not (ROOT / item).exists()]
    if missing:
        print("\nWARNING: Some expected submission items were not found:")
        for item in missing:
            print(f"  - {item}")
        print("Please ensure experiments and reports have been generated.\n")

    files_to_pack = []
    # Collect files from tracked folders
    for folder_name in ["config", "qguard", "backend", "frontend", "tests", "scripts", "docs", "outputs"]:
        folder = ROOT / folder_name
        if folder.exists():
            for p in folder.rglob("*"):
                if p.is_file() and not is_excluded(p):
                    files_to_pack.append(p)

    # Collect root files
    for p in ROOT.iterdir():
        if p.is_file() and not is_excluded(p):
            if p.suffix in {".py", ".md", ".txt", ".json", ".toml"}:
                files_to_pack.append(p)

    files_to_pack = sorted(set(files_to_pack), key=lambda p: str(p.relative_to(ROOT)).lower())

    if not files_to_pack:
        raise SystemExit("Error: No files found to include in submission archive.")

    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(ZIP_PATH, "w", ZIP_DEFLATED) as zf:
        for p in files_to_pack:
            arcname = Path("Q-Guard") / p.relative_to(ROOT)
            zf.write(p, arcname)

    # Verify ZIP integrity
    with ZipFile(ZIP_PATH, "r") as zf:
        corrupted = zf.testzip()
        names = zf.namelist()

    if corrupted:
        raise SystemExit(f"CRITICAL: Submission ZIP integrity check failed at: {corrupted}")

    print("\nSubmission ZIP created and verified successfully.")
    print(f"Total files packaged: {len(names)}")
    print(f"Archive file size: {ZIP_PATH.stat().st_size / 1024:.1f} KB")
    print("Integrity verification: PASS")
    return ZIP_PATH


if __name__ == "__main__":
    build_submission_zip()
