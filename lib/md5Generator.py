import hashlib
from functools import partial

class Md5Generator(object):
	def compute_md5(self, file_path):
		chunksize=2**15
		bufsize=-1
		m = hashlib.md5()
		with open(file_path, 'rb', bufsize) as f:
			for chunk in iter(partial(f.read, chunksize), b''):
				m.update(chunk)
		return m.hexdigest()
