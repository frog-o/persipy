from js import navigator
from pyscript import RUNNING_IN_WORKER
import builtins, os

#-------- main tread part-------------------------------------
if RUNNING_IN_WORKER == False:
    from pyscript import PyWorker, sync
    from _pyscript import interpreter

    OPEN = builtins.open #original open
    MOUNT_PATH = None

class OPFSFileWrapper:
    def __init__(self, file, file_path, mode='r', *args, **kwargs):
        self.file = file
        self.file_path:str = file_path #micropython dosnt have file.name
        self.mode = kwargs.get('mode', args[0])

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.file.close()
    
    def __getattr__(self, attr):
        return getattr(self.file, attr)

    def write(self, data):
        file_path = self.file_path
        """make the original write and go to worker if path in opfs"""
        if file_path.startswith(MOUNT_PATH):
            self.worker_write(file_path, data, self.mode)
        return self.file.write(data)


    @staticmethod
    def worker_write(file_path, data, mode):
        print('not mounted')

    @staticmethod
    def worker_touch(file_path):
        print('not mounted')

def custom_open(file_path, *args, **kwargs):
    file = OPEN(file_path, *args, **kwargs)
    mode = kwargs.get('mode', args[0])
    if mode in {'r', 't', 'rt'}:
        return file
    else:
        return OPFSFileWrapper(file, file_path, mode, *args, **kwargs)

        

async def mount_opfs(mount_path='/opfs', worker_path='persipy.py', worker_type='micropython'):
    global MOUNT_PATH, interpreter

    if not interpreter:
        print('no interpreter')
        return False

    """to be used in main for init"""
    #check for mounted
    if MOUNT_PATH:
        print('cannot mount:', mount_path, 'already is mounted:', OPFSFileWrapper.mounth_path)
        return False
    
    try:
        dirHandle = await navigator.storage.getDirectory() #opfs root
        await interpreter.mountNativeFS(mount_path, dirHandle) #nativefs

    except:
        print('cannot mount:', mount_path)
        return False

    
    builtins.open = custom_open #change original open() so to do write in worker too
    MOUNT_PATH = mount_path

    worker = PyWorker(worker_path, type=worker_type)
    await worker.ready
    await worker.sync.init()
    OPFSFileWrapper.worker_write = worker.sync.write
    OPFSFileWrapper.worker_touch = worker.sync.touch
    return True


#---worker part-------------------------------------
async def worker_init():
    global ROOT_HANDLE
    ROOT_HANDLE = await navigator.storage.getDirectory()
    return True


async def worker_write(file_path, data, mode):
    """
    #this works in chrome not in safary due to not supporting createwritable
    with open(fpath, 'w') as file:
        file.write(fcontent)
        file.close()
        nativefs.syncfs() 
    """
    global ROOT_HANDLE
    #for the example will save file in root only
    dirHandle = ROOT_HANDLE
    path_parts = file_path.split('/') #['', 'opfs', 'test.txt'] shoud miss 0 and 1
    if len(path_parts) > 3: #loop folders for handles
        for folder_name in path_parts[2:-1]: #all folder names except 0,1, and last
            dirHandle = await dirHandle.getDirectoryHandle(folder_name , create=True)

    filename = path_parts[-1]
    fileHandle = await dirHandle.getFileHandle(filename, create=True)
    fileSyncAccessHandle = await fileHandle.createSyncAccessHandle()
    encodedMessage = js_encode(data)
    if mode[0] == 'w':
        fileSyncAccessHandle.truncate(0)
    fileSyncAccessHandle.write(encodedMessage)
    fileSyncAccessHandle.flush()
    fileSyncAccessHandle.close()
    


async def worker_touch(fpath):
    global ROOT_HANDLE
    #for the example will save file in root only
    dirHandle = ROOT_HANDLE
    path_parts = fpath.split('/') #['', 'opfs', 'test.txt'] shoud miss 0 and 1
    if len(path_parts) > 3: #loop folders for handles
        for folder_name in path_parts[2:-1]: #all folder names except 0,1, and last
            dirHandle = await dirHandle.getDirectoryHandle(folder_name , create=True)

    filename = path_parts[-1]
    fileHandle = await dirHandle.getFileHandle(filename, create=True)

    return fileHandle



if RUNNING_IN_WORKER == True:
    from js import TextEncoder
    from pyscript import sync
    
    encoder = TextEncoder.new()
    js_encode = encoder.encode
    sync.init = worker_init
    sync.write = worker_write
    sync.touch = worker_touch



#--- visuals ---------------------------------------------------------
def show_tree(root='/'):
    print('-' * 10)
    arr = os.listdir(root)
    for a in arr:
        if os.path.isdir(a):
            print(f'📁 {a} {os.listdir(a)}')
        else:
            print(f'📝{a}')
    print('-'*10)

"""
'r' open for reading (default)
'w' open for writing, truncating the file first
'x' open for exclusive creation, failing if the file already exists
'a' open for writing, appending to the end of file if it exists
'b' binary mode
't' text mode (default)
'+' open for updating (reading and writing)
The default mode is 'r' (open for reading text, a synonym of 'rt').
'w+' and 'w+b' open and truncate the file.
'r+' and 'r+b' open the file with no truncation.
"""