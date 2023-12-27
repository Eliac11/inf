import os
import ast

def extract_classes(file_path):
    with open(file_path, 'r',encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)

    classes = set()
    class_uses = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.add(node.name)
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            class_uses.add((node.value.id, node.attr))

    return classes, class_uses

def generate_dependency_graph(start_directory):
    dependency_graph = {}

    for foldername, _, filenames in os.walk(start_directory):
        if r"C:\work\interaction_api_vdnh\venv" in foldername:
            continue
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(foldername, filename)
                classes, class_uses = extract_classes(file_path)

                for class_name in classes:
                    if class_name not in dependency_graph:
                        dependency_graph[class_name] = set()

                    for used_class_name, attribute in class_uses:
                        if class_name != used_class_name:
                            dependency_graph[class_name].add((used_class_name, attribute))

    return dependency_graph

def generate_obsidian_project(graph, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for class_name, uses in graph.items():
        file_path = os.path.join(output_directory, f"{class_name}.md")

        with open(file_path, 'w') as file:
            file.write(f"#Class\n\n")
            if uses:
                file.write("#ClassUses\n")
                for used_class_name, attribute in uses:
                    file.write(f"- [[{used_class_name}]] - {attribute}\n")

if __name__ == "__main__":
    project_directory = "C:\work\interaction_api_vdnh"
    obsidian_output_directory = "./data/api_vdnhClasses"

    dependency_graph = generate_dependency_graph(project_directory)
    generate_obsidian_project(dependency_graph, obsidian_output_directory)
