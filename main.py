import argparse
import json
import os
from pathlib import Path

import pyperclip

STOARGE_FILE = "commands.json"
commands = {}


if not os.path.exists(STOARGE_FILE):
    with open(STOARGE_FILE, "w") as f:
        json.dump({}, f, indent=4)
else:
    with open(STOARGE_FILE, "r") as f:
        commands = json.load(f)


def add_command(tag, command):
    if tag in commands:
        commands[tag].append(command)
    else:
        commands[tag] = [command]
    with open(STOARGE_FILE, "w") as f:
        json.dump(commands, f, indent=4)


def copy_command(tag=None):
    if tag is None:
        print("Select a tag to copy from:")
        tags = commands.keys()
        for i, t in enumerate(tags):
            print(f"{i+1}: {t}")
        cmd_selection = int(input("Which command to copy?: "))
        tag = list(tags)[cmd_selection - 1]

    if tag in commands:
        for i in range(len(commands[tag])):
            print(f"{i+1}: {commands[tag][i]}")
        selection = int(input("Which command to copy?: "))
        pyperclip.copy(commands[tag][selection - 1])
    else:
        print("Tag not found")


def list_commands():
    for t, c in commands.items():
        print(f"{t.upper()}:")
        for cmd in c:
            print(f"{cmd}")


def main():
    parser = argparse.ArgumentParser(
        description="A simple CLI tool to store terminal commands."
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-a", "--add", nargs=2, metavar=("tag", "command"), help="Add a new command"
    )
    group.add_argument(
        "-c", "--copy",nargs="?", const="__NO_TAG__", metavar="tag", help="Copy a command to clipboard"
    )
    group.add_argument(
        "-l", "--list", action="store_true", help="List all tags and commands"
    )

    args = parser.parse_args()

    if args.add:
        tag, command = args.add
        add_command(tag, command)
    elif args.copy is not None:
        if args.copy == "__NO_TAG__":
            copy_command(None)
        else:
            copy_command(args.copy)
    elif args.list:
        list_commands()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
