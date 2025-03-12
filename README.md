# persipy
PyScript persistence fs with OPFS

This is a small tool to mount origin private file system of the browser into pyscript fs.

Tested with `micropython` interpreter on:

    - iOS / Safari

    - Android / Chrome

    - OSX / Chrome, Firefox, Safari


Tested with extentions: `txt`


Not tested with `pyodide`, but even if not work as it is - surely will be able with some bugfix.

*Requirements*:
Minimal version of pyscript **2025.2.4**

*Instalation*:
```
#config.toml of the main thread script
[files]
"/persipy.py" = "./persipy.py"
```


*Usage*:
```
#main.py
#with the usual with open() as file in the main thread including modules

from persipy import mount_opfs

await mount_opfs() # by default mount_opfs(mount_path='/opfs')

with open('/opfs/test.txt', 'w') as f:
    f.write('hello world')
```