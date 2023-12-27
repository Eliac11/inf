import os
import ast

def get_imports(file_path):
    with open(file_path, 'r',encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)

    return imports

def generate_dependency_graph(start_directory):
    dependency_graph = {}

    for foldername, _, filenames in os.walk(start_directory):
        if r"C:\work\interaction_api_vdnh\venv" in foldername:
            continue
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(foldername, filename)
                imports = get_imports(file_path)

                dependency_graph[filename] = list(imports)

    return dependency_graph

def generate_obsidian_project(graph, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for node, dependencies in graph.items():
        file_path = os.path.join(output_directory, f"{node}.md")

        with open(file_path, 'w') as file:
            file.write(f"# {node}\n\n")
            if dependencies:
                file.write("## Dependencies\n")
                for dependency in dependencies:
                    file.write(f"- [[{dependency}]]\n")

if __name__ == "__main__":
    project_directory = "C:\work\interaction_api_vdnh"
    obsidian_output_directory = "./data/api_vdnhALL"

    dependency_graph = generate_dependency_graph(project_directory)
    generate_obsidian_project(dependency_graph, obsidian_output_directory)
