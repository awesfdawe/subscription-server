import json
from pathlib import Path
from urllib.parse import unquote
import msgspec

from outbound_models import Outbound

BASE_DIR = Path(__file__).parent.parent
LINKS_FILE = BASE_DIR / "tests" / "uri" / "fixtures" / "fake_valid_links.txt"
OUTPUT_FILE = BASE_DIR / "parsed_output.json"


# vibecoded shit
def serialize_complex_values(data: dict) -> dict:
    clean_data = {}
    for key, value in data.items():
        if isinstance(value, msgspec.Struct):
            clean_data[key] = serialize_complex_values(msgspec.structs.asdict(value))
        elif isinstance(value, dict):
            clean_data[key] = serialize_complex_values(value)
        elif isinstance(value, (list, tuple)):
            clean_data[key] = [
                serialize_complex_values(item) if isinstance(item, (dict, msgspec.Struct)) else str(item)
                for item in value
            ]
        elif isinstance(value, (str, int, float, bool, type(None))):
            clean_data[key] = value
        else:
            clean_data[key] = str(value)
    return clean_data


def run_audit() -> None:
    if not LINKS_FILE.exists():
        print(f"No file in: {LINKS_FILE}")
        return

    with open(LINKS_FILE, "r", encoding="utf-8") as file:
        links = [line.strip() for line in file if line.strip()]

    report = {}

    for index, link in enumerate(links, 1):
        link_name = unquote(link.split("#")[-1]) if "#" in link else f"link_{index}"

        record_key = f"{index:03d}. [{link_name}]"

        try:
            outbound = Outbound.from_uri(link)

            struct_dict = msgspec.structs.asdict(outbound)

            clean_model_data = serialize_complex_values(struct_dict)

            report[record_key] = {
                "status": "SUCCESS",
                "protocol_class": outbound.__class__.__name__,
                "source_url": link,
                "parsed_model": clean_model_data,
            }

        except Exception as error:
            report[record_key] = {"status": "ERROR", "source_url": link, "error_message": str(error)}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as json_file:
        json.dump(report, json_file, indent=4, ensure_ascii=False)

    print(f"Result in {OUTPUT_FILE.name}")


if __name__ == "__main__":
    run_audit()
