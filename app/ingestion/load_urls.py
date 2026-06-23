import yaml
from pathlib import Path

# Absolute path to project_root/data/urls.yaml
project_root = Path(__file__).parent.parent.parent
default_path = project_root / "data" / "urls.yaml"

def load_urls(file_path=default_path):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    return data["urls"]

if __name__ == "__main__":
    urls = load_urls()
    print("Loaded URLs:")
    for u in urls:
        print(u)