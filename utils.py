import os
import time
import pandas as pd


def get_file_paths():
    # for every project, for every YAML file and for every job
    directory = "ci-analyzes"
    project_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if "files.csv" in filename:
                project_files.append(os.path.join(root, filename))

    all_project_files = []
    for file in project_files:
        project_name = file.split("\\")[1]
        if not any(d['name'] == project_name for d in all_project_files):
            all_project_files.append({"name": project_name, "paths": [file]})
        else:
            i = next((i for i, item in enumerate(all_project_files) if item["name"] == project_name), None)
            all_project_files[i]["paths"].append(file)

    return all_project_files


def analyze_file(file_path):
    with open(file_path, 'r') as f:
        df = pd.read_csv(file_path, sep=',')
        paths = df["file_name"].to_list()
        root = TreeNode("", None)

        for path in paths:
            find_and_insert(root, path.split("/")[1:])

        root.print(True)



class TreeNode:
    def __init__(self, name, parent):
        self.parent = parent
        self.name = name
        self.children = []

    def add_child(self, node):
        self.children.append(node)
        return node

    def print(self, is_root):
        pre_0 = "    "
        pre_1 = "│   "
        pre_2 = "├── "
        pre_3 = "└── "

        tree = self
        prefix = pre_2 if tree.parent and id(tree) != id(tree.parent.children[-1]) else pre_3

        while tree.parent and tree.parent.parent:
            if tree.parent.parent and id(tree.parent) != id(tree.parent.parent.children[-1]):
                prefix = pre_1 + prefix
            else:
                prefix = pre_0 + prefix

            tree = tree.parent

        if is_root:
            print(self.name)
        else:
            print(prefix + self.name)

        for child in self.children:
            child.print(False)


def find_and_insert(parent, edges):
    # Terminate if there is no edge
    if not edges:
        return

    # Find a child with the name edges[0] in the current node
    match = [tree for tree in parent.children if tree.name == edges[0]]

    # If there is already a node with the name edges[0] in the children, set "pointer" tree to this node. If there is no such node, add a node in the current tree node then set "pointer" tree to it
    tree = match[0] if match else parent.add_child(TreeNode(edges[0], parent))

    # Recursively process the following edges[1:]
    find_and_insert(tree, edges[1:])

