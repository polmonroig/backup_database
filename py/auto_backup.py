#!/usr/bin/python3
import paths
import os


gigabyte = 1000000000
megabyte = 1000000
kilobyte = 1000

def add_project(projects, root, sep, project, client):
    name = os.path.join(client, project)
    if name in projects:
        if root in projects[name]:
            projects[name][root].append(sep)
        else:
            projects[name][root] = [sep]
    else:
        projects[name] = {}
        projects[name][root] = [sep]

    return projects

# WORK/PROJECT/client/projectName
def find_clients(projects, root, sep):
    path = os.path.join(root, sep)
    if os.path.exists(path):
        for client in os.listdir(path): # client
            client_path = os.path.join(path, client)
            if os.path.isdir(client_path):
                for project in os.listdir(client_path):
                    project_path = os.path.join(client_path, project)
                    if os.path.isdir(project_path):
                        projects = add_project(projects, root, sep, project, client)
    return projects

def get_projects():
    projects = {}
    for root in paths.root_dirs: # work, storage, backup
        for sep in paths.separation_dirs: # project, footage, cache, render
            projects = find_clients(projects, root, sep)
    return projects



def recursive_get_size(path):
    if os.path.isdir(path):
        return sum([recursive_get_size(os.path.join(path, file)) for file in os.listdir(path)])
    else:
        return os.path.getsize(path)


def format_size(size):
    size /= gigabyte
    size = "{:.3f}".format(size) + ' GB'
    return size

def print_directory(p, separations, root, name):
    for sep in separations:
        path = os.path.join(root, sep, p)
        size = recursive_get_size(path)
        main_name = os.path.join(name, sep, p)
        print(main_name, format_size(size))

def print_separation(name, sep):
    print(sep)
    if paths.work_dir in projects[name]:
        work = projects[name][paths.work_dir]
        print_directory(p, work, paths.work_dir, paths.work_name)
    if paths.storage_dir in projects[name]:
        storage = projects[name][paths.storage_dir]
        print_directory(p, storage, paths.storage_dir, paths.backup_name)
    if paths.backup_dir in projects[name]:
        backup = projects[name][paths.backup_dir]
        print_directory(p, backup, paths.backup_dir, paths.storage_name)

def print_project(projects, p):
    p_split = p.split('/')
    client, project = p_split[0], p_split[1]
    name = os.path.join(client, project)
    if not (name in projects):
        print('No project satisfies the requested name.')
        print('The project must be identified by client/project')
    else:
        print(name)
        print_separation(name, paths.project_name)
        print_separation(name, paths.footage_name)
        print_separation(name, paths.render_name)
        print_separation(name, paths.cache_name)






def print_all(projects):
    ids = projects.keys()
    for id in ids:
        print_project(projects, id)
        print("========================================")

def print_client(projects, client):
    keys = projects.keys()
    selected_projects = []
    for key in keys:
        arr = key.split('/')
        if arr[0] == client:
            selected_projects.append(key)
    for id in selected_projects:
        print_project(projects, id)
        print("========================================")

def ask_info(projects):
    # print(projects)
    print('Initializing prompt')
    command = input('>> ')
    while command != 'exit':
        print_all()
        command = input('>> ')




def main():
    print('Starting search')
    projects = get_projects()
    if projects != None:
        ask_info(projects)
    else:
        print('No files where found, exiting application...')




if __name__ == '__main__':
    main()
