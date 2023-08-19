import os

def create_folder_structure_txt(folder_path, output_file, indent=""):
    with open(output_file, "w", encoding="utf-8") as f:
        create_folder_structure_recursive(folder_path, f, indent)

def create_folder_structure_recursive(folder_path, file, indent=""):
    items = os.listdir(folder_path)
    excluded_folders = [".git", "migrations", "__pycache__"]

    for idx, item in enumerate(items):
        if item in excluded_folders:
            continue

        item_path = os.path.join(folder_path, item)
        is_last_item = idx == len(items) - 1

        if os.path.isdir(item_path):
            file.write(f"{indent}{'└──' if is_last_item else '├──'} 📁 {item}\n")
            new_indent = indent + ("    " if is_last_item else "│   ")
            create_folder_structure_recursive(item_path, file, new_indent)
        else:
            file.write(f"{indent}{'└──' if is_last_item else '├──'} 📄 {item}\n")

if __name__ == "__main__":
    project_path = r"C:\Users\alonso\Desktop\arizona\PORTAFOLIOSTACK-MULTI-USER"
    output_file = "foldermap.txt"
    
    create_folder_structure_txt(project_path, output_file)
    print(f"Folder structure saved to {output_file}")
