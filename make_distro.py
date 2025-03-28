"""
Minifying source files to dist folder as well compresing them in a zip file

requirements:
https://dflook.github.io/python-minifier/installation.html#

---
plantipy - @Ridensium - 2005
"""

import os, re, shutil, python_minifier

#source file directory
SRC = './src'

#draft distribution directory
DIST = './dist/dev'

# minified py files
DIST_PY = './dist/dev/py'

#name of the zip file of minified files
DIST_ZIP = 'distro' 
ZIP_FORMAT = 'zip'


def minify(source_code:str) -> str:
    """cleans from documentation strings and minifies with light options"""
    pattern = r'("|\'){3}(?:.|\n)*?("|\'){3}'
    cleaned_code_doc = re.sub(pattern, "", source_code, flags=re.DOTALL)
    cleaned_code_doc = re.sub(r'#.*$', '', cleaned_code_doc, flags=re.MULTILINE)
    
    #cleans docstrings for documentation
    minified_code = python_minifier.minify(
                    cleaned_code_doc,
                    remove_annotations=True,
                    combine_imports=True,
                    constant_folding=True
                )
    
    return minified_code


def compress(source_folder=DIST_PY, destination_folder=DIST, zip_name=DIST_ZIP):
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)
    # Full path for the ZIP file (with the .zip extension)
    zip_path = os.path.join(destination_folder, zip_name)
    # Compress the source folder to the zip file at the specified destination
    shutil.make_archive(zip_path, ZIP_FORMAT, source_folder)
    print('ZIP', zip_path, ZIP_FORMAT)


def main():
    """loop the code in `SRC` without the links/symlinks in it"""
    print('-'*30)
    src_len = len(SRC)
    for root, dirs, files in os.walk(SRC, followlinks=False):
       for file in files:
            
            if file.endswith('.pyc'):
                continue

            file_path = os.path.join(root, file)
            dest_path = DIST_PY + file_path[src_len:]

            if not file.endswith('.py'):
                shutil.copyfile(file_path, dest_path)
                continue
            

            with open(file_path, 'r') as f:
                original_source = f.read()
            minified_source = minify(original_source)
            
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            with open(dest_path, 'w') as f:
                f.write(minified_source)
            
            print(file_path, len(original_source), '->', dest_path, len(minified_source))

    compress()



if __name__ == "__main__":
    main()
