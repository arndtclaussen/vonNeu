
import os

def generate_selected_file_prompt(directory, selected_paths, output_file):
    """Generates prompt with structure and content, ignoring __pycache__ and handling files in directories."""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("1) Folder Structure:\n")

        all_files = [] # List to keep track of all files we need content for

        for path in selected_paths:
            rel_path = os.path.relpath(path, directory)

            if os.path.isdir(path):
                f.write(rel_path + "\n")
                for root, _, files in os.walk(path):
                    for file in files:
                        filepath = os.path.join(root, file)
                        if not "__pycache__" in filepath:
                            rel_filepath = os.path.relpath(filepath, directory)
                            f.write(rel_filepath + "\n")
                            all_files.append(filepath)  # Add files in dirs to the list
            elif os.path.isfile(path):
                f.write(rel_path + "\n")
                all_files.append(path) # Add individually selected files to the list


        f.write("\n2) File Content by File:\n")

        for filepath in all_files:  # Now iterate through ALL the files
            try:
                with open(filepath, "r", encoding="utf-8") as content_file:
                    content = content_file.read()
                    rel_filepath = os.path.relpath(filepath, directory)
                    f.write(f"{rel_filepath}:\n{content}\n\n")
            except Exception as e:
                rel_filepath = os.path.relpath(filepath, directory)
                f.write(f"Error reading {rel_filepath}: {e}\n\n")



if __name__ == "__main__":
    base_directory = "."  # Or specify a different base directory if needed
    selected_items = [
        os.path.join(".", "app.py"), # Example file
        os.path.join(".", "utils"),  # Example directory
        os.path.join(".", "models"),  # Example directory
     
        
        # ... other files/directories you select
    ]
    output_filename = "ZZ_Generated_prompt_select.txt"


    generate_selected_file_prompt(base_directory, selected_items, output_filename)
    print(f"Selected file list and content written to {output_filename}")
