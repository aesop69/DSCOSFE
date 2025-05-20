import os
import re

# Version: 1.0 | Last Updated: May 19, 2025
# Description: Parses `find-man.txt` to extract all options and saves them.

# Directories
WORKING_DIR = os.path.expanduser("~/debian-sid-docs/data")
MAN_DIR = os.path.join(WORKING_DIR, "man")
OPTIONS_DIR = os.path.join(WORKING_DIR, "options")

def extract_options(man_content):
    """Extracts all valid command options from man content."""
    options = set()
    lines = man_content.split("\n")

    for line in lines:
        match = re.findall(r"-[a-zA-Z0-9]+", line)  # Find all options starting with "-"
        options.update(match)

    return sorted(options)

def main():
    """Main execution function."""
    command = "find"  # Currently extracting options for 'find'

    man_file = os.path.join(MAN_DIR, f"{command}-man.txt")
    options_file = os.path.join(OPTIONS_DIR, f"{command}-options.txt")

    # Read man page content
    if os.path.exists(man_file):
        with open(man_file, "r") as f:
            man_content = f.read()
    else:
        print(f"Error: `{man_file}` not found.")
        return

    # Extract options
    options_list = extract_options(man_content)

    # Save to file
    os.makedirs(OPTIONS_DIR, exist_ok=True)
    with open(options_file, "w") as f:
        f.write("\n".join(options_list))

    print(f"✅ Extracted options saved: {options_file}")

if __name__ == "__main__":
    main()
