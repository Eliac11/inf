import os
import ast

def get_file_info(file_path):
    with open(file_path, 'r',encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)

    imports = set()
    classes = []
    global_vars = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    global_vars.append(target.id)

    return imports, classes, global_vars

def generate_dependency_graph(start_directory):
    dependency_graph = {}

    for foldername, _, filenames in os.walk(start_directory):

        if r"venv" in foldername:
            continue
        print(foldername)
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(foldername, filename)
                imports, classes, global_vars = get_file_info(file_path)
                print(imports)
                dependency_graph[filename] = {
                    'imports': list(imports),
                    'classes': classes,
                    'global_vars': global_vars
                }

    return dependency_graph

def generate_obsidian_project(graph, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for node, info in graph.items():
        file_path = os.path.join(output_directory, f"{node}.md")

        with open(file_path, 'w') as file:
            file.write(f"# {node}\n\n")
            file.write("#Class\n")
            if info['classes']:
                file.write("## Classes\n")
                for class_name in info['classes']:
                    file.write(f"- [[{class_name}]]\n")

            if info['global_vars']:
                file.write("## Global Variables\n")
                for var_name in info['global_vars']:
                    file.write(f"- {var_name}\n")

            if info['imports']:
                file.write("## Dependencies\n")
                for dependency in info['imports']:
                    file.write(f"- [[{dependency}.py]]\n")

if __name__ == "__main__":
    project_directory = "C:\work\interaction_editor_api_vdnh"
    obsidian_output_directory = "./data/api_vdnh_creatorClasses"

    dependency_graph = generate_dependency_graph(project_directory)
    generate_obsidian_project(dependency_graph, obsidian_output_directory)
