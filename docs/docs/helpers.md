## helpers

All functions to work with Origin Private File System API
and the class for the helper worker

## *class*:  Helper\_Worker()

<details><summary>[]</summary>


  ```python
class Helper_Worker:
    root:DirHandle
    @classmethod
    async def init(cls):
        cls.root = await navigator.storage.getDirectory()
        sync.read = cls.read
        sync.write = cls.write
        sync.blob = cls.blob
    @classmethod
    async def read(cls, path:str, _)->ArrayBuffer:
          result = await opfs_read(root=cls.root, path=path)
          return result
    @classmethod
    async def blob(cls, path:str, mode:str='', _root='')->str|bytes:
          result = await opfs_blob(root=cls.root, path=path, mode=mode)
          return result
    @classmethod
    async def write(cls, path:str, buffer:ArrayBuffer, root)->int:
        result = await opfs_write(root=cls.root, path=path, buffer=buffer)
        return result
```


</details>


Used by the helper worker to bridge Origin Private File system to the main thread


### *classmethod*:  init()

<details><summary>[]</summary>


  ```python
    @classmethod
    async def init(cls):
        cls.root = await navigator.storage.getDirectory()
        sync.read = cls.read
        sync.write = cls.write
        sync.blob = cls.blob
```


</details>


seting up the helper worker


### *classmethod*:  read()

<details><summary>[path: str, _] ->  <MagicMock name='mock.ArrayBuffer' id='4316313456'></summary>


  ```python
    @classmethod
    async def read(cls, path:str, _)->ArrayBuffer:
          result = await opfs_read(root=cls.root, path=path)
          return result
```


</details>


returns `opfs_read()` see it above


### *classmethod*:  blob()

<details><summary>[path: str, mode: str = '', _root=''] ->  str | bytes</summary>


  ```python
    @classmethod
    async def blob(cls, path:str, mode:str='', _root='')->str|bytes:
          result = await opfs_blob(root=cls.root, path=path, mode=mode)
          return result
```


</details>


returns `opfs_blob()` see it above


### *classmethod*:  write()

<details><summary>[path: str, buffer: <MagicMock name='mock.ArrayBuffer' id='4316313456'>, root] ->  int</summary>


  ```python
    @classmethod
    async def write(cls, path:str, buffer:ArrayBuffer, root)->int:
        result = await opfs_write(root=cls.root, path=path, buffer=buffer)
        return result
```


</details>


writes the file with `opfs_write()` see it above




## *function*:  get\_access()

<details><summary>[root: <MagicMock name='mock.FileSystemDirectoryHandle' id='4318381456'>, path: str = None, option: str = 'readwrite'] ->  <MagicMock name='mock.FileSystemSyncAccessHandle' id='4318382128'></summary>


  ```python
async def get_access(root:DirHandle, path:str=None, option:str="readwrite")->AccessHandle:
        handle = await get_handle(root=root, path=path)
        if handle:
            access = await handle.createSyncAccessHandle(option)
        else:
            return None
        return access
```


</details>


from the provided file path gets the FileSystemSyncAccessHandle object,
which we are gonna using to work with the file



## *function*:  get\_dir\_handle()

<details><summary>[root: <MagicMock name='mock.FileSystemDirectoryHandle' id='4318381456'>, directories: list, create=False] ->  <MagicMock name='mock.FileSystemDirectoryHandle' id='4318381456'></summary>


  ```python
async def get_dir_handle(root:DirHandle, directories:list, create=False)->DirHandle:  
        handle = root
        for dir_name in [d for d in directories if d]:
            handle = await handle.getDirectoryHandle(dir_name,
                                                     create=create).catch(not_found)
            if not handle:
                return None
        return handle
```


</details>


from the list of directories (nested with as top is at index 0)
gets the OPFS API object called `FileSystemDirectoryHandle`
from where will be able to find the file we want to work on



## *function*:  get\_handle()

<details><summary>[root: <MagicMock name='mock.FileSystemDirectoryHandle' id='4318381456'>, path: str, create=True] ->  <MagicMock name='mock.FileSystemFileHandle' id='4318381792'></summary>


  ```python
async def get_handle(root:DirHandle, path:str, create=True)->FileHandle:
        path_parts:list = path.split('/')
        file_name = path_parts.pop()
        dir_handle:DirHandle = await get_dir_handle(root=root, directories=path_parts, create=create)
        if not dir_handle:
              return None
        handle = await dir_handle.getFileHandle(file_name, create=create).catch(not_found)
        return handle
```


</details>


from the provided file path gets the FileSystemFileHandle object,
which we are gonna using to work with the file



## *function*:  get\_root()

<details><summary>[]</summary>


  ```python
async def get_root():
    return await navigator.storage.getDirectory()
```


</details>


get root of the file system



## *function*:  not\_found()

<details><summary>[e]</summary>


  ```python
def not_found(e):
        print(e.message)
        return None   
```


</details>


error handling if not found pointer for a file or directory



## *function*:  opfs\_blob()

<details><summary>[path: str, mode, root: <MagicMock name='mock.FileSystemDirectoryHandle' id='4318381456'>] ->  str | bytes</summary>


  ```python
async def opfs_blob(path:str, mode, root:DirHandle)->str|bytes:
    handle:FileHandle = await get_handle(root=root, path=path)
    if not handle:
          return None
    blob:Blob = await handle.getFile().catch(not_found)
    if mode.endswith('b'):
        return await blob.bytes()
    else:
        return await blob.text()
```


</details>


gets text or string for the file without using FileSystemSyncAccessHandle
fast for big files and depending on mode returns string or bytes



## *function*:  opfs\_read()

<details><summary>[path: str, root: <MagicMock name='mock.FileSystemDirectoryHandle' id='4318381456'>] ->  <MagicMock name='mock.ArrayBuffer' id='4316313456'></summary>


  ```python
async def opfs_read(path:str, root:DirHandle)->ArrayBuffer:
    access:AccessHandle = await get_access(root=root, path=path, option="read-only")
    if not access:
          return None
    size = access.getSize()
    buffer = ArrayBuffer.new(size)
    result = access.read(buffer, at=0)
    access.flush()
    access.close()
    return buffer
```


</details>


read file to transferable buffer



## *function*:  opfs\_write()

<details><summary>[path: str, buffer: <MagicMock name='mock.ArrayBuffer' id='4316313456'>, root: <MagicMock name='mock.FileSystemDirectoryHandle' id='4318381456'>]</summary>


  ```python
async def opfs_write(path:str, buffer:ArrayBuffer, root:DirHandle):
    access:AccessHandle = await get_access(root=root, path=path, option="readwrite")
    if not access:
          return None
    access.truncate(0)
    result = access.write(buffer, at=0)
    access.flush()
    access.close()
    return result
```


</details>


write buffer to the file




