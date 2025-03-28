"""
"""
from js import navigator, TextEncoder, ArrayBuffer, Uint8Array
from pyscript import RUNNING_IN_WORKER


class FileOPFS:
    """Representation of file objects"""
    encoder = TextEncoder.new().encode
    
    def __init__(self, path, mode='r', opfs:'OPFS'=None):
    
        self.path:str = path
        self.mode:str = mode
        self.opfs:'OPFS' = opfs

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


    async def read(self)->str|bytes:
        """read file and return depending on mode string or bytes"""
        buffer = await FileOPFS._read(self.path, self._root)

        if self.mode.endswith('b'):
            return self.buffer_to_bytes(buffer)
        else:
            return self.buffer_to_text(buffer)


    async def get_text(self)->str:
        """read file as blob and return string
        on big files can be much faster than `read()` with caviat
        that in the browser inspector the blob can be seen"""
        result = await FileOPFS._blob(self.path, 't', self._root)

        return result


    async def get_bytes(self)->bytes:
        """read file as blob and return bytes
        on big files can be much faster than `read()` with caviat
        that in the browser inspector the blob can be seen"""

        result = await FileOPFS._blob(self.path, 'b', self._root)

        return bytes(result)



    async def write(self, data:str|bytes)->int:
        """writes the given string or bytes to the file
        returns the number of the written bytes"""

        buffer = self.data_to_buffer(data)

        result = await FileOPFS._write(self.path, buffer, self._root)
        
        return result


    @staticmethod
    async def _read():
        """will be set on `init()`"""
        pass
    @staticmethod
    async def _blob():
        """will be set on `init()`"""
        pass
    @staticmethod
    async def _write():
        """will be set on `init()`"""
        pass





    @staticmethod
    def data_to_buffer(data:str|bytes):
        """convert strings and bytes to `js.ArrayBuffer`"""
        encoder = FileOPFS.encoder
        array = encoder(data) if isinstance(data, str) else Uint8Array.new(data)
        buffer:ArrayBuffer = array.buffer
        return buffer

    @staticmethod
    def buffer_to_bytes(buffer):
        """convert `js.ArrayBuffer` to bytes"""
        array = Uint8Array.new(buffer)
        result_bytes = bytes(array)
        return result_bytes

    @staticmethod
    def buffer_to_text(buffer):
        """convert `js.ArrayBuffer` to string"""
        result_bytes = FileOPFS.buffer_to_bytes(buffer)
        return result_bytes.decode('utf-8') 



class OPFS:
    """Main class to invoke File objects to work with
    Origin Private File System"""
    file_cls = FileOPFS

    def __init__(self):
        pass

    def __call__(self, path:str=None, mode:str='t'):
        return self.file_cls(path=path, mode=mode, opfs=self)
    
    async def init(self):
        """will set the private methods depending where is running:
        if in main thread will engage an helper worker and set them to its exposed functions
        if in worker will set the root directory and set them
        directly to the function to work with the Origin Private File System"""
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



async def start_helper_worker():
    """preparing, engaging and waiting initialisation of the helper worker"""
    from pyscript import PyWorker
    import base64
    import os


    # Get source for the module
    script_path = os.path.abspath(__file__)
    parent_directory = os.path.dirname(script_path)
    file_path = os.path.join(parent_directory, 'helpers.py')
    with open(file_path, 'r') as f:
        src = f.read()
    
    # encoding the source
    python_code_bytes = src.encode('utf-8')
    base64_code = base64.b64encode(python_code_bytes).decode('utf-8')

    # Create the Data URL
    data_url = f"data:application/x-python-code;base64,{base64_code}"

    #startup the helper worker
    worker = PyWorker(data_url, type='pyodide')
    await worker.ready
    await worker.sync.init_helper()

    return worker

