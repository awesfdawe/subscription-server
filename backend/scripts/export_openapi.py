import json
from pathlib import Path
from src.main import app


def export_schema():
    root_dir = Path(__file__).resolve().parent.parent

    with open(root_dir / "openapi.json", "w", encoding="utf-8") as f:
        json.dump(app.openapi(), f, indent=2)

    print("openapi schema exported")


if __name__ == "__main__":
    export_schema()
