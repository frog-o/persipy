_A='utf-8'
from js import navigator,TextEncoder,ArrayBuffer,Uint8Array
from pyscript import RUNNING_IN_WORKER
class FileOPFS:
	encoder=TextEncoder.new().encode
	def __init__(A,path,mode='r',opfs=None):A.path=path;A.mode=mode;A.opfs=opfs
	def __enter__(A):return A
	def __exit__(A,exc_type,exc_val,exc_tb):return False
	async def read(A):
		B=await FileOPFS._read(A.path,A._root)
		if A.mode.endswith('b'):return A.buffer_to_bytes(B)
		else:return A.buffer_to_text(B)
	async def get_text(A):B=await FileOPFS._blob(A.path,'t',A._root);return B
	async def get_bytes(A):B=await FileOPFS._blob(A.path,'b',A._root);return bytes(B)
	async def write(A,data):B=A.data_to_buffer(data);C=await FileOPFS._write(A.path,B,A._root);return C
	@staticmethod
	async def _read():0
	@staticmethod
	async def _blob():0
	@staticmethod
	async def _write():0
	@staticmethod
	def data_to_buffer(data):A=data;B=FileOPFS.encoder;C=B(A)if isinstance(A,str)else Uint8Array.new(A);D=C.buffer;return D
	@staticmethod
	def buffer_to_bytes(buffer):A=Uint8Array.new(buffer);B=bytes(A);return B
	@staticmethod
	def buffer_to_text(buffer):A=FileOPFS.buffer_to_bytes(buffer);return A.decode(_A)
class OPFS:
	file_cls=FileOPFS
	def __init__(A):0
	def __call__(A,path=None,mode='t'):return A.file_cls(path=path,mode=mode,opfs=A)
	async def init(E):
		if not RUNNING_IN_WORKER:A=await start_helper_worker();FileOPFS._root='';FileOPFS._read=A.sync.read;FileOPFS._blob=A.sync.blob;FileOPFS._write=A.sync.write
		else:from.helpers import opfs_read as B,opfs_blob as C,opfs_write as D;FileOPFS._root=await navigator.storage.getDirectory();FileOPFS._read=B;FileOPFS._blob=C;FileOPFS._write=D
async def start_helper_worker():
	from pyscript import PyWorker as B;import base64 as C,os;D=os.path.abspath(__file__);E=os.path.dirname(D);F=os.path.join(E,'helpers.py')
	with open(F,'r')as G:H=G.read()
	I=H.encode(_A);J=C.b64encode(I).decode(_A);K=f"data:application/x-python-code;base64,{J}";A=B(K,type='pyodide');await A.ready;await A.sync.init_helper();return A