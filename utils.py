import os
import json
from pathlib import Path

def get_folder_tree(folder_path, exclusions=None, indent=''):
    if exclusions is None:
        exclusions = []

    tree_structure = ""
    try:
        # Get a list of all items in the current directory
        items = os.listdir(folder_path)
    except PermissionError:
        tree_structure += f"{indent}[Permission Denied]\n"
        return tree_structure

    # Loop through each item in the folder
    for index, item in enumerate(sorted(items)):
        # Skip any item in the exclusions list
        if item in exclusions:
            continue

        # Construct the full item path
        item_path = os.path.join(folder_path, item)
        # Build the tree structure string
        connector = '├── ' if index < len(items) - 1 else '└── '
        tree_structure += f"{indent}{connector}{item}\n"

        # If the item is a directory, recursively get its contents
        if os.path.isdir(item_path):
            new_indent = indent + ('│   ' if index < len(items) - 1 else '    ')
            tree_structure += get_folder_tree(item_path, exclusions, new_indent)

    return tree_structure

def create_master_markdown(folder_path, output_file='master_project_document.md',exclusions=None):
    if exclusions is None:
        exclusions = []

    # Create the master Markdown content
    markdown_content = "# Project Master File\n\n"
    markdown_content += "## Project Structure\n\n"
    markdown_content += "```\n"
    markdown_content += get_folder_tree(folder_path, exclusions)
    markdown_content += "```\n\n"

    # Traverse the folder to add each code file's content
    for root, _, files in os.walk(folder_path):
        # Skip excluded directories
        if any(exclusion in root for exclusion in exclusions):
            continue
        for file in files:
            # Skip excluded files
            if file in exclusions:
                continue

            # Get the full file path
            file_path = os.path.join(root, file)

            # Only include text/code files (you can add more extensions as needed)
            if file.endswith(('.py', '.js', '.html', '.css', '.md', '.java', '.txt', '.sh')):
                markdown_content += f"## {file_path}\n\n"
                markdown_content += "```" + file.split('.')[-1] + "\n"
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        markdown_content += f.read()
                except Exception as e:
                    markdown_content += f"Error reading file: {e}"
                markdown_content += "\n```\n\n"

    # Write the content to a master Markdown file
    with open(output_file, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)


def combine_jsons(folder_path, output_file='combined.json', exclusions:list=None):
    if exclusions is None:
        exclusions = []

    combined_data = []
    for root, _, files in os.walk(folder_path):
        # Skip excluded directories
        if any(exclusion in root for exclusion in exclusions):
            continue
        for file in files:
            # Skip excluded files
            if file in exclusions:
                continue
            if any(exclusion in file for exclusion in exclusions):
                continue

            # Get the full file path
            file_path = os.path.join(root, file)

            # Only include JSON files
            if file.endswith('.json'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # combined_data.append(data)
                        combined_data.extend(data)
                except Exception as e:
                    print(f"Error reading file: {e}")

    # Write the combined data to a single JSON file
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(combined_data, json_file, indent=4)


if __name__ == "__main__":


    # Example usage:
    FOLDER = r'C:\Users\User\OneDrive\Desktop\Code\WebSandbox'
    # FOLDER = r'C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training'
    EXCLUSIONS = ['.git', 'node_modules','ipynb']  # Add any other folder/file names you want to exclude

    create_master_markdown(FOLDER, exclusions=EXCLUSIONS)

    # # Combine all JSON files in the folder and subfolders
    # DATA_FOLDER = Path(FOLDER) / 'data'
    # DATA_Exclusions = ['stable','old']
    # combine_jsons(DATA_FOLDER, output_file=DATA_FOLDER / 'combined.json', exclusions=DATA_Exclusions)