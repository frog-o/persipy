# persipy
PyScript tool to work with the Origin Private File system to provide,
persistant file storage, shared between main thread and workers

Tested with `micropython` and `pyodide` on:

    - iOS / Safari

    - Android / Chrome

    - OSX / Chrome, Firefox, Safari



*Instalation*:

```toml
#config.toml

[files]
"https://cdn.jsdelivr.net/gh/Ridensium/persipy@main/dist/distro.zip" = "./persipy/*"
```


*Usage*:

```python

from persipy import opfs

await opfs.init()

path = '/test/test.txt'

with opfs(path) as file:
    await file.write('asd')
    await file.write(b'asd')

with opfs(path, 'b') as file:
    b = await file.read()

with opfs(path) as file:
    text = await file.read()

with opfs(path) as file:
    b = await file.get_bytes()

```

[Documentation Index](docs/docs/persipy.md)