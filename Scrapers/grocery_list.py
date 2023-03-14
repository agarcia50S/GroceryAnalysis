import argparse
import pathlib
def handle_path_input(path):
    '''
    Change all backslashes in path to forward slashes, allowing python to correctly interpret 
    the string.
    '''
    window_path = pathlib.PureWindowsPath(path)
    py_path = str(window_path.as_posix())
    return py_path

def get_user_list():
    prog_desc = 'Welcome to Shoppy! This program will scour the web to find you the best grocery prices.'

    parser = argparse.ArgumentParser(
                        prog = 'grocery_list_input.py',
                        description = prog_desc)
    
    # create a mutually exclusive group that requires at least one arg
    xor_group = parser.add_mutually_exclusive_group(required=True)
    
    # user can directly pass in thier grocery list
    xor_group.add_argument('-items', nargs='+', type=str, help='Enter all of your grocery list items.')

    # or can pass in the path to a txt file with grocery list
    xor_group.add_argument('-path', type=str, help='Enter the path to the text file that contains your grocery list.')
    args = parser.parse_args()
    
    # accessing value of each argument
    user_list, path_to_list = args.items, args.path

    # handle path slashes
    if user_list is not None: return user_list

    with open(handle_path_input(path_to_list), mode='r') as file:
        return [line.strip() for line in file]
    

            


if __name__ == '__main__':
    print(get_user_list())