"""
generating documentation of the package in `./src`
will make markdown files in the `./docs/dev_docs` directory,
for the modules with some sort of import in the __index__.py

plantipy - @Ridensium - 2005
"""

import os
import sys
import inspect
import importlib
import re
from unittest.mock import MagicMock

#source file directory
SRC:str = './src' 

#draft docs directory
DOCS:str = './docs/dev_docs'

# excluded packages
EXCLUDE:list = ['pyscript', 'js', 'window', 'navigator', 'document', 'pyscript.ffi']

# template for all objects
OBJECT_TEMPLATE:str = """{heading} *{type}*:  {name}()

<details><summary>{signature}</summary>


  ```python
{source}```


</details>


{info}


"""

# template for modules
MODULE_TEMPLATE:str = """## {name}

{info}

{classes}

{functions}

"""


# template for the package index
PACKAGE_TEMPLATE:str = """## {name}

{info}


Modules docs:


{modules}


"""


# mocking what need to exclide
for e in EXCLUDE:
    sys.modules[e] = MagicMock()

# converting src path to absolute
SRC = os.path.abspath(SRC)

# adding so to be found
if SRC not in sys.path:
    sys.path.insert(0, SRC)


def parse_docstrings(text:str):
    """beautify docstrings"""

    if not text:
        return ''
    
    #clean empty lines at begining 
    text = re.sub(r'^\n*', '', text)

    #clean empty lines at end 
    text = re.sub(r'\n*$', '', text)

    #clean the spaces from the empty lines
    text = re.sub(r'^[ ]+$', '\n', text, flags=re.MULTILINE)

    return text


def parse_source(source):
    """clean source for the expand section"""

    #clean docstrings
    pattern_docstrings = r'("|\'){3}(?:.|\n)*?("|\'){3}'
    source = re.sub(pattern_docstrings, '', source, flags=re.DOTALL)

    #clean comments
    source = re.sub(r'#.*$', '', source, flags=re.MULTILINE)

    #clean empty rows
    source = re.sub(r'^\s*\n', '', source, flags=re.MULTILINE)

    return source


class Package:
    """entry point for the parsing"""
    def __init__(self, name, obj):

        doc = inspect.getdoc(obj)
        doc = parse_docstrings(doc)
       
        modules = [Module(name, obj) for name, obj
                   in inspect.getmembers(obj, inspect.ismodule)
                   if name not in EXCLUDE]
        

        file_path = os.path.join(DOCS, f'{name}.md')
        

        #links to the modules docs
        modules_links = '\n'.join([f'- [{m.name}]({m.name}.md)'
                                   for m in modules])

        #final documentation of the package
        parsed_doc = PACKAGE_TEMPLATE.format(
            name=name,
            info = doc,
            modules = modules_links
        )

        with open(file_path, 'w') as f:
            f.write(parsed_doc)

        print('package:', name, file_path)


class ParseStrings:
    """
    super class for all objects
    parsing and preparing data
    """
    def __init__(self, name:str, obj):
        self.obj = obj
        self.name = name

        docstrings = inspect.getdoc(obj)
        docstrings = parse_docstrings(docstrings)
        self.docstrings = docstrings

        source = inspect.getsource(obj)
        source=parse_source(source)
        self.source = source

        try:
            signature = str(inspect.signature(obj))

            if signature.endswith(')'):

                signature=f'[{signature[1:-1]}]'

            else:
                signature = '[' + re.sub(r'\)\s*->', '] -> ', signature[1:])

            self.signature = signature

        except:
            self.signature = None

        try:
            self.qualname = obj.__qualname__

        except:
            self.qualname = None



class Module(ParseStrings):
    """parsing the modules"""
    def __init__(self, name, obj):
        super().__init__(name, obj)

        classes = [Class(name, _obj) for name, _obj
                   in inspect.getmembers(obj, inspect.isclass)
                   if _obj.__module__ == obj.__name__]

        functions = [Object(name, _obj, type='function') for name, _obj
                     in inspect.getmembers(obj, inspect.isfunction)
                     if _obj.__module__ == obj.__name__]
   
        file_path = os.path.join(DOCS, f'{name}.md')
        
        #final documentation of the module
        parsed_doc = MODULE_TEMPLATE.format(
            name=name,
            info = self.docstrings,
            classes = '\n'.join([c.doc for c in classes]),
            functions = '\n'.join([f.doc for f in functions])

        )

        with open(file_path, 'w') as f:
            f.write(parsed_doc)

        print('module:', name, file_path)



class Object(ParseStrings):
    """super class for all objects"""
    template:str = OBJECT_TEMPLATE
    line_number:int
    definition:str
    def __init__(self, name:str, obj, type='method'):
        super().__init__(name, obj)


        if type == 'class':
            heading = 2

        elif type == 'function':
            heading = 2

        # methods, classmethods and static methods type and definition
        else:
            heading = 3
            self.line_number = 0
            lines = self.source.splitlines()
            for l in range(len(lines)):
                line = lines[l]
                if 'def' in line:
                    self.definition = line
                    if l > 0:
                        type = lines[l-1]
                        type = type.replace(' ', '')
                        type = type.replace('@', '')
                    break
                    
        self.doc = self.template.format(
            heading = '#'*heading,
            type=type,
            name=name.replace('_', '\\_'),
            signature=self.signature,
            info=self.docstrings,
            source=self.source)  


class Class(Object):
    """class for the classes in module"""
    heading:int = 2
    def __init__(self, name, obj):
        super().__init__(name, obj, type='class')

        methods: list[Object] = [Object(name, _obj) for name, _obj in inspect.getmembers(obj, inspect.isfunction)]
        static: list[Object] = [Object(name, _obj) for name, _obj in inspect.getmembers(obj, inspect.isroutine) if not name.startswith('__') and not inspect.isfunction(_obj)]
        

        methods_own: list[Object] = []
        methods_inh: list[Object] = []

        static_own: list[Object] = []
        static_inh: list[Object] = []

        #splitting own and inherited
        for f in methods:
            if f.obj.__qualname__.startswith(obj.__qualname__):
                methods_own.append(f)
            else:
                methods_inh.append(f)

        for f in static:
            if f.obj.__qualname__.startswith(obj.__qualname__):
                static_own.append(f)
            else:
                static_inh.append(f)


        class_src = parse_source(self.source)
        class_src_lines = class_src.splitlines()
        
        #sorting by source
        for f in methods_own:
            for i, line in enumerate(class_src_lines):
                if line.startswith(f.definition):
                    f.line_number = i
                    break

        #sorting by source
        for f in static_own:
            for i, line in enumerate(class_src_lines):
                if line.startswith(f.definition):
                    f.line_number = i
                    break

                
        methods_own = sorted(methods_own, key=lambda f: f.line_number)

        static_own = sorted(static_own, key=lambda f: f.line_number)
       
        methods_all = methods_own + static_own + methods_inh + static_inh

        for f in methods_all:
            self.doc += f.doc

 


def clean_old():
    """clean previous generated in the draft docs directory"""

    if not os.path.exists(DOCS):
        return
    
    files = os.listdir(DOCS)

    for file_name in files:

        file_path = os.path.join(DOCS, file_name)
        
        try:
            os.remove(file_path)
        except:
                pass


def make(package='src'):
    """entry point for generating the docs"""

    package = importlib.import_module(package)

    name = os.path.basename(os.path.dirname(SRC))

    print('package:', name)

    os.makedirs(DOCS, exist_ok=True)

    Package(name, package)


if __name__=="__main__":
    clean_old()
    make()