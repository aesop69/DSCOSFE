import os
import re
import sys
import argparse
from pathlib import Path

def read_file(file_path):
    """Reads content from a file, returns empty string if file not found."""
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found. Using empty string.")
        return ""
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            # Make sure we have content
            if not content.strip():
                print(f"Warning: {file_path} is empty")
                return ""
            return content
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return ""

def make_options_clickable(text, command):
    """Makes options in both help and man content clickable links to examples."""
    # Find all options in the text
    options = []
    for line in text.split('\n'):
        # Look for options that start with - or --
        matches = re.finditer(r'(-[a-zA-Z0-9]+|--[a-zA-Z0-9-]+)', line)
        for match in matches:
            option = match.group(0)
            if option not in options:
                options.append(option)

    # Replace options with clickable links
    for option in options:
        # Replace option when it's surrounded by spaces
        text = text.replace(f" {option} ", f" <a href='../examples/{command}-examples.html#{option}'>{option}</a> ")
        # Replace option at the start of a line
        text = text.replace(f"\n{option} ", f"\n<a href='../examples/{command}-examples.html#{option}'>{option}</a> ")
        # Replace option at the end of a line
        text = text.replace(f" {option}\n", f" <a href='../examples/{command}-examples.html#{option}'>{option}</a>\n")
        # Replace option when it's the only thing on a line
        text = text.replace(f"\n{option}\n", f"\n<a href='../examples/{command}-examples.html#{option}'>{option}</a>\n")
        # Replace option when it's at the start of the text
        text = text.replace(f"{option} ", f"<a href='../examples/{command}-examples.html#{option}'>{option}</a> ")

    return text

def format_examples(examples_content, command):
    """Formats examples with anchor tags for linking."""
    examples = []
    current_example = None
    current_description = None
    
    for line in examples_content.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('#'):
            if current_example and current_description:
                examples.append((current_example, current_description))
            current_example = line[1:].strip()
            current_description = ''
        else:
            if current_description is not None:
                current_description += f"{line}\n"
    
    if current_example and current_description:
        examples.append((current_example, current_description))
    
    formatted = ""
    for example, description in examples:
        formatted += f"""
        <div class="example">
            <h3><a href="#{example}" id="{example}">{example}</a></h3>
            <pre>{description}</pre>
        </div>
        """
    
    return formatted


def parse_man_sections(man_content, command):
    """Parses man page content into collapsible sections."""
    sections = []
    current_section = None
    current_content = []
    
    # Split content into lines
    lines = man_content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for section headers (typically in ALL CAPS)
        if line.isupper() and line.endswith(':'):
            if current_section:
                sections.append((current_section, '\n'.join(current_content)))
            current_section = line.rstrip(':')
            current_content = []
        else:
            if current_section:
                current_content.append(line)
    
    if current_section:
        sections.append((current_section, '\n'.join(current_content)))
    
    # Format sections
    formatted = ""
    for section_name, section_content in sections:
        formatted += f"""
        <div class="man-section">
            <div class="section-header">
                <span class="indicator">▶</span>
                <h2>{section_name}</h2>
            </div>
            <div class="section-content">
                <pre>{section_content}</pre>
            </div>
        </div>
        """
    
    return formatted

