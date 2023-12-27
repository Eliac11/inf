import networkx as nx
import matplotlib.pyplot as plt
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
    G = nx.Graph()

    for foldername, _, filenames in os.walk(start_directory):
        print(foldername)
        if r"C:\work\interaction_api_vdnh\venv" in foldername:
            continue
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(foldername, filename)
                imports = get_imports(file_path)

                for imp in imports:
                    if imp != None:
                        G.add_edge(filename, imp)

    return G

def draw_dependency_graph(graph):
    pos = nx.spring_layout(graph, k=0.5)
    nx.draw(graph, pos, with_labels=True, font_weight='bold', font_size=8)
    plt.show()

if __name__ == "__main__":
    project_directory = "C:\work\interaction_api_vdnh"
    dependency_graph = generate_dependency_graph(project_directory)
    draw_dependency_graph(dependency_graph)
