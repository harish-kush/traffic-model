"""Build gridlock_source_submission.zip with all source files at archive root."""
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source_submission"
ZIP_PATH = ROOT / "gridlock_source_submission.zip"

# (source path, name inside zip)
ENTRIES = [
    (SRC / "ZIP_MANIFEST.txt", "ZIP_MANIFEST.txt"),
    (SRC / "approach.txt", "approach.txt"),
    (SRC / "predict.py", "predict.py"),
    (SRC / "requirements.txt", "requirements.txt"),
    (SRC / "README.txt", "README.txt"),
    (SRC / "traffic_demand_solution.ipynb", "traffic_demand_solution.ipynb"),
    (SRC / "Gridlock_Presentation.pptx", "Gridlock_Presentation.pptx"),
    (ROOT / "submission_UPLOAD_THIS_ONE.csv", "submission_UPLOAD_THIS_ONE.csv"),
]

EXPECTED_NAMES = [arc for _, arc in ENTRIES]


def main():
    missing = [arc for path, arc in ENTRIES if not path.exists()]
    if missing:
        raise SystemExit(f"Missing files: {missing}")

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, arcname in ENTRIES:
            zf.write(path, arcname=arcname)
            print(f"  + {arcname} ({path.stat().st_size} bytes)")

    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        names = zf.namelist()
        assert names == EXPECTED_NAMES, f"Zip manifest mismatch: {names}"
        for name in EXPECTED_NAMES:
            assert zf.getinfo(name).file_size > 0, f"Empty entry: {name}"

    print(f"\nOK: {ZIP_PATH} ({ZIP_PATH.stat().st_size} bytes)")
    print("Contents:", names)

    downloads = Path.home() / "Downloads" / "gridlock_source_submission.zip"
    downloads.write_bytes(ZIP_PATH.read_bytes())
    print(f"Copied -> {downloads}")


if __name__ == "__main__":
    main()
