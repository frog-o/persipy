## opfs



## *class*:  FileOPFS()

<details><summary>[path: str, mode='r', opfs: 'OPFS' = None]</summary>


  ```python
class FileOPFS:
    encoder = TextEncoder.new().encode
    def __init__(self, path:str, mode='r', opfs:'OPFS'=None):
        self.path:str = path
        self.mode:str = mode
        self.opfs:'OPFS' = opfs
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
    async def read(self)->str|bytes:
        buffer = await FileOPFS._read(self.path, self._root)
        if self.mode.endswith('b'):
            return self.buffer_to_bytes(buffer)
        else:
            return self.buffer_to_text(buffer)
    async def get_text(self)->str:
        result = await FileOPFS._blob(self.path, 't', self._root)
        return result
    async def get_bytes(self)->bytes:
        result = await FileOPFS._blob(self.path, 'b', self._root)
        return bytes(result)
    async def write(self, data:str|bytes)->int:
        buffer = self.data_to_buffer(data)
        result = await FileOPFS._write(self.path, buffer, self._root)
        return result
    @staticmethod
    async def _read():
        pass
    @staticmethod
    async def _blob():
        pass
    @staticmethod
    async def _write():
        pass
    @staticmethod
    def data_to_buffer(data:str|bytes):
        encoder = FileOPFS.encoder
        array = encoder(data) if isinstance(data, str) else Uint8Array.new(data)
        buffer:ArrayBuffer = array.buffer
        return buffer
    @staticmethod
    def buffer_to_bytes(buffer):
        array = Uint8Array.new(buffer)
        result_bytes = bytes(array)
        return result_bytes
    @staticmethod
    def buffer_to_text(buffer):
        result_bytes = FileOPFS.buffer_to_bytes(buffer)
        return result_bytes.decode('utf-8') 
```


</details>


Representation of file objects


### *method*:  \_\_init\_\_()

<details><summary>[self, path: str, mode='r', opfs: 'OPFS' = None]</summary>


  ```python
    def __init__(self, path:str, mode='r', opfs:'OPFS'=None):
        self.path:str = path
        self.mode:str = mode
        self.opfs:'OPFS' = opfs
```


</details>


initialising file object

`path` - file path

`mode` - when set to **b** `file.read()` will return bytes

`opfs` - is a private and is not shown in the `with` statement


main usage entry point

```python

with opfs(path, mode) as file:
    await file.read()
    await file.write(data)
    await file.get_text()
    await file.get_bytes()

```


### *method*:  \_\_enter\_\_()

<details><summary>[self]</summary>


  ```python
    def __enter__(self):
        return self
```


</details>





### *method*:  \_\_exit\_\_()

<details><summary>[self, exc_type, exc_val, exc_tb]</summary>


  ```python
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
```


</details>





### *method*:  read()

<details><summary>[self] ->  str | bytes</summary>


  ```python
    async def read(self)->str|bytes:
        buffer = await FileOPFS._read(self.path, self._root)
        if self.mode.endswith('b'):
            return self.buffer_to_bytes(buffer)
        else:
            return self.buffer_to_text(buffer)
```


</details>


read file and return depending on mode string or bytes


### *method*:  get\_text()

<details><summary>[self] ->  str</summary>


  ```python
    async def get_text(self)->str:
        result = await FileOPFS._blob(self.path, 't', self._root)
        return result
```


</details>


read file as blob and return string
on big files can be much faster than `read()` with caviat
that in the browser inspector the blob can be seen


### *method*:  get\_bytes()

<details><summary>[self] ->  bytes</summary>


  ```python
    async def get_bytes(self)->bytes:
        result = await FileOPFS._blob(self.path, 'b', self._root)
        return bytes(result)
```


</details>


read file as blob and return bytes
on big files can be much faster than `read()` with caviat
that in the browser inspector the blob can be seen


### *method*:  write()

<details><summary>[self, data: str | bytes] ->  int</summary>


  ```python
    async def write(self, data:str|bytes)->int:
        buffer = self.data_to_buffer(data)
        result = await FileOPFS._write(self.path, buffer, self._root)
        return result
```


</details>


writes the given string or bytes to the file
returns the number of the written bytes


### *staticmethod*:  \_read()

<details><summary>[]</summary>


  ```python
    @staticmethod
    async def _read():
        pass
```


</details>


will be set on `init()`


### *staticmethod*:  \_blob()

