from pathlib import Path

COMMANDS_FILE = Path("commands.json")

if not COMMANDS_FILE.exists():
    COMMANDS_FILE.write_text("{}")
    print("does not exist")
else:
    print("does exist")