def generate_command_html(command):
    """Generates HTML documentation for a specific command."""
    # Directories for help, man, options, and examples
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    HELP_DIR = os.path.join(SCRIPT_DIR, "help")
    MAN_DIR = os.path.join(SCRIPT_DIR, "man")
    EXAMPLES_DIR = os.path.join(SCRIPT_DIR, "examples")
    OUTPUT_DIR = os.path.join(SCRIPT_DIR, "commands")  # Output to commands directory

    # Read content from files
    help_content = read_file(os.path.join(HELP_DIR, f"{command}-help.txt"))
    man_content = read_file(os.path.join(MAN_DIR, f"{command}-man.txt"))
    examples_content = read_file(os.path.join(EXAMPLES_DIR, f"{command}-examples.txt"))

    # Make options clickable in both help and man content
    help_content = make_options_clickable(help_content, command)
    man_content = make_options_clickable(man_content, command)

    # Format examples
    formatted_examples = format_examples(examples_content, command)

    # Create HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{command} Command Manual</title>
    <style>
        :root {{
            --primary-color: #ff9900;  /* Main orange */
            --secondary-color: #ff7f00;  /* Darker orange for links */
            --text-color: #f4f4f4;
            --bg-dark: #1a1a1a;
            --bg-light: #ffffff;
            --border-color: #ff9900;
            --hover-shadow: 0px 0px 15px var(--primary-color);
            --transition: all 0.3s ease;
            --link-color: #ff7f00;  /* Darker orange for links */
            --visited-color: #cc6600;  /* Even darker orange for visited links */
            --hover-color: #ffbf00;  /* Lighter orange for hover */
        }}

        body {{
            font-family: Arial, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-color);
            line-height: 1.6;
            margin: 0;
            padding: 20px;
        }}

        .command-title {{
            text-align: center;
            font-size: 32px;
            color: var(--secondary-color);
            margin: 20px 0;
        }}

        .help-info {{
            font-family: monospace;
            white-space: pre-wrap;
            margin: 10px;
            padding: 15px;
            background-color: var(--bg-light);
            border-radius: 4px;
            border: 1px solid var(--border-color);
            box-shadow: 0px 0px 8px var(--primary-color);
        }}

        .collapsible {{
            background-color: #222;
            color: var(--secondary-color);
            cursor: pointer;
            padding: 12px;
            border: 1px solid var(--border-color);
            box-shadow: 0px 0px 8px var(--primary-color);
            width: auto;
            border-radius: 4px;
            transition: var(--transition);
            margin-bottom: 5px;
        }}

        .collapsible:hover {{
            box-shadow: var(--hover-shadow);
        }}

        .content {{
            padding: 0 18px;
            display: none;
            overflow: hidden;
            background-color: #1a1a1a;
            margin-bottom: 20px;
        }}

        .example {{
            background-color: var(--bg-light);
            padding: 15px;
            border-radius: 4px;
            margin: 10px 0;
            font-family: monospace;
        }}

        a {{
            color: var(--link-color);
            text-decoration: none;
            transition: var(--transition);
        }}

        a:hover {{
            color: var(--hover-color);
            text-decoration: underline;
        }}

        a:visited {{
            color: var(--visited-color);
        }}

        h2 {{
            color: var(--secondary-color);
            margin: 20px 0 10px;
        }}

        pre {{
            margin: 0;
            padding: 10px;
            background-color: var(--bg-light);
            border-radius: 4px;
            font-size: 14px;
            font-family: monospace;
            white-space: pre-wrap;
        }}

        /* Navigation Bar */
        nav {{
            display: flex;
            gap: 10px;
            padding: 12px;
            background: #222;
            box-shadow: 0px 0px 12px var(--primary-color);
            margin-bottom: 20px;
        }}

        nav a, nav input, nav button {{
            padding: 10px;
            background: transparent;
            color: #00ff00;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            transition: var(--transition);
        }}

        nav a:hover, nav button:hover {{
            box-shadow: var(--hover-shadow);
        }}

        /* Man Page Sections */
        .man-section {{
            margin: 15px 0;
            padding: 10px;
            border-left: 3px solid var(--secondary-color);
        }}

        .man-section h2 {{
            margin-top: 0;
            padding: 5px 0;
            border-bottom: 1px solid var(--border-color);
        }}

        .man-section pre {{
            margin: 10px 0;
        }}

        /* Option Links */
        .option-link {{
            color: var(--secondary-color);
            text-decoration: none;
            font-weight: bold;
        }}

        .option-link:hover {{
            text-decoration: underline;
        }}

        /* Clickable Options */
        .clickable-option {{
            cursor: pointer;
            transition: var(--transition);
        }}

        .clickable-option:hover {{
            background-color: rgba(255, 153, 0, 0.1);
        }}

        /* Collapsible Sections */
        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background-color: #282828;
            border-radius: 4px;
            margin: 10px 0;
            cursor: pointer;
        }}

        .section-header:hover {{
            background-color: #303030;
        }}

        .section-header .indicator {{
            transition: transform 0.3s ease;
        }}

        .section-header.expanded .indicator {{
            transform: rotate(90deg);
        }}

        .section-content {{
            display: none;
            margin: 10px 0;
            padding: 10px;
            background-color: #1a1a1a;
            border-radius: 4px;
        }}

        .section-content.expanded {{
            display: block;
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            nav {{
                display: block;
            }}
        }}
    </style>
</head>
<body>
    <!-- Navigation Bar -->
    <nav role="navigation">
        <a href="../../index.html" aria-label="Home page">Home</a>
        <input type="text" id="search" placeholder="Search commands..." aria-label="Search commands">
        <button aria-label="Toggle dark mode" onclick="toggleDarkMode()">Dark Mode</button>
        <button aria-label="Open settings" onclick="openSettings()">Settings</button>
    </nav>

    <main role="main">
        <h1 class="command-title">{command}</h1>

        <!-- Help Info -->
        <section>
            <button class="collapsible" aria-controls="help-content">▶ Help Info (`{command} --help`)</button>
            <div id="help-content" class="content">
                <pre class="help-info">{help_content}</pre>
            </div>
        </section>

        <!-- Man Page -->
        <section>
            <button class="collapsible" aria-controls="man-content">▶ Man Page (`{command}.1`)</button>
            <div id="man-content" class="content">
                <!-- Split man content into sections -->
                {parse_man_sections(man_content.strip(), command)}
            </div>
        </section>

        <!-- Examples -->
        <section>
            <button class="collapsible" aria-controls="examples-content">▶ Examples</button>
            <div id="examples-content" class="content">
                {formatted_examples}
            </div>
        </section>
    </main>

    <!-- Loading Indicator -->
    <div class="loading" aria-hidden="true">
        <div class="loading-spinner"></div>
    </div>
</body>
</html>
"""

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Write to command.html
    output_file = os.path.join(OUTPUT_DIR, f"{command}.html")
    with open(output_file, "w") as output:
        output.write(html_content)

    print(f"✅ HTML file created successfully: {output_file}")

def generate_all_commands():
    """Generate HTML for all commands found in the help directory."""
    # Get all command names from help directory
    commands = []
    for file in os.listdir(HELP_DIR):
        if file.endswith("-help.txt"):
            command = file.replace("-help.txt", "")
            commands.append(command)

    # Generate HTML for each command
    for command in commands:
        print(f"\nGenerating HTML for {command}...")
        try:
            generate_command_html(command)
        except Exception as e:
            print(f"Error generating {command}: {str(e)}")

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Generate HTML documentation for commands.')
    parser.add_argument('--command', '-c', help='Generate HTML for a specific command')
    parser.add_argument('--all', '-a', action='store_true', help='Generate HTML for all commands')

    args = parser.parse_args()

    if args.command:
        print(f"Generating HTML for {args.command}...")
        generate_command_html(args.command)
    elif args.all:
        print("Generating HTML for all commands...")
        generate_all_commands()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
