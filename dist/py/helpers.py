_A='readwrite'
from pyscript import sync
from js import navigator,File,Blob,TextEncoder,ArrayBuffer,Uint8Array
from js import FileSystemDirectoryHandle as DirHandle
from js import FileSystemFileHandle as FileHandle
from js import FileSystemSyncAccessHandle as AccessHandle
def not_found(e):print(e.message)
async def get_dir_handle(root,directories,create=False):
	A=root
	for B in[A for A in directories if A]:
		A=await A.getDirectoryHandle(B,create=create).catch(not_found)
		if not A:return
	return A
async def get_handle(root,path,create=True):
	A=create;B=path.split('/');D=B.pop();C=await get_dir_handle(root=root,directories=B,create=A)
	if not C:return
	E=await C.getFileHandle(D,create=A).catch(not_found);return E
async def get_access(root,path=None,option=_A):
	A=await get_handle(root=root,path=path)
	if A:B=await A.createSyncAccessHandle(option)
	else:return
	return B
async def get_root():return await navigator.storage.getDirectory()
async def opfs_blob(path,mode,root):
	A=await get_handle(root=root,path=path)
	if not A:return
	B=await A.getFile().catch(not_found)
	if mode.endswith('b'):return await B.bytes()
	else:return await B.text()
async def opfs_read(path,root):
	A=await get_access(root=root,path=path,option='read-only')
	if not A:return
	C=A.getSize();B=ArrayBuffer.new(C);D=A.read(B,at=0);A.flush();A.close();return B
async def opfs_write(path,buffer,root):
	A=await get_access(root=root,path=path,option=_A)
	if not A:return
	A.truncate(0);B=A.write(buffer,at=0);A.flush();A.close();return B
class Helper_Worker:
	root:0
	@classmethod
	async def init(A):A.root=await navigator.storage.getDirectory();sync.read=A.read;sync.write=A.write;sync.blob=A.blob
	@classmethod
	async def read(A,path,_):B=await opfs_read(root=A.root,path=path);return B
	@classmethod
	async def blob(A,path,mode='',_root=''):B=await opfs_blob(root=A.root,path=path,mode=mode);return B
	@classmethod
	async def write(A,path,buffer,root):B=await opfs_write(root=A.root,path=path,buffer=buffer);return B
sync.init_helper=Helper_Worker.init