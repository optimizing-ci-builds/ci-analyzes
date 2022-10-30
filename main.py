import utils
import os
import time
import subprocess


def main():
    # GET THE PROJECTS
    os.chdir("..")
    project_file_paths = utils.get_file_paths()

    for project in project_file_paths:
        for file in project["paths"]:
            utils.analyze_file(file)
        break



if __name__ == "__main__":
    main()

