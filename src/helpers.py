"""All functions to work with Origin Private File System API
and the class for the helper worker"""

from pyscript import sync

from js import navigator, File, Blob, TextEncoder, ArrayBuffer, Uint8Array

#these are importet for typing
from js import FileSystemDirectoryHandle as DirHandle
from js import FileSystemFileHandle as FileHandle
from js import FileSystemSyncAccessHandle as AccessHandle

def not_found(e):
        """error handling if not found pointer for a file or directory"""
        print(e.message)
        return None   


async def get_dir_handle(root:DirHandle, directories:list, create=False)->DirHandle:  
        """from the list of directories (nested with as top is at index 0)
        gets the OPFS API object called `FileSystemDirectoryHandle`
        from where will be able to find the file we want to work on"""

        handle = root

        for dir_name in [d for d in directories if d]:
            handle = await handle.getDirectoryHandle(dir_name,
                                                     create=create).catch(not_found)
            if not handle:
                return None
            
        return handle


async def get_handle(root:DirHandle, path:str, create=True)->FileHandle:
        """from the provided file path gets the FileSystemFileHandle object,
        which we are gonna using to work with the file"""

        path_parts:list = path.split('/')
        file_name = path_parts.pop()

        dir_handle:DirHandle = await get_dir_handle(root=root, directories=path_parts, create=create)

        if not dir_handle:
              return None
        
        handle = await dir_handle.getFileHandle(file_name, create=create).catch(not_found)
        
        return handle


async def get_access(root:DirHandle, path:str=None, option:str="readwrite")->AccessHandle:
        """from the provided file path gets the FileSystemSyncAccessHandle object,
        which we are gonna using to work with the file"""       
        
        handle = await get_handle(root=root, path=path)

        if handle:

            access = await handle.createSyncAccessHandle(option)
    
        else:
            return None

        return access


async def get_root():
    """get root of the file system"""
    return await navigator.storage.getDirectory()
    

async def opfs_blob(path:str, mode, root:DirHandle)->str|bytes:
    """gets text or string for the file without using FileSystemSyncAccessHandle
    fast for big files and depending on mode returns string or bytes"""

    handle:FileHandle = await get_handle(root=root, path=path)

    if not handle:
          return None
    
    blob:Blob = await handle.getFile().catch(not_found)

    if mode.endswith('b'):
        return await blob.bytes()
    else:
        return await blob.text()


async def opfs_read(path:str, root:DirHandle)->ArrayBuffer:
    """read file to transferable buffer"""

    access:AccessHandle = await get_access(root=root, path=path, option="read-only")

    if not access:
          return None
    
    size = access.getSize()
    buffer = ArrayBuffer.new(size)

    result = access.read(buffer, at=0)

    access.flush()
    access.close()

    return buffer



async def opfs_write(path:str, buffer:ArrayBuffer, root:DirHandle):
    """write buffer to the file"""

    access:AccessHandle = await get_access(root=root, path=path, option="readwrite")

    if not access:
          return None
    
    access.truncate(0)
    result = access.write(buffer, at=0)

    access.flush()
    access.close()

    return result




class Helper_Worker:
    """Used by the helper worker to bridge Origin Private File system to the main thread"""
    root:DirHandle

    @classmethod
    async def init(cls):
        """seting up the helper worker"""
        cls.root = await navigator.storage.getDirectory()
        sync.read = cls.read
        sync.write = cls.write
        sync.blob = cls.blob

    @classmethod
    async def read(cls, path:str, _)->ArrayBuffer:
          """returns `opfs_read()` see it above"""
          result = await opfs_read(root=cls.root, path=path)

          return result

    @classmethod
    async def blob(cls, path:str, mode:str='', _root='')->str|bytes:
          """returns `opfs_blob()` see it above"""

          result = await opfs_blob(root=cls.root, path=path, mode=mode)

          return result


    @classmethod
    async def write(cls, path:str, buffer:ArrayBuffer, root)->int:
        """writes the file with `opfs_write()` see it above"""

        result = await opfs_write(root=cls.root, path=path, buffer=buffer)

        return result

# the anchor to engage the helper worker from the main thread
sync.init_helper = Helper_Worker.init