from js import navigator
from pyscript import RUNNING_IN_WORKER
import builtins, os

ROOT_HANDLE = None

#---
def show_tree(root='/'):
    print('-' * 60)
    arr = os.listdir(root)
    for a in arr:
        if os.path.isdir(a):
            print(f'📁 {a} {os.listdir(a)}')
        else:
            print(f'📝{a}')
    print('-'*60)

#-------- main tread part-------------------------------------
if RUNNING_IN_WORKER == False:
    from pyscript import RUNNING_IN_WORKER, PyWorker, sync
    from _pyscript import interpreter


class OPFSFileWrapper:
    original_open = builtins.open
    mounth_path = None

    def __init__(self, file_path, *args, **kwargs):
        try:
            self.file = self.original_open(file_path, *args, **kwargs)
        except:
            self.worker_write(file_path, '')
            self.file = self.original_open(file_path, *args, **kwargs)
        self.file_path:str = file_path #micropython dosnt have file.name

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.file.close()
    
    def __getattr__(self, attr):
        return getattr(self.file, attr)

    def write(self, data):
        file_path = self.file_path
        """make the original write and go to worker if path in opfs"""
        if file_path.startswith(self.mounth_path):
            self.worker_write(file_path, data)
        return self.file.write(data)


    @staticmethod
    def worker_write(file_path, data):
        print('not mounted')

def custom_open(file_path, *args, **kwargs):
    return OPFSFileWrapper(file_path, *args, **kwargs)



async def mount_opfs(mount_path='/opfs'):
    """to be used in main for init"""
    #check for mounted
    if OPFSFileWrapper.mounth_path:
        print('cannot mount:', mount_path, 'already is mounted:', OPFSFileWrapper.mounth_path)
        return False
    
    try:
        dirHandle = await navigator.storage.getDirectory() #opfs root
        await interpreter.mountNativeFS(mount_path, dirHandle) #nativefs

    except:
        print('cannot mount:', mount_path)
        return False

    #change original open() so to do write in worker too
    builtins.open = custom_open
    OPFSFileWrapper.mounth_path = mount_path

    #preparing worker
    #worker = await workers["persipy"]
    worker = PyWorker('persipy.py', type='micropython')
    await worker.ready
    await worker.sync.init()
    OPFSFileWrapper.worker_write = worker.sync.write
    return True


#---worker part-------------------------------------
async def worker_init():
    global ROOT_HANDLE
    ROOT_HANDLE = await navigator.storage.getDirectory()
    return True


async def worker_write(fpath, fcontent):
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
    path_parts = fpath.split('/') #['', 'opfs', 'test.txt'] shoud miss 0 and 1
    if len(path_parts) > 3: #loop folders for handles
        for folder_name in path_parts[2:-1]: #all folder names except 0,1, and last
            dirHandle = await dirHandle.getDirectoryHandle(folder_name , create=True)

    filename = path_parts[-1]
    print(filename, fcontent)
    fileHandle = await dirHandle.getFileHandle(filename, create=True)
    fileSyncAccessHandle = await fileHandle.createSyncAccessHandle()
    encodedMessage = js_encode(fcontent)
    fileSyncAccessHandle.truncate(0)
    fileSyncAccessHandle.write(encodedMessage)
    fileSyncAccessHandle.flush()
    fileSyncAccessHandle.close()
    
    return True


if RUNNING_IN_WORKER == True:
    from js import TextEncoder
    from pyscript import sync
    
    encoder = TextEncoder.new()
    js_encode = encoder.encode
    sync.init = worker_init
    sync.write = worker_write
