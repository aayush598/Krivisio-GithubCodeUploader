import os

def create_project_structure(base_path, structure):
    os.makedirs(base_path, exist_ok=True)

    for item in structure:
        item_type = item.get("type")
        item_name = item.get("name")
        path = os.path.join(base_path, item_name)

        if item_type == "file":
            with open(path, "w") as f:
                f.write("")  # Empty file
        elif item_type == "folder":
            os.makedirs(path, exist_ok=True)
            children = item.get("children", [])
            if children:
                create_project_structure(path, children)
