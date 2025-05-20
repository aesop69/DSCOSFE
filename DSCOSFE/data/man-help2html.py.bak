import os
import tkinter as tk
from tkinter import simpledialog

# Version: 1.3 | Last Updated: May 19, 2025
# Description: Converts man/help text files to structured HTML with clickable options linked to examples.

# Directories for help, man, options, and examples
WORKING_DIR = os.path.expanduser("~/debian-sid-docs/data")
HELP_DIR = os.path.join(WORKING_DIR, "help")
MAN_DIR = os.path.join(WORKING_DIR, "man")
OPTIONS_DIR = os.path.join(WORKING_DIR, "options")
EXAMPLES_DIR = os.path.join(WORKING_DIR, "examples")
OUTPUT_DIR = os.path.join(WORKING_DIR, "html")

def read_file(file_path):
    """Reads the content of a file and returns it as a string."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read()
    return f"Error: {file_path} not found."

def parse_options(options_content, command):
    """Parses options and converts them into clickable links."""
    lines = options_content.split("\n")
    formatted_options = ""

    for line in lines:
        option = line.strip()
        if option:
            formatted_options += f'<a href="{command}-examples.html#{option}">{option}</a><br>\n'

    return formatted_options

def format_examples(examples_content):
    """Formats examples with anchor tags for linking."""
    lines = examples_content.split("\n")
    formatted_examples = ""

    for line in lines:
        if line.startswith("-"):
            formatted_examples += f'<h2 id="{line.strip()}">{line.strip()}</h2>\n'
        else:
            formatted_examples += f"<p>{line}</p>\n"

    return formatted_examples

def generate_html(command, help_content, man_content, options_content, examples_content):
    """Generates a structured HTML page with collapsible sections and clickable options."""
    options_links = parse_options(options_content, command)
    formatted_examples = format_examples(examples_content)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{command} Command Manual</title>
    <link rel="stylesheet" href="styles.css">
    <script src="script.js" defer></script>
</head>
<body>

    <h1 class="command-title">{command} Command</h1>

    <!-- Help Info -->
    <section>
        <button class="collapsible">Help Info (`{command} --help`)</button>
        <div class="content">
            <pre class="info-text">{help_content}</pre>
        </div>
    </section>

    <!-- Man Page -->
    <section>
        <button class="collapsible">Man Page (`{command}.1`)</button>
        <div class="content">
            <pre class="info-text">{man_content}</pre>
        </div>
    </section>

    <!-- Options -->
    <section>
        <button class="collapsible">Options (`{command}`)</button>
        <div class="content">
            {options_links}
        </div>
    </section>

    <!-- Examples -->
    <section>
        <button class="collapsible">Examples (`{command}`)</button>
        <div class="content">
            {formatted_examples}
        </div>
    </section>

</body>
</html>
"""
    return html_content

def get_command_input():
    """Creates a Tkinter window for command input."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    command = simpledialog.askstring("Command Input", "Enter the command name:")
    return command.strip() if command else None

def main():
    """Main execution function."""
    command = get_command_input()
    if not command:
        print("No command entered. Exiting.")
        return

    help_file = os.path.join(HELP_DIR, f"{command}-help.txt")
    man_file = os.path.join(MAN_DIR, f"{command}-man.txt")
    options_file = os.path.join(OPTIONS_DIR, f"{command}-options.txt")
    examples_file = os.path.join(EXAMPLES_DIR, f"{command}-examples.txt")
    output_file = os.path.join(OUTPUT_DIR, f"{command}-manual.html")

    help_content = read_file(help_file)
    man_content = read_file(man_file)
    options_content = read_file(options_file)
    examples_content = read_file(examples_file)

    html_output = generate_html(command, help_content, man_content, options_content, examples_content)

    with open(output_file, "w") as output:
        output.write(html_output)

    print(f"✅ HTML file created successfully: {output_file}")

if __name__ == "__main__":
    main()
