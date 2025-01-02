import os

def list_files_recursive(directory, output_file, ignore_list):
    """Lists all files and directories recursively, excluding specified paths, and writes to a file.
       Includes file contents.
    """

    with open(output_file, "w", encoding="utf-8") as f:  # Add encoding for potential special characters
        f.write("1) Folder Structure:\n") # Section header

        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)

                ignore_flag = False
                for ignore_path in ignore_list:
                    if filepath == ignore_path or filepath.startswith(ignore_path + os.sep):
                        ignore_flag = True
                        break

                if not ignore_flag:
                    f.write(filepath + "\n")


        f.write("\n2) File Content by File:\n") # Section header

        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)

                ignore_flag = False
                for ignore_path in ignore_list:
                    if filepath == ignore_path or filepath.startswith(ignore_path + os.sep):
                        ignore_flag = True
                        break

                if not ignore_flag:
                    try: # Try to open and read file, handling potential errors
                        with open(filepath, "r", encoding="utf-8") as content_file:
                            content = content_file.read()
                            f.write(f"{filepath}:\n{content}\n\n")
                    except Exception as e: # Handle exceptions like UnicodeDecodeError, PermissionError, etc.
                        f.write(f"Error reading {filepath}: {e}\n\n")



if __name__ == "__main__":
    directory_to_scan = "."
    output_filename = "ZZ_Generated_prompt.txt"
    ignore_paths = [
        os.path.join(".", "env"),
        os.path.join(".", "ZZ_Generated_prompt.txt"),  # Important to ignore output file!
        os.path.join(".", ".git"),
        os.path.join(".", "__pycache__"),
        os.path.join(".", ".gitignore"),
        os.path.join(".", "ZZ_Generate_prompt.py"),
        os.path.join(".", "ZZ_Generate_prompt_select.py"),
        os.path.join(".", "ZZ_Generate_prompt_select.txt"),        
        os.path.join(".", "views/__pycache__"),
        os.path.join(".", "models/__pycache__"),
        os.path.join(".", "utils/__pycache__"),
        os.path.join(".", "tasks/__pycache__"),
        os.path.join(".", "controllers/__pycache__"),
        os.path.join(".", "ZZ_redis_db_connection.py"),
        

                
    ]

    list_files_recursive(directory_to_scan, output_filename, ignore_paths)
    print(f"File list and content written to {output_filename}")
