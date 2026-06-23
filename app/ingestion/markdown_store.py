import re
from pathlib import Path

markdown_dir = Path(__file__).parent.parent.parent / "data" / "markdown"
markdown_dir.mkdir(parents=True, exist_ok=True)


def save_markdown(url, text):
    name = re.sub(r"[^a-zA-Z0-9]+", "_", re.sub(r"^https?://", "", url)).strip("_")
    file_path = markdown_dir / f"{name}.md"
    file_path.write_text(f"# Source: {url}\n\n{text}\n", encoding="utf-8")
    print(f"Saved markdown: {file_path.name}")
