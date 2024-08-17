import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pyperclip

STORAGE_FILE = "commands.json"
commands = {}


if not os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "w") as f:
        json.dump({}, f, indent=4)
else:
    with open(STORAGE_FILE, "r") as f:
        commands = json.load(f)


def add_command(tag, command):
    if tag in commands:
        commands[tag].append(command)
    else:
        commands[tag] = [command]
    with open(STORAGE_FILE, "w") as f:
        json.dump(commands, f, indent=4)


def validate_tag(action, tag):
    if tag is None:
        print(f"Select a tag to {action} from:")
        tags = commands.keys()
        for i, t in enumerate(tags):
            print(f"{i+1}: {t}")
        cmd_selection = int(input(f"Which tag to {action} from?: "))
        tag = list(tags)[cmd_selection - 1]

    if tag not in commands:
        print("Tag not found")
        return None, None
    else:
        for i in range(len(commands[tag])):
            print(f"{i+1}: {commands[tag][i]}")
        selection = int(input(f"Which command to {action}?: "))
        return selection, tag


def copy_command(action, tag):
    selection, tag = validate_tag(action, tag)
    
    if selection is not None:
        pyperclip.copy(commands[tag][selection - 1])
        print(f"Command copied to clipboard: {commands[tag][selection - 1]}")


def edit_command(action, tag):

    selection, tag = validate_tag(action, tag)

    if selection is not None:
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            temp_file.write(commands[tag][selection - 1])
            temp_filepath = temp_file.name

        subprocess.run(["nvim", temp_filepath])

        with open(temp_filepath, "r") as temp_file:
            updated_command = temp_file.read().strip()

        commands[tag][selection - 1] = updated_command

        with open(STORAGE_FILE, "w") as f:
            json.dump(commands, f, indent=4)

        print(f"Command updated for tag '{tag}'.")


def list_commands():
    for t, c in commands.items():
        print(f"{t.upper()}:")
        for cmd in c:
            print(f"{cmd}")


def main():
    parser = argparse.ArgumentParser(
        description="A simple CLI tool to store terminal commands.",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40),
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-a", "--add", nargs=2, metavar=("[tag]", "[command]"), help="Add a new command"
    )
    group.add_argument(
        "-c",
        "--copy",
        nargs="?",
        const="__NO_TAG__",
        metavar="tag",
        help="Copy a command to clipboard",
    )

    group.add_argument(
        "-e",
        "--edit",
        nargs="?",
        const="__NO_TAG__",
        metavar="edit",
        help="Edit a command",
    )

    group.add_argument(
        "-l", "--list", action="store_true", help="List all tags and commands"
    )

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.add:
        tag, command = args.add
        add_command(tag, command)
    elif args.copy is not None:
        if args.copy == "__NO_TAG__":
            copy_command("copy", None)
        else:
            copy_command("copy", args.copy)
    elif args.edit is not None:
        if args.edit == "__NO_TAG__":
            edit_command("edit", None)
        else:
            edit_command("edit", args.edit)
    elif args.list:
        list_commands()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
