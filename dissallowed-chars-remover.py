#!/usr/bin/python3

import os
import subprocess
import sys


disallowed_chars = list(' \'";:/\,<>?|{}!@#$%^&*=+`')


def is_hidden(item_path):
    '''
    Check if an item is a hidden directory or a hidden file.
    '''
    if item_path.split('/')[-1].startswith('.'):
        return True
    return False


def check_and_replace(path):
    '''
    Check if a directory name contains one or more disallowed chars.
    If true, it replaces the disallowed chars with an underscore.
    '''
    old_path = path
    new_path = ''

    for char in disallowed_chars:
        item_name = path.split('/')[-1]
        item_root = '/'.join(path.split('/')[:-1])

        if char in item_name:
            new_name = item_name.replace(char, '_')
            new_path = os.path.join(item_root, new_name)
            path = new_path

        else:
            continue

    return old_path, new_path


def rename(names):
    '''
    Apply filename changes to the system.
    '''

    old_name = names[0]
    new_name = names[1]
    capture = subprocess.run(['mv', old_name, new_name],
                             capture_output=True, text=True)

    return capture


def traverse(root_path):
    '''
    Traverse each directory recursively.
    '''

    root_path_items = os.listdir(root_path)

    if len(root_path_items) != 0:
        item_paths = list(
            map(lambda item: os.path.join(root_path, item), root_path_items))

        for item_path in item_paths:
            if os.path.isdir(item_path) and not is_hidden(item_path):
                result = check_and_replace(item_path)

                if result[-1] != '':
                    item_path = result[-1]
                    capture = rename(result)

                    if capture.returncode == 0:

                        print(f'[*] A directory changed')
                        print(f'\tFrom\t= {result[0]}')
                        print(f'\tTo\t= {result[-1]}')

                os.chdir(item_path)
                traverse(item_path)

            elif os.path.isfile(item_path) and not is_hidden(item_path):

                result = check_and_replace(item_path)
                if result[-1] != '':
                    capture = rename(result)
                    if capture.returncode == 0:

                        print(f'[*] A file changed')
                        print(f'\tFrom\t= {result[0]}')
                        print(f'\tTo\t= {result[-1]}')


def main():
    try:
        if len(sys.argv) > 1:
            dir = sys.argv[1]
            if dir.startswith('.'):
                root_path = os.path.join(os.getcwd(), dir.split('/')[-1])
            else:
                root_path = os.path.join(os.getcwd(), dir)
        else:
            root_path = os.getcwd()
        traverse(root_path)
    except:
        print(f'[!] Error occured!')


if __name__ == "__main__":
    main()