<details><summary>[]</summary>


  ```python
    @staticmethod
    async def _blob():
        pass
```


</details>


will be set on `init()`


### *staticmethod*:  \_write()

<details><summary>[]</summary>


  ```python
    @staticmethod
    async def _write():
        pass
```


</details>


will be set on `init()`


### *staticmethod*:  data\_to\_buffer()

<details><summary>[data: str | bytes]</summary>


  ```python
    @staticmethod
    def data_to_buffer(data:str|bytes):
        encoder = FileOPFS.encoder
        array = encoder(data) if isinstance(data, str) else Uint8Array.new(data)
        buffer:ArrayBuffer = array.buffer
        return buffer
```


</details>


convert strings and bytes to `js.ArrayBuffer`


### *staticmethod*:  buffer\_to\_bytes()

<details><summary>[buffer]</summary>


  ```python
    @staticmethod
    def buffer_to_bytes(buffer):
        array = Uint8Array.new(buffer)
        result_bytes = bytes(array)
        return result_bytes
```


</details>


convert `js.ArrayBuffer` to bytes


### *staticmethod*:  buffer\_to\_text()

<details><summary>[buffer]</summary>


  ```python
    @staticmethod
    def buffer_to_text(buffer):
        result_bytes = FileOPFS.buffer_to_bytes(buffer)
        return result_bytes.decode('utf-8') 
```


</details>


convert `js.ArrayBuffer` to string



## *class*:  OPFS()

<details><summary>[]</summary>


  ```python
class OPFS:
    file_cls = FileOPFS
    def __init__(self):
        pass
    def __call__(self, path:str=None, mode:str='t'):
        return self.file_cls(path=path, mode=mode, opfs=self)
    async def init(self):
        if not RUNNING_IN_WORKER:
            worker = await start_helper_worker()
            FileOPFS._root = ''
            FileOPFS._read = worker.sync.read
            FileOPFS._blob = worker.sync.blob
            FileOPFS._write = worker.sync.write
        else:
            from .helpers import opfs_read, opfs_blob, opfs_write
            FileOPFS._root = await navigator.storage.getDirectory()
            FileOPFS._read = opfs_read
            FileOPFS._blob = opfs_blob
            FileOPFS._write = opfs_write
```


</details>


Main class to invoke File objects to work with
Origin Private File System


### *method*:  \_\_init\_\_()

<details><summary>[self]</summary>


  ```python
    def __init__(self):
        pass
```


</details>


Initialize self.  See help(type(self)) for accurate signature.


### *method*:  \_\_call\_\_()

<details><summary>[self, path: str = None, mode: str = 't']</summary>


  ```python
    def __call__(self, path:str=None, mode:str='t'):
        return self.file_cls(path=path, mode=mode, opfs=self)
```


</details>


Call self as a function.


### *method*:  init()

<details><summary>[self]</summary>


  ```python
    async def init(self):
        if not RUNNING_IN_WORKER:
            worker = await start_helper_worker()
            FileOPFS._root = ''
            FileOPFS._read = worker.sync.read
            FileOPFS._blob = worker.sync.blob
            FileOPFS._write = worker.sync.write
        else:
            from .helpers import opfs_read, opfs_blob, opfs_write
            FileOPFS._root = await navigator.storage.getDirectory()
            FileOPFS._read = opfs_read
            FileOPFS._blob = opfs_blob
            FileOPFS._write = opfs_write
```


</details>


will set the private methods depending where is running:
if in main thread will engage an helper worker and set them to its exposed functions
if in worker will set the root directory and set them
directly to the function to work with the Origin Private File System




## *function*:  start\_helper\_worker()

<details><summary>[]</summary>


  ```python
async def start_helper_worker():
    from pyscript import PyWorker
    import base64
    import os
    script_path = os.path.abspath(__file__)
    parent_directory = os.path.dirname(script_path)
    file_path = os.path.join(parent_directory, 'helpers.py')
    with open(file_path, 'r') as f:
        src = f.read()
    python_code_bytes = src.encode('utf-8')
    base64_code = base64.b64encode(python_code_bytes).decode('utf-8')
    data_url = f"data:application/x-python-code;base64,{base64_code}"
    worker = PyWorker(data_url, type='pyodide')
    await worker.ready
    await worker.sync.init_helper()
    return worker
```


</details>


preparing, engaging and waiting initialisation of the helper worker




