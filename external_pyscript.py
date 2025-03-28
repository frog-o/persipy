"""
adding pyscript as submodule to the project repo in external/pyscript
and making symlinks of the python pyscript package to src/pyscript
"""

import os, subprocess

EXTERNAL_PYSCRIPT = os.path.abspath('external/pyscript')
SRC_PYSCRIPT = os.path.abspath('src/pyscript')
EXTERNAL_PYSCRIPT_STDLIB = os.path.abspath('external/pyscript/core/src/stdlib/pyscript')

GIT = 'https://github.com/pyscript/pyscript.git'

# Function to check if the submodule already exists
def is_submodule_added(submodule_path=EXTERNAL_PYSCRIPT):
    # Check if the directory already exists in the submodule path
    if os.path.isdir(submodule_path):
        print(f"Submodule already exists at {submodule_path}.")
        return True
    return False

# Function to add the submodule
def add_submodule(git=GIT, target=EXTERNAL_PYSCRIPT):
    if not is_submodule_added(EXTERNAL_PYSCRIPT):
        try:
            # Running the git submodule add command
            subprocess.check_call(['git', 'submodule', 'add', git, target])
            print("Submodule added successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error adding submodule: {e}")
    else:
        print("Skipping submodule addition.")

# Remove the symlinks if exists
def delete_symlink(symlink = SRC_PYSCRIPT):
    try:
        os.unlink(symlink)
        print(f'Symlink {symlink} has been removed.')
    except:
        print(f'No symlink removed.')

def add_symlinks(origin=EXTERNAL_PYSCRIPT_STDLIB, target=SRC_PYSCRIPT):
    # Create the symlink
    os.symlink(origin, target)
    print(f'Symlink created from {origin} to {target}')


def main():
    add_submodule()
    delete_symlink()
    add_symlinks()


if __name__ == "__main__":
    main()


