# добавляет "state": {} во все случаи, где metadata.widgets — словарь и в нём отсутствует ключ state
# запускать из anomaly_detection_project - poetry run python scripts/fix_widgets.py
import nbformat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # корень проекта
NOTEBOOK_DIR = ROOT / "notebooks" / "2_NN"

def fix_notebook(path: Path) -> bool:
    nb = nbformat.read(path, as_version=nbformat.NO_CONVERT)
    meta = nb.get("metadata", {})
    widgets = meta.get("widgets")
    changed = False
    if isinstance(widgets, dict) and "state" not in widgets:
        widgets["state"] = {}
        nb["metadata"]["widgets"] = widgets
        nbformat.write(nb, path)
        changed = True
    return changed

def main():
    if not NOTEBOOK_DIR.exists():
        print("Notebook directory not found:", NOTEBOOK_DIR)
        return
    files = sorted(NOTEBOOK_DIR.glob("*.ipynb"))
    if not files:
        print("No .ipynb files in", NOTEBOOK_DIR)
        return
    for fp in files:
        try:
            changed = fix_notebook(fp)
            print(f"{'Fixed' if changed else 'No change'}: {fp.name}")
        except Exception as e:
            print(f"Error processing {fp.name}: {e}")

if __name__ == "__main__":
    main()
