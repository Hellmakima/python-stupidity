import os
import sys

def list_files(directory, level=0):
    """Recursively lists all files and directories in the specified path."""
    try:
        # Print the current directory
        indent = '│   ' * (level) + '├── ' if level < 1 else '│   ' * (level - 1) + '├── '
        file_indent = '│   ' * (level) + '└── ' if level < 1 else '│   ' * (level - 1) + '└── '

        # List contents of the directory
        dirs = []
        files = []
        
        # Separate directories and files
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                dirs.append(item)
            else:
                files.append(item)

        # Sort directories and files
        dirs.sort()
        files.sort()

        # Print directories first
        for i, dir_name in enumerate(dirs):
            if i == len(dirs) - 1:
                print(f"{'│   ' * level}└── {dir_name}/")
            else:
                print(f"{'│   ' * level}├── {dir_name}/")
            # Recursively call list_files for the directory
            list_files(os.path.join(directory, dir_name), level + 1)

        # Print files
        for i, file_name in enumerate(files):
            if i == len(files) - 1:
                print(f"{'│   ' * level}└── {file_name}")
            else:
                print(f"{'│   ' * level}├── {file_name}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default to current directory if no argument is provided
        directory = '.'
    else:
        directory = sys.argv[1]

    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
    else:
        list_files(directory)
