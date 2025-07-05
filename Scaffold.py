# scaffold.py -- run once to create folders & starter files
from pathlib import Path

folders = [
    "firmware",          # Arduino / PlatformIO sketches
    "python",            # data collection & ML code
    "data/raw",          # untouched logs
    "data/processed",    # cleaned CSVs
    "docs",              # design notes, diagrams
    "tests",             # unit tests if/when you add them
]

files = {
    ".gitignore": """
# Python
__pycache__/
*.py[cod]
# PlatformIO / Arduino
*.bin
*.elf
*.uf2
# Data
data/raw/
# VS Code
.vscode/
""",
    "README.md": "# Offline Wireless AI SOS Project\n\n> Encrypted ESP-NOW mesh with AI-assisted routing.\n\n## Quick start\n```bash\npython -m venv .venv\n. .venv/Scripts/Activate   # or source .venv/bin/activate\npip install -r requirements.txt\n```",
}

for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

for path, content in files.items():
    Path(path).write_text(content.strip() + "\n")

print("✅ Scaffold created")
